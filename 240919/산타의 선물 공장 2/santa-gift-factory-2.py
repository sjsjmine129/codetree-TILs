#n개의 벨트를 설치하고, 총 m개의 물건

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

#벨트, 선물 현황 그리기
def printAll():
    for index in range(1,len(belt)):
        i = belt[index]
        print("belt",index,"===========")
        print("first:",i[front])
        print("last:",i[back])
        print("middle:",i[middle])
        print("length:",i[length])
        node = i[front]
        while node != -1:
            print(node,end=" ")
            node = present[node][back]
        print("\n")

# 공장 설림
def buildFac(inputList):
    # 데이터 입력
    for newP in range(1,len(inputList)-2):
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
            #선물 정보 갱신
            present[beLast][back] = newP # 전놈 뒤에 이번꺼
            present[newP][front] = beLast # 이번꺼 앞에 전 마지막

            #벨트 정보 갱신
            belt[nowBelt][back] = newP
            belt[nowBelt][length] = belt[nowBelt][length] + 1
            if belt[nowBelt][length]%2 == 1: #총 개수가 홀수가 되었을 때 중간놈 변경
                belt[nowBelt][middle] = present[belt[nowBelt][middle]][back]




for time in range(q):
    inputL = [ int(i) for i in input().split() ]

    if inputL[0] == 100:
        n = inputL[1]
        m = inputL[2]

        belt = [[-1, -1, 0, -1] for _ in range(n+1) ]
        present = [[-1, -1] for _ in range(m+1) ]

        buildFac(inputL)
        # printAll()
    
    elif inputL[0] == 200: