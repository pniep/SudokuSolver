# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 02:14:42 2021

@author: sebtac
@contact: https://www.linkedin.com/in/sebastian-taciak-5893861/

@title: 'sebtac's Sudoku Solver'

"""
import numpy as np

# r = row
# c = column
# l = layer
# z = zone
# v = value

# INITIALIZE BOARD
# board.shape = (r,c) 
board = np.zeros((9,9))

# INSERT INITIAL VALUES - taken from Windows SUDOKU implementation
# start_values = (r,c,v)
start_values = ((0,0,9),
(0,4,8),
(0,8,2),
(1,1,8),
(1,2,6),
(1,3,9),
(1,6,4),
(1,7,7),
(1,8,5),
(2,1,5),
(2,5,6),
(2,7,9),
(3,1,2),
(3,2,5),
(3,3,1),
(3,6,8),
(4,0,7),
(4,2,8),
(4,4,2),
(4,5,3),
(4,6,6),
(5,1,1),
(5,4,6),
(5,7,2),
(6,0,8),
(6,1,7),
(6,2,3),
(6,7,4),
(7,2,9),
(8,3,3),
(8,4,5),
(8,6,7),
(8,7,8))
))

for i in start_values:
    r = i[0]
    c = i[1]
    v = i[2]
    
    board[r,c] = v
    
    #print(x,y,v)
    
print("Initial Board:\n", board)



solved = False
iteration = 1
while not solved:
    
    # SOLVED VALUES INDICATOR TABLE (taking from 2-Dim intager based representation to 3-Dim binarry representation) 
    solved_values = np.zeros((9,9,9))
    
    # ST change it to np.loc_at Vectorized implementation!!!
    r_val = 0
    for r in board:
        c_val = 0
        for c in r:
            if c == 0:
                pass
            else:
                v = int(board[r_val,c_val])
                #print(y_val, x_val, value)
                solved_values[r_val,c_val,v-1] = 1
            c_val += 1
        r_val += 1
        
    #print(values)
    #print(values.shape)
    #print(values[0,0,8])
        
    c_solved = np.expand_dims(np.amax(solved_values, axis=0),axis=0)
    c_solved = np.repeat(c_solved,9, axis=0)
    #print("4"c_solved.shape)
    
    #print(c_solved[0])
    #print(c_solved[8])
    #print(c_solved[0,0,8])
    #print(c_solved[8,0,8])
    #print(c_solved, np.sum(c_solved)/9)
    
    r_solved = np.expand_dims(np.amax(solved_values, axis=1),axis=1)
    r_solved = np.repeat(r_solved,9, axis=1)
    #print(r_solved.shape)
    #print(r_solved, np.sum(r_solved/9))
    
    values_split_vertical = np.split(solved_values, [3,6])
    #print(values_split_vertical)
    #print(type(a2)) # list
    
    values_split_vertical_ph = np.zeros([1,9,9])
    for a in values_split_vertical:
        values_split_horizontal = np.split(a, [3,6],axis=1)
        #print(a3)
        values_split_horizontal_ph = np.zeros([3,1,9])
        for b in values_split_horizontal:
            b[:,:] = np.amax(b, axis = (0,1))
            #print(a)
            values_split_horizontal_ph = np.concatenate((values_split_horizontal_ph,b), axis = 1)
        values_split_horizontal_ph = values_split_horizontal_ph[:,1:,:]
        #print(a3_ph)
        #print(a3_ph.shape)
        #print(a2_ph.shape)
        values_split_vertical_ph = np.concatenate((values_split_vertical_ph,values_split_horizontal_ph), axis = 0)
    z_solved = values_split_vertical_ph[1:,:,:]
    #print(z_solved[:,:,8])    
    
    all_solved = np.zeros((9,9,9))
    all_solved = np.add(all_solved,c_solved)
    all_solved = np.add(all_solved,r_solved)
    all_solved = np.add(all_solved,z_solved)
    #print("all_solved",all_solved)
    
    
    already_solved_indicator = np.expand_dims((board>0).astype(int), axis = 2)
    #print(already_solved_indicator)
    possible_values_indicator = (all_solved==0).astype(int)
    #print(possible_values_indicator[3])
    possible_values_indicator = np.subtract(possible_values_indicator, already_solved_indicator)
    #print(possible_values_indicator[3])
    possible_values_indicator = np.where((possible_values_indicator < 0), 0, possible_values_indicator)
    #print(possible_values_indicator[3])
    
    # UNIQUE IN CELL
    potential_unique = np.sum(possible_values_indicator, axis = 2)
    potential_unique = np.expand_dims(np.where((potential_unique > 1), 0, potential_unique),axis=2)
    #print(potential_unique.shape)
    potential_unique_flat = np.amax(possible_values_indicator, axis = 2)
    potential_unique_indicator = possible_values_indicator*potential_unique
    #print("potential_unique_indicator:\n",potential_unique_indicator)
    potential_unique_indicator_flat = np.amax(potential_unique_indicator, axis = 2)
    #print("potential_unique_indicator_flat:\n",potential_unique_indicator_flat)
    new_solved_values_unique = np.expand_dims(((np.argmax(potential_unique_indicator, axis = 2)+1)+potential_unique_indicator_flat)*potential_unique_indicator_flat-1, axis = 2)
    #print("new_solved_values_unique:\n",new_solved_values_unique)
    
    # UNIQUE IN ROW    
    potential_row = np.sum(possible_values_indicator, axis = 1)
    potential_row = np.expand_dims(np.where((potential_row > 1), 0, potential_row),axis=1)
    #print(potential_row.shape)
    potential_row_flat = np.amax(possible_values_indicator, axis = 1)
    potential_row_indicator = possible_values_indicator*potential_row
    #print("potential_row_indicator:\n",potential_row_indicator)
    potential_row_indicator_flat = np.amax(potential_row_indicator, axis = 2)
    #print("potential_row_indicator_flat:\n",potential_row_indicator_flat)
    new_solved_values_row = np.expand_dims(((np.argmax(potential_row_indicator, axis = 2)+1)+potential_row_indicator_flat)*potential_row_indicator_flat-1, axis = 2)
    #print("new_solved_values_row:\n",new_solved_values_row)

    # UNIQUE IN COLUMN
    potential_column = np.sum(possible_values_indicator, axis = 0)
    potential_column = np.expand_dims(np.where((potential_column > 1), 0, potential_column),axis=0)
    #print(potential_column.shape)
    potential_column_flat = np.amax(possible_values_indicator, axis = 0)
    potential_column_indicator = possible_values_indicator*potential_column
    #print("potential_column_indicator:\n",potential_column_indicator)
    potential_column_indicator_flat = np.amax(potential_column_indicator, axis = 2)
    #print("potential_column_indicator_flat:\n",potential_column_indicator_flat)
    new_solved_values_column = np.expand_dims(((np.argmax(potential_column_indicator, axis = 2)+1)+potential_column_indicator_flat)*potential_column_indicator_flat-1, axis = 2)
    #print("new_solved_values_column:\n",new_solved_values_column)
    
    # UNIQUE IN ZONE -- To Be Implemented!!!
    
    new_solved_values = np.concatenate((new_solved_values_unique,new_solved_values_row,new_solved_values_column), axis = 2) 
    new_solved_values = np.amax(new_solved_values, axis = 2)
    new_solved_values = np.where((new_solved_values < 0), 0, new_solved_values)
    print("5",new_solved_values)
    
    if np.sum(new_solved_values)==0:
        solved = True
        print("\nSUDOKU Solved!")
        print("\nFINAL Board:\n", board)
    else:
        board = board + new_solved_values
        print("\nUpdated Board", iteration,":\n", board)
        iteration += 1

# COMBINATORICAL SEARCH -- To Be Implemented!!!

# FINAL CHECK -- To Be Implemented!!!
        
        
        
# NOTES:        
# zone_ind[start_row,end_row,start_column,end_column]
# call format: r_solved[0][0:3,6:9] = r_solved[0][zone_ind[0]:zone_ind[1],zone_ind[2]:zone_ind[3]]
""" 
zone_ind = [[0,3,0,3],
            [0,3,3,6],
            [0,3,6,9],
            [3,6,0,3],
            [3,6,3,6],
            [3,6,6,9],
            [6,9,0,3],
            [6,9,3,6],
            [6,9,6,9]]
"""

