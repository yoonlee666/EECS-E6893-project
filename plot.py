import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import os.path
path='/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/all/'
#y_axis=np.zeros((1584,1),np.float32)
#y_axis=np.arange(-8, 7.84, 0.01)
#mean_freq_male=np.zeros((1584,1))
#y_axis=[]*1584
mean_freq_male=[]
#mean_freq_female=np.zeros((1584,1))
mean_freq_female=[]
for i in range(1, 3169):
    filename=str('voice')+str(i)
    file = open(path+filename)
    f = file.read()
    aaa=f.split(',')
    length = len(aaa)
    if aaa[length-1]=='"male"':
        mean_freq_male.extend([aaa[0]])   #attribute 0
    else:
        mean_freq_female.extend([aaa[0]])   #attribute 0
    file.close()
#y_male=[0]*len(mean_freq_male)
y_male=range(1,len(mean_freq_male)+1,1)
#y_female=[0]*len(mean_freq_female)
y_female=range(1,len(mean_freq_male)+1,1)
pl.plot(mean_freq_male, y_male, 'bo')
pl.plot(mean_freq_female, y_female, 'ro')
pl.show()
