import os.path
path1='/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice-all/male/'
path2='/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice-all/female/'
path3='/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/all/'

#file = open('/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice.csv')
file = open('/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice.csv')
f = file.read()
aaa = f.split('\n')
for i in range(1,3169):
    filename=str('voice')+str(i)
    file=open(os.path.join(path3, filename),'w')
    file.write(aaa[i])
    file.close()

for i in range(1, 3169):
    filename=str('voice')+str(i)
    file = open(path3+filename)
    f = file.read()
    aaa=f.split(',')
    length = len(aaa)
    if (aaa[length-1]=='"male"') :
        f=''
        for j in range(length-1):
            f+='feature'+str(j)+', '+aaa[j]+','
        f+='feature'+str(length-1)+', '+'"male"'   #1==male
        file=open(os.path.join(path1, filename),'w')
        file.write(f)
        file.close()
    else:
        f=''
        for j in range(length-1):
            f+='feature'+str(j)+', '+aaa[j]+','
        f+='feature'+str(length-1)+', '+'"female"'   #0==female
        file=open(os.path.join(path2, filename),'w')
        file.write(f)
        file.close()
    file.close()
