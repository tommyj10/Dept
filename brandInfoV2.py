import numpy as np
import csv
import time

def getSum(array)    :

    category = array[:,0]
    valNum = array[:,1]

    countArr = [1]*len(category)
    countArr = np.array(countArr)

    newIndex = np.argsort(category)
    category = category[newIndex]
    valNum = valNum[newIndex]
    valNum.cumsum(out=valNum)
    countArr.cumsum(out=countArr)
    i = np.ones(len(category), 'bool')
    i[:-1] = category[1:] != category[:-1]
    valNum = valNum[i]
    category = category[i]
    countArr = countArr[i]
    valNum[1:] = valNum[1:] - valNum[:-1]
    countArr[1:] = countArr[1:] - countArr[:-1]

    outArray = np.array([category, valNum, countArr])
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

##   [0:'custid' 1:'date_time' 2:'store' 3:'product' 4:'brand' 5:'corner' 6:'pc' 7:'part'
##   8:'imported' 9:'amount' 10:'discount' 11:'installment']

mthArray = tuple([int(x.split('-')[1]) for x in data[1]])
stores = tuple([x for x in data[2]])
brands = tuple([x for x in data[4]])
originalPrice = tuple([int(x) for x in data[9]])
offPrice = tuple([int(x) for x in data[10]])
priceList = tuple(np.subtract(originalPrice, offPrice))
short = np.array([mthArray, stores, brands, priceList])
storeID = list(set(stores))
storeID.sort()
brandID = list(set(brands))
brandID.sort()
dictBrand = dict(zip(brandID, np.array(range(len(brandID)))))
dictStore = dict(zip(storeID, np.array(range(len(storeID)))))
brandIDList = [int(dictBrand[x]) for x in brands]
storeIDList = [int(dictStore[x]) for x in stores]
short = np.array([mthArray, storeIDList, brandIDList, priceList])
short = np.transpose(short)

startTime = time.time()

with open("점포별 월별 최고 인기n수익 브랜드V2.txt", 'w') as file1:

    for storeIndex in range(len(storeID)):

        for mth in range(1,13)   :

            Z = np.copy(short)
            Z_filtered = [x for x in Z if int(x[1]) == storeIndex and int(x[0]) == mth]
            brandFiltered = [x[2] for x in Z_filtered]
            priceFiltered = [int(x[3]) for x in Z_filtered]

            x = np.array([brandFiltered, priceFiltered])
            x = np.transpose(x)
            outArr = getSum(x)
            brandSum = outArr[:,0]
            priceSum = outArr[:,1]
            countSum = outArr[:,2]

            srtPrice = np.argsort(priceSum)[::-1]
            srtPop = np.argsort(countSum)[::-1]

            titleStr = "\n\n--- %s %d월 최고 인기/수익 브랜드---\n" % (storeID[storeIndex], mth)
            file1.write(titleStr)
            #list(my_dict.keys())[list(my_dict.values()).index(112)]
            for i in range(5)  :
                orderN = "{2:}위 인기 브랜드 주문 건 수  : {0:} --> {1:,}건\n" .format (list(dictBrand.keys())[list(dictBrand.values()).index(brandSum[srtPop[i]])], countSum[srtPop[i]], i+1)
                profitN = "{2:}위 인기 브랜드 판매 수익   : {0:} --> {1:,}원\n" .format (list(dictBrand.keys())[list(dictBrand.values()).index(brandSum[srtPop[i]])], priceSum[srtPop[i]], i+1)
                file1.write(orderN)
                file1.write(profitN)
            file1.write('\n')
            for i in range(5)  :
                orderN = "{2:}위 매출 브랜드 주문 건 수  : {0:} --> {1:,}건\n" .format (list(dictBrand.keys())[list(dictBrand.values()).index(brandSum[srtPrice[i]])], countSum[srtPrice[i]], i+1)
                profitN = "{2:}위 매출 브랜드 판매 수익   : {0:} --> {1:,}원\n" .format (list(dictBrand.keys())[list(dictBrand.values()).index(brandSum[srtPrice[i]])], priceSum[srtPrice[i]], i+1)
                file1.write(orderN)
                file1.write(profitN)

print("--- %s seconds ---" % (time.time() - startTime))