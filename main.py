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


class MinHeap:
    def __init__(self, start):
        self.heap = [start]

    def insert(self, uzol):
        hq.heappush(self.heap, uzol)

    def pop(self):
        return hq.heappop(self.heap)


def najdiMedzeru(stav):
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo == 0:
                return (i, j)


def vykonajOperator(stav, operator):
    i, j = najdiMedzeru(stav)
    novyStav = [sublist[:] for sublist in stav]  # skopiruje data

    if operator == "VPRAVO":
        if j == len(stav[i]) - 1:
            return None
        novyStav[i][j], novyStav[i][j + 1] = novyStav[i][j + 1], novyStav[i][j]
    elif operator == "DOLE":
        if i == len(stav) - 1:
            return None
        novyStav[i][j], novyStav[i + 1][j] = novyStav[i + 1][j], novyStav[i][j]
    elif operator == "VLAVO":
        if j == 0:
            return None
        novyStav[i][j], novyStav[i][j - 1] = novyStav[i][j - 1], novyStav[i][j]
    elif operator == "HORE":
        if i == 0:
            return None
        novyStav[i][j], novyStav[i - 1][j] = novyStav[i - 1][j], novyStav[i][j]

    return novyStav


def VPRAVO(stav):
    return vykonajOperator(stav, "VPRAVO")


def DOLE(stav):
    return vykonajOperator(stav, "DOLE")


def VLAVO(stav):
    return vykonajOperator(stav, "VLAVO")


def HORE(stav):
    return vykonajOperator(stav, "HORE")


def loadFile(nazov):
    stav = []
    with open(nazov, "r") as file:
        for index, line in enumerate(file):
            stav.append([])
            znaky = line.strip().split(" ")
            stav[index].append(znaky)
    return stav


def loadInput():
    print("Pocet policok, ktore nie su na svojom mieste[1]")
    print("Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície")
    # heuristika = int(input("Zadajte typ heuristiky: "))
    heuristika = 1
    if heuristika == 1:
        heuristika = heuristika1
    elif heuristika == 2:
        heurestika = heuristika2
    else:
        print("Zly vstup :)")
        quit()
    start = loadFile("start.txt")
    ciel = loadFile("ciel.txt")
    return (start, ciel), heuristika


def heuristika1(stav):
    return 1
    pass


def heuristika2(stav):
    print("pes")
    pass


def lacne_hladanie(problem, heuristika):
    start, ciel = problem
    start = Node(start, None, None, heuristika)
    ciel = Node(ciel, None, None, heuristika)
    spracovaneStavy = {}
    minHeap = MinHeap(start)


if __name__ == "__main__":
    problem, heuristika = loadInput()
    # riesenie = lacne_hladanie(problem, heuristika)
    vstup = [[6, 1, 2, 3], [4, 5, 7, 0], [8, 9, 10, 11]]
    vystup = DOLE(vstup)
    pass