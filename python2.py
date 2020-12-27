import os
import pickle

# Get the path of current working directory
#path = os.getcwd()
#print(path)
# Get the list of all files and directories
# in current working directory
#dir_list = os.listdir(path)

#print("Files and directories in '", path, "' :")
# print the list
#print(dir_list)

#print(result)

model = pickle.load(open('/content/modelbro', 'rb'))

example = ["Rishi" ]
result = model.predict(example)

print(result)

#create the model/evaluate/getting metrics such as accuracy, precision, recall
#save the model file on the system to specific hardcoded directory
# - run Python script 1.exe - run this part in Index action



#edit import file and set sentiments = the user input
#load the model - read model file from system - hardcoded
#run python script 2.exe - read result
