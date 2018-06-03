import generator
import pymorphy2
import nltk
from nltk.collocations import *
import time
import re
from stemmer import stemmer1

"""
This programme performs terms extraction based on different approaches
"""

parser = pymorphy2.MorphAnalyzer()

class TaggedWord(object):
    def __init__(self, string, normal_form, token_type):
        self.string = string
        self.normal_form = normal_form
        self.token_type = token_type
    def __repr__(self):
        return '%s (%s) %s' %(self.string, self.normal_form, self.token_type)
    
def tagging(file): # this function creates a dictionary with sentence number as a key and object of class TaggedWord as a value
    myDict = {}
    TaggedWords = {}
    myFile = open(file, encoding='utf-8')
    for num, line in enumerate(myFile):
        for token in generator.get_token(line):
            setdef = myDict.setdefault(num+1, [])
            setdef.append(token)
    for key in myDict.keys():
        for token in myDict[key]:
            if token.token_type is 'Alpha':
                res = parser.parse(token.string) # morphological analysis
                myTag = res[0].tag.POS # extraction of pos tag
                form = res[0].normal_form # extraction of normal form
                tagWord = TaggedWord(token.string, form, myTag) 
                setdef = TaggedWords.setdefault(key, [])
                setdef.append(tagWord)
            if token.token_type is 'Punctuation': 
                if token.string == '—' or token.string == '–' or token.string == '-':
                    tagWord = TaggedWord('-', form, token.token_type) # bringing all possible spellings of dash to one form
                    setdef = TaggedWords.setdefault(key, [])
                    setdef.append(tagWord)
                else:
                    tagWord = TaggedWord(token.string, form, token.token_type)
                    setdef = TaggedWords.setdefault(key, [])
                    setdef.append(tagWord)
            if token.token_type is 'Space':
                tagWord = TaggedWord(token.string, form, token.token_type)
                setdef = TaggedWords.setdefault(key, [])
                setdef.append(token)
    myFile.close()
    return TaggedWords


"""
Functions of this class perform terms extraction based on statistical approach (using MI measure)
"""
class MI(object):
    def __init__(self, file):
        self.file = open(file, encoding='utf-8')
        
    def stop_words_noun_Noun(self, file): # this function creates a list of stop-words for the extraction of 'noun Noun' type of constructions
        TaggedWords = tagging(file)
        stopWords = []
        for key in TaggedWords.keys():
            for token in TaggedWords[key]:
                if token.token_type == 'NOUN':
                    continue
                else:
                    stopWords.append(token.string) # list contains all types of tokens but nouns
        return stopWords

    def stop_words_adjf_noun(self, file): # this function creates a list of stop-words for the extraction of 'adjf noun' type of constructions
        TaggedWords = tagging(file)
        stopWords = []
        for key in TaggedWords.keys():
            for token in TaggedWords[key]:
                if token.token_type == 'NOUN' or token.token_type == 'ADJF':
                    continue
                else:
                    stopWords.append(token.string) # list contains all types of tokens but nouns and adjectives 
        return stopWords
    
    def noun_Noun_mi(self, file): # this function uses MI measure to extract constructions of 'noun Noun' type
        array = []
        result = []
        stopWords = self.stop_words_noun_Noun(file)    
        for num, line in enumerate(self.file):
            for token in generator666.get_token(line):
                if token.token_type == 'Alpha':
                   array.append(token.string)        
        wordFilter = lambda w: w in stopWords
        ngramFilter = lambda x, y: y[0].islower() # ngram_filter is used in order to remove constructions with the second word starting with small letter 
        finder = BigramCollocationFinder.from_words(array)
        finder.apply_ngram_filter(ngramFilter)
        finder.apply_word_filter(wordFilter)
        finder.apply_freq_filter(0.5)
        measures = nltk.collocations.BigramAssocMeasures()
        for x in finder.score_ngrams(measures.mi_like):
            term = '%s %s' % (x[0][0], x[0][1])
            result.append(term)
        return result
    
    def adjf_noun_mi(self, file): # this function uses MI measure to extract constructions that are likely to be terms
        array = []
        result = []
        stopWords = self.stop_words_adjf_noun(file)
        for num, line in enumerate(self.file):
            for token in generator.get_token(line):
                if token.token_type == 'Alpha':
                   array.append(token.string)
        wordFilter = lambda w: w in stopWords
        ngramFilter = lambda x, y: y[0].isupper() # ngram_filter is used in order to remove constructions with the second word starting with capital letter
        finder = BigramCollocationFinder.from_words(array)
        finder.apply_ngram_filter(ngramFilter)
        finder.apply_word_filter(wordFilter)
        finder.apply_freq_filter(0.5)
        measures = nltk.collocations.BigramAssocMeasures()
        for x in finder.score_ngrams(measures.mi_like):
            term = '%s %s' % (x[0][0], x[0][1])
            result.append(term)
        return result
    
    def adjf_noun_mi_stem(self, file): # this function uses stemmer and suffix templates in order to improve the acquired list of constructions
        array = self.adjf_noun_mi(file)
        result = []
        for item in array:
            tokenized = nltk.word_tokenize(item)
            for word in tokenized:
                res = parser.parse(word)
                tag = res[0].tag.POS
                form = res[0].normal_form
                newTok = TaggedWord(word, form, tag)
                ind = tokenized.index(word)
                tokenized.pop(ind)
                tokenized.insert(ind, newTok)
            if tokenized[0].token_type == 'ADJF' and tokenized[1].token_type == 'NOUN': # extraction of 'adjf noun' type of constructions
                stem = stemmer1.get_stem1(tokenized[0].normal_form)
                if stem.endswith('овск') or stem.endswith('евск') or stem.endswith('ов') or stem.endswith('ев'): # suffixes that are likely to occur in terms
                    term = '%s %s' %(tokenized[0].string.lower(), tokenized[1].string.lower())
                    result.append(term)
        return result
    
    def __del__(self):
        self.file.close()
        
get_terms_MI = MI('corpus.txt')

"""
Functions of this class perform terms extraction using syntactic templates
"""
class Templates(object):
    def __init__(self, file):
        self.file = open(file, encoding='utf-8')

    def filter_text(self, file): # this function creates a dictionary with nouns, adjectives and dash only
        TaggedWords = tagging(file)
        filteredWords = {}
        stopWords = []
        for key in TaggedWords.keys():
            for token in TaggedWords[key]:
                if token.token_type == 'NOUN' or token.token_type == 'ADJF' or token.string == '-':
                    setdef = filteredWords.setdefault(key, [])
                    setdef.append(token)
        return filteredWords
    
    def noun_Noun(self, file): # this function extracts constructions of 'noun_Noun' type
        noun_Noun = set()
        filteredWords = self.filter_text(file)
        for key in filteredWords.keys():
            for i in range(len(filteredWords[key]) - 1):            
                if filteredWords[key][i].token_type == 'NOUN' and filteredWords[key][i+1].token_type == 'NOUN': 
                    if filteredWords[key][i+1].string[0].isupper(): # extraction of two co-occuring nouns (if the second one starts with a capital letter)
                        if i+1 >= len(filteredWords[key]) - 1: # a case when a construction occurs at the end of a sentence
                            res = filteredWords[key][i].string + ' ' + filteredWords[key][i+1].string
                            noun_Noun.add(res)
                        if i+1 < len(filteredWords[key]) - 1:
                            result = filteredWords[key][i].string + ' ' + filteredWords[key][i+1].string
                            noun_Noun.add(result)
        return noun_Noun        
        
    def noun_Noun_mi_template(self, file): # this function intersects two sets with constructions of 'noun Noun' type
        filteredWords = self.filter_text(file)
        mi_array = get_terms_MI.noun_Noun_mi(file) # the set obtained with use of MI measure
        mi_set = set()
        for item in mi_array:
            mi_set.add(item)
        result_set = self.noun_Noun(file) # the set obtained with use of the syntactic template        
        intersec = result_set.intersection(mi_set)
        #dif = result_set.difference(intersec)
        return intersec
    
    def noun_Noun_Noun(self, file): # this function retrieves constructions of 'noun Noun-Noun' type
        filteredWords = self.filter_text(file)
        noun_Noun_Noun = {}
        noun_Noun_Noun_set = set()
        for key in filteredWords.keys():
            for i in range(len(filteredWords[key]) - 1):
                if filteredWords[key][i].string == '-':
                    if filteredWords[key][i-1].string[0].isupper() and filteredWords[key][i+1].string[0].isupper():
                        if filteredWords[key][i-2].string == '-':
                            result = filteredWords[key][i-2].string + filteredWords[key][i-1].string + filteredWords[key][i].string + filteredWords[key][i+1].string
                            # result is a construction of type '-Noun-Noun'
                            setdef = noun_Noun_Noun.setdefault(key, [])
                            setdef.append(result)
                        else:
                            result = filteredWords[key][i-2].string + ' ' + filteredWords[key][i-1].string + filteredWords[key][i].string + filteredWords[key][i+1].string
                            # result is a construction of type 'noun Noun-Noun'
                            setdef = noun_Noun_Noun.setdefault(key, [])
                            setdef.append(result) 
        for key in noun_Noun_Noun.keys():
            for i in range(len(noun_Noun_Noun[key])):
                if noun_Noun_Noun[key][i].startswith('-'): # concatenation of constructions 'noun Noun-Noun' and '-Noun-Noun'
                    index = noun_Noun_Noun[key][i].rindex('-')
                    string = noun_Noun_Noun[key][i][index:]
                    newTerm = noun_Noun_Noun[key][i-1] + string
                    noun_Noun_Noun[key][i-1] = newTerm
                    noun_Noun_Noun[key].pop(i)
        for value in noun_Noun_Noun.values():
            for item in value:
                noun_Noun_Noun_set.add(item)
        return noun_Noun_Noun_set
    
    def __del__(self):
        self.file.close()

get_terms_templates = Templates('corpus.txt')
