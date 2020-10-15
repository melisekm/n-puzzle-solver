import heapq as hq  # https://docs.python.org/2/library/heapq.html
import timeit

# uzol
class Node:
    def __init__(self, stav, parent, lastOperator, heuristika, ciel):
        self.stav = stav  # int[]
        self.parent = parent  # class Node
        # string, ked sa pozrem na rodica mam vediet vypocitat cestu mozem usetrit
        self.lastOperator = lastOperator
        self.cenaCiel = heuristika(stav, ciel)  # podla heurestickej funkcie

    def __lt__(self, other):  # custom comparator pre minHeap
        return self.cenaCiel < other.cenaCiel


# wrapper pre reprezentaciu minhaldy
class MinHeap:
    def __init__(self, start):
        self.heap = [start]

    # vlozi prvok do haldy
    def insert(self, uzol):
        hq.heappush(self.heap, uzol)

    # odoberie a vrati prvok z haldy
    def pop(self):
        return hq.heappop(self.heap)

    # vrati stav ci je halda prazdna
    def isEmpty(self):
        return not self.heap


# predvypocita pozicie pre cisla v ciely
def ziskajPozicieCisel(ciel):
    global pozicieCisel
    pozicieCisel = {}
    for sublist in ciel:
        for cislo in sublist:
            pozicieCisel[cislo] = najdiPosCisla(ciel, cislo)


# vrati x y poziciu pre vstupne cislo v hlavolame
def najdiPosCisla(stav, target):
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo == target:
                return (i, j)


# ak je to mozne vrati novy stav po vykonani operatora
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


def loadFile(nazov):
    stav = []  # je reprezentovany ako list of lists
    with open(nazov, "r") as file:
        for index, line in enumerate(file):
            stav.append([])
            znaky = line.strip().split(" ")  # extrahuje cisla z riadku
            stav[index] = list(map(int, znaky))  # zmeni ich na inty
    return stav


def loadInput():
    print("Pocet policok, ktore nie su na svojom mieste[1]")
    print("Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície[2]")
    # heuristika = int(input("Zadajte typ heuristiky: ")) # vyber funkcie pre heuristiku
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


# Pocet policok, ktore nie su na svojom mieste
def heuristika1(stav, ciel):
    vysledok = 0
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo != 0 and cislo != ciel[i][j]:  # kontrolujem ci tam je alebo nie
                vysledok += 1

    return vysledok


# Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície
def heuristika2(stav, ciel):
    vysledok = 0
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo != 0:
                # x, y = najdiPosCisla(ciel, cislo) # pocitam
                x, y = pozicieCisel[cislo]  # predvypocitana pozicia cisla v ciely
                vysledok += abs((x - i)) + abs((y - j))

    return vysledok


def opacnySmer(newOperatorIndex, parentOperator, operatory):
    if parentOperator is not None:
        parentOperatorIndex = operatory.index(parentOperator)
        if (newOperatorIndex + parentOperatorIndex) % 2 == 0:
            return True
    return False


def vytriedNasledovnikov(nasledovnici, spracovaneStavy, minHeap):
    for nasledovnik in nasledovnici:
        hashableStav = tuple(tuple(riadok) for riadok in nasledovnik.stav)
        if hashableStav in spracovaneStavy:
            nasledovnici.remove(nasledovnik)
    for nasledovnik in nasledovnici:
        minHeap.insert(nasledovnik)


def vytvorNasledovnikov(parent, heuristika, ciel, operatory):
    nasledovnici = []
    for i, operator in enumerate(operatory):
        if not opacnySmer(i, parent.lastOperator, operatory):
            novyStav = vykonajOperator(parent.stav, operator)
            if novyStav is not None:
                novyUzol = Node(novyStav, parent, operator, heuristika, ciel)
                nasledovnici.append(novyUzol)
    return nasledovnici


def zostavRiesenie(uzol):
    result = []
    while uzol is not None:
        result.append(uzol.lastOperator)
        uzol = uzol.parent
    result.reverse()
    return result[1:]


def lacne_hladanie(problem, heuristika):
    start, ciel = problem
    if "heuristika2" == heuristika.__name__:
        ziskajPozicieCisel(ciel)
    operatory = ["VPRAVO", "DOLE", "VLAVO", "HORE"]
    start = Node(start, None, None, heuristika, ciel)
    spracovaneStavy = {}
    minHeap = MinHeap(start)  # vlozi start uzol do haldy
    while not minHeap.isEmpty():
        current = minHeap.pop()
        if current.stav == ciel:
            return zostavRiesenie(current)
        nasledovnici = vytvorNasledovnikov(current, heuristika, ciel, operatory)
        hashableStav = tuple(tuple(riadok) for riadok in current.stav)
        spracovaneStavy[hashableStav] = current
        vytriedNasledovnikov(nasledovnici, spracovaneStavy, minHeap)
    return None


if __name__ == "__main__":
    problem, heuristika = loadInput()
    start = timeit.default_timer()
    riesenie = lacne_hladanie(problem, heuristika)
    print(timeit.default_timer() - start)
    # vystup = heuristika2(problem[0], problem[1])
    print(len(riesenie))