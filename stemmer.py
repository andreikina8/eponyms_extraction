from proga666 import get_word
import shelve

"""
get_stem1 retrieves only one stem of a query word
get_stem2 retrieves all possible stems of a query word
get_stem_wiki retrieves stems which are found in the base containing data from Wiktionary
"""

i = ["ая", "ий", "ый", "ая", "яя", "ое", "ее", "ые", "ие"]
#i = ["ая", "ий", "ый", "ая", "яя", "ое", "ее", "ые", "ие", "ого", "а", "я", "о", "ом", "ому", "им", "ое", "ем", "ов", "ев", "ю", "ой", "ей", "ею", "ы", "е", "у", "ой", "ам", "ям", "ами", "ями", "ах", "ях", "и", " "]
#i = ['ый' 'ий', 'ая', 'яя', 'ое', 'ее', 'ые', 'ие']
inflexions = set(i)
maxLen = 0
for infl in inflexions:
    if len(infl) > maxLen:
        maxLen = len(infl)
        
class Stemmer(object):
    def __init__(self, line, basest, baseinfl, baselem):
        self.basest = shelve.open(basest)
        self.baseinfl = shelve.open(baseinfl)
        self.baselem = shelve.open(baselem)
    def get_stem1(self, line):
        if line in inflexions:
            return self.line
        for word in get_word(line):
            inflexion = word[len(word) - maxLen:]
            if inflexion in inflexions:
                result = word[:len(word) - maxLen]
                return result
            else:
                i = 1
                while i <= maxLen:
                    infl1 = inflexion[i:]
                    if infl1 in inflexions:
                        result = word[:len(word) - len(infl1)]
                        return result
                    else:
                        return word
                    i += 1
    def get_stem2(self, line):
        myStems = []
        if line in inflexions: #if the query is in the set of inflexions, we do not analyze it
            return line
        for word in get_word(line):
            myStems.append(word) #in case of zero inflexion
            inflexion = word[len(word) - maxLen:]
            i = 0
            while i <= maxLen: #in case we have overlapping stems 
                inflexion1 = inflexion[i:]
                if inflexion1 in inflexions: 
                    stem = word[:len(word) - len(inflexion1)]
                    myStems.append(stem)
                i+=1
        return myStems
    def get_stem_wiki0(self, line, basest, baseinfl):
        stems = self.get_stem2(line)
        myStemsSet = set()
        arrOfStems = []
        myInflexions = set()
        maxlen = len(line)
        i = 0
        while i <= maxlen:
            infl = line[maxlen - i:]
            stem = line[:maxlen - i]
            if infl in self.baseinfl and stem in self.basest:
                arrOfStems.append(stem)
            else:
                stem1 = self.get_stem2(line)
            i+=1
        if arrOfStems:
            return arrOfStems
        else:
            return stem1
        
    def get_stem_wiki(self, line, basest, baseinfl):    
        stems = self.get_stem2(line)
        myStemsSet = set()
        arrOfStems = []
        myInflexions = set()
        maxlen = len(line)
        i = 0
        while i <= maxlen:
            infl = line[maxlen - i:]
            stem = line[:maxlen - i]
            if infl in self.baseinfl and stem in self.basest:
                arrOfStems.append(stem)
                for inflexion in self.baseinfl[infl]:
                    myInflexions.add(inflexion)
                for st in self.basest[stem]:
                    myStemsSet.add(st)
            i+=1
        a = myInflexions.intersection(myStemsSet)
        if a:
            return arrOfStems
        else:
            stem1 = self.get_stem2(line)
            return stem1
        if infl not in self.baseinfl and stem not in self.basest:
            stem2 = self.get_stem2(line)
            return stem2
    def get_lemma(self, line, dataBaseInfl, dataBaseLem):
        myArrayOfLem = []
        for item in self.baseinfl:
            if item == '<!--':
                self.baseinfl.pop(item)
        maxlen = 0
        for item in self.baseinfl:
            if len(item) > maxlen:
                maxlen = len(item) 
        i = 0
        while i <= maxlen:
            stem = line[:len(line) - i]
            inflexion = line[len(line) - i:]
            if stem in self.baselem and inflexion in self.baseinfl:
                a = set()
                b = set()
                for item in self.baselem[stem]:
                    a.add(item)
                for item in self.baseinfl[inflexion]:
                   b.add(item)
                intersec = a.intersection(b)
                if intersec: #if intersection is not empty, this stem is compatible with this inflexion
                    for tuple1 in self.baselem[stem]:
                        if tuple1 in intersec:
                            for lem in self.baselem[stem][tuple1]:                        
                                myArrayOfLem.append(lem)
            i+=1
        if stem not in self.baselem: #if there is no such stem in database, we return to the stemmer which does not use wiktionary
            stem1 = self.get_stem2(line)
            return stem1
        return myArrayOfLem
    def __del__(self):
        self.basest.close()
        self.baseinfl.close()
        self.baselem.close()


        
stemmer1 = Stemmer('абаканка', 'nouns', 'nounsinfl', 'nounslem1')

"""        
def get_stem1(line):
    if line in inflexions:
        return line
    for word in get_word(line):
        inflexion = word[len(word) - maxLen:]
        if inflexion in inflexions:
            result = word[:len(word) - maxLen]
            return result
        else:
            i = 1
            while i <= maxLen:
                infl1 = inflexion[i:]
                if infl1 in inflexions:
                    result = word[:len(word) - len(infl1)]
                    return result
                else:
                    return word
                i += 1

def get_stem2(line):
    myStems = []
    if line in inflexions: #if the query is in the set of inflexions, we do not analyze it
        return line
    for word in get_word(line):
        myStems.append(word) #in case of zero inflexion
        inflexion = word[len(word) - maxLen:]
        i = 0
        while i <= maxLen: #in case we have overlapping stems 
            inflexion1 = inflexion[i:]
            if inflexion1 in inflexions: 
                stem = word[:len(word) - len(inflexion1)]
                myStems.append(stem)
            i+=1
    return myStems
          
def get_stem_wiki(line, dataBaseStem, dataBaseInfl):
    stems = get_stem2(line)
    myStemsSet = set()
    arrOfStems = []
    myInflexions = set()
    basestem = shelve.open(dataBaseStem)
    baseinfl = shelve.open(dataBaseInfl)
    maxlen = len(line)
    i = 0
    while i <= maxlen:
        infl = line[maxlen - i:]
        stem = line[:maxlen - i]
        if infl in baseinfl and stem in basestem:
            arrOfStems.append(stem)
            for inflexion in baseinfl[infl]:
                myInflexions.add(inflexion)
            for st in basestem[stem]:
                myStemsSet.add(st)
        i+=1
    a = myInflexions.intersection(myStemsSet)
    if a:
        return arrOfStems
    else:
        stem1 = get_stem2(line)
        return stem1
    if infl not in baseinfl and stem not in basestem:
        stem2 = get_stem2(line)
        return stem2       
    basestem.close()
    baseinfl.close()
        

def get_lemma(line, dataBaseInfl, dataBaseLem):
    baseinfl = shelve.open(dataBaseInfl)
    baselem = shelve.open(dataBaseLem)
    myArrayOfLem = []
    for item in baseinfl:
        if item == '<!--':
            baseinfl.pop(item)
    maxlen = 0
    for item in baseinfl:
        if len(item) > maxlen:
            maxlen = len(item) 
    i = 0
    while i <= maxlen:
        stem = line[:len(line) - i]
        inflexion = line[len(line) - i:]
        if stem in baselem and inflexion in baseinfl:
            #print(stem, 'st')
            #print(inflexion, 'infl')
            a = set()
            b = set()
            for item in baselem[stem]:
                a.add(item)
            for item in baseinfl[inflexion]:
                b.add(item)
            intersec = a.intersection(b)
            #print(a, 'stems')
            #print(intersec, 'inter')
            if intersec: #if intersection is not empty, this stem is compatible with this inflexion
                for tuple1 in baselem[stem]:
                    if tuple1 in intersec:
                        for lem in baselem[stem][tuple1]:                        
                            myArrayOfLem.append(lem)
        i+=1
    if stem not in baselem: #if there is no such stem in database, we return to the stemmer which does not use wiktionary
        stem1 = get_stem2(line)
        return stem1
    return myArrayOfLem
"""
    
