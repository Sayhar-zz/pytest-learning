#! /usr/bin/env python3
#Sahar Massachi coding exercise for AlphaSights

import pytest
from predict import *

## Test Helper methods

def test_clean():
	assert clean("Yes") == "yes"
	assert clean("no") == "no"
	assert clean("D'nesh") == "dnesh"
	assert clean("D-nesh") == "dnesh"

def test_firstlast():
	assert firstlast( "Mary O'Hanlon") == ("mary", "ohanlon")
	assert firstlast( "John Wayne Gacy Jr.") == ("john", "gacy")
	assert firstlast( "Dr. John Watson") == ("john", "watson")
	assert firstlast("So many names, nicknames, and so on") == ("so", "on")

def test_trainingdata():
	assert return_training("apple.com")['Steve Jobs'] == "s.j@apple.com"
	assert return_training("google.com")["Larry Page"] == "larry.p@google.com"
	assert return_training("alphasights.com")["Linda Li"] != "larry.p@google.com"

def test_trainingdata_errors():
	assert return_training("bing.com") == -1


@pytest.fixture
def newtraining(request):
	#setup/teardown for test_jsonload
	#Used for easily testing our methods with different training data
	#Proof of concept
	gooddata = TRAININGDATA
	tdata = {
		"google.com" : {
	        "Sergey Brin" : "s.brin@google.com"}
	}
	def fin():
		print("replacing with good TRAININGDATA")
		TRAININGDATA = gooddata
	request.addfinalizer(fin)
	return tdata


def test_jsonload(newtraining):
	#Change TRAININGDATA temporarily
	#Proof of concept that you can run more interesting tests using simulated data
	TRAININGDATA = newtraining
	assert TRAININGDATA['google.com'] == {"Sergey Brin" : "s.brin@google.com"}
	assert TRAININGDATA == {
		"google.com" : {
	        "Sergey Brin" : "s.brin@google.com"}
	}
	##Now google.com is just Sergey. So we can predict google addresses now
	assert predict("Paul Irish", "google.com") == "p.irish@google.com"





def test_match():
	#Test the match function in general
	assert match( "Larry Page", "larry.p@google.com", "i" ) == False
	assert match( "Larry Page", "larry.p@google.com", "ii" ) == True
	assert match( "Larry Page", "larry.p@google.com", "iii" ) == False
	assert match( "Larry Page", "larry.p@google.com", "iv" ) == False

	assert match( "Linda Joan", "linda.li@alphasights.com", "i" ) == False
	assert match( "Mary O'Hanlon", "mary.ohanlon@alphasights.com", "i" ) == True
	assert match( "Tweet Tweet", "@twitter.com", "i") == False
	assert match( "Tweet Tweet", "@twitter.com", "iv") == False
	assert match( "Forgot Atsign", "forgot.atsign", "ii" ) == False

def test_match_i():
	#Test the i pattern specifically
	#aka   first_name_dot_last_name
	assert match( "Damon Aw", "damon.aw@alphasights.com", "i" ) == True
	assert match( "Ash Ketchum", "ash.ketchum@pokedex.com", "i" ) == True
	assert match( "Linda Joan", "linda.li@alphasights.com", "i" ) == False
	assert match( "Larry Page", "larry.p@google.com", "i"  ) == False
	assert match( "A Ng", "a.ng@pokedex.com", "i" ) == True

def test_match_ii():
	#Test the ii pattern specifically
	#aka  first_name_dot_last_initial
	assert match( "Larry Page", "larry.p@google.com", "ii"  ) == True
	assert match( "Larry Page", "larry.p@google.org", "ii" ) == True
	assert match( "Larry Page", "page.l@google.org", "ii" ) == False
	assert match( "Larry Page", "p.larry@google.org", "ii" ) == False
	assert match( "Damon Aw", "damon.aw@alphasights.com", "ii" ) == False
	assert match( "Ash Ketchum", "ash.k@pokedex.com", "ii" ) == True

def test_match_iii():
	#Test the iii pattern specifically
	#aka first_initial_dot_last_name
	assert match( "Sergey Brin", "s.brin@google.com", "iii") == True
	assert match( "Sergey Brin", "sergey.brin@google.com", "iii") == False
	assert match( "Carrot Top", "c.top@youtube.com", "iii") == True

def test_match_iv():
	#Test the iv pattern specifically
	#aka first_initial_dot_last_initial
	assert match( "Sergey Brin", "s.brin@google.com", "iv") == False
	assert match( "Steve Jobs", "s.j@apple.com", 'iv') == True
	assert match( "Alice in Wonderland", "a.w@madhatter.onion", 'iv') == True


## Testing the predict function:
def test_predict_errors():
	#Errors and edge cases relating to predict()
	assert predict("John Ives", "yahoo.com") == "Unknown. No email address with that domain in our records."
	assert predict("John Ferguson", "bing.com") == "Unknown. No email address with that domain in our records."
	assert predict("Paul Irish", "google.com") == "Unknown. There are at least 2 equally compelling candidates"
	assert predict("Dr. Jason Henry Simon Birenbaum", "apple.com") == "j.b@apple.com"
	assert predict("Sarah Wilson", "alphasights.com") == "sarah.wilson@alphasights.com"


## The 4 things to test:

def test_one():
	assert predict("Peter Wong", "alphasights.com") == "peter.wong@alphasights.com"

def test_two():
	assert predict("Craig Silverstein", "google.com") == "Unknown. There are at least 2 equally compelling candidates"

def test_three():
	assert predict("Steve Wozniak", "apple.com") == "s.w@apple.com"

def test_four():
	assert predict("Barack Obama", "whitehouse.gov") == "Unknown. No email address with that domain in our records."

