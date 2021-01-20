import random
import math

# first we read the info from the dump file into python

lines = open('dump.just_hex_lattice').read().split("\n")

# this is the first 9 lines, the header info.
# the number of atoms will need to be updated after deletions

header = lines[:9]

# The atom data

data = lines[9:]
data.pop()

# Here we tokenize the data to get the id easily, to use for sorting
data_as_tokens = []
for line in data:
    tokens = line.split(" ")
    data_as_tokens.append(tokens)

def get_first_token(line):
    return int(line[0])

# We use the atom id to sort the atoms. For some reason the dump
# file has them in a strange order. It will be easier to work with the
# data once it has been placed into atom id order.

data_as_tokens.sort(key = get_first_token)

# Here we make functions to delete atoms

# This function is used in the delete_row_to_right function.
# It allows to determine where the 'end' of the material is
def roundup(starting_point):
    return int(math.ceil(starting_point / 400.0)) * 400

def rounddown(starting_point):
    return int(math.floor(starting_point / 400.0)) * 400

# This function deletes the close pack atoms to a starting point
# in the direction of 60 degrees from the right horizontal aka pi/3.
def delete_row_60(data_as_tokens, starting_point):
    x_max = 227.125
    y_max = 97.6087
    while( starting_point < len(data_as_tokens) and float( data_as_tokens[starting_point][1] ) <= x_max and float( data_as_tokens[starting_point][2] ) <= y_max ):
        data_as_tokens[starting_point][3] = "1"
        if( int( data_as_tokens[starting_point][0]) % 2 == 0):
            if( float( data_as_tokens[starting_point][1] ) == x_max or float( data_as_tokens[starting_point][2] ) == y_max ):
                starting_point = 100000
            starting_point = starting_point + 401
        else:
            if( float( data_as_tokens[starting_point][1] ) == x_max or float( data_as_tokens[starting_point][2] ) == y_max ):
                starting_point = 100000
            starting_point = starting_point + 1

# This function deletes the close pack atoms to a starting point
# in the direction of 120 degrees from the right horizontal aka 2pi/3.
def delete_row_120(data_as_tokens, starting_point):
    x_min = 0
    y_max = 97.6087
    while( starting_point < len(data_as_tokens) and float( data_as_tokens[starting_point][1] ) >= x_min and float( data_as_tokens[starting_point][2] ) <= y_max ):
        data_as_tokens[starting_point][3] = "1"
        if( int( data_as_tokens[starting_point][0]) % 2 == 0):
            if( float( data_as_tokens[starting_point][1] ) == x_min or float( data_as_tokens[starting_point][2] ) == y_max ):
                starting_point = 100000
            starting_point = starting_point + 399
        else:
            if( float( data_as_tokens[starting_point][1] ) == x_min or float( data_as_tokens[starting_point][2] ) == y_max ):
                starting_point = 100000
            starting_point = starting_point - 1

# This function deletes the close pack atoms to a starting point
# in the direction of 240 degrees from the right horizontal aka 3pi/2
def delete_row_240(data_as_tokens, starting_point):
    x_min = 0
    y_min = 0
    while( starting_point < len(data_as_tokens) and float( data_as_tokens[starting_point][1] ) >= x_min and float( data_as_tokens[starting_point][2] ) >= y_min ):
        data_as_tokens[starting_point][3] = "1"
        if( int( data_as_tokens[starting_point][0]) % 2 == 0):
            if( float( data_as_tokens[starting_point][1] ) == x_min or float( data_as_tokens[starting_point][2] ) == y_min ):
                starting_point = 100000
            starting_point = starting_point - 1 
        else:
            if( float( data_as_tokens[starting_point][1] ) == x_min or float( data_as_tokens[starting_point][2] ) == y_min ):
                starting_point = 100000
            starting_point = starting_point - 401 

# This function deletes the close pack atoms to a starting point
# in the direction of 300 degrees from the right horizontal aka 3pi/2
def delete_row_300(data_as_tokens, starting_point):
    x_max = 227.125
    y_min = 0
    while( starting_point < len(data_as_tokens) and float( data_as_tokens[starting_point][1] ) <= x_max and float( data_as_tokens[starting_point][2] ) >= y_min ):
        data_as_tokens[starting_point][3] = "1"
        if( int( data_as_tokens[starting_point][0]) % 2 == 0):
            if( float( data_as_tokens[starting_point][1] ) == x_max or float( data_as_tokens[starting_point][2] ) == y_min ):
                starting_point = 100000
            starting_point = starting_point + 1 
        else:
            if( float( data_as_tokens[starting_point][1] ) == x_max or float( data_as_tokens[starting_point][2] ) == y_min ):
                starting_point = 100000
            starting_point = starting_point - 399 

# This function picks a random atom as a starting point
# and deletes all the atoms directly to the right of it.
def delete_row_to_right(data_as_tokens, starting_point):
    rounded_to_400 = roundup(starting_point)
    if(rounded_to_400 == 20000):
        rounded_to_400 = rounded_to_400 - 2
    while(int(data_as_tokens[starting_point][0]) <= rounded_to_400):
        data_as_tokens[starting_point][3] = "1" 
        starting_point = starting_point + 2

# This function picks a random atom as a starting point
# and deletes all the atoms directly to the left of it.
def delete_row_to_left(data_as_tokens, starting_point):
    rounded_to_lower_400 = rounddown(starting_point)
    if(rounded_to_lower_400 == 0):
        rounded_to_lower_400 = rounded_to_lower_400 + 2
    while(int(data_as_tokens[starting_point][0]) >= rounded_to_lower_400):
        data_as_tokens[starting_point][3] = "1"
        starting_point = starting_point - 2

# This function randomly selects one of the above deletion functions,
# and then repeats for a total of 10 delete operations.
def delete_30_times(data_as_tokens):
    for i in range(31):
        random_starting_point = random.randrange(0,len(data_as_tokens))
        random_delete_method = random.randrange(6)
        if random_delete_method == 0:
            delete_row_to_right(data_as_tokens, random_starting_point)
        elif random_delete_method == 2:
            delete_row_60(data_as_tokens, random_starting_point)
        elif random_delete_method == 3:
            delete_row_120(data_as_tokens, random_starting_point)
        elif random_delete_method == 4:
            delete_row_240(data_as_tokens, random_starting_point)
        elif random_delete_method == 5:
            delete_row_300(data_as_tokens, random_starting_point)
        else:
            delete_row_to_left(data_as_tokens, random_starting_point)

delete_30_times(data_as_tokens)

# Make a modified file with the header and deleted data
def count_deleted_atoms(data_as_tokens):
    count = 0
    for i in range(len(data_as_tokens)):
        if(data_as_tokens[i][3] == "1"):
            count = count + 1
    return count

number_deleted_atoms = count_deleted_atoms(data_as_tokens)
header[3] = str( len(data_as_tokens) - number_deleted_atoms )

file_name = 'dump.modified_hex_lattice_'
simulation_id = input ("Enter the trial number: ")
file_name = file_name + simulation_id
f = open(file_name, 'w')
for line in header:
    f.write(line + "\n")

def untokenize(line):
    return line[0] + " " + line[1] + " " + line[2] + " " + line[3] + " " + line[4] 

for line in data_as_tokens:
    if(line[3] != "1"):
        f.write(untokenize(line) + "\n")
