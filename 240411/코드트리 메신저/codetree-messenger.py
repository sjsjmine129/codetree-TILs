from dataclasses import dataclass 

[n,q] = map(int,input().split())
first = list(map(int,input().split()))

@dataclass
class Node:
    parent: int = -1
    child1: int = -1
    child2: int = -1
    block: bool = False
    power: int = -1
    me: int = 0
    getNoti: int = 0

#get child list
def getChildList(node):
    ret = []
    if node.child1 != -1:
        ret.append(node.child1)
    if node.child2 != -1:
        ret.append(node.child2)
    return ret

#init
def initChild(node, ch):
    if node.child1 == -1:
        node.child1 = ch
    else:
        node.child2 = ch

#add Child
def addChild(node, cnode):
    ch = cnode.me
    if node.child1 == -1:
        node.child1 = ch
    else:
        node.child2 = ch

#delete Child
def delChild(node, cnode):
    ch = cnode.me
    if node.child1 == ch:
        node.child1 = -1
    else:
        node.child2 = -1


tree = [Node() for _ in range(n+1)]


#init
for i in range(1,n+1):
    tree[i].power = first[i+n]
    tree[i].parent = first[i]
    temp = tree[first[i]]
    if temp.child1 == -1:
        temp.child1 = i
    else:
        temp.child2 = i
    tree[i].me = i


##### functions
#print tree
def printTree():
    for i in tree:
        print(i.parent, getChildList(i), i.getNoti, i.block, i.power, i.me)

#어떤 노드의 아래부분이 영향을 끼치는 높이 확인
def checkImpact(node):
    impact = node.power

    clist = getChildList(node)
    for i in clist:
        cNode = tree[i]
        cImpact = checkImpact(cNode)
        if cImpact - 1 > impact:
            impact = cImpact - 1
    
    return impact

#알림 받을 수 있는 채팅방 수 기록
def checkNotiNum(node, distence):
    clist = getChildList(node)
    
    ret = 0
    for i in clist:
        chileNode = tree[i]
        if chileNode.block: #알림 막힌상태면 그만
            continue
        if chileNode.power >= distence:
            ret +=1
        ret += checkNotiNum(chileNode, distence+1)
    
    if distence == 1:
        node.getNoti = ret
    return ret

# 바뀐 위쪽에 영향만큼 다시 기록
def resetNotiNum(level, node):
    if level == 0 :
        return 

    checkNotiNum(node, 1)
    if node.parent != -1:
        resetNotiNum(level-1, tree[node.parent])

# 알림 바꾸기
def changeBlock(index):
    node = tree[index]
    node.block = not node.block

    upperLevel = checkImpact(node)
    resetNotiNum(upperLevel, tree[node.parent])

# 파워 바꾸기
def changePower(index, newPower):
    node = tree[index]
    impactBefore = checkImpact(node)
    node.power = newPower
    impactAfter = checkImpact(node)

    temp = max(impactBefore, impactAfter)
    resetNotiNum(temp, tree[node.parent])

#부모 교환
def changeParent(index1, index2):
    node1 = tree[index1]
    node2 = tree[index2]
    pnode1 = tree[node1.parent]
    pnode2 = tree[node2.parent]
    #부모의 자식 바꾸기
    delChild(pnode1, node1)
    delChild(pnode2, node2)
    addChild(pnode1, node2)
    addChild(pnode2, node1)
    #자식의 부모 바꾸기
    node1.parent = pnode2.me
    node2.parent = pnode1.me
    #부모들 알림 다시 기록
    upperLevel1 = checkImpact(node1)
    resetNotiNum(upperLevel1, tree[node1.parent])
    upperLevel2 = checkImpact(node2)
    resetNotiNum(upperLevel2, tree[node2.parent])




### main logic
#init notiNum
for i in tree:
    checkNotiNum(i,1)

#test codes
# changePower(8,3)
# printTree()
# changeParent(4,5)
# printTree()

num=0
for turn in range(q-1):
    order = list(map(int,input().split()))

    if order[0] == 200:
        changeBlock(order[1])
    elif order[0] == 300:
        changePower(order[1],order[2])
    elif order[0] == 400:
        changeParent(order[1],order[2])
    elif order[0] == 500:
        print(tree[order[1]].getNoti)