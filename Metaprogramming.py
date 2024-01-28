#assert string_name != 'a3'

from importlib import invalidate_caches
from importlib import import_module

def load_function(name):
    """
    load_function - imports a module recently created by name
    and returns the function of the same name from inside of it
    name - a string name of the module (not including .py at the end)
    """
    
    # invalidate_caches is necessary to import any files created after this file started!

    invalidate_caches()
    print(f" Attempting to import {name}...")
    module = import_module(name)
    print(f" Imported!")
    assert hasattr(module, name), f"{name} is missing from {name}.py"
    function = getattr(module, name)
    assert callable(function), f"{name} in {name}.py isn't a function"
    assert type(function) is type(load_function), f"{name} in {name}.py isn't a function"
    return function

def write_py(function_name, function_parameter, function_code):
    assert function_name != 'a3'
    
    file_name = function_name + '.py'

    with open(file_name, 'w') as file_write:    
        file_write.write('def ' + function_name + '(' + ', '.join(function_parameter) + '):\n')
        for code_line in function_code:
            file_write.write('     ' + code_line + '\n')
            
def fixed_bubble(size):
    '''
    This function takes the bubble sort algorithm and breaks it down into each step depending
    upon the size of the list and writes it into the a file with the end .py which makes it
    into a code with the name of the file as bitonic with the size of the list it
    has to order
    '''
    bubble_name = 'bubble'+str(size)

    code_list = []

    for bubbles in range(size):
        if bubbles != size - 1:
            code_list.append('#bubble {}'.format(bubbles))
        for index in range(size - bubbles - 1):
            code_list.append('  if a_list[{}] {} a_list[{}]:'.format(index,sign,index + 1))
            code_list.append('      a_list[{}], a_list[{}] = a_list[{}], a_list[{}]'.format(index,index + 1,index + 1,index))

    code_list.append('return a_list')
           
    write_py(bubble_name, ['a_list'], code_list)

def flip(sign):
    '''
    This function takes the sign and flips it
    '''
    if sign == '>':
        return '<'
    else:
        return '>'

def greatest_power_of_two_less_than(reference):
    '''
    his function finds the greatest power 2 should be raised to until it is becomes greater
    than or equal to the reference number
    '''
    i = 0
    while 2**i < reference:
        i += 1
    return i - 1

def bitonic_merge(a_list, start, end, direction):
    '''
    This function is a code for bitonic merge for which the pseudoalgorithm was provided
    in the assignment
    '''
    if not start < end:
        return
    
    distance = greatest_power_of_two_less_than(end - start)
    middle = end - distance
    for index in range(start, middle):
        if direction == '<':
            if a_list[index] < a_list[index+distance]:
                a_list[index], a_list[index+distance] = a_list[index+distance], a_list[index]
        elif direction == '>':
            if a_list[index] > a_list[index+distance]:
                a_list[index], a_list[index+distance] = a_list[index+distance], a_list[index]

    bitonic_merge(a_list, start, middle, direction)
    bitonic_merge(a_list, middle, end, direction)

def bitonic_sort(a_list, start, end, direction):
    '''
    This function is a code for bitonic sort for which the pseudoalgorithm was provided
    in the assignment
    '''
    if not start < end:
        return
    
    middle = (start + end)//2
    bitonic_sort(a_list, start, middle, '>')
    bitonic_sort(a_list, middle, end, '<')
    bitonic_merge(a_list,start,end,direction)
    
def bitonic(a_list):
    '''
    This function simply runs the whole bitonic algorithm on the list in the parameter
    '''
    bitonic_sort(a_list, 0, len(a_list)-1, '>')

def fixed_bitonic(size):
    '''
    This function takes the bitonic sort algorithm and breaks it down into each step depending
    upon the size of the list and writes it into the a file with the end .py which makes it
    into a code with the name of the file as bitonic with the size of the list it
    has to order
    '''
    bitonic_name = 'bitonic'+str(size)

    bitonic_list = []

    for bitonics in range(size):
        for index in range(size - bitonics - 1):
            bitonic_list.append('   if (a_list[{}] {} a_list[{}]):'.format(index,sign,index + 1))
            bitonic_list.append('        a_list[{}], a_list[{}] = a_list[{}], a_list[{}]'.format(index,index + 1,index + 1,index))

    bitonic_list.append('return a_list')

    write_py(bitonic_name, ['a_list'], bitonic_list)
    
def main():
    write_py("divide", ["a", "b"], ["r = a // b", "return r"])
    divide = load_function("divide")
    assert divide(4, 2) == 2

if __name__ == '__main__':
    main()



    
    
