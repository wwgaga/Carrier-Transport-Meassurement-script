## van der pauw geometry ,['R'] --> quick vdw

from scipy import stats, constants
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os 

class PpmsData():
    def __init__(self, data, re_xx_T, d, W, L , T, my_path ,nBins = 10, silent = False, plot = False):
        # self is the object itself, a manditory input of object functions/methods. 
        # bins: the range of values , if you choose bins equal to 10 then your input will be divided into 10 intervals or bins
        # silent = False ,keyword augument  
        
        #print('This is the data before transfermation', data)
        
        if type(data) == pd.core.frame.DataFrame:
        # type(data) meaning ??
        #dataframe is two dimensional tabular data structure 
            self.data = pd.DataFrame(data.values, columns=['B','R','H'])
        #else:
            #self.data = pd.DataFrame(np.array(data).T, columns=['B','H','R'])
        # change rows and columns 
        #print('This is transfered data',self.data)

        self.data['B']/=1e4 #Oe->Tesla
        self.path = my_path
        #self.re_xx_T = re_xx_T*1e2#[ohm*m]=>[ohm*cm]
        self.re_xx_T = re_xx_T#[ohm*cm]
        self.T = T
        self.d = d 
        self.W = W
        self.L = L
        self.plot = plot
        self.fData = self.filterSym(self.data, index='H',nBins=nBins, plot=plot)[['B', 'asData', 'symData']].rename(columns={'asData':'hasym', 'symData':'hsym'})
        #print('this is fData: ', self.fData)
        self.pData = self.filterSym(self.data, index='R',nBins=nBins, plot=plot)[['B', 'asData', 'symData']].rename(columns = {'asData':'rasym','symData':'rsym'})
        #print('this is pData: ', self.pData)
        self.pData.index.name = None
        self.asSlope = self.slopeHall(self.fData)
        self.simpleSlope = self.simpleSlopeHall(self.data)
        self.n = self.nHall(self.asSlope, d)*1e-6 #1/m³->1/cm³
        self.R = self.zeroBMedian(self.data[['B', 'R']])
        #self.rho = self.R * d * 1e5 #Ohm*m -> mOhm*cm 
        #sheet resistance * thickness = reisistiviety => vdp 
        self.rho = self.R * W * d / L *1e2 #Ohm*m -> Ohm*cm 
        self.mu_by_n = self.muHall_r(self.n, self.re_xx_T)
        print('This is mobility by n:',self.mu_by_n,self.T)
        self.mu_by_slope = self.muHall(self.asSlope,self.R,self.W,self.L)*1e4 # 1 [Tesla] = 1[v*s/m2],m2=>cm2

    def returnData(self, filename):
        data_stored = pd.DataFrame({'(Asymmetric) Slope:':self.asSlope,
                                    'Carrier concentration[1/cm^3]:':self.n,
                                    'Resistivity at 0 Oe:':self.rho,
                                    'Resistance at 0 Oe':self.R,
                                    'Mobility by n :':self.mu_by_n,
                                    'Mobility by slope :':self.mu_by_slope},index =[0])

        filename_calculated_parameter = "Hall calculated parameter_"+str(self.T) + "K"

        data_stored.to_csv(os.path.join(self.path,filename_calculated_parameter),sep = ',')
        
        if not self.plot:
            plt.ioff()
            fig = plt.figure()
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            ax1.plot(self.fData['B'], self.fData['hasym'], 'r.')
            ax2.plot(self.fData['B'], self.fData['hsym'], 'b.')
            ax1.set_title('asymmetric part')
            ax1.grid(True)
            ax2.set_title('symmetric part')
            ax2.grid(True)
            ax1.set_xticks(np.arange(-1,1, step=0.4))
            ax2.set_xticks(np.arange(-1,1, step=0.4))
            #ax1.set_xticks(np.arange(-9,9, step=1))
            #ax2.set_xticks(np.arange(-9,9, step=1))
            #ax1.set_yticks(np.arange(min(self.fData['hasym']),max(self.fData['hasym']), step= abs(max(self.fData['hasym'])-min(self.fData['hasym']))/5)) 
            #ax2.set_yticks(np.arange(min(self.fData['hsym']),max(self.fData['hsym']), step= abs(max(self.fData['hsym'])-min(self.fData['hsym']))/5))
            ax1.set_xlabel('Magnetic Field (Telsa)')
            ax1.set_ylabel('Rh(Ohm)')
            ax2.set_xlabel('Magnetic Field (Telsa)')
            ax2.set_ylabel('MR(Ohm)')
            plt.tight_layout()
            fig.savefig(os.path.join(self.path, filename),bbox_inches = "tight") 
            plt.close()
            #plt.show()
        
        print(str(self.T) +'K')

        filename = "hall_symasymData_" + str(self.T) + "K" 
        self.fData.to_csv(os.path.join(self.path,filename), sep=',')

        return {'n':self.n,
                'R':self.R,
                'rho':self.rho,
                'mu_by_n':self.mu_by_n,
                'mu_by_slope':self.mu_by_slope,
                'fData':self.fData,
                'pData':self.pData}

    def print(self):
        print('Tempearature'+str(self.T))
        print('(Asymmetric) Slope: ' + str(self.asSlope) + ' [Ohm/T]')
        #print('(Symmetric) Slope: ' + str(symSlope) + ' [Ohm/T]')
        print('simple Slope: ' + str(self.simpleSlope) + ' [Ohm/T]')
        print('Carrier concentration: ' + str(self.n) + ' [1/cm^3]')
        print('Resistivity at 0 Oe: ' + str(self.rho) + ' [Ohmcm]')
        print('Mobility by n : ' + str(self.mu_by_n) + ' [cm^2/Vs]')
        print('Mobility by slope: ' + str(self.mu_by_slope) + ' [cm^2/Vs]')
    
    def normMR(self, data=None, pp = 1):# expects pandas dataframe with ['B', 'R'] and returns MR% without field
        if type(data) == type(None):
           r_filename = "R_symasymData_" + str(self.T) + "K" 
           self.pData.to_csv(os.path.join(self.path,r_filename), sep=',')
           pData = self.pData[['B','rsym']].rename(columns={'rsym':'R'})
        mr0=self.zeroBMedian(pData, pp=pp)
        pData['MR%']=(pData['R']-mr0)/mr0
        mr_filename = "MR " + str(self.T) + "K" 
        pData.to_csv(os.path.join(self.path,mr_filename), sep=',')
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(pData['B'], pData['MR%'], 'b--')
        ax.set_title(mr_filename )
        ax.grid(True)
        ax.set_xticks(np.arange(-1,1,step=0.4))
        ax.set_xlabel('Magnetic Field (Telsa)')
        ax.set_ylabel('MR%')
        fig.savefig(os.path.join(self.path,mr_filename),bbox_inches = "tight") 
        #plt.show()
        plt.close()
        return pData

    @staticmethod
    def filterSym(data, index = 'H', fieldIndex = 'B', nBins = 10, plot = False):
        #brackets = [n*max(abs(data[0]))/nBrackets for n in range(1,nBrackets)]
        bins=np.concatenate((np.linspace(-max(abs(data[fieldIndex])),0,nBins)[:-1], np.linspace(0,max(abs(data[fieldIndex])),nBins)),0)
        #Join a sequence of arrays along an existing axis. axis = 0 along row direction , axis =1 along column;
        bData = data.groupby(pd.cut(data[fieldIndex], bins)).mean()
        #DataFrame.groupby(self, by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, squeeze=False, observed=False, **kwargs)
        #level :If the axis is a MultiIndex (hierarchical), group by a particular level or levels.
        # data is grouped into different bins and then take an mean value of them 
        #pd.cut: Use cut when you need to segment and sort data values into bins. This function is also useful for going from a continous variables to categorial  variables
        #eg: cuts convert age to age ranges 
        lData=bData.iloc[0:nBins-1]
        rData=bData.iloc[nBins-1:]


        fData=pd.DataFrame({fieldIndex:bData[fieldIndex],
                            'asData':(bData[index].values - bData[index].values[::-1])/2,
                            # [::-1] reverse the list
                            'symData':(bData[index].values + bData[index].values[::-1])/2
                            })
        if plot:
            plt.ioff()
            fig = plt.figure()
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)
            ax1.plot(fData[fieldIndex], fData['asData'], 'r.')
            ax2.plot(fData[fieldIndex], fData['symData'], 'b.')
            ax1.set_title('asymmetric part')
            ax2.set_title('symmetric part')
            plt.close()
            # plt.show()
        # symData=(bData['H'].values+bData['H'].values[::-1])/2
        # asData=(bData['H'].values-bData['H'].values[::-1])/2
        # symData=(rData.R.values-lData.R.values)/2
        return fData

    @staticmethod
    def slopeHall(fData):#expects 2D-list [x,y]
        #from scipy import stats
        slope, intercept, r_value, p_value, stderr = stats.linregress(fData[['B', 'hasym']])
        # slopeR, interceptR, r_valueR, p_valueR, stderrR = stats.linregress(right)
        # beware sign, both fits from low to high (without absolute value)
        return slope #Ohm/Tesla #moved to beginning
        # asSlope = (slopeR + slopeL) / 2 * 1e4 #Ohm/Oe -> Ohm/Tesla
        # symSlope = (slopeR - slopeL) / 2 * 1e4 #Ohm/Oe -> Ohm/Tesla
        # return asSlope, symSlope, [slopeL, interceptL, r_valueL, p_valueL, stderrL], [slopeR, interceptR, r_valueR, p_valueR, stderrR]

    # def plot(x,y, d=5):
    #     import matplotlib.pyplot as plt
    #     plt.figure()
    #     xd = np.linspace(min(x), max(x), 100)
    #     lin = np.polyfit(x,y,deg=d)[-2]
    #     abs = np.polyfit(x,y,deg=d)[-1]
    #     print(lin)
    #     yd=abs+xd*lin
    #     plt.plot(x,y)
    #     plt.plot(xd,yd, 'r')
    #     plt.show()

    @staticmethod
    def simpleSlopeHall(data):# quick linear fit over the whole range for testing, not used in further calculations
        slope, intercept, r_value, p_value, stderr = stats.linregress(np.array(data).T[:2])
        #return slope*1e4 #Ohm/Oe -> Ohm/Tesla
        return slope # ohm/Tesla

    @staticmethod
    def nHall(asslope, d):
        return 1/asslope/-constants.e/d #1/m³ #carrier type (negative=electrons)#p typle

    @staticmethod
    def cutArray(ds, col=0, min=-np.inf, max=np.inf):
        cutData = ds.data
        inilen = len(cutData[col])
        for i in range(inilen):
            if cutData[col][inilen - 1 - i] < min or cutData[col][inilen - 1 - i] > max:
                cutData = np.delete(cutData, inilen - 1 - i, 1)
        else:
            return cutData

    @staticmethod
    def zeroBMedian(pData, pp = 1): #using median of lowest field pp% of points to determine 0-field resistance 
        tData=pData.copy()
        tData['B']=abs(tData['B'])
        sData=tData.sort_values(['B'])
        try:
            if pp >=1: #number of points
                return sData.iloc[:pp].median().R
            #lowField = np.transpose(sorted(abs(np.transpose(MRdata)), key = lambda point: point[0])[:int(pp)])
            elif pp > 0 and pp<1: #percentage of field
                m = sData[sData['B']<=max(sData['B'])*pp].median().R
                if  pd.isna(m)==True:
                    return sData.iloc[:1].median().R
                else:
                    return sData[sData['B']<=max(sData['B'])*pp].median().R
            #lowField = np.transpose(sorted(abs(np.transpose(MRdata)), key = lambda point: point[0])[:int(len(MRdata[0])/(100/pp))])
        except IndexError:
            return sData.median().R
        
    @staticmethod
    def muHall_r(n,re_xx_T):#expects list like [[field],[Hall],[MR]]
        return abs(1/constants.e/n/re_xx_T) #cm2/（v*s）

    @staticmethod
    def muHall(slope,R,W,L):#expects list like [[field],[Hall],[MR]]
        return abs(slope * L / R / W ) #m

    @staticmethod
    def getHallData(data, d, silent = False, nBins = 10, plot = False):#expects list like [[field],[Hall],[MR]] or pandas slice
        if type(data) == pd.core.frame.DataFrame:
            data=pd.DataFrame(data.values, columns=['B','H','R'])
        else:
            data = pd.DataFrame(np.array(data).T, columns=['B','H','R'])
        fData = filterSym(data, nBins=nBins, plot=plot)
        asSlope = slopeHall(fData)
        simpleSlope = simpleSlopeHall(data)
        n = nHall(asSlope, d)*1e-6 #1/m³->1/cm³
        res = zeroBMedian(data[:3:2]) * d * 1e5 #Ohm*m -> mOhm*cm
        mu = muHall(data)
        if not silent:
            print('(Asymmetric) Slope: ' + str(asSlope) + ' [Ohm/T]')
            #print('(Symmetric) Slope: ' + str(symSlope) + ' [Ohm/T]')
            print('simple Slope: ' + str(simpleSlope) + ' [Ohm/T]')
            print('Carrier concentration: ' + str(n) + ' [1/cm^3]')
            print('Resistivity at 0 Oe: ' + str(res) + ' [mOhmcm]')
            print('Mobility: ' + str(mu) + ' [cm^2/Vs]')
        return {'asSlope':asSlope, 'n':n, 'R':res, 'mob':mu, 'fData':fData}

    def normalize(data):# expects [field, Resistance] and returns normalized data according to zeroBMedian
        return [data[0], data[1]/zeroBMedian(data[0:2])]

def quickHall(data, hall=3, mr=1, *args, **kwargs):#convenience function for panda hall data
    return PpmsData(data[['Magnetic Field (Oe)','Bridge {} Resistance (ohms)'.format(int(hall)),'Bridge {} Resistance (ohms)'.format(int(mr))]], *args, **kwargs)

def vdpHall(data, *args, **kwargs):#convenience function for panda hall data
    data['R'] = (data['Bridge 1 Resistance (ohms)']+data['Bridge 2 Resistance (ohms)'])*np.pi*np.log(2)/2
    return PpmsData(data[['Magnetic Field (Oe)','Bridge 3 Resistance (ohms)','R']], *args, **kwargs)

