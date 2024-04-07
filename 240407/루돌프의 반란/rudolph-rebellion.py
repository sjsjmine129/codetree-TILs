[n,m,p,c,d] = map(int, input().split())
[ry, rx] = map(int, input().split())

def calDistense(y1,x1,y2,x2):
    return (y1-y2)**2+(x1-x2)**2

santa = [[] for _ in range(p+1)]
score = [0]*(p+1)

board=[]
board.append([-1]*(n+2))
for i in range(n):
    temp = [0]*n
    temp.insert(0,-1)
    temp.append(-1)
    board.append(temp)
board.append([-1]*(n+2))

for i in range(p):
    [index, sy, sx] = map(int, input().split())
    santa[index] = [sy, sx, 0, index]
    board[sy][sx]=index

y=0
x=1
state=2
index=3

# print(santa)
# for i in board:
#     print(i)

for turn in range(m):
    #rudolf
    closeSanta = 0
    minDistance = -1
    for i in range(1,p+1):
        s = santa[i]
        if s[state] == -1: # 밖이면 스킵
            continue
        
        distense = calDistense(ry,rx,s[y],s[x])
        if minDistance == -1 or minDistance > distense: # 이번게 더 가까움
            closeSanta = i
            minDistance = distense
        elif minDistance == distense: # 거리 동일
            beforeS = santa[closeSanta]
            if beforeS[y] < s[y]: # y좌표 더 큰거
                closeSanta = i
                minDistance = distense
            elif beforeS[y] == s[y] and beforeS[x] < s[x]: #y 동일시 x큰놈
                closeSanta = i
                minDistance = distense
    
    # 루돌프 이동 방향
    s = santa[closeSanta]
    dy = 0
    dx = 0

    if ry > s[y]:
        dy = -1
    elif ry < s[y]:
        dy = +1
    if rx > s[x]:
        dx = -1
    elif rx < s[x]:
        dx = +1

    ry += dy
    rx += dx

    if board[ry][rx] >0: # 충돌시
        s = santa[board[ry][rx]]
        board[ry][rx] = 0 # 그 자리 0
        score[s[index]]+=c # 점수 추가

        nextSanta = [s[y]+dy*c, s[x]+dx*c, 2, s[index]]

        while len(nextSanta)>0:
            if nextSanta[y] <= 0 or nextSanta[y] > n or nextSanta[x] <= 0 or nextSanta[x] > n : #out
                nextSanta[state] = -1 # 산타 리스트에 저장
                santa[nextSanta[index]] = [nextSanta[y], nextSanta[x], nextSanta[state], nextSanta[index]] # 산타에 저장
                nextSanta = []
            else: #in board
                if board[nextSanta[y]][nextSanta[x]] >0: # 그 자리에 누구 있음
                    nextIndex = board[nextSanta[y]][nextSanta[x]] # 튕겨져 나갈 놈
                    board[nextSanta[y]][nextSanta[x]] = nextSanta[index] #그 자리에 놓음
                    santa[nextSanta[index]] = [nextSanta[y], nextSanta[x], nextSanta[state], nextSanta[index]] # 산타에 저장
                    nextSanta = [santa[nextIndex][y]+dy, santa[nextIndex][x]+dx, santa[nextIndex][state], nextIndex]
                else: # 아무도 없음
                    board[nextSanta[y]][nextSanta[x]] = nextSanta[index] #그 자리에 놓음
                    santa[nextSanta[index]] = [nextSanta[y], nextSanta[x], nextSanta[state], nextSanta[index]] # 산타에 저장
                    nextSanta = []

    # print(turn,"== Ru ====")
    # for i in board:
    #     print(i)
    # print("santa:",santa)
    # print(ry,rx)
    # print("score: ",score)

    dList = [[-1,0], [0,1], [1,0], [0,-1]]

    #Santa turn
    for i in range(1,p+1):
        s = santa[i]
        if s[state] != 0: # check fade or out
            if s[state] >= 1:
                santa[s[index]][state] -= 1
            continue
        
        closeDirc = []
        minDistance = calDistense(ry,rx,s[y],s[x])
        for dirc in dList:
            nexty = s[y]+dirc[y]
            nextx = s[x]+dirc[x]
            if board[nexty][nextx] == 0: #움직이기 가능
                nextDistance = calDistense(ry,rx,nexty,nextx)
                if nextDistance < minDistance:
                    minDistance = nextDistance
                    closeDirc = [dirc[y],dirc[x]]
        
        if len(closeDirc)==0: #nowhere to go
            continue

        #move
        board[s[y]][s[x]] = 0  # remove santa
        nextSanta = [s[y]+closeDirc[y], s[x]+closeDirc[x], s[state], s[index]]
        if nextSanta[y]==ry and nextSanta[x]==rx:#루돌프 충돌
            score[nextSanta[index]] += d # 점수 추가
            nextSanta = [nextSanta[y]-closeDirc[y]*d, nextSanta[x]-closeDirc[x]*d, 2, nextSanta[index]] # 튕기는 위치

            while len(nextSanta)>0:
                if nextSanta[y] <= 0 or nextSanta[y] > n or nextSanta[x] <= 0 or nextSanta[x] > n : #out
                    nextSanta[state] = -1 
                    santa[nextSanta[index]] = [nextSanta[y], nextSanta[x], nextSanta[state], nextSanta[index]] # 산타에 저장
                    nextSanta = []
                else: #in board
                    if board[nextSanta[y]][nextSanta[x]] >0: # 그 자리에 누구 있음
                        nextIndex = board[nextSanta[y]][nextSanta[x]] # 튕겨져 나갈 놈
                        board[nextSanta[y]][nextSanta[x]] = nextSanta[index] #그 자리에 놓음
                        santa[nextSanta[index]] = [nextSanta[y], nextSanta[x], nextSanta[state], nextSanta[index]] # 산타에 저장
                        nextSanta = [santa[nextIndex][y]-closeDirc[y], santa[nextIndex][x]-closeDirc[x], santa[nextIndex][state], nextIndex]
                    else: # 아무도 없음
                        board[nextSanta[y]][nextSanta[x]] = nextSanta[index] #그 자리에 놓음
                        santa[nextSanta[index]] = [nextSanta[y], nextSanta[x], nextSanta[state], nextSanta[index]] # 산타에 저장
                        nextSanta = []

        else:# 바로 옮김
            board[nextSanta[y]][nextSanta[x]] = nextSanta[index] #그 자리에 놓음
            santa[nextSanta[index]] = [nextSanta[y], nextSanta[x], nextSanta[state], nextSanta[index]] # 산타에 저장 

    #end turn
    for i in range(1,p+1):
        s = santa[i]
        if s[state] != -1:
            score[i] +=1
    
    # if turn+1>=3:
    #     print(turn+1,"== santa ====")
    #     for i in board:
    #         print(i)
    #     print("santa:",santa[1])
    #     print(ry,rx)
    #     print("score: ",score)
    
for i in range(1,p+1):
    print(score[i],end=' ')