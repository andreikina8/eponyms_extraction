class Token(object):
    def __init__(self, string, position):
        self.string = string
        self.position = position
        self.length = len(string)
        #self.token_type = token_type
        self.right_position = self.position + self.length
    def __repr__(self):
        if hasattr(self, "token_type") == True:
            return "%s [%s...%s]..%s" % (self.string, self.position, self.right_position, self.token_type)
        else:
            return "%s [%s...%s]" % (self.string, self.position, self.right_position)
        
class NumericValue(Token):
    token_type = "Numeric"
class AlphaValue(Token):
    token_type = "Alpha"
class SpaceValue(Token):
    token_type = "Space"
class PuncValue(Token):
    token_type = "Punctuation"
class UnknownValue(Token):
    token_type = "Unknown"

    
    
        
         
