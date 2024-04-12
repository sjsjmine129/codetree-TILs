#회전 -> 놓기 -> 앉기 -> 먹기 -> 사진(사람 수, 초밥수)
[l, q] = map(int, input().split())

belt = [{} for _ in range(l)]
seat = [['']]*l

sushiNum = 0
customerNum = 0
time = 0

###functions
# 벨트 위치 찾기
def findBelt(x):
    offset = time % l
    return x-offset

# 초밥 놓기
def makeSushi(name, x):
    global sushiNum 
    index = findBelt(x)

    if name in belt[index]:
        belt[index][name] = belt[index][name] + 1
    else:
        belt[index][name] = 1
    sushiNum += 1

# 손님 들어옴
def customerCome(name, x, n):
    global customerNum 

    seat[x] = [name, n]
    customerNum += 1

#초밥 먹기
def eatSushi():
    global customerNum 
    global sushiNum 

    for i in range(l):
        person = seat[i]
        if person[0] == '': #아무도 없음
            continue
        
        index = findBelt(i)

        if person[0] in belt[index]: # 초밥 있음
            afterEat = person[1] - belt[index][person[0]]

            #벨트에서 초밥 삭제
            sushiNum -= belt[index][person[0]]
            del belt[index][person[0]]

            if afterEat == 0: #배부르면 나감
                seat[i] = ['']
                customerNum -= 1
            else: #아직이면 그대로
                seat[i][1] = afterEat



# main logic
for i in range(q):
    order = input().split()

    #move belt
    nextTime =int(order[1])
    while time < nextTime:
        time += 1
        eatSushi()

    #초밥 만들기
    if order[0] == '100':
        makeSushi(order[3], int(order[2]))

    #손님 입장
    if order[0] == '200':
        customerCome(order[3], int(order[2]), int(order[4]))

    # 초밥 먹기
    eatSushi()

    #사진 촬영
    if order[0] == '300':
        print(customerNum, sushiNum)