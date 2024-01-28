from random import randrange
import re
import sys
from importlib import invalidate_caches
from importlib import import_module
from io import BytesIO
from os.path import exists
from os import remove
from math import log2
from math import floor
from math import ceil

SORTS = ["bubble", "bitonic"]

SORT_SIZES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 20, 32, 50, 64, 100, 101]

OUTPUTS = [
    "like",
    "add",
    "exp",
    ] + [
        f"{sort}{size}" for size in SORT_SIZES for sort in SORTS
    ]

DELETABLES = [output + ".py" for output in OUTPUTS]

def bubble_complexity(size):
    return (
        (size * (size - 1)) // 2,
        (size * (size + 1)) // 2,
        )

def bitonic_complexity(size):
    p = floor(log2(size))
    q = ceil(log2(size))
    return (
        floor(2 ** (p-1) * p * (p + 1) / 2),
        ceil(floor(size/2) * q * (q + 1) / 2)
        )

def main():
    print("Warning! Running this file will DELETE the following files:")
    print(" ".join(DELETABLES))
    print("It will only delete the files listed above.")
    print("These files should be O.K. to delete if your assignment is programmed correctly.")
    print("It will NOT delete a3.py, which is where all the code you wrote should be.")
    if input("Type YES to continue: ") != "YES":
        print("You didn't type 'YES' so check1.py is not running.")
        print("No files were deleted.")
        sys.exit(0)

    for deletable in DELETABLES:
        if exists(deletable):
            assert "a3" not in deletable
            print(f"Deleting {deletable}...")
            remove(deletable)

    for deletable in DELETABLES:
        assert not exists(deletable), f"{deletable} still exists :("

    for output in OUTPUTS:
        try:
            __import__(output)
        except ModuleNotFoundError:
            pass # this is what we want
        else:
            print(f"{output}.py deleted but could still import {output}")
            print(f"check1.py might not work correctly... :(")
            print(f"Make sure there's no {output}.py or {output}.pyc files anywhere else.")
            sys.exit(1)

    print("Checking your code is named a3.py in the same directory as this file!")
    import a3
    print("OK")

    print("Checking your code contains the write_py function!")
    from a3 import write_py
    print("OK")

    call = """
    write_py("like", ["fruit"], ["print('I like', fruit)"])
    """.strip()
    print(f"Checking we can call {call}")
    write_py("like", ["fruit"], ["print('I like', fruit)"])
    print("OK")

    filename = DELETABLES.pop(0)
    output = OUTPUTS.pop(0)
    print(f"Checking that {filename} now exists...")
    assert exists("like.py")
    print("OK")

    line = "def like(fruit):"
    print(f"Checking that {filename} starts with: {line}")
    contents = open(filename).readlines()
    assert contents[0].rstrip() == line
    print("OK")

    line = "print"
    print(f"Checking that 2nd line of {filename} contains {line}")
    assert line in contents[1]
    print("OK")

    print(f"Checking that 2nd line {filename} of is indented...")
    assert contents[1].lstrip() != contents[1]
    print("OK")

    line = "print('I like', fruit)"
    print(f"Checking that 2nd line of {filename} is {line}")
    assert contents[1].strip() == line
    print("OK")

    print(f"Checking that all other lines of {filename} are blank")
    for line in contents[2:]:
        assert line.strip() == ""
    print("OK")

    print(f"Checking {filename} contains no syntax errors...")
    invalidate_caches()
    import_module(output)
    print("OK")

    print(f"Checking {filename} has the function '{output}'")
    function = load_function(output)
    print(f"OK")

    print(f"Checking we can call the function...")
    returned = function("banana")
    print(f"OK (You should see 'I like banana' above)")

    print(f"Checking return value is correct...")
    assert returned is None
    print(f"OK")

    call = """
    write_py("add", ["a", "b"], ["r = a + b", "return r"])
    """.strip()
    print(f"Checking we can call {call}")
    eval(call)
    print("OK")

    filename = DELETABLES.pop(0)
    output = OUTPUTS.pop(0)
    print(f"Checking that {filename} now exists...")
    assert exists(filename)
    print("OK")

    line = "def add(a, b):"
    print(f"Checking that {filename} starts with: {line}")
    contents = open(filename).readlines()
    assert contents[0].rstrip() == line
    print("OK")

    line = "a + b"
    print(f"Checking that 2nd line of {filename} contains {line}")
    assert line in contents[1]
    print("OK")

    line = "return"
    print(f"Checking that 3rd line of {filename} contains {line}")
    assert line in contents[2]
    print("OK")

    print(f"Checking that 2nd, 3rd... line {filename} is indented...")
    for line_index in range(1, len(contents)):
        if contents[line_index].strip() != "":
            assert contents[line_index].lstrip() != contents[line_index]
    print("OK")

    print(f"Checking that all other lines of {filename} are blank")
    for line in contents[3:]:
        assert line.strip() == ""
    print("OK")

    print(f"Checking {filename} contains no syntax errors...")
    invalidate_caches()
    import_module(output)
    print("OK")

    print(f"Checking {filename} has the function '{output}'")
    function = load_function(output)
    print(f"OK")

    print(f"Checking we can call the add function...")
    returned = function(1, 2)
    print(f"OK")

    print(f"Checking return value is correct...")
    assert returned == 3
    print(f"OK")

    print(f"Checking we can make a program that computes an exponent...")
    check_function("exp", ["base", "power"], ["return base ** power"], [3, 2], 9)
    print(f"OK")
    
    print(f"Task 1 checks OK")
    print()
    print()
    print(f"Checking task 2...")

    print(f"Checking your a3.py has a function named fixed_bubble...")
    from a3 import fixed_bubble
    print("OK")

    print(f"Checking we can run fixed_bubble...")
    fixed_bubble(2)
    print("OK")
    
    print(f"Checking bubble2([20, 10]) returns [10, 20]...")
    function = check_output("bubble2", [[20, 10]], [10, 20])
    print(f"OK")
    
    print(f"Checking bubble2([30, 40]) returns [30, 40]...")
    check_short(function, [[30, 40]], [30, 40])
    print(f"OK")
    
    print(f"Checking that bubble2 has 1 if statement...")
    bubble2_py = open("bubble2.py").read()
    assert bubble2_py.count("if") == 1
    print(f"OK")
    
    print(f"Checking that bubble2 actually sorts things...")
    check_sort_random('bubble2', 2)
    print(f"OK")
    
    print(f"Checking that other sizes of bubble work...")
    check_sort_multi('fixed_bubble', 'bubble', bubble_complexity)
    print(f"OK")
    
    print(f"Task 2 checks OK")
    print()
    print()
    print(f"Checking task 2...")
    
    print(f"Checking a3.py has a flip function...")
    from a3 import flip
    print(f"OK")
    
    print(f"Checking that flip works...")
    assert flip("<") == ">"
    assert flip(">") == "<"
    print(f"OK")
    
    print(f"Checking a3.py has a greatest_power_of_two_less_than function...")
    from a3 import greatest_power_of_two_less_than
    print(f"OK")
    
    print(f"Checking that flip works...")
    assert greatest_power_of_two_less_than(2) == 1
    assert greatest_power_of_two_less_than(3) == 2
    assert greatest_power_of_two_less_than(4) == 2
    assert greatest_power_of_two_less_than(5) == 4
    assert greatest_power_of_two_less_than(6) == 4
    assert greatest_power_of_two_less_than(7) == 4
    assert greatest_power_of_two_less_than(8) == 4
    assert greatest_power_of_two_less_than(9) == 8
    assert greatest_power_of_two_less_than(10) == 8
    assert greatest_power_of_two_less_than(15) == 8
    assert greatest_power_of_two_less_than(16) == 8
    assert greatest_power_of_two_less_than(17) == 16
    assert greatest_power_of_two_less_than(31) == 16
    assert greatest_power_of_two_less_than(32) == 16
    assert greatest_power_of_two_less_than(33) == 32
    assert greatest_power_of_two_less_than(63) == 32
    assert greatest_power_of_two_less_than(64) == 32
    assert greatest_power_of_two_less_than(65) == 64
    assert greatest_power_of_two_less_than(127) == 64
    assert greatest_power_of_two_less_than(128) == 64
    assert greatest_power_of_two_less_than(129) == 128
    print(f"OK")
    
    print(f"Checking a3.py has a bitonic function...")
    from a3 import bitonic
    print(f"OK")

    for size in range(1, 100):
        print(f"Checking that bitonic sort actually sorts... list size: {size}")
        a_list = []
        for _ in range(size):
            a_list.append(randrange(0, 1000))
        bitonic(a_list)
        print(a_list)
        assert a_list == sorted(a_list)
        print(f"OK")

    print(f"Task 3 checks OK")
    print()
    print()
    print(f"Checking task 4...")

    check_sort_multi('fixed_bitonic', 'bitonic', bitonic_complexity)

    print("ALL OK")

def load_function(name):
    '''
    load_function - imports a module recently created by name
        and returns the function of the same name from inside of it
    name - a string name of the module (not including .py at the end)
    '''
    # invalidate_caches is necessary to import any files created after this file started!
    invalidate_caches()
    print(f"    Attempting to import {name}...")
    module = import_module(name)
    print(f"    Imported!")
    assert hasattr(module, name), f"{name} is missing from {name}.py"
    function = getattr(module, name)
    assert callable(function), f"{name} in {name}.py isn't a function"
    assert type(function) is type(load_function), f"{name} in {name}.py isn't a function"
    return function



BANNED = [
    "import",
    "for",
    "while",
    "map",
    "filter",
    "next",
    "list",
    "enumerate",
    "sort",
    "sorted",
    "range",
    "reversed",
    "reverse",
    ]

def check_function(
    name,
    parameters,
    statements,
    arguments,
    should_return
    ):
    '''
    check_function - checks write_py works correctly for some input...
    
    name - a string name of the module/function (not including .py at the end)
    parameters - a list of parameter names (strings), passed to write_py
    statements - a list of python statements (strings), passed to write_py
    arguments - a list of values to call the function with as arguments
    should_return - whatever value the function should return when called with
        those arguments
    '''
    print(f"    Calling write_py...")
    from a3 import write_py
    write_py(name, parameters, statements)
    
    check_output(name, arguments, should_return)


def check_output(name, arguments, should_return):
    '''
    check_output - checks output of write_py works correctly...
    
    parameters - a list of parameter names (strings) (should have already been passed to write_py)
    name - a string name of the module/function (not including .py at the end)
    arguments - a list of values to call the function with as arguments
    should_return - whatever value the function should return when called with
        those arguments
    '''
    filename = name + ".py"
    print(f"    Checking that {filename} exists...")
    assert exists(filename)
    print("    OK")

    print(f"    Checking that {filename} starts with function definition")
    contents = open(filename).readlines()
    assert contents[0].startswith("def")
    assert name in contents[0]
    print("    OK")
    
    print(f"    Checking that first line ends with :")
    assert contents[0].rstrip().endswith(":")
    print(f"    OK")
    
    print(f"    Checking that 2nd, 3rd, 4th... line {filename} is indented...")
    line_index = 1
    while line_index < len(contents) and contents[line_index].strip() != "":
        assert contents[line_index].lstrip() != contents[line_index]
        line_index += 1
    print("    OK")

    print(f"    Checking that remaining lines are blank...")
    line_index = 1
    while line_index < len(contents):
        contents[line_index].strip() == ""
        line_index += 1
    print("    OK")
    
    whole_contents = re.split(r'\b', " ".join(contents))
    
    print(f"    Checking that {filename} doesn't contain...")
    for banned in BANNED:
        print(f"        {banned}")
        assert banned not in whole_contents
    print("    OK")

    print(f"    Checking {filename} contains no syntax errors...")
    invalidate_caches()
    import_module(name)
    print("    OK")
    
    print(f"    Checking {filename} has the function '{name}'")
    function = load_function(name)
    print(f"    OK")
    
    check_short(function, arguments, should_return)
    
    return function
    
def check_short(function, arguments, should_return):
    args_string = ", ".join(map(repr, arguments))
    print(f"    Checking we can call the function {function.__name__}({args_string})...")
    returned = function(*arguments)
    print(f"    OK")

    print(f"    Checking return value is {repr(should_return)}...")
    assert returned == should_return, f"Got {repr(returned)} but expected {repr(should_return)}"
    print(f"    OK")
    
    return function

def check_sort_random(name, size):
    arguments = [list(range(size*10, 0, -10))]
    should_return = sorted(arguments[0])
    function = check_output(name, arguments, should_return)
    for repeat in range(1,3+1):
        print(f"  Checking {name} can sort a random list... (#{repeat})")
        a_list = [randrange(100,1000) for _ in range(size)]
        arguments = [a_list]
        should_return = sorted(a_list)
        check_short(function, arguments, should_return)
        print(f"  OK")

def check_sort_multi(generator_name, name, complexity):
    import a3
    
    print("Checking a3.py has a function named {generator_name}...")
    generator = getattr(a3, generator_name)
    print("OK")
    for size in SORT_SIZES:
        print("Checking we can run {generator_name}({size})...")
        generator(size)
        print("OK")
        
        fixed_name = f"{name}{size}"
        
        check_sort_random(fixed_name, size)
        
        lb, ub = complexity(size)
        
        print(f"Checking {fixed_name}.py has at least {lb} if statements...")
        py = open(f"{fixed_name}.py").read()
        assert py.count("if") >= lb
        print("OK")
        
        print(f"Checking {fixed_name}.py has at most {ub} if statements...")
        py = open(f"{fixed_name}.py").read()
        assert py.count("if") <= ub
        print("OK")

if __name__=="__main__":
    main()
