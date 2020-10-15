import heapq as hq  # https://docs.python.org/2/library/heapq.html


class Node:
    def __init__(self, stav, parent, lastOperator, heuristika):
        self.stav = stav  # int[]
        self.parent = parent  # class Node
        # string, ked sa pozrem na rodica mam vediet vypocitat cestu
        self.lastOperator = lastOperator
        self.cenaCiel = heuristika(stav)  # podla heurestickej funkcie

    def __lt__(self, other):  # custom comparator
        return self.cenaCiel < other.cenaCiel

    pass


class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, uzol):
        hq.heappush(self.heap, uzol)

    def pop(self):
        return hq.heappop(self.heap)


def VPRAVO(stav):
    pass


def DOLE(stav):
    pass


def VLAVO(stav):
    pass


def HORE(stav):
    pass


def loadFile(nazov):
    stav = []
    with open(nazov, "r") as file:
        for line in file:
            znak = line.strip().split(" ")
            for i in znak:
                stav.append(i)
    return Node(stav, None, None, heuristika)


def loadInput():
    print("Pocet policok, ktore nie su na svojom mieste[1]")
    print("Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície")
    heuristika = int(input("Zadajte typ heuristiky: "))
    if heuristika == 1:
        return heuristika1
    elif heuristika == 2:
        return heuristika2
    else:
        print("Zly vstup :)")
        quit()


def heuristika1(stav):
    return 1
    pass


def heuristika2(stav):
    print("pes")
    pass


def lacne_hladanie(problem, heuristika):
    start, ciel = problem
    minHeap = MinHeap()
    minHeap.insert(start)


if __name__ == "__main__":
    spracovane = {}
    # heuristika = loadInput()
    heuristika = heuristika1
    start = loadFile("start.txt")
    ciel = loadFile("ciel.txt")
    lacne_hladane(problem, heuristika)

    pass