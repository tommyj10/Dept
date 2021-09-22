##   전달드리는 사항엔 # 두 개를 써넣었습니다.
# 한 개 있는 건 참조용 코드로 #를 지우시고 출력하시면 데이터 분석 알고리즘을 만드는데
# 도움이 될 겁니다.

##   외부 라이브러리 numpy와 csv를 부릅니다.
import numpy as np
import csv
import time

##   빈 리스트를 하나 만듭니다.
dataList = []

##   CSV 라이브러리를 통해서 데이터를 불러모읍니다.
with open("X_train_0404.csv") as f:

    reader = csv.reader(f)

    for row in reader:

        dataList.append(row)

##   df가 dataList를 numpy array로 변형시킨 변수/리스트입니다. del dataList는 dataList라는 변수를
## 지우는 명령입니다.
df = np.array(dataList)
del dataList

##   뒤 코드부터 data[숫자]를 입력하시면 밑에 설명되어있는 항목들을 찾아보실 수 있습니다.
##   참고로 transpose 는 
##   1 2 3
##   4 5 6
##   같은 array들을
##   1 4
##   2 5
##   3 6
##   으로 바꿔줍니다. 유용하게 쓰일 수 있다 싶어서 사용했습니다.
##   [0:'custid' 1:'date_time' 2:'store' 3:'product' 4:'brand' 5:'corner' 6:'pc' 7:'part'
##   8:'imported' 9:'amount' 10:'discount' 11:'installment']
dataIndex = np.array(df[0])
data = np.transpose(df[1:-1])
del df

#print(data)

##   여기 이후로 코딩을 해주시면 됩니다.
##   data array 전부 있습니다. 
##   예를 들자면 data[0] 는 고객번호, data[1] 은 주문 시간들을 다 모아놓았습니다.

##   date_time 대신 원하시는 분류를 선택하시면 data[result]에 모든 데이터가 있습니다.
result = np.where(dataIndex == 'date_time')[0][0]

#print(np.where(dataIndex = 'date_time'))

##   원하시는 데이터를 targetArray에 넣으시면 됩니다.
##   참고로 말씀드리자면 원하시는 데이터가 int 형식이 아니면 int만 지워주시면 됩니다.
##   
#mthArray = []
#for i in range(len(data[result]))   :

 #   try :
        ##   만약에 날짜 중 몇 달인지만 알고싶으시면
        ##   밑에 있는 코드 한 줄을 지우시고
        #mthArray.append(int(data[result][i].split('-')[1])) 
        ##   으로 대체해주세요.
        #mthArray.append(int(data[result][i]))
  #  except ValueError   :
   #     continue

mthArray = tuple([int(x.split('-')[1]) for x in data[result]])
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

dictShort = dict(enumerate(short))
dictShort['month'] = dictShort.pop(0)
dictShort['store'] = dictShort.pop(1)
dictShort['brand'] = dictShort.pop(2)
dictShort['price'] = dictShort.pop(3)

dictBrand = dict(zip(brandID, np.array(range(len(brandID)))))
dictStore = dict(zip(storeID, np.array(range(len(storeID)))))
short = np.transpose(short)

startTime = time.time()
storeIndex = 0
with open("점포별 월별 최고 인기n수익 브랜드wo식품.txt", 'w') as file1:

    storeIndex = 0
    for mth in range(1,13)  :

        Z = np.array([x for x in short if int(x[0]) == mth])
        Z = np.transpose(Z)
        dictZ = dict(enumerate(Z))
        dictZ['month'] = dictZ.pop(0)
        dictZ['store'] = dictZ.pop(1)
        dictZ['brand'] = dictZ.pop(2)
        dictZ['price'] = dictZ.pop(3)

        brandSale = [0]*len(brandID)
        brandCnt = [0]*len(brandID)

        for i in range(len(dictZ['price']))    :

            if int(dictZ['month'][i]) == mth and dictStore[dictZ['store'][i]] == storeIndex   :
                brandSale[dictBrand[dictZ['brand'][i]]] += int(dictZ['price'][i])
                brandCnt[dictBrand[dictZ['brand'][i]]] += 1

                #print("분석 중 ...%7.3f%% 완료" % ((i+1)/len(dictZ['price'])*100))
                #print(brandID[i],brandSale[i],brandCnt[i])

            ## 식품 제외
            #brandSale[dictBrand['식품']] = 0
            #brandCnt[dictBrand['식품']] = 0

        brandSale2 = np.array(brandSale, dtype='int')
        brandCnt2 = np.array(brandCnt, dtype='int')
        brandID2 = np.array(brandID, dtype='object')

        #sortedIndex = np.argsort(brandSale2)
        sortedIndex = np.argsort(brandSale2)[::-1]
        newID = brandID2[sortedIndex]
        newSale = brandSale2[sortedIndex]
        newCnt = brandCnt2[sortedIndex]

        sortedIndex2 = np.argsort(brandCnt2)[::-1]
        newID2 = brandID2[sortedIndex2]
        newSale2 = brandSale2[sortedIndex2]
        newCnt2 = brandCnt2[sortedIndex2]

        finalVal = [(x,int(y),int(z)) for (x,y,z) in zip(newID, newSale, newCnt)]
        finalVal = finalVal[0:5]
        finalVal2 = [(x,int(y),int(z)) for (x,y,z) in zip(newID2, newSale2, newCnt2)]
        finalVal2 = finalVal2[0:5]


        titleStr = "\n\n--- %s %d월 최고 인기/수익 브랜드---\n" % (storeID[storeIndex], mth)

        file1.write(titleStr)
        cnt = 1
        for i in (finalVal2)  :
            orderN = "{2:}위 인기 브랜드 주문 건 수  : {0:} --> {1:,}건\n" .format (i[0], i[2], cnt)
            profitN = "{2:}위 인기 브랜드 판매 수익   : {0:} --> {1:,}원\n" .format (i[0], i[1], cnt)
            file1.write(orderN)
            file1.write(profitN)
            cnt += 1
        cnt = 1
        file1.write('\n')
        for i in (finalVal)  :
            orderN = "{2:}위 매출 브랜드 주문 건 수  : {0:} --> {1:,}건\n" .format (i[0], i[2], cnt)
            profitN = "{2:}위 매출 브랜드 판매 수익   : {0:} --> {1:,}원\n" .format (i[0], i[1], cnt)
            file1.write(orderN)
            file1.write(profitN)
            cnt += 1
    storeIndex += 1

    for mth in range(1,13)  :

        Z = np.array([x for x in short if int(x[0]) == mth])
        Z = np.transpose(Z)
        dictZ = dict(enumerate(Z))
        dictZ['month'] = dictZ.pop(0)
        dictZ['store'] = dictZ.pop(1)
        dictZ['brand'] = dictZ.pop(2)
        dictZ['price'] = dictZ.pop(3)

        brandSale = [0]*len(brandID)
        brandCnt = [0]*len(brandID)

        for i in range(len(dictZ['price']))    :

            if int(dictZ['month'][i]) == mth and dictStore[dictZ['store'][i]] == storeIndex   :
                brandSale[dictBrand[dictZ['brand'][i]]] += int(dictZ['price'][i])
                brandCnt[dictBrand[dictZ['brand'][i]]] += 1

                #print("분석 중 ...%7.3f%% 완료" % ((i+1)/len(dictZ['price'])*100))
                #print(brandID[i],brandSale[i],brandCnt[i])

            ## 식품 제외
            #brandSale[dictBrand['식품']] = 0
            #brandCnt[dictBrand['식품']] = 0

        brandSale2 = np.array(brandSale, dtype='int')
        brandCnt2 = np.array(brandCnt, dtype='int')
        brandID2 = np.array(brandID, dtype='object')

        #sortedIndex = np.argsort(brandSale2)
        sortedIndex = np.argsort(brandSale2)[::-1]
        newID = brandID2[sortedIndex]
        newSale = brandSale2[sortedIndex]
        newCnt = brandCnt2[sortedIndex]

        sortedIndex2 = np.argsort(brandCnt2)[::-1]
        newID2 = brandID2[sortedIndex2]
        newSale2 = brandSale2[sortedIndex2]
        newCnt2 = brandCnt2[sortedIndex2]

        finalVal = [(x,int(y),int(z)) for (x,y,z) in zip(newID, newSale, newCnt)]
        finalVal = finalVal[0:5]
        finalVal2 = [(x,int(y),int(z)) for (x,y,z) in zip(newID2, newSale2, newCnt2)]
        finalVal2 = finalVal2[0:5]


        titleStr = "\n\n--- %s %d월 최고 인기/수익 브랜드---\n" % (storeID[storeIndex], mth)

        file1.write(titleStr)
        cnt = 1
        for i in (finalVal2)  :
            orderN = "{2:}위 인기 브랜드 주문 건 수  : {0:} --> {1:,}건\n" .format (i[0], i[2], cnt)
            profitN = "{2:}위 인기 브랜드 판매 수익   : {0:} --> {1:,}원\n" .format (i[0], i[1], cnt)
            file1.write(orderN)
            file1.write(profitN)
            cnt += 1
        cnt = 1
        file1.write('\n')
        for i in (finalVal)  :
            orderN = "{2:}위 매출 브랜드 주문 건 수  : {0:} --> {1:,}건\n" .format (i[0], i[2], cnt)
            profitN = "{2:}위 매출 브랜드 판매 수익   : {0:} --> {1:,}원\n" .format (i[0], i[1], cnt)
            file1.write(orderN)
            file1.write(profitN)
            cnt += 1
    storeIndex += 1

    for mth in range(1,13)  :

        Z = np.array([x for x in short if int(x[0]) == mth])
        Z = np.transpose(Z)
        dictZ = dict(enumerate(Z))
        dictZ['month'] = dictZ.pop(0)
        dictZ['store'] = dictZ.pop(1)
        dictZ['brand'] = dictZ.pop(2)
        dictZ['price'] = dictZ.pop(3)

        brandSale = [0]*len(brandID)
        brandCnt = [0]*len(brandID)

        for i in range(len(dictZ['price']))    :

            if int(dictZ['month'][i]) == mth and dictStore[dictZ['store'][i]] == storeIndex   :
                brandSale[dictBrand[dictZ['brand'][i]]] += int(dictZ['price'][i])
                brandCnt[dictBrand[dictZ['brand'][i]]] += 1

                #print("분석 중 ...%7.3f%% 완료" % ((i+1)/len(dictZ['price'])*100))
                #print(brandID[i],brandSale[i],brandCnt[i])

            ## 식품 제외
            #brandSale[dictBrand['식품']] = 0
            #brandCnt[dictBrand['식품']] = 0

        brandSale2 = np.array(brandSale, dtype='int')
        brandCnt2 = np.array(brandCnt, dtype='int')
        brandID2 = np.array(brandID, dtype='object')

        #sortedIndex = np.argsort(brandSale2)
        sortedIndex = np.argsort(brandSale2)[::-1]
        newID = brandID2[sortedIndex]
        newSale = brandSale2[sortedIndex]
        newCnt = brandCnt2[sortedIndex]

        sortedIndex2 = np.argsort(brandCnt2)[::-1]
        newID2 = brandID2[sortedIndex2]
        newSale2 = brandSale2[sortedIndex2]
        newCnt2 = brandCnt2[sortedIndex2]

        finalVal = [(x,int(y),int(z)) for (x,y,z) in zip(newID, newSale, newCnt)]
        finalVal = finalVal[0:5]
        finalVal2 = [(x,int(y),int(z)) for (x,y,z) in zip(newID2, newSale2, newCnt2)]
        finalVal2 = finalVal2[0:5]


        titleStr = "\n\n--- %s %d월 최고 인기/수익 브랜드---\n" % (storeID[storeIndex], mth)

        file1.write(titleStr)
        cnt = 1
        for i in (finalVal2)  :
            orderN = "{2:}위 인기 브랜드 주문 건 수  : {0:} --> {1:,}건\n" .format (i[0], i[2], cnt)
            profitN = "{2:}위 인기 브랜드 판매 수익   : {0:} --> {1:,}원\n" .format (i[0], i[1], cnt)
            file1.write(orderN)
            file1.write(profitN)
            cnt += 1
        cnt = 1
        file1.write('\n')
        for i in (finalVal)  :
            orderN = "{2:}위 매출 브랜드 주문 건 수  : {0:} --> {1:,}건\n" .format (i[0], i[2], cnt)
            profitN = "{2:}위 매출 브랜드 판매 수익   : {0:} --> {1:,}원\n" .format (i[0], i[1], cnt)
            file1.write(orderN)
            file1.write(profitN)
            cnt += 1
    storeIndex += 1

    for mth in range(1,13)  :

        Z = np.array([x for x in short if int(x[0]) == mth])
        Z = np.transpose(Z)
        dictZ = dict(enumerate(Z))
        dictZ['month'] = dictZ.pop(0)
        dictZ['store'] = dictZ.pop(1)
        dictZ['brand'] = dictZ.pop(2)
        dictZ['price'] = dictZ.pop(3)

        brandSale = [0]*len(brandID)
        brandCnt = [0]*len(brandID)

        for i in range(len(dictZ['price']))    :

            if int(dictZ['month'][i]) == mth and dictStore[dictZ['store'][i]] == storeIndex   :
                brandSale[dictBrand[dictZ['brand'][i]]] += int(dictZ['price'][i])
                brandCnt[dictBrand[dictZ['brand'][i]]] += 1

                #print("분석 중 ...%7.3f%% 완료" % ((i+1)/len(dictZ['price'])*100))
                #print(brandID[i],brandSale[i],brandCnt[i])

            ## 식품 제외
            #brandSale[dictBrand['식품']] = 0
            #brandCnt[dictBrand['식품']] = 0

        brandSale2 = np.array(brandSale, dtype='int')
        brandCnt2 = np.array(brandCnt, dtype='int')
        brandID2 = np.array(brandID, dtype='object')

        #sortedIndex = np.argsort(brandSale2)
        sortedIndex = np.argsort(brandSale2)[::-1]
        newID = brandID2[sortedIndex]
        newSale = brandSale2[sortedIndex]
        newCnt = brandCnt2[sortedIndex]

        sortedIndex2 = np.argsort(brandCnt2)[::-1]
        newID2 = brandID2[sortedIndex2]
        newSale2 = brandSale2[sortedIndex2]
        newCnt2 = brandCnt2[sortedIndex2]

        finalVal = [(x,int(y),int(z)) for (x,y,z) in zip(newID, newSale, newCnt)]
        finalVal = finalVal[0:5]
        finalVal2 = [(x,int(y),int(z)) for (x,y,z) in zip(newID2, newSale2, newCnt2)]
        finalVal2 = finalVal2[0:5]


        titleStr = "\n\n--- %s %d월 최고 인기/수익 브랜드---\n" % (storeID[storeIndex], mth)

        file1.write(titleStr)
        cnt = 1
        for i in (finalVal2)  :
            orderN = "{2:}위 인기 브랜드 주문 건 수  : {0:} --> {1:,}건\n" .format (i[0], i[2], cnt)
            profitN = "{2:}위 인기 브랜드 판매 수익   : {0:} --> {1:,}원\n" .format (i[0], i[1], cnt)
            file1.write(orderN)
            file1.write(profitN)
            cnt += 1
        cnt = 1
        file1.write('\n')
        for i in (finalVal)  :
            orderN = "{2:}위 매출 브랜드 주문 건 수  : {0:} --> {1:,}건\n" .format (i[0], i[2], cnt)
            profitN = "{2:}위 매출 브랜드 판매 수익   : {0:} --> {1:,}원\n" .format (i[0], i[1], cnt)
            file1.write(orderN)
            file1.write(profitN)
            cnt += 1
    storeIndex += 1

print("--- %s seconds ---" % (time.time() - startTime))