list1=[]
list4=[]
import math
import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns


count=0
samples=input("enter number of samples")  #Number of permutations 
dup=samples
x1=[]
x2=[]
def permutations(lis1,obs,n=0): #Method which permutes numbers and check whether mean of new list is greater than mean of observed list
	global count
	global samples
	global x1
	global x2
	global list1
	global list4
	length=len(list1)+len(list4)
	length1=len(list1)
        length2=len(list4)
	samples=samples-1;
	if(n==len(lis1)):
		lis1=x1+lis1+x2
		temp1=lis1[:length1]
		temp2=lis1[length1:]
		avg=math.fabs(np.mean(temp1)-np.mean(temp2))
		if(avg>obs):
			count=count+1
	else:	
		for i in xrange(n,len(lis1)):
			if(samples<=0):
				break
			lis1[i],lis1[n]=lis1[n],lis1[i]
			permutations(lis1,obs,n+1)
			lis1[i],lis1[n]=lis1[n],lis1[i]



def diff(f,s):
        s=set(s)
        return [it for it in f if it not in s]

def outlier(x): # METHOD FOR detecting outliers
        x = np.array(x)
        upper_q = np.percentile(x, 75)
        lower_q = np.percentile(x, 25)
        iqr = (upper_q - lower_q) * 1.5
        acceptable_range = (lower_q - iqr, upper_q + iqr)
        return acceptable_range

def calculate():
	global list1
	global list2
	global list3
	global list4
	global list5
	global list6
	global x1
	global x2
	flag=True
	flag1=True
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
                        if(float(row[32]) >  accept[0] and float(row[32]) <  accept[1]): # REmoving Outliers
                                if(row[5]=='Police Administrator I'):
                                        list1.append(float(row[32])) # Police Administrator I costs will be in this list
                                elif(row[5]=='Fire Administrator'):
                                        list4.append(float(row[32])) #Fire Administrator costs will be in this list
		obs=math.fabs(np.mean(list1)-np.mean(list4))
		newlist=list1+list4
		newlist.sort()
		length=len(list1)+len(list4)
		length1=3*(length)/4;
		length2=(length)/4;  #Implementing permutations by taking bunch of numbers from middle of appended list and permuting them because of limited stack depth
		x1=newlist[:length2]
		newl=newlist[length2:length1]
		x2=newlist[length1:length]
		permutations(newl,obs)
		pvalue=float(count)/dup
		if(pvalue<=0.05): #comparing p value with 95% CI alpha value
			print("Rejecting NUll Hypothesis --- Distributions Police Administrator I and Fire Administrator are Different")
		else:
			print("Accepting Null Hypothesis --- Distributions Police Administrator I and Fire Administrator are Identical")
		#Plotting CDF's of two Distributions
		cnt,edge=np.histogram(list1,bins=10,normed=True)
                cdf=np.cumsum(cnt)
                plt.plot(edge[1:],cdf/cdf[-1],label='CDF of Police Administrator I')
                plt.xlabel('Data')
                plt.ylabel('Probability')
                plt.legend()
                cnt,edge=np.histogram(list4,bins=10,normed=True)
                cdf=np.cumsum(cnt)
                plt.plot(edge[1:],cdf/cdf[-1],label='CDF of Fire Administrator')
                plt.xlabel('Data')
                plt.ylabel('Probability')
                plt.legend()
                plt.show()

calculate()
