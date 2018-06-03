import generator666
import pymorphy2
import nltk

parser = pymorphy2.MorphAnalyzer()

class TaggedWord(object):
    def __init__(self, string, normal_form, token_type):
        self.string = string
        self.normal_form = normal_form
        self.token_type = token_type
    def __repr__(self):
        return '%s (%s) %s' %(self.string, self.normal_form, self.token_type)
    
def tagging(file): #эта функция создает словарь, где ключ - номер предложения, значение - объект класса TaggedWord
    myDict = {}
    TaggedWords = {}
    myFile = open(file, encoding='utf-8')
    for num, line in enumerate(myFile):
        for token in generator666.get_token(line):
            setdef = myDict.setdefault(num+1, [])
            setdef.append(token)
    for key in myDict.keys():
        for token in myDict[key]:
            if token.token_type is 'Alpha':
                res = parser.parse(token.string) #морфологический анализ каждого токена
                myTag = res[0].tag.POS #извлечение информации о частеречной принадлежности
                form = res[0].normal_form
                tagWord = TaggedWord(token.string, form, myTag)
                setdef = TaggedWords.setdefault(key, [])
                setdef.append(tagWord)
            if token.token_type is 'Punctuation': #приводим все варианты тире к одному виду
                if token.string == '—' or token.string == '–' or token.string == '-':
                    tagWord = TaggedWord('-', form, token.token_type)
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

def filter_text(file): #эта функция создает словарь с токенами типа NOUN, ADJF и тире
    TaggedWords = tagging(file)
    filteredWords = {}
    stopWords = []
    for key in TaggedWords.keys():
        for token in TaggedWords[key]:
            if token.token_type == 'NOUN' or token.token_type == 'ADJF' or token.string == '-':
                setdef = filteredWords.setdefault(key, [])
                setdef.append(token)
    return filteredWords
