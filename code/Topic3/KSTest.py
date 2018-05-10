import math
import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

def diff(f,s):
        s=set(s)
        return [it for it in f if it not in s]

def outlier(x): #Method for Outlier Detection
        x = np.array(x)
        upper_q = np.percentile(x, 75)
        lower_q = np.percentile(x, 25)
        iqr = (upper_q - lower_q) * 1.5
        acceptable_range = (lower_q - iqr, upper_q + iqr)
        return acceptable_range

def calculate():
	list1=[]
	list4=[]
	flag1=True
	flag=True
	with open('processed_data.csv','r') as inf:
                reader=csv.reader(inf)
                lst=[]
                for row in reader:
                        if flag1:
                                flag1=False
                                continue
                        lst.append(float(row[32]))
                accept=outlier(lst)
        with open('processed_data.csv','r') as f:
                reader=csv.reader(f)
                for row in reader:
                        if flag:
                                flag=False
                                continue
                        if(float(row[32]) >  accept[0] and float(row[32]) <  accept[1]):  # Removing Outliers
                                if(row[5]=='Police Administrator I'):
                                        list1.append(float(row[32])) # police Administrators Costs will be in this list
                                elif(row[5]=='Fire Administrator'):
                                        list4.append(float(row[32])) #Fire ADministrators Costs will be in this List
		
		result=scipy.stats.ks_2samp(list1,list4) #Using Library Function to Compute Absolute Maximum difference of two CDF's

		m=len(list1)
		n=len(list4)
		threshold=1.36*(((m+n)/m*n*1.0)**0.5)
		val=(m+n)/float(m*n)		
		val1=np.sqrt(val)
		thr=1.36*val1
		print(result[0],thr)
		if(result[0]>=thr): #CHecking whether absolute difference will be greater than threshold
			print("Rejecting Null Hypothesis ---- Distributions Police Administrator I and Fire Administrator are Different")
		else :
			print("Accepting Null Hypothesis ---- Distributions Police Administrator I and Fire Administrator are Identical")
		#Plotting Distributions PDF's
		sns.distplot(list1)
		plt.show()
		sns.distplot(list4)
		plt.show()
calculate()
