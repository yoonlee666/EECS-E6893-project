## This python file is for doing main features extraction from raw dataset.
## Output is a plot of one attribute

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
        mean_freq_male.extend([aaa[11]])   #can change attribute here
    else:
        mean_freq_female.extend([aaa[11]])   #can change attribute here
    file.close()
#y_male=[0]*len(mean_freq_male)
y_male=range(1,len(mean_freq_male)+1,1)
#y_female=[0]*len(mean_freq_female)
y_female=range(1,len(mean_freq_female)+1,1)

pl.plot(mean_freq_male, y_male, 'bo', label='male')
pl.plot(mean_freq_female, y_female, 'ro', label='female')
pl.legend(loc='upper right')
pl.title('average of fundamental frequency measured across acoustic signal', fontsize=14)
pl.show()
