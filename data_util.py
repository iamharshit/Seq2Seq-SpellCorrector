import numpy as np
import pandas as pd

def judge(word):
    return word.isalpha()

def clean(data):
	#Remove Commas
	try:
		for i in range(len(data)):
			if(type(data[i][0])==float  or type(data[i][1])==float):
				del data[i]
				continue
			if(data[i][0][-1]==','):
				data[i] = (data[i][0][:-1], data[i][1])
			if(data[i][1][-1]==','):
				data[i] = (data[i][0], data[i][1][:-1])
	except:
		pass	

	try:
		i=0
		while(i<len(data)):
			if judge(data[i][0])==False or judge(data[i][1])==False:
				del data[i]
				i-=1
			i+=1
	except:
				pass
	return data

def remove_conflicting_examples(data):
	correct_words, incorrect_words = np.array(data)[:,0], np.array(data)[:,1]
	correct_vocab, incorrect_vocab = list(set(correct_words)), list(set(incorrect_words))
   
	try:
		i=0
		while(i<len(data)):
			
			if data[i][0] in incorrect_vocab or data[i][1] in correct_vocab:
				del data[i]
				i-=1
			i+=1
	except:
		pass
	return data	

def load(filename):
    df = pd.read_csv(filename)
    ans = zip( list(df['Correct Words']), list(df['Incorrect Words']))
    return remove_conflicting_examples(clean(ans ))

def left_pad(list_):
    max_seq_len = 20
    ans = np.zeros((max_seq_len), dtype=int)
    ans[:len(list_)] = np.array(list_[:max_seq_len] )
    return ans
    
def string2indexes(word):
    return left_pad([ord(char)-96 for char in list(word)])
    
def preprocess(data):
    ans = []
    for row  in data:
        ans.append(( string2indexes(row[0].lower()), string2indexes(row[1].lower() ) ))
    return ans

def split_dataset_(data, ratio = [0.7, 0.15, 0.15]):
	x = np.array(data)[:,1]
	y = np.array(data)[:,0]
	data_len = len(x)
	lens = [ int(data_len*item) for item in ratio ]

	trainX, trainY = x[:lens[0]], y[:lens[0]]
	testX, testY = x[lens[0]:lens[0]+lens[1]], y[lens[0]:lens[0]+lens[1]]
	validX, validY = x[-lens[-1]:], y[-lens[-1]:]

	return (trainX,trainY), (testX,testY), (validX,validY)

def indexes2string(list_):
    temp = []
    for item in list_:
     if item!=0:
       temp.append(item)
    return ''.join([chr(item+96) for item in temp])
