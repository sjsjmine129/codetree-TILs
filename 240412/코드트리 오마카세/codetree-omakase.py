import heapq
#회전 -> 놓기 -> 앉기 -> 먹기 -> 사진(사람 수, 초밥수)
[l, q] = map(int, input().split())

# belt = [{} for _ in range(l)]
# seat = [['']]*l

sushiNum = []
customerNum = []

sushi = {}
customer = {}

photo = []

###functions
def printAll():
    print("[customer]")
    for i in customer:
        print(i, customer[i])
    print("[suchi]")
    for i in sushi:
        print(i, sushi[i])
    print(photo)


# 특정 시간에 벨트의 위치
def findBeltInTime(belt, t):
    return (belt + t)%l

def findXInTime(x,t):
    belt0 = t%l
    if x >= belt0:
        return x -belt0
    else:
        return x + l - belt0 


def makeSushi(name, x, t):
    if name in sushi:
        sushi[name].append([t, findXInTime(x, t)])
    else:
        sushi[name] =[[t, findXInTime(x, t)]]

def customerCome(name, x, n, t):
    customer[name] = [t, x, n]


# main logic
for i in range(q):
    order = input().split()

    #초밥 만들기 기록
    if order[0] == '100':
        makeSushi(order[3], int(order[2]), int(order[1]))
    #손님 입장
    elif order[0] == '200':
        customerCome(order[3], int(order[2]), int(order[4]), int(order[1]))
    #사진 촬영
    elif order[0] == '300':
        photo.append(int(order[1]))

# printAll()


### 손님 들어오고 나가는것 and 초밥 올리고 먹는것 계산
for name in sushi:
    SList = sushi[name]
    appear = customer[name][0]
    x = customer[name][1]
    n = customer[name][2]
    heapq.heappush(customerNum, (appear, 1))

    lastEat = 0
    for i in SList: # [ 오는 시간, 벨트 위치 ]
        heapq.heappush(sushiNum,(i[0], 1))

        arrive = i[0]
        position = i[1]
        start = max(appear, arrive)
        
        offset = findBeltInTime(position, start)
        eatTime = start
        if offset <= x:
            eatTime = eatTime + x - offset
        else:
            eatTime += (l - offset + x)

        heapq.heappush(sushiNum,(eatTime, -1))
        if lastEat < eatTime:
            lastEat = eatTime
    
    heapq.heappush(customerNum, (lastEat, -1))

# printAll()
# print("customer",customerNum)
# print("sushi", sushiNum)   


sushiEvent = [0,0]
customerEvent = [0,0]
sNum = 0
cNum = 0
for i in photo:
    while sushiEvent[0] <= i :
        sNum += sushiEvent[1]
        sushiEvent = [0,0]
        if len(sushiNum)==0:
            break
        sushiEvent = heapq.heappop(sushiNum)
    while customerEvent[0] <= i :
        cNum += customerEvent[1]
        customerEvent = [0,0]
        if len(customerNum) == 0:
            break
        customerEvent = heapq.heappop(customerNum)  

    print(cNum, sNum) 
    







########## past code -> out of time

# #회전 -> 놓기 -> 앉기 -> 먹기 -> 사진(사람 수, 초밥수)
# [l, q] = map(int, input().split())

# belt = [{} for _ in range(l)]
# seat = [['']]*l

# sushiNum = 0
# customerNum = 0
# time = 0

# ###functions
# # 벨트 위치 찾기
# def findBelt(x):
#     offset = time % l
#     return x-offset

# # 초밥 놓기
# def makeSushi(name, x):
#     global sushiNum 
#     index = findBelt(x)

#     if name in belt[index]:
#         belt[index][name] = belt[index][name] + 1
#     else:
#         belt[index][name] = 1
#     sushiNum += 1

# # 손님 들어옴
# def customerCome(name, x, n):
#     global customerNum 

#     seat[x] = [name, n]
#     customerNum += 1

# #초밥 먹기
# def eatSushi():
#     global customerNum 
#     global sushiNum 

#     for i in range(l):
#         person = seat[i]
#         if person[0] == '': #아무도 없음
#             continue
        
#         index = findBelt(i)

#         if person[0] in belt[index]: # 초밥 있음
#             afterEat = person[1] - belt[index][person[0]]

#             #벨트에서 초밥 삭제
#             sushiNum -= belt[index][person[0]]
#             del belt[index][person[0]]

#             if afterEat == 0: #배부르면 나감
#                 seat[i] = ['']
#                 customerNum -= 1
#             else: #아직이면 그대로
#                 seat[i][1] = afterEat


# # main logic
# for i in range(q):
#     order = input().split()

#     #move belt
#     nextTime =int(order[1])
#     while time < nextTime:
#         time += 1
#         eatSushi()

#     #초밥 만들기
#     if order[0] == '100':
#         makeSushi(order[3], int(order[2]))

#     #손님 입장
#     if order[0] == '200':
#         customerCome(order[3], int(order[2]), int(order[4]))

#     # 초밥 먹기
#     eatSushi()

#     #사진 촬영
#     if order[0] == '300':
#         print(customerNum, sushiNum)