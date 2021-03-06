from algo1 import String, substr
from hashmap import HashMapNode
from mergesort import mergeSort
from trie import Trie, insert, search
from serializacion import save


"""create()"""


def indexDocs(path, docs):
    lenD = len(docs)

    T = Trie()
    for doc in docs:
        if doc[-4:] != '.txt':
            continue

        dir = path + doc
        with open(dir, encoding='utf-8') as file:
            txt = file.read()
            txt = String(txt)
            indexWords(txt, doc, T, lenD)

            save(T)


def indexWords(txt, doc, T, lenD):
    s = 0
    withinWord = False

    for i in range(len(txt) - 1):
        if not withinWord:
            if isLetter(txt[i]):
                s = i
                withinWord = True
        else:
            if isEndOfWord(txt, i):
                withinWord = False
                word = substr(txt, s, i)
                insert(T, word, doc, lenD)

        if ord(txt[i]) == 64:
            email = extractMail(txt, i)
            insert(T, email, doc, lenD)


def toUpp(c):
    if ord(c) > 96 and ord(c) < 123:
        return chr(ord(c) - ord('a') + ord('A'))
    else:
        return c


def isLetter(c):
    c = toUpp(c)
    if ord(c) > 64 and ord(c) < 91:
        return True
    else:
        return False


def isEndOfWord(txt, i):
    if not isLetter(txt[i]):
        if ord(txt[i]) != 39:
            return True

        if isLetter(txt[i + 1]):
            return False
        else:
            return True

    else:
        return False


def extractMail(txt, i):
    s = i
    while s > 0:
        s -= 1
        if ord(txt[s]) == 32 or ord(txt[s]) == 10:
            if isLetter(txt[s+1]):
                s += 1
            else:
                s += 2
            break

    while i < len(txt):
        i += 1
        if ord(txt[i]) == 32 or ord(txt[i]) == 10:
            if not isLetter(txt[i-1]) and txt[i-1] != '@':
                i -= 1
            break

    return substr(txt, s, i)


"""create()"""


"""search()"""


def fetchDocList(T, word):
    temp = search(T, word)

    if temp:
        doclist = temp.rep.head
    else:
        return None

    nil = HashMapNode()
    nil.value = 0

    for i in range(len(doclist)):
        if doclist[i] is None:
            doclist[i] = nil

    mergeSort(doclist)
    return doclist


"""search()"""
