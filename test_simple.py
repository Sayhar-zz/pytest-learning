from simple import *

def two():
    return 2

def test_one():
    assert one() == 1

def test_two():
    assert two() == 9, "it's okay, I expect this to fail"

def test_sample():
    assert return_sample()['Sergey Brin'] == "s.brin@google.com"    
