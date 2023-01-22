import sys
import pandas as pd
import math as m
import warnings
from pandas.api.types import is_numeric_dtype
warnings.filterwarnings("ignore")
##Error Handling
#For checkin no of parameters in command line argument
if(len(sys.argv)<5):
    print("Number of parameters entered are less than required parameters")
    sys.exit(1)
elif(len(sys.argv)>5):
    print("Number of parameters entered are more than required parameters")
    sys.exit(1)

input_file=sys.argv[1]
weights=sys.argv[2]
impacts=sys.argv[3]
resFileName=sys.argv[4]
lenInput=len(input_file)
lenOutput=len(resFileName)

#For checking file format
if(input_file[-4:]!=".csv"):
    print("File format not supported,Please upload csv file")
    sys.exit(1)
elif(resFileName[-4:]!=".csv"):
    print("output file format not supported,Please enter valid output format")
    sys.exit(1)

 #For checking valid entry and comma separation of
try:
    weights=weights.split(',')
    numbers = [int(x.strip()) for x in weights]
    impacts=impacts.split(',')
    characters=[str(x.strip()) for x in impacts]
except:
    print('Please enter weights with only numbers separated by commas ')
    sys.exit(1)

for i in impacts:
    if i not in ['+','-']:
        print("Please enter valid impact '+' or '-' separated by commas")
        sys.exit(1)
try:
    df=pd.read_csv(input_file)
except:
    print("File not found")
    sys.exit(1)
finalData=df
if((df.columns.size-1)<3):
    print("Less no of columns in input file")
    sys.exit(1)
elif(((df.columns.size-1)!=len(weights))&((df.columns.size-1)!=len(impacts))):
    print("Weights,impacts are not equal to no of columns")
    sys.exit(1)
if(df.columns.size-1>len(weights)):
    print("Insufficient number of weights are entered")
    sys.exit(1)
elif(df.columns.size-1>len(impacts)):
    print("Insufficient number of impacts are entered")
    sys.exit(1)
elif(df.columns.size-1<len(weights)):
    print("More than required number of weights are entered")
    sys.exit(1)
elif(df.columns.size-1<len(impacts)) :
    print("More than required number of impacts are entered")
    sys.exit(1)
noOfColumns=df.axes[1]
colNames=list(df.columns)
colNames.pop(0)
df=df[colNames]

for i in colNames:
    if(is_numeric_dtype(df[i])==False):
        print("Input File contains non numeric data")
        sys.exit(1)

sqrSum={}
idealBest={}
idealWorst={}
idealBestDistance=[]
idealWorstDistance=[]
perfScore=[]
ranking={}
rank=[]
def rootSquareSum(value):
    sum=0
    for i in value:
        sum=sum+(i*i)
    return m.sqrt(sum)

def normalization(value):
    for i in colNames:
        df[i]=df[i]/value[i]

##For normalization
for i in colNames:
    sqrSum[i]=rootSquareSum(df[i])

normalization(sqrSum)


##weight assignment
weights=[int(i) for i in weights]
index=0

for i in colNames:
    df[i]=df[i]*weights[index]
    index=index+1

##finding ideal best and ideal worst
indexImpact=0
for i in colNames:
    if impacts[indexImpact]=='-':
        idealBest[i]=min(df[i])
        idealWorst[i]=max(df[i])
        indexImpact=indexImpact+1
    else:
        idealBest[i]=max(df[i])
        idealWorst[i]=min(df[i])
        indexImpact=indexImpact+1

##finding ideal best and ideal worst distance
for i in df.index:
    sum=0
    for j in colNames:
        sum=sum+m.pow((df[j][i]-idealBest[j]),2)
    idealBestDistance.append(m.sqrt(sum))

for i in df.index:
    sum=0
    for j in colNames:
        sum=sum+m.pow((df[j][i]-idealWorst[j]),2)
    idealWorstDistance.append(m.sqrt(sum))

#finding performance score
for i in df.index:
    perfScore.append(idealWorstDistance[i]/(idealBestDistance[i]+idealWorstDistance[i]))

finalData["Topsis Score"]=perfScore

##finding rank
sortedScore=sorted(perfScore,reverse=True)
for i in range(0,len(sortedScore)):
    ranking[sortedScore[i]]=i
for j in perfScore:
    rank.append(ranking[j]+1)
finalData['Rank']=rank
finalData.to_csv(resFileName,index=False)



# print("hello from python")
