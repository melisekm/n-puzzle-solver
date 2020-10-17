import heapq as hq  # https://docs.python.org/2/library/heapq.html
import timeit

import drawImages as draw

# uzol
class Node:
    def __init__(self, stav, parent, lastOperator, heuristika, ciel):
        self.stav = stav  # int[]
        self.parent = parent  # class Node
        # string, ked sa pozrem na rodica mam vediet vypocitat cestu mozem usetrit ale aj stratit
        self.lastOperator = lastOperator
        self.cenaCiel = heuristika(stav, ciel)  # podla heurestickej funkcie

    def __lt__(self, other):  # custom comparator pre minHeap
        return self.cenaCiel < other.cenaCiel

    def __le__(self, other):
        return self.cenaCiel <= other.cenaCiel


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
    heuristika = int(input("Zadajte typ heuristiky: "))  # vyber funkcie pre heuristiku
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


# Pocet policok, ktore nie su na svojom mieste
def heuristika1(stav, ciel):
    vysledok = 0
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo != 0 and cislo != ciel[i][j]:  # kontrolujem ci tam je alebo nie
                vysledok += 1

    return vysledok


# predvypocita pozicie pre cisla v ciely
def ziskajPozicieCisel(ciel):
    global pozicieCisel
    pozicieCisel = {}
    for sublist in ciel:
        for cislo in sublist:
            pozicieCisel[cislo] = najdiPosCisla(ciel, cislo)


# Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície
def heuristika2(stav, ciel):
    vysledok = 0
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo != 0:
                # x, y = najdiPosCisla(ciel, cislo)  # pocitam
                x, y = pozicieCisel[cislo]  # predvypocitana pozicia cisla v ciely
                vysledok += abs((x - i)) + abs((y - j))

    return vysledok


# ad hoc :D
def opacnySmer(newOperatorIndex, parentOperator, operatory):
    if parentOperator is not None:
        parentOperatorIndex = operatory.index(parentOperator)
        if newOperatorIndex == parentOperatorIndex:
            return False
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
    uzly = []
    while uzol is not None:
        result.append(uzol.lastOperator)
        uzly.append(uzol)
        uzol = uzol.parent
    result.reverse()
    uzly.reverse()
    return result[1:], uzly  # bez None od start pozicie


def lacne_hladanie(problem, heuristika):
    start, ciel = problem
    if heuristika.__name__ == "heuristika2":
        ziskajPozicieCisel(ciel)  # ak je to heurestika 2 dokazem si dopredu vypocitat pozicie
    operatory = ["VPRAVO", "DOLE", "VLAVO", "HORE"]
    start = Node(start, None, None, heuristika, ciel)
    spracovaneStavy = {}  # hashTable uz preskumanych stavov
    minHeap = MinHeap(start)  # vlozi start uzol do haldy
    while not minHeap.isEmpty():  # pokym existuju vytvorene ale nespracovane uzly
        current = minHeap.pop()  # vyberiem z topu haldy
        if current.stav == ciel:  # nasiel som koniec
            print(f"Pocet spracovanych uzlov: {len(spracovaneStavy)}")
            print(f"Pocet vygenerovanych uzlov: {len(spracovaneStavy) + len(minHeap.heap)}")
            return zostavRiesenie(current)
        nasledovnici = vytvorNasledovnikov(current, heuristika, ciel, operatory)  # potencialny
        hashableStav = tuple(tuple(riadok) for riadok in current.stav)  # konvert na hashable TODO
        spracovaneStavy[hashableStav] = current
        vytriedNasledovnikov(nasledovnici, spracovaneStavy, minHeap)
        # odstranenie uz spracovanych stavov
    return None


def pocetVacsichPredchodcov(start, cislo):
    res = 0
    for sublist in start:
        for num in sublist:
            if num != 0:
                if num == cislo:
                    return res
                if num > cislo:
                    res += 1
    return res


def paritaPreStav(stav):
    res = 0
    for i, sublist in enumerate(stav, start=1):
        for cislo in sublist:
            if cislo != 0:
                res += pocetVacsichPredchodcov(stav, cislo)
            else:
                medzeraPos = i
    return res, medzeraPos


def isSolvable(problem):
    start, ciel = problem
    parita1, medzera1 = paritaPreStav(start)
    if len(start) % 2 == 1 and len(start[0]) % 2 == 1:
        if parita1 % 2 == 1:  # 7x7 toto nie je zjavne na vsetko :)
            return False
        else:
            return True
    parita2, medzera2 = paritaPreStav(ciel)
    if (parita1 + medzera1) % 2 == (parita2 + medzera2) % 2:
        return True
    return False


if __name__ == "__main__":
    problem, heuristika = loadInput()
    if isSolvable(problem):
        start = timeit.default_timer()
        riesenie, uzly = lacne_hladanie(problem, heuristika)
        end = timeit.default_timer() - start
        for i in riesenie:
            print(i)
        print(f"Hladanie trvalo: {end}")
        print(f"Dlzka riesenia: {len(riesenie)}")
        draw.drawImages(uzly)

    else:
        print("Riesenie neexistuje.")
