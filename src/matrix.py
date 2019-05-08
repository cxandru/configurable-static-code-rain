import random
import functools

#fake enum
blank=0
glyph=1

##########Utility###############################

class ColorHSB:
    #h :: Int, s, b :: Float ∈[0,1]
    def __init__(self, h, s, b):
        self.h = h
        self.s = s
        self.b = b

#we don't check if the maximum value is exceeded.
def brighten(amount,color):
    return ColorHSB(color.h, color.s, color.b+amount)

def markov2(p11, p22, initial_state):
    '''Transition application of markov chain w/ two states, blank and glyph.'''
    if initial_state == blank:
        if random.random() <= p11:
            return blank
        else:
            return glyph
    else:
        if random.random() <= p22:
            return glyph
        else:
            return blank


#The 'glyphs' are just latex mathmode strings.
class Glyph:
    def __init__(self, symbol, color):
        self.symbol=symbol
        self.color=color
    def __str__(self):
        '''
        the output requires the latex package xcolor to be displayed.
        '''
        colorSurround = "\color[Hsb]{{{:d}, {:.2f}, {:.2f}}}".format(
            self.color.h, self.color.s, self.color.b
            )
        return "{{ {:s} {:s} }}".format(colorSurround, self.symbol)


#################Business Logic####################################

def populateSeq(length, markov, symbols, baseColor, colorChange):
    '''
    generates a sequence of glyphs from the given inputs. colorChange is wrapped around the array
    modulo. It is applied for every glyph above any glyph bordering on a blank (chain head).
    '''
    #we first use a markov chain to mark the spots that should contain glyphs. Then we reiterate over the array: find the first blank, go back one step, then retreat from there, colouring the glyphs as you go. 
    marks = []
    state = glyph #start with glyphs
    firstM = None #instead of a separate bool flag
    for i in range(length):
        state = markov(state)
        if not firstM and state == blank:
            firstM = i #need this to start our pass later
        marks.append(state)
        
    if not firstM: #if there was no blank, make the chain end at the bottom.
        firstM = length-1

    column_string_seq = [None]*length #need to init bc we need indexed access from firstM on
    cur_colr = baseColor
    for i in range(length):#iterate backward.
        pos = firstM - i #start from the first blank position
        if marks[pos] == blank:
            cur_colr = baseColor #reset to chain head color
            column_string_seq[pos] = ""
        else: 
            symbol = random.choice(symbols)
            column_string_seq[pos] = str(Glyph(symbol, cur_colr))
            cur_colr = colorChange(cur_colr)
    return column_string_seq

    
def gen(rows, cols, markov, symbols, baseColor, colorChange):
    '''generates a latex matrix in inline math from the given info.'''
    col_arr=[populateSeq(rows, markov, symbols, baseColor, colorChange)
             for _ in range(cols)]
    
    bgStr="\\(\\arraycolsep=0em\\def\\arraystretch{1}\n \\begin{array}{"+"c"*cols+"}"+"\n"
    #\( begins mathmode, the colsep/stretch are so that the glyphs are packed without v/h buffer space
    endStr="\n\\end{array}\\)"#\) terminates mathmode
    row_arr=map(list, zip(*col_arr)) #transposes list of lists. See https://stackoverflow.com/questions/6473679/transpose-list-of-lists
    return bgStr + "\\\\\n".join([" & ".join(line) for line in row_arr]) + endStr


##########Application Specific - Substitute your own values here##################
chain_end_color=ColorHSB(201,1,0.2)
colorChange = functools.partial(brighten, 0.05) #5% increase in brightness
markov = functools.partial(markov2, 0.95, 0.95) #95% chance to stay in glyph, %95% also to stay in blank - smaller percentages mean shorter continuous chains. These values produce the file in the example/ dir.
symbols=["\\forall", "\\exists", "\\in", "\\wedge", "\\vee", "f", "g","\\sigma", "\\phi", "\\varepsilon", "\\delta", "\\nexists", "\\circ", "\\mathbb{R}", "\\mathbb{N}", "\\mathbb{Z}", "\\mathbb{Q}","\\mathbb{C}","K", "\\mathcal{L}", "G", "E_n", "e", "\\simeq", "\\sim", "\\trianglelefteq", "\\sum", "a_n", "\\times", "\\mathcal{P}", "\\emptyset", "\\mathcal{N}", "\\prod", "\\cap", "\\cup", "\\mathfrak{G}", "\\subseteq", "\\notin", "q", "=", "\\nu", "\\Omega", "\\partial", "\int", "\\mathfrak{S}", "\\mathfrak{P}", "\\infty"]

def main(): 
    print(gen(50,38,markov, symbols, chain_end_color, colorChange))

if __name__ == '__main__':
    main()
