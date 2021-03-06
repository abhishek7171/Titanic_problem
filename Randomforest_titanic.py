import csv 
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
import re
from sklearn.cross_validation import cross_val_score

# Convert the gender to integers
def convertGender(gender):
	if gender == 'female':
		gender = 0
	if gender == 'male':
		gender = 1
	return gender

# Convert the embarked field to integers
def convertEmbarked(embarked):
	if embarked == 'C':
		embarked = 0
	if embarked == 'Q':
		embarked = 1
	if embarked == 'S':
		embarked = 2
	else:
		embarked = '2'
	return embarked

# return title
def getTitle(name):
	for word in name.split():
		if word.endswith('.'):
			title=word
			break
	return title

# convert title to hash 

def getTitleHash(title,gender):
	has = ord(title[0]) + len(title) + int(gender)
	return has

# returns one if the passenger had a family
def getFamily(sibsp,parch):
	if int(sibsp) + int(parch) > 0:
		family = 1
	else:
		family = 0
	return family

# Pull out the dept from the ticket number
def getTicketCode(ticket):
    deptName = re.sub(r"$\d+\W+|\b\d+\b|\W+\d+$", "", ticket)
    if len(deptName) == 0:
        deptName = 'none'
    deptCode = ord(deptName[0]) + len(deptName)
    return deptCode

if __name__ == '__main__':	

	
	
	train = csv.reader(open('train_titanic.csv','rb'))
	header = train.next()
	
	#READING TRAIN DATA	
	train_data=[]
	for row in train:
	        train_data.append(row)
	
	train_data = np.array(train_data)
	
	print("DONE Reading Train Data")
	
	print("Preprocessing Train Data")
	# replace categorical attributes
	for row in train_data:
		
		row[4] = convertGender(row[4])
		title = getTitle(row[3])
		row[3] = getTitleHash(title,row[4])
		row[6] = getFamily(row[6],row[7])
		row[8] = getTicketCode(row[8])
		row[11] = convertEmbarked(row[11])
		

	features = train_data[0::,[2,3,4,6,8,11]]
	result = train_data[0::,1]
	print("DONE Preprocessing Train Data")

	print("Fitting Train Data")
	forest =RandomForestClassifier(n_estimators = 1000)
	
	forest = forest.fit(features,result)
	print("DONE Fitting Train Data")

	print("Calculating score")
	scores = cross_val_score(forest, features, result)
	print("Training score")
	print scores.mean()
	print("DONE Calculating score")
	

	#READING TEST DATA
	print("Reading Test Data")
	test = csv.reader(open('test_titanic.csv','rb'))
	header = test.next()
	
	test_data=[]
	for row in test:
	        test_data.append(row)
	test_data = np.array(test_data)
	print("DONE Reading Test Data")
	
	# replace categorical attributes
	print("Preprocessing Test Data")
	for row in test_data:
		
		row[3] = convertGender(row[3])
		title = getTitle(row[2])
		row[2] = getTitleHash(title,row[3])
		row[5] = getFamily(row[5],row[6])
		row[7] = getTicketCode(row[7])
		row[10] = convertEmbarked(row[10])
		

	features = test_data[0::,[1,2,3,5,7,10]]
	print("DONE Preprocessing Test Data")
	
	print("Predicting Test Data")
	Output = forest.predict(features)
	
	#np.savetxt("RandomForest.csv",Output,delimiter=",",fmt="%s")	
	#print("DONE Predicting Test Data")