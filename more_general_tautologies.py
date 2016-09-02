"""
Program to find the most general tautologies with the same bracket type
"""

#test_wff = raw_input("Please input a wff to generalize:")

def variable_count(formula):
    """
    Determines the number of distinct variables in a formula
    """
    variable_counter_list = ['C', 'K', 'A', 'E', 'D', 'N']
    variable_counter = 0
    for letter in formula:
        if not(letter in variable_counter_list):
            variable_counter +=1
            variable_counter_list.append(letter)
    return variable_counter
               
def test_empty():
    """
    Empty test for the variable_count function
    """
    return variable_count('') == 0
        
def test_single():
    """
    Single variable test for the variable_count function
    """
    return variable_count('p') == 1
    
def test_no_repeat():
    """
    No repetition test for the formula
    """
    return variable_count('Cpq') == 2
    
def test_repeat():
    """
    Repetition test for the formula
    """
    return variable_count('Cpp') == 1
    
def test_multi():
    """
    Test for multiply connectives
    """
    return variable_count('CpCqr')

def binary_converter(number):
    """
    Converts a number to binary as a string
    """
    # start with an empty string, a reversed string, and a counter
    string = ''
    reversed_string = ''
    counter = -1
    while True:
        if number == 0:
            return '0'
        elif number // 2 == 0:
            # add a 1 to the string and reverse it and return that
            string += str(1)
            number = 0
            for number in range(len(string)):
                reversed_string += string[counter]
                counter -= 1
            return reversed_string
        else:
            # add the remainder to the string and update the number
            string += str(number % 2)
            number = number // 2
            
def bin_convert_test1():
    return binary_converter(0) == '0'
    
def bin_convert_test2():
    return binary_converter(1) == '1'
    
def bin_convert_test3():
    return binary_converter(2) == '10'
    
def bin_convert_test4():
    return binary_converter(3) == '11'
    
def bin_convert_test5():
    return binary_converter(6) == '110'
    
def bin_convert_test6():
    return binary_converter(5) == '101'
            
def bit_list(integer, elements = 2):
    """
    Given a non-zero integer returns an n-ary list of all of the bits
    which have length of the integer, which defaults to bit strings in ['0', '1']
    """
    if integer == 0:
        return []
    element_list =[]
    for element in range(elements):
        element_list.append(str(element))
    if integer == 1:
        return element_list
    else:
        bit_start = bit_list(integer - 1, elements)
        new_bit_list = []
        for element in bit_start:
            for num_string in element_list:
                clone = element[:]
                clone += num_string
                new_bit_list.append(clone)
        return new_bit_list
        
def bit_list_test1():
    return bit_list(0) == []
    
def bit_list_test2():
    return bit_list(1) == ['0', '1']
    
def bit_list_test3():
    return bit_list(2) == ['00', '01', '10', '11']
    
def bit_list_test4():
    return bit_list(3) == ['000', '001', '010', '011', '100', '101', '110', '111']
    
def bit_list_test5():
    return bit_list(1, 3) == ['0', '1', '2']
    
def bit_list_test6():
    return len(bit_list(2, 4)) == 16
    
def needed_tests(wff):
    """
    Find all number strings needed to test, the numbers are strings in a list
    """
    # find the number of possibilities needed to test
    possibilities = 2 ** variable_count(wff)
    number_list = []
    # find all numbers in "binary" notation 
    for number in range(possibilities):
        number = binary_converter(number)
        listed = list(number)
        # correct all numbers which don't have the appropriate length
        while len(number) < len(binary_converter(possibilities - 1)):
            listed.insert(0, str(0))
            number = listed
        number = listed
        number_list.append(number)
    return number_list
    
def Polish(wff):
    """ 
    Determines whether or not is in Polish notation
    """
    counter = 1
    length_counter = 0
    while length_counter < len(wff):
    # The variable letter keeps track of the letters input and updates the counters 
        letter = wff[length_counter]
        if letter in 'CAKED':
            counter += 1 
        elif letter == 'N':
            counter += 0
        else:
            counter -= 1  
        length_counter += 1
        if (counter == 0 and length_counter != len(wff)) or (counter > 0 and length_counter == len(wff)) or (counter < 0):
            return False
    return True
    
def evaluate_wff(num_wff):
    """
    Evaluates a wff by pushing and popping
    """
    # if it's not a numerical wff just return the original wff
    for character in num_wff:
        if not(character in 'CAKEDN01') and Polish(num_wff) == False:
            return num_wff
    replace_dict = {'C00':'1', 'C01':'1', 'C10':'0', 'C11':'1',
                    'D00':'1', 'D01':'1', 'D10':'1', 'D11':'0',
                    'K00':'0', 'K01':'0', 'K10':'0', 'K11':'1',
                    'A00':'0', 'A01':'1', 'A10':'1', 'A11':'1',
                    'E00':'1', 'E01':'0', 'E10':'0', 'E11':'1',
                    'N0':'1', 'N1':'0'}
    # reverse the wff and iterate over the wff
    reversed_wff = num_wff[::-1]
    stack = []
    # for each letter if it's an operand push onto the stack
    for letter in reversed_wff:
        if letter in '01':
            stack.insert(0, letter)
    # if it's a unary operator then pop operand1 off the stack
        elif letter == 'N':
            popped_1 = stack.pop(0)
    # compute N operand1 and push it onto the stack
            replace_string = letter + popped_1
            replace_number = replace_dict[replace_string]
            stack.insert(0, replace_number)
    # if it's a binary operator X pop operand1 and operand2 off of the stack
    # and push X(operand1, operand2) onto the stack
        elif letter in 'CAKED':
            popped_1 = stack.pop(0)
            popped_2 = stack.pop(0)
            replace_string = letter + popped_1 + popped_2
            replace_number = replace_dict[replace_string]
            stack.insert(0, replace_number)
    # return the result of the stack
    truth_dict = {'0':False, '1':True}
    return truth_dict[stack[0]] 
    
def tautology_tester(wff):
    """
    Tests a wff to see if it is a tautology or not
    """
    # find all possibilities needed to test
    test_list = needed_tests(wff)
    build_test_list = []
    # clone the wff
    wff_clone = ''
    listed = list(wff)
    for letter in listed:
        wff_clone += letter
    # replace the cloned version of the wff appropriately for testing
    for test_variables in test_list:
        # reset the wff and the variable counter list and the counter
        counter = 0
        wff = wff_clone
        variable_counter_list = ['C', 'K', 'A', 'E', 'D', 'N']
        for letter in wff:
            if not(letter in variable_counter_list):
                wff = wff.replace(letter, test_variables[counter])
                counter += 1
                variable_counter_list.append(letter)
        build_test_list.append(wff)
    # test each possibility if any possibility fails return False, otherwise return True
    for wff_object in build_test_list:
        if evaluate_wff(wff_object) == False or Polish(wff_object) == False:
            return False
    return True
    
def add_var(string):
    """
    Adds the variable after the maximum variable in the string
    """
    var_dict = {'p':'q', 'q':'r', 'r':'s', 's':'t', 't':'u', 'u':'v', 'v':'w', 'w':'x', 'x':'y', 'y':'z',
    'z':'a', 'a':'b', 'b':'c', 'c':'d', 'd':'e', 'e':'f', 'f':'g', 'g':'h', 'h':'i', 'i':'j', 'j':'k', 'k':'l', 'l':'m', 'm':'n', 'n':'o', 'o':'p'}
    letter = 'a'
    # find the greatest variable and then add the next variable to the string
    for var in string:
        if var > letter:
            letter = var
    string += var_dict[letter]
    return string
    
def add_list(string):
    """
    Finds the list of variables need to added for the current step
    """
    string_list = []
    string_variable = 'pqrstuvwxyzabcdefghijklmno'
    add_list_end = add_var(string)[-1]
    # number of elements to add
    element_spot = string_variable.find(add_list_end) + 1
    for element in range(element_spot):
        string_list.append(string_variable[element])
    return string_list

def next_strings(string):
    """
    Appends all possible next letters to the string and returns a list of
    these possibilites
    """
    final_list =[]
    # find the possibile letters which can get added and add them
    var_list = add_list(string)
    for element in var_list:
        add_this = string + element
        final_list.append(add_this)
    return final_list
    
def var_list(number):
    """
    Find all possible variable combinations needed to test
    """
    final_list = []
    if number == 1:
        return ['p']
    else:
        # take the previous list and for each member in the list append
        # every member of the next_string_list
        var_list_var = var_list(number - 1)
        for string in var_list_var:
            next_string_list = next_strings(string)
            for string2 in next_string_list:
                final_list.append(string2)
        return final_list
        

def wff_list(wff):
    """
    Given a wff it finds the list of wffs which have the same bracket type
    """
    # find the number of variable spots in the wff 
    var_counter = 0
    connective_list = ['C', 'K', 'A', 'E', 'D', 'N']
    for letter in wff:
        if not(letter in connective_list):
            var_counter += 1
    # generate the variable list via that number
    variable_list = var_list(var_counter)
    # find the most general wff
    most_general_wff = ''
    join_counter = 0
    for letter in wff:
        if letter in connective_list:
            most_general_wff += letter
        else:
            most_general_wff += variable_list[-1][join_counter]
            join_counter += 1
    # substitute each variable in the most general wff
    clone = most_general_wff[:]
    return_list = []
    for string in variable_list:
        most_general_wff = clone
        letter_counter = 0
        for letter in clone:
            if not(letter in connective_list):
                most_general_wff = most_general_wff.replace(letter, string[letter_counter])
                # append each of those wffs to a wff-list and return it           
                letter_counter += 1
        return_list.append(most_general_wff)
    return return_list
    
def taut_list_test(wff):
    """
    given a wff this tests all wffs with the same bracket type
    and returns the tautologies
    """
    # call wff_list and then test every member of it using filter
    test_list = wff_list(wff)
    tautology_list = filter(tautology_tester, test_list)  
    return tautology_list
    
#print "tautology list:", taut_list_test(test_wff)
#print "number of more general wffs which are tautologies:", len(taut_list_test(test_wff)) - 1

def unify(wff_1, wff_2):
    """
    Checks to see if two wffs unify
    """
    pass
    
def reletterer(wff):
    """ 
    reletters a wff with p-z letters to a-k letters
    """
    letter_dict = {'C':'C', 'D':'D', 'E':'E', 'K':'K', 'A':'A', 'N':'N',
    'p':'a', 'q':'b', 'r':'c', 's':'d', 't':'e', 'u':'f', 'v':'g',
    'w':'h', 'x':'i', 'y':'j', 'z':'k'}
    relettered = ''
    for letter in wff:
        relettered += letter_dict[letter]
    return relettered
   
def bracket_subsume(wff_1, wff_2):
    """
    Checks to see if wff_1 subsumes wff_2 or if wff_2 subsumes wff_1 or neither
    returns whichever wff is most general if one exists, when they are of
    the same bracket type
    """
    # reletter each wff and see if we can get the other one by substitution
    reletter_wff1 = reletterer(wff_1)
    for letter_pos in range(len(reletter_wff1)):
        reletter_wff1 = reletter_wff1.replace(reletter_wff1[letter_pos], wff_2[letter_pos])
    reletter_wff2 = reletterer(wff_2)
    for letter_pos in range(len(reletter_wff2)):
        reletter_wff2 = reletter_wff2.replace(reletter_wff2[letter_pos], wff_1[letter_pos])
    if reletter_wff1 == wff_2:
        return wff_1
    elif reletter_wff2 == wff_1:
        return wff_2
    else:
        return 'neither' 
    
def more_general_wff_list(wff):
    """
    Finds all more general tatuologies of a given tautology
    """
    # find all tautologies with the same bracket type
    tautologies = taut_list_test(wff)
    # if any member of the tautology list subsumes the given wff put it on the
    # return list
    more_general_list = []
    for formula in tautologies:
        if bracket_subsume(formula, wff) == formula:
            more_general_list.append(formula)
    return more_general_list
    
def most_general_wff_list(wff):
    """
    Finds all most general tautologies of a given wff
    """
    # find the more general list
    more_general = more_general_wff_list(wff)
    # if any member of the more general list subsumes a second member
    # and they are not equal, put it on a delete list
    delete_list = []
    for formula in more_general:
        for formula2 in more_general:
            if bracket_subsume(formula, formula2) == formula \
            and formula != formula2 \
            and not(formula2 in delete_list):
                delete_list.append(formula2)
    # delete all members from a clone of the more general list and return it
    clone = more_general[:]
    for formula in more_general:
        if formula in delete_list:
            clone.remove(formula)
    return clone

print most_general_wff_list('CpCpp')
print more_general_wff_list('CKNNpNqp')    
    
def var_spots(wff):
    """
    Takes a wff and returns the most distinct wff with the same bracket type
    """
    connective_string = 'CAKEDN'
    distinct_wff = ''
    variable_string = 'pqrstuvwxyzabcdefghijklmno'
    var_counter = 0
    for element in wff:
        if not(element in connective_string):
            distinct_wff += variable_string[var_counter]
            var_counter += 1
        else:
            distinct_wff += element
    return distinct_wff

def variables(wff):
    """
    returns a list of all the variables in a wff
    """
    connective_string = 'CAKEDN'
    variables = []
    for letter in wff:
        if not(letter in connective_string):
            variables.append(letter)
            connective_string += letter
    return variables  
            
def parenthesize(wff):
    """
    parenthesizes a wff in Polish notation
    """
    # put all variables into a wff_list
    wffs = variables(wff)            
    # make a list of the wff
    wff_list = list(wff)
    while len(wff_list) > 1:
    # initialize some variables for this run of the loop
        parenthesized_list = []
        index_list = []
        new_level_list = []
        ignore_list = []
        parenthesized_counter = 0
        clone = wff_list[:]
        for number in range(len(wff_list)):        
            if wff_list[number] in 'CAKED' and wff_list[number + 1] in wffs \
            and wff_list[number + 2] in wffs: 
                parenthesized = wff_list[number] + '(' +  wff_list[number + 1] \
                + ',' + wff_list[number + 2] + ')'
                parenthesized_list.append(parenthesized)
    # append parenthesized found to a clone of the wff_list for the next level
                clone.append(parenthesized)
            # store the indexes of the spot where the connective is 
                index_list.append(number)
                ignore_list.append(number + 1)
                ignore_list.append(number + 2)
            elif wff_list[number] == 'N' and wff_list[number + 1] in wffs:
                parenthesized = wff_list[number] + '(' + wff_list[number + 1] \
                + ')'
                parenthesized_list.append(parenthesized)
                clone.append(parenthesized)
                index_list.append(number)
                ignore_list.append(number + 1)
        # build the list of the current level
        for number in range(len(wff_list)):
            if not(number in index_list) and not(number in ignore_list):
                new_level_list.append(wff_list[number])
            elif not(number in ignore_list):
                new_level_list.append(parenthesized_list[parenthesized_counter])
                parenthesized_counter += 1
    # reset the wff_list for the next level and update the wffs
        for wff in parenthesized_list:
            wffs.append(wff)
        wff_list = new_level_list
    return wff_list[0]

def subwff(wff):
    """
    Finds all subwffs of a wff
    """
# iterate through the wff and put each wff which corersponds to that letter on the subwff_list
    subwff_list = []
    subwff_list2 = []
    wff_list = list(wff)
    for dummy_index in range(len(wff)):
        counter = 0
        subwff_string = ''
        for letter in wff_list:
# put each letter in the wff_list into the string until the counter reaches 0 and it is variable
            if counter >= 0:
                subwff_string += letter
                if letter in ['C', 'A', 'K', 'E', 'D']:
                    counter += 1 
                elif letter == 'N':
                    counter += 0
                else:
                    counter -= 1
        subwff_list.append(subwff_string)
        wff_list.pop(0)
## create a second list which only stores non-duplicates and return it
    for wff in subwff_list:
       if not(wff in subwff_list2):
            subwff_list2.append(wff)
    return subwff_list2
    
def organic(wff):
    """
    Determines whether or not a wff is organic
    """
# Find all subformulas for the current wff and filter each of them
    subwff_list = subwff(wff)
    subwff_tautologies = filter(tautology_tester, subwff_list)
# If any tautologies do not exist in the subformula add it to the organic list
    if len(subwff_tautologies) == 1:
        return True
    else:
        return False

def wff_list_tester(function, wff_list):
    """
    Tests all wffs on the wff list for a property which the function evaluates
    and returns those that satisfy it
    """
    return filter(function, wff_list) 
    
def bracket_types(length, prinicipal_connective = 'C'):
    """
    Given a length and a principal binary connective this returns all
    bracket_types of the given length in a list
    """
    bracket_type_list = []
    # access the bit_list and use '1' for connective symbols and '0' for 
    # variable spots
    bit_listed = bit_list(length)
    symbol_dict = {'0':'x', '1':prinicipal_connective,}
    for bit_string in bit_listed:
        bracket_type = ''
        if bit_string[0] == '1' and bit_string[-1] == '0' and \
        bit_string[-2] == '0' and bit_string.count('1') + 1 == bit_string.count('0'):
            for bit in bit_string:
                bracket_type += symbol_dict[bit]
            if Polish(bracket_type) == True:
                bracket_type_list.append(bracket_type)
    return bracket_type_list
    
def N_bracket_types(length, prinicipal_connective = 'C'):
    """
    Given a length and a principal binary connective this returns
    all bracket types of the given length with N in a list, where C is the 
    principal connective and N is not in the 2nd (index of 1 instead of 0) 
    spot in the wff
    """
    bracket_type_list = []
    bit_listed = bit_list(length, 3)
    symbol_dict = {'0':'x', '1':prinicipal_connective, '2':'N'}
    for bit_string in bit_listed:
        bracket_type = ''
        # first three elements of bit_string
        first_three = bit_string[0:3]
        if bit_string[0] == '1' and bit_string[-1] == '0' \
        and bit_string[1] != '2' and first_three != '112tat':
            for bit in bit_string:
                bracket_type += symbol_dict[bit]
            if Polish(bracket_type) == True and 'N' in bracket_type:
                bracket_type_list.append(bracket_type)
    return bracket_type_list

def all_taut_length(length, connective = 'C'):
    """
    returns all tautologies of a given length by their bracket type for a single
    connective
    """
    # get the bracket_type list
    # get the list of all tautologies for each element in that bracket_type
    bracket_list = bracket_types(length, connective)
    taut_list = []
    for wff in bracket_list:
        taut_wff_list = taut_list_test(wff)
        if taut_wff_list != []:
            taut_list.append(taut_wff_list)
    return taut_list
    
def all_most_general(length, connective = 'C'):
    """
    given a length returns all most general wffs for a single connective
    """
    bracket_list = bracket_types(length, connective)
    most_general_list = []
    for wff in bracket_list:
        most_general_class = most_general_wff_list(wff)
        if most_general_class != []:
            most_general_list.append(most_general_class)
    return most_general_list
    
def all_most_general_CN(length):
    """
    given a length returns all most general C-N wffs where C is the principal
    connective.
    """
    bracket_list = N_bracket_types(length)
    most_general_list = []
    for wff in bracket_list:
        most_general_class = most_general_wff_list(wff)
        if most_general_class != []:
            most_general_list.append(most_general_class)
    return most_general_list
    
    
def number_most_general(length, connective = 'C'):
    """
    gets the number of a most_general class of classes of a given length
    """
    all_most_general_list = all_most_general(length, connective)
    counter = 0
    for bracket_class in all_most_general_list:
        for wff in bracket_class:
            counter += 1
    return counter
    
def model_tester(wff_1, wff_2, rule):
    """
    Given a model and a wff, this tests to see if the wff always evaluates
    to a designated_value
    """
    pass
    
    
def model_tester_1(model, taut_1, taut_2):
    """
    Tests a given model to see if two tautologies evaluate to the same value
    """
    pass
    
class Wff:
    """
    class for tautologies
    """
    def __init__(self, string):
        """
        Initializes a string as a wff
        """
        assert Polish(string)
        #self._string = string
        #if Polish(self._string) == False:
         #   print "This is not a wff in Polish notation." 
            
def prove(wff):
    """
    Formally proves that a string is a wff by the rules of formation
    """
    # find all variables in the wff and place them into a list
    proved_list = []
    for letter in wff:
        if letter in 'abcdefghijklmnopqrstuvwxyz':
            proved_list.append(letter)
    # clone the list
    new_list = proved_list[:]
    # Compute all N-wffs of that formula and put them into the clone
    # Compute all C-wffs of that formula and put them into the clone
    # Check to see if the wff is in the clone list
    # halt the loop if every computed consequence in the new list is longer than the wff
    
# more_general_wff_list(wff)

#wff_listed = ['CxCyx', 'CCxCyzCCxyCxz', 'CCNxyCCNxNyx', 'CCxyCNyNx', 'CNNxx', 'CxNNx']

#for wff in wff_listed:
#   print Polish(wff), wff
#    if not(Polish(wff)):
#        print wff, ' is not in Polish notation.'
        
#for wff in wff_listed:
#    print 'P(' + parenthesize(wff) + ').'
    
#for wff in wff_listed:
#    print 'weight(P(' + parenthesize(wff) + '), 1).'

def deparenthesize(wff):
    """ Removes parentheses from a wff    """
    new_wff = ''
    for symbol in wff:
        if symbol != '(' and symbol != ')' and symbol != ',' and symbol != 'P' and symbol != '.':
            new_wff += symbol
    return new_wff
    


    





