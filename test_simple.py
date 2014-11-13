import simple

def two():
    return 2

def test_one():
    assert one() == 1

def test_two():
    assert two() == 2

def test_sample():
    assert return_sample()['Sergey Brin'] == "s.brin@google.com"    
