import numpy as np
import csv

def getSum(array)    :

    category = array[:][0]
    valNum = array[:][1]

    newIndex = np.argsort(category)
    category = category[newIndex]
    valNum = valNum[newIndex]
    valNum.cumsum(out=valNum)
    i = np.ones(len(category), 'bool')
    i[:-1] = category[1:] != category[:-1]
    valNum = valNum[i]
    category = category[i]
    valNum[1:] = valNum[1:] - valNum[:-1]

    outArray = np.array([category, valNum])
    outArray = np.transpose(outArray)
    return outArray

dataList = []
with open("X_train_0404.csv") as f:

    reader = csv.reader(f)

    for row in reader:

        dataList.append(row)

df = np.array(dataList)
del dataList

dataIndex = np.array(df[0])
data = np.transpose(df[1:-1])
del df
 
custID = [int(x) for x in data[0]]

originalPrice = [int(x) for x in data[9]]
offPrice = [int(x) for x in data[10]]

priceList = np.subtract(originalPrice, offPrice)
uniqueCust = list(set(custID))

purchasedCost = [0]*len(uniqueCust)
purchasedCnt = [0]*len(uniqueCust)

trialArray = np.array([custID, priceList])

out = getSum(trialArray)

print(out)