import heapq as hq  # https://docs.python.org/2/library/heapq.html


class Node:
    def __init__(self, stav, parent, lastOperator, heuristika, ciel):
        self.stav = stav  # int[]
        self.parent = parent  # class Node
        # string, ked sa pozrem na rodica mam vediet vypocitat cestu mozem usetrit
        self.lastOperator = lastOperator
        self.cenaCiel = heuristika(stav, ciel)  # podla heurestickej funkcie

    def __lt__(self, other):  # custom comparator pre minHeap
        return self.cenaCiel < other.cenaCiel


class MinHeap:
    def __init__(self, start):
        self.heap = [start]

    def insert(self, uzol):
        hq.heappush(self.heap, uzol)

    def pop(self):
        return hq.heappop(self.heap)


def ziskajPozicieCisel(ciel):
    global pozicieCisel
    pozicieCisel = {}
    for sublist in ciel:
        for cislo in sublist:
            pozicieCisel[cislo] = najdiPosCisla(ciel, cislo)


def najdiPosCisla(stav, target):
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo == target:
                return (i, j)


def vykonajOperator(stav, operator):
    i, j = najdiPosCisla(stav, 0)  # pozicia medzery
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
            stav[index] = list(map(int, znaky))
    return stav


def loadInput():
    print("Pocet policok, ktore nie su na svojom mieste[1]")
    print("Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície")
    # heuristika = int(input("Zadajte typ heuristiky: "))
    heuristika = 2
    if heuristika == 1:
        heuristika = heuristika1
    elif heuristika == 2:
        heuristika = heuristika2
    else:
        print("Zly vstup :)")
        quit()
    start = loadFile("start.txt")
    ciel = loadFile("ciel.txt")
    return (start, ciel), heuristika


def heuristika1(stav, ciel):
    vysledok = 0
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo != 0 and cislo != ciel[i][j]:
                vysledok += 1

    return vysledok


# je mozne si predvypocitat pozicie pre kazde cislo
def heuristika2(stav, ciel):
    vysledok = 0
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo != 0:
                # x, y = najdiPosCisla(ciel, cislo)
                x, y = pozicieCisel[cislo]
                vysledok += abs((x - i)) + abs((y - j))

    return vysledok


def lacne_hladanie(problem, heuristika):
    start, ciel = problem
    if "heuristika2" == heuristika.__name__:
        ziskajPozicieCisel(ciel)
    start = Node(start, None, None, heuristika, ciel)
    ciel = Node(ciel, None, None, heuristika, ciel)
    spracovaneStavy = {}
    minHeap = MinHeap(start)


if __name__ == "__main__":
    problem, heuristika = loadInput()
    riesenie = lacne_hladanie(problem, heuristika)
    # vystup = heuristika2(problem[0], problem[1])
    pass