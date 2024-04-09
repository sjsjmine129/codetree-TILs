#### Setting data
[l,n,q] = map(int, input().split())
r = 0
c = 1
h = 2
w = 3
k = 4
knightNum = 5
#make board
board = []
board.append([2]*(l+2))
for i in range(l):
    temp = []
    temp = list(map(int, input().split()))
    temp.insert(0,2)
    temp.append(2)
    board.append(temp)
board.append([2]*(l+2))

knightPosition = []
knightPosition.append([0]*(l+2))
for i in range(l):
    temp = []
    temp = [0]*l
    temp.insert(0,0)
    temp.append(0)
    knightPosition.append(temp)
knightPosition.append([0]*(l+2))

# record knight
knight = [[]]
firstKnightLife = [0]
for i in range(n):
    temp = list(map(int, input().split()))
    temp.append(i+1)
    firstKnightLife.append(temp[k])
    for dy in range(temp[h]):
        for dx in range(temp[w]):
            knightPosition[temp[r]+dy][temp[c]+dx] = i+1
    knight.append(temp)
    


##### functions
def printBoard():
    print("board")
    for i in board:
        print(i)

def printKnight():
    print("== knightPosition ==")
    for i in knightPosition:
        print(i)
    print("== knight Data ==")
    for i in range(1,n+1):
        print(knight[i])

# 기사 보드의 정보 변경
def changeKinghtBoardData(knightData, data):
    for dy in range(knightData[h]):
        for dx in range(knightData[w]):
            knightPosition[knightData[r]+dy][knightData[c]+dx] = data

#주어진 기사의 현재 위치에 대한 데미지 값 계산
def calDamage(knightData):
    ret = 0
    for dy in range(knightData[h]):
        for dx in range(knightData[w]):
            temp = board[knightData[r]+dy][knightData[c]+dx]
            if temp == 1:
                ret += 1
    return ret

# 기사 이동시키는 함수
# 죽으면 빼버림 -> 쓰기전에 첫놈은 데미지만큼 회복 미리 시켜야함
def changeKinghtPosition(knightList, dirction):
    for i in knightList:
        knightData = knight[i]
        dx = 0
        dy = 0
        if dirction == 0:
            dy = -1
        elif dirction == 1:
            dx = 1
        elif dirction == 2:
            dy = 1
        elif dirction == 3:
            dx = -1

        # 기사 보드에 기존 위치에서 지움
        changeKinghtBoardData(knightData, 0)

        # 이동한 위치로 기사 정보 바꿈
        knightData[r] = knightData[r] + dy
        knightData[c] = knightData[c] + dx

    for i in knightList: 
        knightData = knight[i]   
        #데미지 계산
        damage = calDamage(knightData)
        knightData[k] = knightData[k] - damage
        # 기사 보드에 새 위치 기록
        if knightData[k] > 0 :
            changeKinghtBoardData(knightData, knightData[knightNum])


# 움직일 수 있는지 체크
#만약 움직인다면 가는 칸에 벽이 있으면 못 움직임
# 반환 길이가 0이면 그냥 out
#움직여야하는 기사들 번호 리턴
def checkCanMove(knightData, dirction):
    dx = 0
    dy = 0
    if dirction == 0:
        dy = -1
    elif dirction == 1:
        dx = 1
    elif dirction == 2:
        dy = 1
    elif dirction == 3:
        dx = -1

    # 이동을 한다면 되는 기사의 상태 정보
    tempKinght = knightData.copy()
    tempKinght[r] += dy
    tempKinght[c] += dx

    #벽이 있는지 체크 & 그곳에 기사가 있는지 체크
    nextKnight = set()
    for i in range(tempKinght[h]):
        for j in range(tempKinght[w]):
            #벽이 있는지 체크 있으면 리턴
            temp = board[tempKinght[r]+i][tempKinght[c]+j]
            if temp == 2:
                ret = set()
                return ret # do not move
            #기사가 있는지 체크
            temp = knightPosition[tempKinght[r]+i][tempKinght[c]+j]
            if temp != 0 and temp != tempKinght[knightNum] and temp not in nextKnight:
                nextKnight.add(temp)
    
    for i in nextKnight:
        temp = checkCanMove(knight[i], dirction)
        if len(temp) == 0:
            ret = set()
            return ret
        else:
            nextKnight.union(temp)

    nextKnight.add(knightData[knightNum])
    #움직여야 하는 기사들 number
    return nextKnight

#첫놈 미리 회복 시키는 함수
def healFirstKinght(knightData, dirction):
    dx = 0
    dy = 0
    if dirction == 0:
        dy = -1
    elif dirction == 1:
        dx = 1
    elif dirction == 2:
        dy = 1
    elif dirction == 3:
        dx = -1
    
    # 이동을 한다면 되는 기사의 상태 정보
    tempKinght = knightData.copy()
    tempKinght[r] += dy
    tempKinght[c] += dx
    
    # 받을 데미지 만큼 미리 회복 시키기
    knightData[k] += calDamage(tempKinght)


#test Settings
# printBoard()
# printKnight()

# changeKinghtPosition([1,2,3],1)

# printKnight()


#do game -> main logic
for turn in range(q):
    print("====",turn)
    for i in knight:
        print(i)
    [i, d] = map(int, input().split())
    #기사 죽었는지 체크 -> 죽으면 스킵
    if knight[i][k] <= 0:
        continue
    
    # 움직일 수 있는지 체크
    moveSet = checkCanMove(knight[i],d)
    
    # 못 움직이면 다음
    if len(moveSet) == 0:
        continue
    
    #첫놈 미리 회복 시키기
    healFirstKinght(knight[i],d)
    # 이동시키기
    changeKinghtPosition(moveSet, d)


for i in knight:
    print(i)


ret = 0
for i in range(1,n+1):
    knightData = knight[i]
    if knightData[k] > 0:
        ret += firstKnightLife[i]-knightData[k]

print(ret)
printKnight()