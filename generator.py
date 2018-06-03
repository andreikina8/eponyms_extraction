from token1 import Token
from token1 import AlphaValue
from token1 import NumericValue
from token1 import SpaceValue
from token1 import PuncValue
from token1 import UnknownValue
import unicodedata
def get_token(t):
    #first_token = 0
    first_alpha = 0
    first_num = 0
    first_space = 0
    first_punc = 0
    in_punc = False
    in_space = False
    in_alpha = False
    in_num = False
    first_unknown = 0
    in_unknown = False
    #in_token = False    
    #array1 = []    
    for x, y in enumerate(t):
        if y.isalpha():
            if in_alpha:
                continue
            else:
                first_alpha = x
                in_alpha = True
        else:
            if in_alpha:
                if t[first_alpha:x].isalpha():
                    tokenAlpha = AlphaValue(t[first_alpha:x], first_alpha)
                    #array1.append(tokenAlpha)
                    yield tokenAlpha
                    in_alpha = False
        if y.isdigit():
            if in_num:
                continue
            else:
                first_num = x
                in_num = True
        else:
            if in_num:
                if t[first_num:x].isdigit():
                    tokenNum = NumericValue(t[first_num:x], first_num)
                    #array1.append(tokenNum)
                    yield tokenNum
                    in_num = False
        if y.isspace():
            if in_space:
                continue
            else:
                first_space = x
                in_space = True
        else:            
            if in_space:
                if t[first_space:x].isspace():
                    tokenSpace = SpaceValue(t[first_space:x], first_space)
                    #array1.append(tokenSpace)
                    yield tokenSpace
                    in_space = False
        if unicodedata.category(y)[0] == 'P':
            if in_punc:
                continue
            else:
                first_punc = x
                in_punc = True
        else:
            if in_punc:
               # if unicodedata.category(t[first_punc:x])[0] == 'P':
                tokenPunc = PuncValue(t[first_punc:x], first_punc)
                #array1.append(tokenPunc)
                yield tokenPunc
                in_punc = False
        if y.isalpha() == False and y.isdigit() == False and y.isspace() == False and unicodedata.category(y)[0] != 'P':
            if in_unknown:
                continue
            else:
                first_unknown = x
                in_unknown = True
        else:
            if in_unknown:
               # if y.isalpha() == False and y.isdigit() == False and y.isspace() == False and unicodedata.category(y)[0] != 'P':
                tokenUnknown = UnknownValue(t[first_unknown:x], first_unknown)
               #array1.append(tokenUnknown)
                yield tokenUnknown
                in_unknown = False
                
    if in_alpha:
        if t[first_alpha:].isalpha():            
            tokenAlpha = AlphaValue(t[first_alpha:], first_alpha)
            yield tokenAlpha
    if in_num:
        if t[first_num:].isdigit():            
            tokenNum = NumericValue(t[first_num:], first_num)
            yield tokenNum
    if in_space:
        if t[first_space:].isspace():            
            tokenSpace = SpaceValue(t[first_space:], first_space)
            yield tokenSpace
    if in_punc:
        print(t[first_space:])
        if unicodedata.category(t[first_space:])[0] == 'P':            
            tokenPunc = PuncValue(t[first_punc:], first_punc)
            yield tokenPunc
    if in_unknown:
        #if y.isalpha() == False and y.isdigit() == False and y.isspace() == False and unicodedata.category(y)[0] != 'P':            
        tokenUnknown = UnknownValue(t[first_unknown:], first_unknown)
        yield tokenUnknown
    
