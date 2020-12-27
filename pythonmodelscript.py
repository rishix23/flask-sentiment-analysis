import warnings
import io
import pandas as pd

warnings.filterwarnings('ignore')

#Dataset is now stored in a Pandas Dataframe
dataFrame = pd.read_csv(('Final_Data2.csv'))
dataFrame.head()

# #dataFrame.shape()

# #shows info on data frame
dataFrame.info()

print(dataFrame.describe().transpose())

# """**Cleaning**"""
# finding null valiues (should be 0)
count = dataFrame.isnull().sum().sort_values(ascending=True)
 # pandas.set_option('display.max_rows', dataFrame.shape[0]+1)
print(count)

# # Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
%matplotlib inline
print('Percentage for defualt\n')

# #With normalize set to True, returns the relative frequency
print(round(dataFrame.Sentiment.value_counts(normalize=True)*100,2))

round(dataFrame.Sentiment.value_counts(normalize=True)*100,2).plot(kind='bar')
plt.title('Percenatage of sentiment')
plt.show()

# # try with uneven distribution

import re
import string

def text_clean_1(text):
  text = text.lower()
  text = re.sub('\[.*?\]', '', text)
  text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
  text = re.sub('\w*\d\w*', '', text)
  return text

cleaned_1 = lambda x: text_clean_1(x)

dataFrame['cleaned_text'] = pd.DataFrame(dataFrame.Text.apply(cleaned_1))

dataFrame.head()

from sklearn.model_selection import train_test_split

Independent = dataFrame.cleaned_text
Dependent = dataFrame.Sentiment

IV_train, IV_test, DV_train, DV_test = train_test_split(Independent, Dependent, test_size = 0.1, random_state = 225)

print('IV_train', len(IV_train))
print('IV_test', len(IV_test))
print('DV_test', len(DV_train))
print('DV_test', len(DV_test))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

tvec = TfidfVectorizer()
clf2 = LogisticRegression(solver = "lbfgs")

from sklearn.pipeline import Pipeline
model = Pipeline([('vectorizer', tvec),('classifier', clf2)])

model.fit(IV_train, DV_train)

from sklearn.metrics import confusion_matrix

predictions = model.predict(IV_test)

confusion_matrix(predictions, DV_test)

from sklearn.metrics import accuracy_score, precision_score, recall_score

print("Accuaracy: ", accuracy_score(predictions, DV_test))
print("Precision : ", precision_score(predictions, DV_test, average= 'weighted'))
print("Recall : ", recall_score(predictions, DV_test, average = 'weighted'))

example = ["Rishi" ]

result = model.predict(example)

print(result)

# import pickle

# pickle.dump(model, open('modelbro', 'wb'))
