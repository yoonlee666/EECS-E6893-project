import os.path
path1='/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice-all/voice-train/male'
path2='/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice-all/voice-train/female'
path3='/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice-all/voice-test/male'
path4='/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice-all/voice-test/female'
file = open('/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice.csv')
f = file.read()
aaa = f.split('\n')
for i in range(301,1585):
    filename=str('male')+str(i)
    file=open(os.path.join(path1, filename),'w')
    file.write(aaa[i])
    file.close()
for i in range(1,301):
    filename=str('male')+str(i)
    file=open(os.path.join(path3, filename),'w')
    file.write(aaa[i])
    file.close()
for i in range(1885,3169):
    filename=str('female')+str(i)
    file=open(os.path.join(path2, filename),'w')
    file.write(aaa[i])
    file.close()
for i in range(1585,1885):
    filename=str('female')+str(i)
    file=open(os.path.join(path4, filename),'w')
    file.write(aaa[i])
    file.close()
