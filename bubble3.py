def bubble3(a_list):
     #bubble 0
       if a_list[0] > a_list[1]:
           a_list[0], a_list[1] = a_list[1], a_list[0]
       if a_list[1] > a_list[2]:
           a_list[1], a_list[2] = a_list[2], a_list[1]
     #bubble 1
       if a_list[0] > a_list[1]:
           a_list[0], a_list[1] = a_list[1], a_list[0]
     return a_list
