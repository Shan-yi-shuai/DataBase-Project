import math
import numpy

def point(x, y):
    return '[' + str(x) + ',' + str(y) + ']'

class CalculateSequeceSimilarity(object):
    def __init__(self, A, B, W = 1, M = 1, N = -1/3):
        self.A = A
        self.B = B
        self.W = W
        self.M = M
        self.N = N
        self.similarity = []
        self.SimthWaterman(self.A, self.B, self.W)
 
    def score(self,a, b):
        if a == b:
            return self.M
        else:
            return self.N
 
    def traceback(self,A, B, H, path, value, result):
        if value:
            temp = value[0]
            result.append(temp)
            value = path[temp]
            x = int((temp.split(',')[0]).strip('['))
            y = int((temp.split(',')[1]).strip(']'))
        else:
            return
        if H[x, y] == 0:  # 终止条件
            xx = 0
            yy = 0
            sim = 0
            for item in range(len(result) - 2, -1, -1):
                position = result[item]
                x = int((position.split(',')[0]).strip('['))
                y = int((position.split(',')[1]).strip(']'))
                if x == xx:
                    pass
                elif y == yy:
                    pass
                else:
                    sim = sim + 1
                xx = x
                yy = y
            self.similarity.append(sim * 2 / (len(A) + len(B)))
 
        else:
            self.traceback(A, B, H, path, value, result)
 
    def SimthWaterman(self, A, B, W):
        n, m = len(A), len(B)
        H = numpy.zeros([n + 1, m + 1], int)
        path = {}
        for i in range(0, n + 1):
            for j in range(0, m + 1):
                if i == 0 or j == 0:
                    path[point(i, j)] = []
                else:
                    s = self.score(A[i - 1], B[j - 1])
                    L = H[i - 1, j - 1] + s
                    P = H[i - 1, j] - W
                    Q = H[i, j - 1] - W
                    H[i, j] = max(L, P, Q, 0)
 
                    # 添加进路径
                    path[point(i, j)] = []
                    if math.floor(L) == H[i, j]:
                        path[point(i, j)].append(point(i - 1, j - 1))
                    if math.floor(P) == H[i, j]:
                        path[point(i, j)].append(point(i - 1, j))
                    if math.floor(Q) == H[i, j]:
                        path[point(i, j)].append(point(i, j - 1))
 
        end = numpy.argwhere(H == numpy.max(H))
        for pos in end:
            key = point(pos[0], pos[1])
            value = path[key]
            result = [key]
            self.traceback(A, B, H, path, value, result)
 
    def Answer(self): # 取均值
        if len(self.similarity) == 0:
            if len(self.A) >= len(self.B):
                return (len(self.B) + 1) / (len(self.A) + 1)
            else:
                return (len(self.A) + 1) / (len(self.B) + 1)
        return sum(self.similarity) / len(self.similarity)
