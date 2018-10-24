import math

class Pqueue:
    def __init__(self):

        self.heap = []

    def heapify(self, A, i):
        n = len(A)
        if 2 * i > n:
            return

        elif 2 * i == n:
            if A[2 * i - 1] >= A[i - 1]:
                A[2 * i - 1], A[i - 1] = A[i - 1], A[2 * i - 1]
                return

        else:
            if A[2 * i] >= A[i - 1] or A[2 * i - 1] >= A[i - 1]:
                if A[2 * i] >= A[2 * i - 1]:
                    A[2 * i], A[i - 1] = A[i - 1], A[2 * i]
                    self.heapify(A, 2 * i + 1)
                else:
                    A[2 * i - 1], A[i - 1] = A[i - 1], A[2 * i - 1]
                    self.heapify(A, 2 * i)

    def build_heap(self, arr):
        for i in range(int(math.floor(len(arr) / 2)), 0, -1):
            self.heapify(arr, i)
        return arr

    def apply_heap(self, arr):
        self.heap = self.build_heap(arr)

    def max(self):
        return self.heap[0]

    def extract_max(self):
        maximum = self.heap[0]
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        del self.heap[-1]
        self.heapify(self.heap, 1)
        return list(maximum.keys())[0], list(maximum.values())[0]

    def increase_key(self, i, k):
        self.heap[i - 1] = k
        while self.heap[math.floor(i / 2) - 1] < self.heap[i - 1]:
            self.heap[math.floor(i / 2) - 1], self.heap[i - 1] = self.heap[i - 1], self.heap[math.floor(i / 2) - 1]
            if math.floor(i / 2) >= 3:
                i = math.floor(i / 2)

    def insert(self, k):
        self.heap.append(math.inf)
        self.increase_key(len(self.heap), k)

class MinHqueue(Pqueue):
    def heapify(self, A, i):
        n = len(A)
        if 2 * i > n:
            return

        elif 2 * i == n:
            if list(A[2 * i - 1].values()) <= list(A[i - 1].values()):
                A[2 * i - 1], A[i - 1] = A[i - 1], A[2 * i - 1]
                return

        else:
            if list(A[2 * i].values()) <= list(A[i - 1].values()) or list(A[2 * i - 1].values()) <= list(A[i - 1].values()):
                if list(A[2 * i].values()) <= list(A[2 * i - 1].values()):
                    A[2 * i], A[i - 1] = A[i - 1], A[2 * i]
                    self.heapify(A, 2 * i + 1)
                else:
                    A[2 * i - 1], A[i - 1] = A[i - 1], A[2 * i - 1]
                    self.heapify(A, 2 * i)

    def increase_key(self, i, k):
        self.heap[i - 1] = k
        while list(self.heap[math.floor(i / 2) - 1].values()) > list(self.heap[i - 1].values()):
            self.heap[math.floor(i / 2) - 1], self.heap[i - 1] = self.heap[i - 1], self.heap[math.floor(i / 2) - 1]
            if math.floor(i / 2) >= 3:
                i = math.floor(i / 2)


class Djk:
    def __init__(self, s=0):
        self.s = 0
        self.graph = {}
        self.read()
        self.d = []
        self.minheap = MinHqueue()
        self.initialize(s)
        self.main()

    def read(self):
        inp = []
        with open('input.txt') as f:
            for line in f:
                inp.append(line)

        self.n = int(inp[0])
        self.m = int(inp[1])
        self.source = int(inp[2])
        self.dest = int(inp[3])

        # for i in range(self.n):
        #     self.graph[i] = []

        self.raw_gr = {}

        for i in range(self.n):
            self.raw_gr[i] = []

        for i in range(self.m):
            l, r = map(int, inp[4 + i].split(' '))
            self.raw_gr[l].append({r: 1})

        distances = self.bfs()

        for dis in distances:
            if dis % 2 == 0:
                for j in self.raw_gr[dis]:
                    for kj in j:
                        j[kj] = 1
            else:
                for j in self.raw_gr[dis]:
                    for kj in j:
                        j[kj] = 2

        self.graph = self.raw_gr


    def bfs(self, s=0):
        V = [False for _ in range(self.n)]
        d = [math.inf for _ in range(self.n)]
        gr = {}
        for node in self.raw_gr:
            keys = []
            for j in self.raw_gr[node]:
                keys.append(list(j.keys())[0])
            gr[node] = keys

        d[s] = 0
        queue = [s]
        while len(queue) > 0:
            s_prime = queue[0]
            queue.pop(0)
            for t in gr[s_prime]:
                if not V[t]:
                    V[t] = True
                    d[t] = d[s_prime] + 1
                    queue.append(t)
        return d


    def initialize(self, s):
        self.minheap.apply_heap([{i: math.inf} if i != s else {i: 0} for i in range(self.n)])
        self.d = [math.inf if i != s else 0 for i in range(self.n)]


    def get_weight(self, q, r):
        for i in self.graph[q]:
            for k in i.keys():
                if k == r:
                    return i[k]


    def relax(self, q, r):
        if self.d[q] + self.get_weight(q, r) < self.d[r]:
            self.d[r] = self.d[q] + self.get_weight(q, r)
            for n, it in enumerate(self.minheap.heap):
                key = list(it.keys())[0]
                if key == r:
                    self.minheap.increase_key(n + 1, {key: self.d[r]})

    def get_successors(self, q):
        ks = []
        for it in self.graph[q]:
            ks.append(list(it.keys())[0])
        return ks

    def main(self):
        S = []
        while len(self.minheap.heap) > 0:
            q, q_val = self.minheap.extract_max()
            if q == self.dest:
                return
            for it in self.get_successors(q):
                self.relax(q, it)

    def get_distances(self):
        return self.d[self.dest]


djk = Djk()

with open('output.txt', 'w+') as f:
    f.write(str(djk.get_distances()))