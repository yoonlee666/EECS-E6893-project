## this python file is for prediciton
## usage: write ten features in /usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice_ext.csv file
## output male/female for each instance

from sklearn.ensemble import GradientBoostingClassifier
import pickle

all_data = []
all_label = []
with open("/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice_ext.csv", 'rb') as file:
    row = 0
    for line in file.readlines():
        row += 1
        if row == 1:
            continue
        else:
            tokens = line[:-1].split(',')
            all_data.append([float(t) for t in tokens[:-1]])
            all_label.append(tokens[-1][0:-1])
# GB-ext dataset
gbclf = GradientBoostingClassifier()

pickle.dump(gbclf, open( "/Users/yoonlee/Desktop/model.pkl", "wb" ) )
gbclf = pickle.load(open('/Users/yoonlee/Desktop/model.pkl', 'rb'))
gbclf.fit(all_data, all_label)
test_data = []
with open("/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/test_data.csv", 'rb') as file:
    row = 0
    for line in file.readlines():
        row += 1
        tokens = line[:-1].split(',')
        test_data.append([ float(t) for t in tokens[:]])
print gbclf.predict(test_data)
