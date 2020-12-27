# import pygraphviz as pgv
from pprint import pprint
from random import choice as rchoice
import xml.etree.ElementTree as ET
from xml.dom import minidom

number = int(input ("Enter NUMBER: "))
base = int(input ("Enter BASE of number system: "))

def baseN(n, b, syms="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    """ converts a number `n` into base `b` string """
    return ((n == 0) and syms[0]) or (
        baseN(n//b, b, syms).lstrip(syms[0]) + syms[n % b])

def divided_by_N(number, base):
    """
    constructs DFA that accepts given `base` number strings
    those are divisible by a given `number`
    """
    ACCEPTING_STATE = START_STATE = '0'
    SYMBOL_0 = '0'
    dfa = {
        str(from_state): {
            str(symbol): 'to_state' for symbol in range(base)
        }
        for from_state in range(number)
    }
    dfa[START_STATE][SYMBOL_0] = ACCEPTING_STATE
    # `lookup_table` keeps track: 'number string' -->[dfa]--> 'end_state'
    lookup_table = { SYMBOL_0: ACCEPTING_STATE }.setdefault
    for num in range(number * base):
        end_state = str(num % number)
        num_s = baseN(num, base)
        before_end_state = lookup_table(num_s[:-1], START_STATE)
        dfa[before_end_state][num_s[-1]] = end_state
        lookup_table(num_s, end_state)
    return dfa

##################################################################
    
def print_transition_table(dfa):
    global number
    f = open('transitions_' + str(number) + '.txt', "w")
    pprint(dfa, stream=f)
    f.close()
    pprint(dfa)
    # print(dfa['3']['1']) 
###############XML##################################

    # automaton = minidom.Document()
    structure = minidom.Document()
    xml = structure.createElement("structure")
    structure.appendChild(xml)
    type = structure.createElement("type")
    type_text = structure.createTextNode("fa")
    type.appendChild(type_text)
    xml.appendChild(type)
    automaton = structure.createElement("automaton")
    xml.appendChild(automaton)

    for i in range(number):
        state_ = structure.createElement("state")
        state_.setAttribute('name','q0')
        state_.setAttribute('id','0')
        # automaton.appendChild(state_)
        X_ = structure.createElement("x")
        Y_ = structure.createElement("y")
        X_text = structure.createTextNode('0.0')
        Y_text = structure.createTextNode('0.0')
        X_.appendChild(X_text)
        Y_.appendChild(Y_text)
        automaton.appendChild(state_)
        state_.appendChild(X_)
        state_.appendChild(Y_)
        if(i == 0):
            initial_ = structure.createElement("initial")
            final_ = structure.createElement("final")
            state_.appendChild(initial_)
            state_.appendChild(final_)

    for i in range(number*2):
        transition_ = structure.createElement("transition")
        # automaton.appendChild(transition_)
        automaton.appendChild(transition_)
        from_ = structure.createElement("from")
        to_ = structure.createElement("to")
        read_ = structure.createElement("read")
        transition_.appendChild(from_)
        transition_.appendChild(to_)
        transition_.appendChild(read_)
        
    save_path_file = "gfg.xml"
    
    xml_str = structure.toprettyxml(indent="\t")

    with open(save_path_file, "w") as f: 
        f.write(xml_str)  
    

##############################################################3    
    # tree = ET.parse(str(number)+'.xml')
    tree = ET.parse('gfg.xml')
    root = tree.getroot()

    numArr = []
    for i in range(number):
        numArr.append(i)
    count = 0
    for state in root.iter('state'):
        state.set('id',str(count))
        state.set('name','q'+str(count))
        count += 1
####################################################
    
    transgenderList = []
    for FromState,transgender in dfa.items():
        for Char,toState in transgender.items():
            myList = []
            myList.append(FromState)
            myList.append(Char)
            myList.append(toState)
            transgenderList.append(myList)
    # print(transgenderList)
#output transitions in ascending order
    newListTrans = transgenderList.copy()
    newListTrans.sort()
    f = open(str(number) + '_sorted.txt', 'w')
    pprint(newListTrans, stream=f)
    f.close()
    # print(newListTrans)
        
####################################################
    k=0

    for trans in root.iter('transition'):
        for From in trans.iter('from'):
            From.text = str(transgenderList[k][0])
        
        for to in trans.iter('to'):
            to.text = str(transgenderList[k][2])
        
        for read in trans.iter('read'):
            read.text = str(transgenderList[k][1])
        k += 1
      

    tree.write('output_' + str(number) + '.jff')

# if __name__ == "__main__":

dfa = divided_by_N(number, base)

print_transition_table(dfa)
