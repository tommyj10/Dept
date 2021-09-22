##   전달드리는 사항엔 # 두 개를 써넣었습니다.
# 한 개 있는 건 참조용 코드로 #를 지우시고 출력하시면 데이터 분석 알고리즘을 만드는데
# 도움이 될 겁니다.

##   외부 라이브러리 numpy와 csv를 부릅니다.
import time
start_time = time.time()
import numpy as np
import csv

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

mthArray = [int(x.split('-')[1]) for x in data[result]]
custID = [int(x) for x in data[0]]

originalPrice = [int(x) for x in data[9]]
offPrice = [int(x) for x in data[10]]

priceList = np.subtract(originalPrice, offPrice)
uniqueCust = tuple(set(custID))

purchasedCost = [0]*len(uniqueCust)
purchasedCnt = [0]*len(uniqueCust)

for i in range(len(priceList))  :

    purchasedCost[custID[i]] += priceList[i]
    purchasedCnt[custID[i]] += 1

print("--- %s seconds ---" % (time.time() - start_time))

purchasedCost = tuple(purchasedCost)
purchasedCnt = tuple(purchasedCnt)


with open("고객별 총 구매 횟수와 액수.txt", 'w') as f:

    for i in range(len(uniqueCust)):

        row = '\n\n고객번호: {0:}\n구매 횟수: {1:}회\n총 비용: {2:,}원\n'.format(uniqueCust[i],purchasedCnt[i], purchasedCost[i])
        f.write(row)

print("--- %s seconds ---" % (time.time() - start_time))