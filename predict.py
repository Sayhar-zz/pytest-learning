#! /usr/bin/env python

import pdb
import itertools
import json

# Types:
#i.   first_name_dot_last_name
#ii.  first_name_dot_last_initial
#iii. first_initial_dot_last_name
#iv   first_initial_dot_last_initial


# Since this is read from a json file, it is much easier
# to non-destructively modify the trainingdata during a test.
# I've done 1 test doing so as a proof of concept.
# Check out test_jsonload in test_predict.py
with open("training.json") as f:
    ff = f.read()
    TRAININGDATA = json.loads(ff)

PATTERNS = {
    "i" : lambda first, last: first + '.' + last,
    "ii" : lambda first, last: first + '.' + last[0],
    "iii" : lambda first, last: first[0] + '.' + last,
    "iv" : lambda first, last: first[0] + '.' + last[0],
    }

######
######
###### Simple Helpers
######
######

def propose(first, last, pattern):
    """
        Given a name and pattern, 
        show what email address would look like using that pattern

    """
    return PATTERNS[pattern](first, last)


def firstlast(name):
    """ 
    Given a string that is a name, 
    return a cleaned and lowercased first and last name.

    Note -- While we clean up a few honorifics (Dr., Jr. Sr.), it's just a proof of concept.
    """

    #Obviously you could make more intelligent rules to replace other patterns. 
    #   "PhD", "Esq", etc. But how you have a proof of concept
    name = name.lower().replace("jr.", '').replace("sr.", "").replace("dr.", "")
    name = name.strip().replace("  ", " ")
    
    # Below is a safer way to write this:  firstname, lastname = name.split(" ")    
    names = name.split(" ")
    firstname, lastname = clean(names[0]), clean(names[-1])
    return firstname, lastname



def clean(name):
    """
    Given a first or last name,
    Return a version after removing strange characters and converting to lowercase.
    """
    return name.lower().replace("'",'').replace("-", '')

def return_training(domain):
    """
        Given a domain name, return a training set associated with that domain name
    """
    try:
        return TRAININGDATA[domain]
    except: 
        return -1

######
######
###### More complex helpers
######
######


def match(name, mail, pattern):
    """ Does the name/email combination match the given pattern?
    Note -- assumes names are in format "First Last", 
            # no nicknames, no prefixes
            # Middle names dropped
    """

    firstname, lastname = firstlast(name)
    #compose email address from name according to pattern:
    proposed = propose(firstname, lastname, pattern)
    if mail.count("@") != 1:
        #This means there's the wrong number of @ signs in the email. 
        #Error -- bad input
        return False 

    actual = mail.partition("@")[0]
    return True if proposed == actual else False


def find_matches(training):
    """
        Given all the training data we have, 
        Return an array matches such that
            matches[i-1] = the number of times our training data matched pattern i
        Later, we'll figure out which pattern had the most matches, and then choose it.
    """
    allpatterns = PATTERNS.keys()
    matches = {key: 0 for key in allpatterns}

    for name, pattern in itertools.product(training, allpatterns):
        email = training[name]
        #for each type of pattern:
        ismatch = match(name, email, pattern )
        if ismatch:
            matches[pattern] = matches[pattern] + 1
    return matches

def choose_best_match(matches_distribution):
    """
        Given a dict that shows the distribution of how well 
        different patterns performed on the training data:

        Find and return the winning pattern 
        Also return "if there is a tie" (repeats)
        Also return the number of matched 

    """
    max_matches = 0
    total = 0
    repeats = False
    winner = None
    for pattern in matches_distribution:  
        #For this pattern, how many matches were there?    
        num_matches = matches_distribution[pattern]
        total += num_matches
        if num_matches > max_matches:
            #We have a new winning pattern!
            max_matches = num_matches
            winner = pattern
            repeats = False
        elif num_matches == max_matches:
            #We have a repeat!
            repeats = True
        else:
            #This is an inferior pattern
            pass

    if(total == 0):
        max_percent = 0
    else:
        max_percent = float(max_matches) / float(total)
        max_percent = round(max_percent, 5) 
    #The 5 is arbitrary -- we are rounding to prevent floating point errors
    return winner, max_percent, repeats


######
######
###### The main function
######
######


def predict(name, domain):
    """
    Given a full name & domain, guess the email address associated with it.

    The approach:
        1. Find a training set of all emails on file in that domain
        2. See which of the 4 general patterns matches the training set best.
        2b. (If there is a tie, then return an error)
        3. Apply the winning pattern to the data to guess an email address

    """

    #Get the training set of all email addresses in the relevant domain.
    training = return_training(domain)

    if training == -1:
        return "Unknown. No email address with that domain in our records."

    #Number of matches per pattern:
    matches_distribution = find_matches(training)
    winner, max_percent, repeats = choose_best_match(matches_distribution)
    
    if max_percent == 0:
        #We have no data on this domain that matches one of the 4 known patterns.
        return "Unknown. Not enough training data."

    if repeats == True:
        #This means there are at least 2 patterns with equal # of matches
        # Error!
        return "Unknown. There are at least 2 equally compelling candidates"
    
    firstname, lastname = firstlast(name)
    proposed = propose(firstname, lastname, winner)

    return proposed +"@"+domain



if __name__ == "__main__":
    loop = True
    while(loop):
        print("Type quit at any time to exit")

        name = input("Full name of person: ")
            
        if name.lower().strip() == "quit":
            print("See you!")
            break
            loop = False #This won't be needed. This is just a safety net to prevent infinite loops

        domain = input("Domain of email address: ")
        if domain.lower().strip() == "quit":
            print("See you!")
            break
            loop = False

        print(predict(name, domain))
        
            
