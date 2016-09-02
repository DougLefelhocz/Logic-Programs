""" Program to compute the CoDEN number of a condensed detachment proof. """

print 'This is an assistant to help compute the CoDEN number of' 
print 'a condensed detachment proof in Polish notation.'
print 'It presumes that the inputs you give it have a most general unifier, which' 
print 'yield a most general consequent of the major premiss' 
print 'under the rule of condensed detachment.'
print 'My author wants to warn you that the function used to one-way unify'
print 'the antecedent of the major_premiss and the minor_premiss may not work.'
print "It's designed for conditionals mostly.  So, keep that in mind."
print

major_prem = raw_input('Please input the major premiss in Polish notation. ')
minor_prem = raw_input('Please input the minor premiss in Polish notation. ')

def number(string):
    """ Assigns numbers to letters. """
    for let in string:
        if let in 'abcdefghijklmnopqrstuvwxyz':
            return 1
        if let in 'CKAEDP':
            return -1
    return 0

def number_2(string):
    """ Assigns numbers to letters in 'forward' manner. """
    for let in string:
        if let in 'abcdefghijklmnopqrstuvwxyz':
            return -1
        if let in 'CKAEDP':
            return 1
    return 0

def Polish(wff):
    """ Checks a string to see if it is in Polish notation or not."""
    rever_wff = wff[::-1]
    if number(rever_wff) != 1:
        return "This is not a wff."
    counter = 1
    for letter in rever_wff[1:]:
        counter += number(letter)
        if counter == -1:
            return "This is not a wff."
    if counter == 1:        
        return True
    return "This is not a wff."
    
def Polish_check(wff_can):
    """ Checks to make sure a string is a wff. """
    if Polish(wff_can) == True:
        print wff_can + " is a wff."
        return True
    print wff_can + " is not a wff."
    
a = Polish_check(major_prem)
b = Polish_check(minor_prem)
if a != True or b != True:
    print "Please input wffs in Polish notation. "
    exit()

def left_wff(wff):
    """ Finds the left_wff of a wff """
    antecedent_start = wff[1:]
    return_wff = ''
    if Polish(wff) == True:
        for letter in antecedent_start:
            return_wff += letter
            if Polish(return_wff) == True:
                return return_wff
    return "This string is not in Polish notation. "
    
def right_wff(wff):
    """ Finds the right_wff of a wff """
    left = left_wff(wff)
    leng_left = len(left)
    return wff[leng_left + 1:]
    
def var_det(wff):
    """ Determines the number of propositional variables in a wff. """
    counter = 0
    letters_used = ''
    for letter in wff:
        if not letter in letters_used and not letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            counter += 1
            letters_used += letter
    return counter
    
def letters(wff):
    """ Returns the string of variables in a wff. """
    string = ''
    for letter in wff:
        if letter in 'abcdefghijklmnopqrstuvwxyz':
            string += letter
    return string
   
def numeral_form(wff):
   """ Reletters the wff to usable numerals if it has less than 10 letters. """
   used_var = ''
   counter = 1
   let_str = letters(wff)
   for letter in wff:
       if letter in let_str and not letter in used_var:
           wff = wff.replace(letter, str(counter))
           counter += 1
           used_var += letter
   return wff
           
def second_wff_unify(first_wff, second_wff):
    """ Unifies the first_wff with the second by substitutions in the first wff or fails, but does not have symbol clash. """
    numeraled = numeral_form(first_wff)
    len_2 = len(second_wff)
    for num in range(len_2):
        subs_wff = ''
        counter = 0
        if numeraled[num] != second_wff[num]: 
            if second_wff[num] in 'abcdefghijklmnopqrstuvwxyz':
                numeraled = numeraled.replace(numeraled[num], second_wff[num])
            spot = num
            while counter != -1:
                subs_wff += second_wff[spot]
                counter += number_2(second_wff[spot])
                spot += 1
            numeraled = numeraled.replace(numeraled[num], subs_wff)
            if numeraled[0] in 'abcdefghijklmnopqrstuvwxyz':
                return False
    if numeraled == second_wff:
        return True
    else:
        return False
        
def Coden_num(major_premiss, minor_premiss):
    """ Computes the Condensed Detachment Expansion Number of a major_premiss and a minor_premiss, if they unify. """  
    antecedent = left_wff(major_premiss)
    if antecedent == minor_premiss:
        return 1
    elif second_wff_unify(antecedent, minor_premiss) == True:
        return 2
    elif second_wff_unify(minor_premiss, antecedent) == True:
        return 2
    else:
        return 3
        
print Coden_num(major_prem, minor_prem)

def de_paren(string):
    """ Deparenthesizes a Prover9 formula. """
    new_wff = ''
    for letter in string:
        if not letter in 'P(), ':
            new_wff += letter
    return new_wff
    
print de_paren('C(C(p, q), C(N(q), r))')
print de_paren('C(C(r, s), C(C(C(t, u), v)))')





    
