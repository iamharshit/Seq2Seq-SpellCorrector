import csv
import sys

def filewriter(filename, row_list):
	with open(filename, 'a') as f:
		writer = csv.writer(f)
		for row in row_list:
			writer.writerow([row[0],row[1]])

def check(filename, final_list):
	for item in final_list:
		if item[0].isdigit() or item[0].isdigit() or item=='':
			print 'Falseness!!!! in ',filename
			sys.exit(1)			

def process_BLOORDAT643():
	final_list = []
	filename = 'BLOORDAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			final_list.append((row[0],row[2]))
	check(filename, final_list)
	return final_list

def process_FAWTHROP1DAT643():
	final_list = []
	filename = 'FAWTHROP1DAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			final_list.append((row[0],row[-1]))
	check(filename, final_list)
	return final_list

def process_FAWTHROP2DAT643():
	final_list = []
	filename = 'FAWTHROP2DAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			row = list(filter(lambda x: x != '', row))
			final_list.append((row[0],row[1]))
	check(filename, final_list)
	return final_list

def process_SHEFFIELDDAT643():
	final_list = []
	filename = 'SHEFFIELDDAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			row = list(filter(lambda x: x != '', row))
			final_list.append((row[0],row[1]))
	check(filename, final_list)
	return final_list

def process_UPWARDDAT643():
	final_list = []
	filename = 'UPWARDDAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			final_list.append((row[0],row[2]))
	check(filename, final_list)
	return final_list

def process_ABODAT643():
	final_list = []
	filename = 'ABODAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=',')
		for row in reader:
			if(row[0][0]!='$'):
				row = list(filter(lambda x: x != '', row))
				row = [item.strip() for item in row]
				row =	[item[:-1] if item[-1]=='.' else item for item in row]			
				for item in row:
					ans=item.split(' ')	
					final_list.append((ans[1],ans[0]))
	check(filename, final_list)
	return final_list

def process_APPLING2DAT643():
	final_list = []
	filename = 'APPLING2DAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			if row[0][0]!='$' and len(row)!=1:
				final_list.append((row[0],row[1]))
	check(filename, final_list)
	return final_list

def process_EXAMSDAT_643():
	final_list = []
	filename = 'EXAMSDAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			row = list(filter(lambda x: x != '', row))
			if len(row)>=2 and row[0][0]!='$' and row[0].isdigit()==False and row[1].isdigit()==False:
				final_list.append((row[1],row[0]))
	check(filename, final_list)
	return final_list

def process_PERIN1DAT643():
	final_list = []
	filename = 'PERIN1DAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			if len(row)>=2 and row[0][0]=='+':
				flag = True
				for item in row:
					if(item.isdigit()):
						flag = False
				if flag:
					row = list(filter(lambda x: x != '' and x != '+' and x != '!', row))
					row =	[item[:-1] if item[-1]==',' else item for item in row]
					it = iter(row)
					for item in it:
						final_list.append((next(it),item))
	check(filename, final_list)
	return final_list

def process_SUOMIDAT643():
	final_list = []
	filename = 'SUOMIDAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			if len(row)>=2 and row[0][0]!='$':
					row = list(filter(lambda x: x != '' and x != '+' and x != '!' and x != '.', row))
					row =	[item[:-1] if item[-1]==',' or item[-1]=='.' else item for item in row]
					it = iter(row)
					for item in it:
						if(item.isdigit()==False):
							final_list.append((next(it),item))
	check(filename, final_list)
	return final_list

def process_TELEMARKDAT643():
	final_list = []
	filename = 'TELEMARKDAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			row = list(filter(lambda x: x != '', row))
			final_list.append((row[1],row[0]))
	check(filename, final_list)
	return final_list

def process_TESDELLDAT643():
	final_list = []
	filename = 'TESDELLDAT.643'
	with open(filename, 'r') as f:	
		reader = csv.reader(f,delimiter=' ')
		for row in reader:
			if len(row)>=2 and row[0][0]=='+':
				flag = True
				for item in row:
					if(item.isdigit()):
						flag = False
				if flag:
					row = list(filter(lambda x: x != '' and x != '+' and x != '!', row))
					row =	[item[:-1] if item[-1]==',' else item for item in row]
					it = iter(row)
					for item in it:
						final_list.append((next(it),item))
	check(filename, final_list)
	return final_list

#format: Correct, Incoorect
filewriter('final_dataset.csv',[('Correct Words', 'Incorrect Words')])

filewriter('final_dataset.csv',process_BLOORDAT643())
filewriter('final_dataset.csv',process_FAWTHROP1DAT643())
filewriter('final_dataset.csv',process_FAWTHROP2DAT643())
filewriter('final_dataset.csv',process_SHEFFIELDDAT643())

filewriter('final_dataset.csv',process_UPWARDDAT643())
filewriter('final_dataset.csv', process_ABODAT643())

filewriter('final_dataset.csv', process_APPLING2DAT643() )

filewriter('final_dataset.csv', process_EXAMSDAT_643() )
filewriter('final_dataset.csv', process_PERIN1DAT643() )
filewriter('final_dataset.csv', process_SUOMIDAT643() )
filewriter('final_dataset.csv', process_TELEMARKDAT643() )
filewriter('final_dataset.csv', process_TESDELLDAT643() )

