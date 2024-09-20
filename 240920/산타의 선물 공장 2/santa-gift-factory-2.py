# n개의 벨트를 설치하고, 총 m개의 물건

#  벨트 리스트 [(맨앞놈, 맨뒷놈, 길이, 중간놈?)  ]
#  선물 리스트 [(앞놈: 없으면 -1, 뒷놈),()....]

from math import floor

q = int(input())

belt = []
present = []
n = 0
m = 0
length = 2
front = 0
back = 1
middle = 3

# 벨트, 선물 현황 그리기


def printAll():
    for index in range(1, len(belt)):
        i = belt[index]
        print("belt", index, "===========")
        print("first:", i[front])
        print("last:", i[back])
        print("middle:", i[middle])
        print("length:", i[length])
        node = i[front]
        while node != -1:
            print(node, end=" ")
            node = present[node][back]
        print("")
        node = i[back]
        while node != -1:
            print(node, end=" ")
            node = present[node][front]
        print("")

# 공장 설림


def buildFac(inputList):
    # 데이터 입력
    for newP in range(1, len(inputList)-2):
        nowBelt = inputList[newP+2]
        # 빈 벨트의 경우
        if belt[nowBelt][length] == 0:
            # 벨트 정보 갱신
            belt[nowBelt][front] = newP
            belt[nowBelt][back] = newP
            belt[nowBelt][middle] = newP
            belt[nowBelt][length] = 1

        # 벨트에 다른 것이 있는 경우
        else:
            beLast = belt[nowBelt][back]
            # 선물 정보 갱신
            present[beLast][back] = newP  # 전놈 뒤에 이번꺼
            present[newP][front] = beLast  # 이번꺼 앞에 전 마지막

            # 벨트 정보 갱신
            belt[nowBelt][back] = newP
            belt[nowBelt][length] = belt[nowBelt][length] + 1
            if belt[nowBelt][length] % 2 == 0 and  belt[nowBelt][length] > 2 :  # 총 개수가 짝수가 되었을 때 중간놈 변경
                belt[nowBelt][middle] = present[belt[nowBelt][middle]][back]


# 물건 모두 옮기기
def moveAll(src, dst):
    if belt[src][length] == 0:
        print(belt[dst][length])
        return

    # 박스들의 위치 바꾸기
    present[belt[dst][front]][front] = belt[src][back]  # dst의 맨 앞놈 앞
    present[belt[src][back]][back] = belt[dst][front]  # src의 맨 뒤놈 뒤

    # dst 벨트 정보 바꾸기
    lenBefore = belt[dst][length]
    lenAdd = belt[src][length]
    belt[dst][length] = lenBefore + lenAdd  # 개수 늘리기
    belt[dst][front] = belt[src][front]  # 맨 앞놈 지정
    # 중간놈 바꾸기
    if lenBefore == 1:
        toMove = 1 + lenAdd - floor(belt[dst][length]/2)
    else:
        toMove = floor(lenBefore/2) + lenAdd - floor(belt[dst][length]/2)
    newMid = belt[dst][middle]
    #길이가 0이면 마지막놈 바꾸기
    if belt[dst][length] == 1:
        belt[dst][back] = belt[dst][front]

    for i in range(toMove):
        newMid = present[newMid][front]

    belt[dst][middle] = newMid

    # src 벨트 정보 바꾸기
    belt[src] = [-1, -1, 0, -1]

    # print
    print(belt[dst][length])


# 앞 물건 옮기기
def changeFront(src, dst):
    srcFront = belt[src][front]
    dstFront = belt[dst][front]

    if srcFront == -1 and dstFront == -1:  # 둘다 빔
        print(belt[dst][length])
        return
    elif srcFront == -1:  # src만 빔
        # 안빈놈 벨트 정보 수정
        belt[dst][front] = present[dstFront][back]  # 두번째놈 맨앞으로
        present[belt[dst][front]][front] = -1
        belt[dst][length] = belt[dst][length] - 1  # 길이 감소
        if belt[dst][length] % 2 != 1:  # 중간놈 수정
            belt[dst][middle] = present[belt[dst][middle]][back]
        if belt[dst][length] == 0:  # 만약 다 비워지면 뒤도 삭제
            belt[dst][back] = -1

        # 이동한 선물 정보 수정
        present[dstFront][back] = -1

        # 원래 비엇던 벨트 정보 수정
        belt[src] = [dstFront, dstFront, 1, dstFront]

    elif dstFront == -1:  # dst만 빔
        # 안빈놈 벨트 정보 수정
        belt[src][front] = present[srcFront][back]  # 두번째놈 맨앞으로
        present[belt[src][front]][front] = -1
        belt[src][length] = belt[src][length] - 1  # 길이 감소
        if belt[src][length] % 2 != 1:  # 중간놈 수정
            belt[src][middle] = present[belt[src][middle]][back]
        if belt[src][length] == 0:  # 만약 다 비워지면 뒤도 삭제
            belt[src][back] = -1

        # 이동한 선물 정보 수정
        present[srcFront][back] = -1

        # 원래 비엇던 벨트 정보 수정
        belt[dst] = [srcFront, srcFront, 1, srcFront]

    else:  # 둘 다 있음
        # 맨 앞의 두놈의 뒤 교체
        temp = present[srcFront][back]
        present[srcFront][back] = present[dstFront][back]
        present[dstFront][back] = temp

        present[present[srcFront][back]][front] = srcFront
        present[present[dstFront][back]][front] = dstFront

        # 벨트 정보 수정
        belt[src][front] = dstFront
        belt[dst][front] = srcFront
        if belt[src][length] == 1:
            belt[src][back] = dstFront
            belt[src][middle] = dstFront
        elif belt[src][length] <= 3:
            belt[src][middle] = dstFront
        if belt[dst][length] == 1:
            belt[dst][back] = srcFront
            belt[dst][middle] = srcFront
        elif belt[dst][length] <= 3:
            belt[dst][middle] = srcFront

    print(belt[dst][length])


# 물건 나누기
def splitPresent(src, dst):
    srcLen = belt[src][length]
    if srcLen <= 1:  # 1 이하면 종료
        print(belt[dst][length])
        return

    halfSrcLen = floor(srcLen/2)
    srcFront = belt[src][front]
    srcMiddle = belt[src][middle]

    # middle 선물의 값 변경
    newSrcFront = present[srcMiddle][back]
    present[belt[dst][front]][front] = srcMiddle
    present[srcMiddle][back] = belt[dst][front]

    # 가는 벨트의 정보 변경
    beforeDstFront = belt[dst][front]
    belt[dst][front] = srcFront  # 앞 교체
    beforeLen = belt[dst][length]
    belt[dst][length] = belt[dst][length] + halfSrcLen  # 길이 수정

    if beforeLen == 0:  # 원래 아무것도 없으면
        belt[dst][back] = srcMiddle  # 맨뒤 교체
        # 중간 찾기
        toMove = floor(halfSrcLen/2)
        newMid = belt[dst][front]
        if toMove != 1:
            for i in range(toMove-1):
                newMid = present[newMid][back]
        belt[dst][middle] = newMid
    else:  # 원래 좀 있음
        present[beforeDstFront][front] = srcMiddle  # 기존 맨앞의 앞이 middle
        # 중간 찾기
        if beforeLen == 1:
            toMove = 1 + halfSrcLen - floor(belt[dst][length]/2)
        else:
            toMove = floor(beforeLen/2) + halfSrcLen - floor(belt[dst][length]/2)
        newMid = belt[dst][middle]

        for i in range(toMove):
            newMid = present[newMid][front]

        belt[dst][middle] = newMid


    # src 벨트 값 변경
    belt[src][length] = srcLen - halfSrcLen
    belt[src][front] = newSrcFront
    present[newSrcFront][front] = -1
    # 중간 찾기
    toMove = floor(belt[src][length]/2)
    newMid = belt[src][front]
    if toMove > 1:
        for i in range(toMove-1):
            newMid = present[newMid][back]
    belt[src][middle] = newMid

    print(belt[dst][length])

# 선물정보 얻기
def getPresent(pId):
    a = present[pId][front]
    b = present[pId][back]

    print(a+2*b)

# 선물정보 얻기
def getBelt(bId):
    a = belt[bId][front]
    b = belt[bId][back]
    c = belt[bId][length]

    print(a+ 2*b + 3*c)

######################## 작동부 ###################


for time in range(q):
    inputL = [int(i) for i in input().split()]

    if inputL[0] == 100:
        n = inputL[1]
        m = inputL[2]

        belt = [[-1, -1, 0, -1] for _ in range(n+1)]
        present = [[-1, -1] for _ in range(m+2)]

        buildFac(inputL)
        # printAll()

    elif inputL[0] == 200:
        moveAll(inputL[1], inputL[2])
        # printAll()

    elif inputL[0] == 300:
        changeFront(inputL[1], inputL[2])
        # printAll()

    elif inputL[0] == 400:
        splitPresent(inputL[1], inputL[2])
        # printAll()

    elif inputL[0] == 500:
        getPresent(inputL[1])
        # printAll()

    elif inputL[0] == 600:
        getBelt(inputL[1])
        # printAll()