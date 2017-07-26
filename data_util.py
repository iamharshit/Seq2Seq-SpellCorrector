import numpy as np
import pandas as pd

def judge(word):
    return word.isalpha()

def clean(data):
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

def load(filename):
    df = pd.read_csv(filename)
    ans = zip( list(df['Correct Words']), list(df['Incorrect Words']))
    return clean(ans)

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
