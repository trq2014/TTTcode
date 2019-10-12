import random
filename = 'iris.txt' # txt文件和当前脚本在同一目录下，所以不用写具体路径
# 一个特征项类，包括特征值，类别和预测类别和最近点记录集合
class Item(object):
    def __init__(self, x, y, z, w, category):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.category = category
        self.predictCategory = -1;
        self.nearList = []
    def insertNearItem(self, index, distance):
        if(len(self.nearList) == 0):
            self.nearList.append(NearestItem(index, distance))
        else:
            isInsert = False
            for listIndex in range(0, len(self.nearList)):
                if(self.nearList[listIndex].distance > distance):
                    self.nearList.insert(listIndex, NearestItem(index, distance))
                    isInsert = True
                    break
            if not isInsert:
                self.nearList.append(NearestItem(index, distance))
#一个最近点类，包括所在list编号和最近距离
class NearestItem(object):
    def __init__(self, index, distance):
        self.index = index
        self.distance = distance

#特征向量集合（0-89 训练集，90-119 验证集合，120-149 测试集合）
Efield = []
with open(filename, 'r') as file_to_read:
  while True:
    lines = file_to_read.readline() # 整行读取数据
    if not lines or len(lines.strip()) == 0:
        break
    else:
        lines = lines.replace('\n', '')
        E_tmp = [float(i) for i in lines.split(',')]
        ItemExample = Item(E_tmp[0], E_tmp[1], E_tmp[2], E_tmp[3], E_tmp[4])
        print(ItemExample.w)
        Efield.append(ItemExample)

print(len(Efield))
random.shuffle(Efield)
Efield[0].insertNearItem(1, 12.26)
Efield[0].insertNearItem(1, 12.36)
Efield[0].insertNearItem(1, 12.16)
#按训练集将按距离远近将index存入各个验证和测试集中
def getNearest():
    for index in range(90, 150):
        for trainIndex in range(0, 90):
            distance = ((Efield[index].w - Efield[trainIndex].w) ** 2
                        + (Efield[index].x - Efield[trainIndex].x) ** 2
                        + (Efield[index].y - Efield[trainIndex].y) ** 2
                        + (Efield[index].z - Efield[trainIndex].z) ** 2) ** 0.5
            Efield[index].insertNearItem(trainIndex, distance)
getNearest()
#验证超参数
bestK = -1;
bestKSuccess = 0;
KRANGE = 50
for i in range(2, 31):
    rightNum = 0
    for index in range(90, 90 + KRANGE):
        categoryEnum = [0, 0, 0]
        for nearIndex in range(0, i):
            categoryEnum[int(Efield[(Efield[index].nearList[nearIndex]).index].category - 1)] += 1
        if categoryEnum[0] >= categoryEnum[1] and categoryEnum[0] >= categoryEnum[2]:
            Efield[index].predictCategory = 1
        elif categoryEnum[1] >= categoryEnum[0] and categoryEnum[1] >= categoryEnum[2]:
            Efield[index].predictCategory = 2
        elif categoryEnum[2] >= categoryEnum[0] and categoryEnum[2] >= categoryEnum[1]:
            Efield[index].predictCategory = 3
        if Efield[index].predictCategory == Efield[index].category:
            rightNum += 1
    print('k = %d, 正确率为%.2f'%(i, 100 * rightNum / KRANGE))
    if rightNum / KRANGE > bestKSuccess:
        bestK = i
        bestKSuccess = rightNum / KRANGE
print('最佳K值为%d, 正确率为%.2f'%(bestK, bestKSuccess * 100))
rightNum = 0
for index in range(140, 150):
    categoryEnum = [0, 0, 0]
    for nearIndex in range(0, bestK):
        categoryEnum[int(Efield[(Efield[index].nearList[nearIndex]).index].category - 1)] += 1
    if categoryEnum[0] >= categoryEnum[1] and categoryEnum[0] >= categoryEnum[2]:
        Efield[index].predictCategory = 1
    elif categoryEnum[1] >= categoryEnum[0] and categoryEnum[1] >= categoryEnum[2]:
        Efield[index].predictCategory = 2
    elif categoryEnum[2] >= categoryEnum[0] and categoryEnum[2] >= categoryEnum[1]:
        Efield[index].predictCategory = 3
    if Efield[index].predictCategory == Efield[index].category:
        rightNum += 1
print('测试正确率为%.2f'%(100 * rightNum / 10))