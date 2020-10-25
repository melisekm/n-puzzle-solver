import heapq as hq  # https://docs.python.org/2/library/heapq.html
import timeit

# uzol
class Node:
    def __init__(self, stav, parent, lastOperator, heuristika, ciel):
        self.stav = stav  # 2D pole
        self.parent = parent  # class Node
        # string, ked sa pozrem na rodica mam vediet vypocitat cestu mozem usetrit ale aj stratit
        self.lastOperator = lastOperator
        self.cenaCiel = heuristika(stav, ciel)  # podla heurestickej funkcie

    def __lt__(self, other):  # custom comparator pre minHeap
        return self.cenaCiel < other.cenaCiel


# wrapper pre reprezentaciu minhaldy
class MinHeap:
    def __init__(self, start):  # vytvori jednoprvkovu haldu
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


def getKonfiguracia(stav):
    result = "\n"
    for riadok in stav:
        for cislo in riadok:
            result += str(cislo) + " "
        result += "\n"
    return result


def loadInput():
    print("Koniec [q]")
    print("Predvygenerovane: [2x7] [3x2] [3x3] [4x3] [5x2] [5x5] [6x6] [7x7] [9x3] [neriesitelne]")
    print("alebo [vlastny] zo suboru tests - start.txt a ciel.txt: ")
    vstup = input()

    if vstup in ("2x7", "3x2", "3x3", "4x3", "5x2", "5x5", "6x6", "7x7", "9x3", "neriesitelne"):
        path = "tests\\" + vstup + "\\"
    elif vstup == "vlastny":
        path = "tests\\"
    elif vstup == "q":
        print("Ukoncujem")
        quit()
    else:
        return None, None

    start = loadFile(path + "start.txt")
    ciel = loadFile(path + "ciel.txt")
    print("Start:" + getKonfiguracia(start))
    print("Ciel:" + getKonfiguracia(ciel))
    print("Zadajte typ heuristiky: ")
    print("Pocet policok, ktore nie su na svojom mieste[1]")
    print("Sucet vzdialenosti jednotlivych policok od ich cielovej pozicie[2]")
    heuristika = input()  # vyber funkcie pre heuristiku
    if heuristika == "1":
        heuristika = heuristika1
    elif heuristika == "2":
        heuristika = heuristika2
    else:
        return None, None
    print(f"Spustam hladanie ({len(start[0])}x{len(start)})...")
    return (start, ciel), heuristika


# vrati x y poziciu pre vstupne cislo v hlavolame
def najdiPosCisla(stav, target):
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo == target:
                return (i, j)


# Pocet policok, ktore nie su na svojom mieste
def heuristika1(stav, ciel):
    vysledok = 0
    for i, sublist in enumerate(stav):
        for j, cislo in enumerate(sublist):
            if cislo != 0 and cislo != ciel[i][j]:
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
                x, y = pozicieCisel[cislo]  # predvypocitana pozicia cisla v ciely
                vysledok += abs((x - i)) + abs((y - j))

    return vysledok


def isValid(stav, operator, i, j):
    if operator == "VPRAVO":
        if j == len(stav[i]) - 1:
            return False
    elif operator == "DOLE":
        if i == len(stav) - 1:
            return False
    elif operator == "VLAVO":
        if j == 0:
            return False
    elif operator == "HORE":
        if i == 0:
            return False
    return True


# ak je to mozne vrati novy stav po vykonani operatora
def vykonajOperator(stav, operator, i, j):
    novyStav = [sublist[:] for sublist in stav]  # skopiruje data

    if operator == "VPRAVO":
        novyStav[i][j], novyStav[i][j + 1] = novyStav[i][j + 1], novyStav[i][j]
    elif operator == "DOLE":
        novyStav[i][j], novyStav[i + 1][j] = novyStav[i + 1][j], novyStav[i][j]
    elif operator == "VLAVO":
        novyStav[i][j], novyStav[i][j - 1] = novyStav[i][j - 1], novyStav[i][j]
    elif operator == "HORE":
        novyStav[i][j], novyStav[i - 1][j] = novyStav[i - 1][j], novyStav[i][j]

    return novyStav


def opacnySmer(newOperator, parentOperator):
    if newOperator == "VPRAVO" and parentOperator == "VLAVO":
        return True
    elif newOperator == "VLAVO" and parentOperator == "VPRAVO":
        return True
    elif newOperator == "HORE" and parentOperator == "DOLE":
        return True
    elif newOperator == "DOLE" and parentOperator == "HORE":
        return True
    return False


def vytvorNasledovnikov(parent, heuristika, ciel, operatory):
    nasledovnici = []
    i, j = najdiPosCisla(parent.stav, 0)  # pozicia medzery
    for operator in operatory:  # skusam vsetkych operatorov
        if not opacnySmer(operator, parent.lastOperator):  # do opcaneho smeru nejdem
            if isValid(parent.stav, operator, i, j):  # ak sa da aplikovat operator
                novyStav = vykonajOperator(parent.stav, operator, i, j)
                novyUzol = Node(novyStav, parent, operator, heuristika, ciel)
                nasledovnici.append(novyUzol)
    return nasledovnici


def vytriedNasledovnikov(nasledovnici, spracovaneStavy, minHeap):
    for nasledovnik in nasledovnici:  # hlada nasledovnikov v spracovanych stavoch
        hashableStav = tuple(tuple(riadok) for riadok in nasledovnik.stav)
        if hashableStav in spracovaneStavy:
            nasledovnici.remove(nasledovnik)
    for nasledovnik in nasledovnici:  # ti co niesu uz spracovany su priadny do haldy
        minHeap.insert(nasledovnik)


def zostavRiesenie(uzol):
    result = []
    while uzol is not None:
        result.append(uzol.lastOperator)
        uzol = uzol.parent
    result.reverse()
    return result[1:]  # bez None od start pozicie


def lacne_hladanie(problem, heuristika):
    riesenie = None
    start, ciel = problem
    if heuristika.__name__ == "heuristika2":
        ziskajPozicieCisel(ciel)  # ak je to heurestika 2 dokazem si dopredu vypocitat pozicie
    operatory = ["VPRAVO", "DOLE", "VLAVO", "HORE"]
    start = Node(start, None, None, heuristika, ciel)
    spracovaneStavy = set()  # hashSet uz preskumanych stavov
    minHeap = MinHeap(start)  # vlozi start uzol do haldy
    while not minHeap.isEmpty():  # pokym existuju vytvorene ale nespracovane uzly
        current = minHeap.pop()  # vyberiem z topu haldy

        if current.stav == ciel:  # nasiel som koniec
            riesenie = zostavRiesenie(current)
            break

        nasledovnici = vytvorNasledovnikov(current, heuristika, ciel, operatory)  # potencialny
        hashableStav = tuple(tuple(riadok) for riadok in current.stav)  # konvert na hashable
        spracovaneStavy.add(hashableStav)  #
        vytriedNasledovnikov(nasledovnici, spracovaneStavy, minHeap)
        # odstranenie uz spracovanych stavov

    print(f"Pocet spracovanych uzlov: {len(spracovaneStavy)}")
    print(f"Pocet vygenerovanych uzlov: {len(spracovaneStavy) + len(minHeap.heap)}")
    return riesenie


if __name__ == "__main__":
    while True:
        problem, heuristika = loadInput()
        if problem == None:
            print("Zly vstup :)")
            continue

        start = timeit.default_timer()

        riesenie = lacne_hladanie(problem, heuristika)
        end = timeit.default_timer() - start

        print(f"Hladanie trvalo: {end}")
        if riesenie is not None:
            print(f"Dlzka riesenia: {len(riesenie)}")
            vstup = input("Chcete vypisat riesenie?: ")
            if vstup == "y":
                if riesenie is not None:
                    for i in riesenie:
                        print(i)
        else:
            print("Riesenie neexistuje.")