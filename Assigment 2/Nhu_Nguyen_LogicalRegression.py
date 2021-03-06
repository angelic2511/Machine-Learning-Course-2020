
#************************************************************************************
# Nhu Nguyen
# EE5321 – HW#2 - Logical Regression model
# Filename: Nhu_Nguyen_LogicalRegression.py
# Due: 9/23/20
##************************************************************************************


#imports for the program
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

#reading the dataset, creating dataframe
#directory must be changed to your computer's directory
df = pd.read_csv (r'C:\Users\angel\Desktop\FALL 2020\EE\Asignment 1\cars.csv')
df.columns = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'output']

#preprocessing required feature's data and classlabel
#manual buying value assignments for the data
buying_mapping = {
'vhigh': 4,
'high': 3,
'med': 2,
'low': 1}
df['buying'] = df['buying'].map(buying_mapping)

#manual maintenance value assignments for the data
maint_mapping = {
 'vhigh': 4,       
'high': 3,
'med': 2,
'low': 1}
df['maint'] = df['maint'].map(maint_mapping)

#manual safety value assignments for the data
safety_mapping = {
'high': 3,
'med': 2,
'low': 1}
df['safety'] = df['safety'].map(safety_mapping)


#filtering dataset for "high" "safety" and >="high" "price"
new_df = df.loc[(df['buying']>=3) & (df['maint'] >=3) & (df['safety'] ==3)]


#declare a new column named "price"
new_df['price']=0
#combining "buying" and "maint" in one "price"
new_df.loc[(new_df['buying'] == 4) &  (new_df['maint'] == 4),'price'] = 4
new_df.loc[(new_df['buying'] == 4) & (new_df['maint'] == 3), 'price'] = 3
new_df.loc[(new_df['buying'] == 3) & (new_df['maint'] == 4), 'price'] = 2 
new_df.loc[(new_df['buying'] == 3) & (new_df['maint'] == 3), 'price'] = 1 

output_mapping = {label:idx for idx,label in enumerate(np.unique(df['output']))}
new_df['output'] = df['output'].map(output_mapping)
print(new_df)

#Separating data & target information
X=new_df.iloc [:, [5, 7]]
y= new_df.iloc [:, 6]
print(X)
print(y)

#Data split for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=1, stratify=y)


#Scaling training & test input data
sc = StandardScaler()
sc.fit(X_train)
sc.fit(X_test)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

print ('Train set: ', X_train.shape, y_train.shape)
print ('Test set: ', X_test.shape, y_test.shape)

#Creating Logistic Regression with C parameter
LR = LogisticRegression(C=1, solver='liblinear', penalty='l1', max_iter=1000)

#This is training the model
LR.fit(X_train_std, y_train) 
LR

#Testing the model data
y_pred = LR.predict(X_test_std)
y_pred

# Predict Probability
y_pred_prob = LR.predict_proba(X_test)
y_pred_prob

#calculating the training and test accuracy values
train_acc = ('\nTraining Accuracy: %.2f' % LR.score(X_train_std, y_train))
test_acc = ('\nTest Accuracy: %.2f' % LR.score(X_test_std, y_test))
miss_sample = ('\nMisclassified samples: %d' % (y_test != y_pred).sum())

#printing out train_acc, test_acc, miss_sample
print(train_acc)
print(test_acc)
print(miss_sample)

#printing out the training and test accuracy values to a text file
LR_file = open("C:/Users/angel/Desktop/FALL 2020/EE/Assignment 2/LR_output.txt","w")
   
LR_file.write(train_acc)
LR_file.write(test_acc)
LR_file.write(miss_sample)

LR_file.close()    

#------------------------function for plotting  
def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    class_label=('acc', 'good', 'unacc', 'vgood')
    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1], alpha=0.8, c=colors[idx], marker=markers[idx], label=class_label[cl], edgecolor='black')
    if test_idx:
       # plot all samples
        X_test, y_test = X[test_idx, :], y[test_idx]
        plt.scatter(X_test[:, 0], X_test[:, 1],
        c='', edgecolor='black', alpha=1.0,
        linewidth=1, marker='o',
        s=100, label='test set')
#--------------------------end of the plotting function

# combine traing and test splits into variable for plotting purposes
X_combined_std = np.vstack((X_train_std, X_test_std))
y_combined = np.hstack((y_train, y_test))

#calling the function "plot_decision_regions"
plt.figure(1)
plot_decision_regions(X=X_combined_std, y=y_combined, classifier=LR, test_idx=range(1, 144))
plt.xlabel('price')
plt.ylabel('safety')
plt.legend(loc='upper left')

#saving plot
plt.savefig('LR_plot.png')

#showing plot
plt.show()


