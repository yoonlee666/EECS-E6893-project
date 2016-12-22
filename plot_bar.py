### this python file tests the accuracy of using three algorithms with raw and extracted dataset
### output is the accuracy for each algorithm and a corresponding accuracy plot

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
all_data = []
all_label = []
with open("/usr/local/Cellar/hadoop/2.7.3/mahout/mahout_voice/voice.csv", 'rb') as file:
    row = 0
    for line in file.readlines():
        row += 1
        if row == 1:
            continue
        else:
            tokens = line[:-1].split(',')
            all_data.append([float(t) for t in tokens[:-1]])
            all_label.append(tokens[-1][1:-1])
# NB-raw dataset
nbclf = GaussianNB()
scores1 = cross_val_score(nbclf, all_data, all_label, cv=5, scoring='accuracy')
print 'naive bayes using raw dataset:'
print np.mean(scores1)
# RF-raw dataset
rfclf = RandomForestClassifier()
scores3 = cross_val_score(rfclf, all_data, all_label, cv=5, scoring='accuracy')
print 'Random Forest using raw dataset:'
print np.mean(scores3)
# GB-raw dataset
gbclf = GradientBoostingClassifier()
scores4 = cross_val_score(gbclf, all_data, all_label, cv=5, scoring='accuracy')
print 'Gradient Boosting using raw dataset:'
print np.mean(scores4)

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
# NB-ext dataset
nbclf = GaussianNB()
scores2 = cross_val_score(nbclf, all_data, all_label, cv=5, scoring='accuracy')
print 'naive bayes using extracted dataset:'
print np.mean(scores2)
# RF-ext dataset
rfclf = RandomForestClassifier()
scores5 = cross_val_score(rfclf, all_data, all_label, cv=5, scoring='accuracy')
print 'Random Forest using extracted dataset:'
print np.mean(scores5)
# GB-ext dataset
gbclf = GradientBoostingClassifier()
scores6 = cross_val_score(gbclf, all_data, all_label, cv=5, scoring='accuracy')
print 'Gradient Boosting using extracted dataset:'
print np.mean(scores6)
# plot graph
y_NB = [np.mean(scores1), np.mean(scores2)]
y_RF = [np.mean(scores3), np.mean(scores5)]
y_GB = [np.mean(scores4), np.mean(scores6)]
x = [0.1, 0.5]
width = 0.4/1
plt.bar([0.1, 1.5], y_NB, width, color="blue", label='Naive Bayes')
plt.bar([0.5, 1.9], y_RF, width, color="red", label='Random Forest')
plt.bar([0.9, 2.3], y_GB, width, color="green", label='Gradient Boosting')
plt.legend(loc='upper right')
plt.axis([0, 3.8, 0, 1])
my_xticks = ['raw dataset','extracted dataset']
plt.xticks([0.7,2.1], my_xticks, fontsize=15)
plt.text(0.1-0.05,np.mean(scores1)+0.01, str(np.mean(scores1)), color='black')
plt.text(0.5-0.05,np.mean(scores3)+0.01, str(np.mean(scores3)), color='black')
plt.text(0.9-0.05,np.mean(scores4)-0.03, str(np.mean(scores4)), color='black')
plt.text(1.5-0.05,np.mean(scores2)+0.01, str(np.mean(scores2)), color='black')
plt.text(1.9-0.05,np.mean(scores5)+0.01, str(np.mean(scores5)), color='black')
plt.text(2.3-0.05,np.mean(scores6)-0.03, str(np.mean(scores6)), color='black')
plt.title('accuracy comparison', fontsize=25)
fig = plt.gcf()
plt.show()
