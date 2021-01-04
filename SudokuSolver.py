# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 02:14:42 2021

@author: sebtac
@contact: https://www.linkedin.com/in/sebastian-taciak-5893861/

@title: 'sebtac's Sudoku Solver'

@ Purpose: 'Explore Numpy's Vectorization and Broadcasting Capabilities (Non-ML Implementation)'

@Imlementation_Details:
    - Uses Unique Potential Values in Cells, Rows, Columns and Zones to derive candidates for the value in a cell.
    - once reaches point where no new vales can be deducted from the above it uses Search
      by trying different potential values according to their probability of being in given cell
    - It is not Exhaustive Search as only Level one Probabilities are preserved
      i.e. probabilities of entries as they are when the no-solution condition is met for the first time (max 729 search iterations)
    - it goes deeper into levels 2 to n but only once per level 1 iteration
    - this is the potentioal reason why the most difficut case (10) fails to be solved - to be updated soon
    
    - Use SudokuSolver-Helper.xls file to generate input
"""

import numpy as np
import copy

# r = row
# c = column
# l = layer
# z = zone
# v = value

##############################################################
###################### INITIALIZATION ########################
##############################################################

# INITIALIZE BOARD
# board.shape = (r,c) 
board = np.zeros((9,9))

# INITIALIZE BOARD - taken from various SUDOKU implementations
# start_values = (r,c,v)

max_iterations = 300000
difficultry_level = 9

# Windows Difficulty Classification
# 3 - Hard Windows # 9 Iterations to Solve
# 7 - Grandmaster Windows # 23 Iterations to Solve
# 8 - Grandmaster Windows # 25 Iterations to Solve
# 9 - Super Difficult - Hardest in Aunt Ela's Book # 136 Iterations to Solve
# 10 - the 3rd Hardest Sudoku Ever - !!!NOT SOLVED!!! - https://www.calcudoku.org/hardest_logic_number_puzzles/

if difficultry_level == 3:
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

if difficultry_level == 7:
    start_values = ((0,0,6),
                    (0,2,5),
                    (0,5,3),
                    (0,6,2),
                    (1,3,1),
                    (2,4,2),
                    (2,7,8),
                    (3,0,1),
                    (3,4,5),
                    (3,5,2),
                    (3,6,4),
                    (3,7,3),
                    (3,8,7),
                    (4,0,4),
                    (4,3,7),
                    (4,6,8),
                    (4,7,9),
                    (4,8,6),
                    (5,0,7),
                    (5,4,4),
                    (6,1,6),
                    (6,7,1),
                    (7,3,2),
                    (7,4,8),
                    (7,5,9),
                    (8,2,8),
                    (8,8,3))

if difficultry_level == 8:
    start_values = ((0,2,4),
                    (0,3,1),
                    (0,6,3),
                    (0,7,9),
                    (1,0,6),
                    (1,3,7),
                    (1,4,3),
                    (2,7,4),
                    (2,8,7),
                    (3,2,7),
                    (3,6,9),
                    (4,0,2),
                    (4,5,5),
                    (4,7,1),
                    (5,0,9),
                    (5,1,4),
                    (5,4,1),
                    (5,6,5),
                    (5,7,3),
                    (6,0,7),
                    (6,6,4),
                    (6,7,2),
                    (7,4,4),
                    (7,5,3),
                    (7,8,9),
                    (8,2,3),
                    (8,3,9),
                    (8,5,8))
    
if difficultry_level == 9:
    start_values = ((0,3,9),
(1,5,7),
(1,6,6),
(2,1,5),
(2,2,1),
(2,5,8),
(2,7,9),
(3,0,5),
(3,5,9),
(3,6,4),
(3,7,3),
(4,0,7),
(4,2,4),
(4,4,2),
(5,3,5),
(5,8,2),
(6,0,4),
(6,1,9),
(6,4,3),
(6,6,5),
(7,0,2),
(7,2,3),
(7,6,1),
(8,1,8),
(8,2,5),
(8,4,7),
(8,5,2),
)

 
if difficultry_level == 10:
    start_values = ((0,0,8),
(1,2,3),
(1,3,6),
(2,1,7),
(2,4,9),
(2,6,2),
(3,1,5),
(3,5,7),
(4,4,4),
(4,5,5),
(4,6,7),
(5,3,1),
(5,7,3),
(6,2,1),
(6,7,6),
(6,8,8),
(7,2,8),
(7,3,5),
(7,7,1),
(8,1,9),
(8,6,4))

for i in start_values:
    r = i[0]
    c = i[1]
    v = i[2]
    
    board[r,c] = v
    
print("Initial Board:\n", board)

##############################################################
######################### SOLVIING ###########################
##############################################################

solved = False # Runs till True; Set True when Solved
iteration = 1 # To control progress;
fails = 0 # How many times Fail condition was reached; 1 Triggers saving of level 1 probabiliy tables for search
reverseto1 = 0 # makes SOLVER come back to Exploration Level 1 

while not solved:
    
    # SOLVED VALUES INDICATOR TABLE (migrating from 2-Dim intager representation to 3-Dim binarry representation)
    
    # RxCxV # 0 Not Solved, 1 Solved
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
        
    #print("\nsolved_values:\n",solved_values)
    
    # c_solved - Cube representing what values are solved in each column
    # 9 same row layers = same column in a table acros tables
    # layer RxCxV 0 Not Solved, 1 Solved     
    c_solved = np.expand_dims(np.amax(solved_values, axis=0),axis=0)
    c_solved = np.repeat(c_solved,9, axis=0)
    #print("\nc_solved\n:",c_solved)

    # r_solved - Cube representing what values are solved in each row
    # 9 same columns layers = same row accross a table
    # layer RxCxV 0 Not Solved, 1 Solved     
    
    r_solved = np.expand_dims(np.amax(solved_values, axis=1),axis=1)
    r_solved = np.repeat(r_solved,9, axis=1)
    #print("\nr_solved\n:",r_solved)
    
    # z_solved - Cube representing what values are solved in each zone
    # 9 value layers groupped in 3 = same value accross three consequitev tables
    # layer RxCxV 0 Not Solved, 1 Solved     
    
    values_split_vertical = copy.deepcopy(np.split(solved_values, [3,6]))    
    values_split_vertical_ph = np.zeros([1,9,9])
    for a in values_split_vertical:
        values_split_horizontal = np.split(a, [3,6],axis=1)
        values_split_horizontal_ph = np.zeros([3,1,9])
        for b in values_split_horizontal:
            b[:,:] = np.amax(b, axis = (0,1))
            values_split_horizontal_ph = np.concatenate((values_split_horizontal_ph,b), axis = 1)
        values_split_horizontal_ph = values_split_horizontal_ph[:,1:,:]
        values_split_vertical_ph = np.concatenate((values_split_vertical_ph,values_split_horizontal_ph), axis = 0)
    
    z_solved = values_split_vertical_ph[1:,:,:]
    #print("\nz_solved\n:",z_solved)
    
    # all_solved - 0 indicates that given value is posisble in given cell
    # sums the above three indicators - values higher than 0 indicate that given value is not possible in this cell
    # layer RxCxV 0 is Potential value, >0 Excluded
    all_solved = np.zeros((9,9,9))
    all_solved = np.add(all_solved,c_solved)
    all_solved = np.add(all_solved,r_solved)
    all_solved = np.add(all_solved,z_solved)
    #("\nall_solved:\n",all_solved)
    

    # already_solved_indicator - 1 Cell is Not Solved, 0 Solved
    already_solved_indicator = np.expand_dims(1-(board>0).astype(int), axis = 2)
    #print("ASI",already_solved_indicator)

    # It is possible that all_solved indicates posibility of a value in a cell that is already solved
    # Thus multiplication to clear out such cases
    possible_values_indicator = (all_solved==0).astype(int)
    possible_values_indicator = possible_values_indicator*already_solved_indicator
    possible_values_indicator = np.where((possible_values_indicator < 0), 0, possible_values_indicator)
    #print("\npossible_values_indicator:\n",possible_values_indicator)
    
    # UNIQUE IN CELL
    potential_unique_sum = np.sum(possible_values_indicator, axis = 2)
    potential_unique = np.expand_dims(np.where((potential_unique_sum > 1), 0, potential_unique_sum),axis=2)
    potential_unique_indicator = possible_values_indicator*potential_unique
    potential_unique_indicator_flat = np.amax(potential_unique_indicator, axis = 2)
    
    # returns newly solved value in given cell; -1 otherwise RxCx1
    new_solved_values_unique = np.expand_dims(((np.argmax(potential_unique_indicator, axis = 2)+1)+potential_unique_indicator_flat)*potential_unique_indicator_flat-1, axis = 2)
    #print("new_solved_values_unique:\n",new_solved_values_unique)

    # UNIQUE IN ROW    
    potential_row_sum = np.sum(possible_values_indicator, axis = 1)
    potential_row = np.expand_dims(np.where((potential_row_sum > 1), 0, potential_row_sum),axis=1)
    potential_row_indicator = possible_values_indicator*potential_row
    potential_row_indicator_flat = np.amax(potential_row_indicator, axis = 2)
    
    # returns newly solved value in given cell; -1 otherwise RxCx1
    new_solved_values_row = np.expand_dims(((np.argmax(potential_row_indicator, axis = 2)+1)+potential_row_indicator_flat)*potential_row_indicator_flat-1, axis = 2)
    #print("new_solved_values_row:\n",new_solved_values_row)

    # UNIQUE IN COLUMN
    potential_column_sum = np.sum(possible_values_indicator, axis = 0)
    potential_column = np.expand_dims(np.where((potential_column_sum > 1), 0, potential_column_sum),axis=0)
    potential_column_indicator = possible_values_indicator*potential_column
    potential_column_indicator_flat = np.amax(potential_column_indicator, axis = 2)
    
    # returns newly solved value in given cell; -1 otherwise RxCx1
    new_solved_values_column = np.expand_dims(((np.argmax(potential_column_indicator, axis = 2)+1)+potential_column_indicator_flat)*potential_column_indicator_flat-1, axis = 2)
    #print("new_solved_values_column:\n",new_solved_values_column)
    
    # UNIQUE IN ZONE 
    uz_split_vertical = copy.deepcopy(np.split(possible_values_indicator, [3,6]))
    uz_split_vertical_ph = np.zeros([1,9,9])
    
    for a in uz_split_vertical:
        uz_split_horizontal = np.split(a, [3,6],axis=1)
        uz_split_horizontal_ph = np.zeros([3,1,9])
        for b in uz_split_horizontal:
            b[:,:] = np.sum(b, axis = (0,1))
            uz_split_horizontal_ph = np.concatenate((uz_split_horizontal_ph,b), axis = 1)
        uz_split_horizontal_ph = uz_split_horizontal_ph[:,1:,:]
        uz_split_vertical_ph = np.concatenate((uz_split_vertical_ph,uz_split_horizontal_ph), axis = 0)  
    potential_zone_sum = uz_split_vertical_ph[1:,:,:]
    potential_zone = np.where((potential_zone_sum > 1), 0, potential_zone_sum)
    potential_zone_indicator = possible_values_indicator*potential_zone
    potential_zone_indicator_flat = np.amax(potential_zone_indicator, axis = 2)

    # returns newly solved value in given cell; -1 otherwise RxCx1
    new_solved_values_zone = np.expand_dims(((np.argmax(potential_zone_indicator, axis = 2)+1)+potential_zone_indicator_flat)*potential_zone_indicator_flat-1, axis = 2)
    #print("\nnew_solved_values_zone\n", new_solved_values_zone)
    
    # Indicates new value and its position
    # RxC
    new_solved_values = np.concatenate((new_solved_values_unique,new_solved_values_row,new_solved_values_column,new_solved_values_zone), axis = 2) 
    new_solved_values = np.amax(new_solved_values, axis = 2)
    new_solved_values = np.where((new_solved_values < 0), 0, new_solved_values)
    print("\nNew Solved Values:\n",new_solved_values)
    
    # IF NO NEW SOLVED VALUES to work with
    if np.sum(new_solved_values)==0:
        
        fails += 1
        
        # Check if SOLUTION was achieved 
        checksum_r = np.sum(board, axis = 1)
        checksum_c = np.sum(board, axis = 0)

        checksum_split = []        
        checksum_split_vertical = np.split(board, [3,6])        
        for a in checksum_split_vertical:
            checksum_split_horizontal = np.split(a, [3,6],axis=1)
            for b in checksum_split_horizontal:
                checksum_split_mean = np.sum(b)
                checksum_split.append(checksum_split_mean)        
        checksum_z = np.array(checksum_split)
        
        checksum_rcz = np.concatenate((checksum_r,checksum_c,checksum_z))
        
        checksum_rcz_mean = np.average(checksum_rcz)
        checksum_rcz_min = np.min(checksum_rcz)
        checksum_rcz_max = np.max(checksum_rcz)

        print("\nCheckSums (All Values Should Be 45):")
        print("Rows:", checksum_r)
        print("Columns:", checksum_c)
        print("Zones:", checksum_z)
        
        if checksum_rcz_mean == 45 and checksum_rcz_min == 45 and checksum_rcz_max == 45:
            # If SOLVED:
            print("\nTotal Average:", checksum_rcz_mean)
            print("Total Min:", checksum_rcz_min)
            print("Total Max:", checksum_rcz_max)
            print("\nSUDOKU Solved!")
            print("\nFINAL Board:\n", board)            
            solved = True
        else:
            # If NOT SOLVED:
            print("\n!?!??! *^*&%&$ ??!?!?... sth went wrong") 
            print("\nTotal Average:", checksum_rcz_mean)
            print("Total Min:", checksum_rcz_min)
            print("Total Max:", checksum_rcz_max,"\n")

            print("\nCURRENT Board:\n", board) 
            
            # SOLUTION SEARCH
            
            # GENERATE PROBABILITY OF GIVEN VALUE BELOGING TO GIVEN CELL
            ### It needs to say how many times given value is possible in given row Accross all columns
            #RxV
            potential_row_sum = np.where((potential_row_sum == 0), 1, potential_row_sum).reshape((9,1,9))
            potential_column_sum = np.where((potential_column_sum == 0), 1, potential_column_sum)
            potential_zone_sum = np.where((potential_zone_sum == 0), 1, potential_zone_sum)
                                    
            potential_row_probability = np.divide(possible_values_indicator,potential_row_sum, where = potential_row_sum>0)
            potential_column_probability = np.divide(possible_values_indicator,potential_column_sum, where = potential_column_sum>0)
            potential_zone_probability = np.divide(possible_values_indicator,potential_zone_sum, where = potential_zone_sum>0)
            
            potential_probability = np.mean([potential_row_probability,
                                                    potential_column_probability,
                                                    potential_zone_probability], axis = 0)*(1-solved_values)
            
            potential_probability_max = np.max(potential_probability)
            
            
            # CREATE ARRAY WITH PROIRITIZED PROBABILITES for SEARCH
            c = np.arange(9)
            d = np.arange(9)
            e = np.arange(9)
            
            l2=[]
            g = ((x,y,z) for x in c for y in d for z in e)
            for i in g:
                l2.append(i)            
            
            arr_sorted = np.array(l2)
            arr_sorted = arr_sorted[arr_sorted[:,2].argsort(kind='mergesort')] # First sort doesn't need to be stable.
            arr_sorted = arr_sorted[arr_sorted[:,1].argsort(kind='mergesort')]
            arr_sorted = arr_sorted[arr_sorted[:,0].argsort(kind='mergesort')]
            
            probs = np.expand_dims(potential_probability.reshape(-1), axis = 1)
            randsearch_probabilities = np.hstack((arr_sorted, probs))
            
            randsearch_probabilities = randsearch_probabilities[randsearch_probabilities[:,3].argsort(kind='mergesort')][::-1]
            #print("\nrandsearch_probabilities\n", randsearch_probabilities[:30,:])
            
            # LOGIC CONGROLING EXECUTION FLOW
            if fails == 1 and reverseto1 == 0:
                # THE FIRST FAIL - PRESERVE THE LEVEL 1 PROBABILITY TABLE and BOARD
                print("scenario 1", fails, reverseto1)
                # SAVE LEVEL 1 probabilities for future search
                randsearch_probabilities1 = randsearch_probabilities
                # CHOSe the first SEARCH VALUE
                tryit = randsearch_probabilities1[0]
                # REMOVE THE USED VALUE FROM THE PROBABILITY TABLE
                randsearch_probabilities1 = randsearch_probabilities1[1:,:]
                # PRESERVE LEVEL 1 BOARD
                board1 = copy.deepcopy(board)
                
            elif fails > 1 and reverseto1 == 1:
                # NEXT VALUE FORM THE PROBABILITY TABLE
                print("scenario 2", fails, reverseto1)
                tryit = randsearch_probabilities1[0]
                randsearch_probabilities1 = randsearch_probabilities1[1:,:]
                board = copy.deepcopy(board1)
                reverseto1 = 0
            else:
                # REGULAR EXPLORATION
                print("scenario 3", fails, reverseto1)
                tryit = randsearch_probabilities[0]
            
            print("tryit",tryit)
            
            if tryit[3] == 0.0 :
                # IF NO NEW CANDIDATE VALUE TRY ANOTHER VALUE FORM THE LEVEL 1 PROBABILITY TABLE (SCENARIO 2)
                print("\n!?!??! *^*&%&$ ??!?!?... DID NOT CONVERGE!!!")
                
                print("\nCheckSums (All Values Should Be 45):")
                
                print("Rows:", checksum_r)
                print("Columns:", checksum_c)
                print("Zones:", checksum_z)
        
                print("\nTotal Average:", checksum_rcz_mean)
                print("Total Min:", checksum_rcz_min)
                print("Total Max:", checksum_rcz_max,"\n")
                print("\nCURRENT Board:\n", board)
                reverseto1 = 1

            else:
                # IF CANDIDATE VALUE EXIST
                new_solved_values[int(tryit[0]),int(tryit[1])] = int(tryit[2])+1
                print("\nNew Solved Values:\n",new_solved_values)
                
                board = board + new_solved_values
                print("\nUpdated Board", iteration,":\n", board)           
                
            iteration += 1
            
            # IF SOLVED!
            if iteration >= max_iterations:
                solved = True # UPDATE TERMINATION LOGIC!
    else:
        # NEXT UPDATE
        board = board + new_solved_values
        print("\nUpdated Board", iteration,":\n", board)
        iteration += 1
