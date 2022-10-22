import sys
import math

limit_number = 15000
sys.setrecursionlimit(limit_number)

# Data Science Assignment3
# 2017029589 Ryu Jibeom
Eps = None
MinPts = None
n = None
DataSet = list()
isProcessed = None
isCore = None
DDRlist = list()
CoreList = list()
Cluster = list()
ClusterList = list()


def check_core(idx):
    global isCore, CoreList
    ddr = list()
    cnt = 0
    x = DataSet[idx][1]
    y = DataSet[idx][2]

    for data in DataSet:
        dist = math.sqrt((x - data[1]) * (x - data[1]) + (y - data[2]) * (y - data[2]))
        if dist <= Eps:
            cnt += 1
            ddr.append(data[0])

    if cnt >= MinPts:
        isCore[idx] = True
        CoreList.append(idx)
        return ddr
    else:
        return list()


def init_core():
    global DDRlist
    for i in range(len(DataSet)):
        DDRlist.append(check_core(i))

def retrieve_density_reachable(p):
    global isProcessed, Cluster
    if isCore[p]:
        if not isProcessed[p]:
            isProcessed[p] = True
            Cluster.append(p)
            for ddr in DDRlist[p]:
                if not isProcessed[ddr]:
                    Cluster.append(ddr)
                    retrieve_density_reachable(ddr)
    else:
        return

def DBscan():
    global Cluster, ClusterList

    for p in CoreList:
        Cluster = list()
        retrieve_density_reachable(p)
        if (len(Cluster)) > 0:
            ClusterList.append(Cluster)


def sort_cluster():
    idxArray = list()
    for i in range(len(ClusterList)):
        idxArray.append((len(ClusterList[i]), i))

    idxArray.sort(key=lambda x: -x[0])

    return idxArray


def read_input(name):
    global DataSet, isProcessed, isCore
    with open(name, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            temp = line.split()
            data = [int(temp[0]), float(temp[1]), float(temp[2])]
            DataSet.append(data)
    isProcessed = [False] * len(DataSet)
    isCore = [False] * len(DataSet)


def write_output(input_num):
    fileName = "input" + input_num + "_cluster_"
    outArr = sort_cluster()

    for i in range(n):
        out = open(fileName + str(i) + ".txt", "w")
        idx = outArr[i][1]
        for data in ClusterList[idx]:
            line = str(data) + '\n'
            out.write(line)
        out.close()


if __name__ == '__main__':
    input = sys.argv[1]
    n = int(sys.argv[2])
    Eps = int(sys.argv[3])
    MinPts = int(sys.argv[4])

    input_num = input[5]


    read_input(input)
    init_core()
    DBscan()
    write_output(input_num)