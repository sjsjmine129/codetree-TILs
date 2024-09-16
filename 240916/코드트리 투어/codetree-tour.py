import heapq
INF=int(1e9)

# n = node (0 ~ n-1)
# m = edge (no direction, self, multiple)
graph = []
n = 0
m = 0
noEdge = 101
costs = []
tripQ = []
toDelete = []


#그래프 출력
def printGraph():
    for i in graph:
        print(i)


# 시작지로부터 최단거리 측정
def dijkstra(start):
    global costs
    costs = [INF]*n
    costs[start]=0

    q = []
    heapq.heappush(q,(0,start))

    while(q):
        dist, now = heapq.heappop(q)
        
        if costs[now] < dist:
            continue
        
        for i in graph[now]:
            newCost = dist + i[1]
            if newCost < costs[i[0]]:
                costs[i[0]] = newCost
                heapq.heappush(q,(newCost,i[0]))
    
    # print(costs)



# 코드랜드 건설
def buildCodeLand(inputL):
    global graph
    global n
    global m
    global costs

    n = inputL[1]
    m = inputL[2]
    costs = [-1]*n

    tempGraph =[[101]*n for _ in range(n)]

    index = 3
    for i in range((len(inputL)-3)//3):
        v = inputL[index]
        u = inputL[index+1]
        w = inputL[index + 2]

        if v != u and tempGraph[v][u] > w:
            tempGraph[v][u] = w
            tempGraph[u][v] = w

        index += 3
    
    # 간단한형태로 그래프 재정리
    graph = [[] for _ in range(n)]
    for v in range(n):
        for u in range(n):
            if tempGraph[v][u] != 101:
                graph[v].append([u,tempGraph[v][u]])

    # printGraph()


# 새 여행
def newTrip(id, revenue, dest):
    global tripQ
    if costs[dest] == INF:
        heapq.heappush(tripQ, (INF, id, dest, revenue))
    else:
        value = revenue - costs[dest]
        heapq.heappush(tripQ, (-value, id, dest, revenue))

# 여행 삭제
def deleteTrip(id):
    toDelete.append(id)


#최고의 상품 판매
def getBest():
    global tripQ
    if len(tripQ) == 0:
        print(-1)
        return

    best = heapq.heappop(tripQ)
    
    while best[1] in toDelete:
        toDelete.remove(best[1])
        if len(tripQ) == 0:
            print(-1)
            return
        best = heapq.heappop(tripQ)
        
    if best[0] <= 0:
        print(best[1])
    else:
        print(-1)
        heapq.heappush(tripQ,best)


# 시작점 재정렬
def changeStart(start):
    # 새로운 시작점 기준으로 다시 최단거리들 기록
    dijkstra(start)
    # print(costs)
    
    # 여행 상품 heap 다시 구성
    global tripQ
    newTripQ = []

    for i in tripQ:
        if costs[i[2]] == INF:
            heapq.heappush(newTripQ,(INF, i[1], i[2], i[3]))
        else:
            heapq.heappush(newTripQ,(-(i[3]-costs[i[2]]), i[1], i[2], i[3]))

    tripQ = newTripQ


# 여행 상품 생성

# 여행 상품 삭제 -> id로

# 맵을 유지하고
# 각 노드에서 다른 노드로의 최단 거리를 다익스트라로 재는 로직을 두고 각 도착지의 cost를 잰다
# 각


################## 작동 부 #####################
times = int(input())
for time in range(times):
    inputList = [int(x) for x in input().split()]
    # print(inputList)

    if inputList[0] == 100:
        buildCodeLand(inputList)
        dijkstra(0)
        # printGraph()
        # print(costs)

    elif inputList[0] == 200:
        newTrip(inputList[1],inputList[2],inputList[3])
        # print("200 ",tripQ)

    elif inputList[0] == 300:
        deleteTrip(inputList[1])
        # print("300 ",tripQ)

    elif inputList[0] == 400:
        getBest()

    elif inputList[0] == 500:
        # print(tripQ)
        changeStart(inputList[1])
        # print(tripQ)

    # print(costs)