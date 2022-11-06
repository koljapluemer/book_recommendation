import json

# open out/matrix.json and print last line
with open('out/matrix.json') as f:


    for line in f:
        pass
    # get the 5 highest values of the last line and print them and their indices
    # first, remove all values below 4
    # use memory friendly method
    print('reducing list to only values above 4')
    reduced_line = [float(x) for x in line.split() if float(x) > 4]
    print('sorting to find highest values')
    highest_values = sorted(reduced_line, reverse=True)[:5]
    print('finding indices of highest values')
    highest_values_indices = [line.index(x) for x in highest_values]
    print('========= Here are the 5 highest values of the last line of the matrix:')
    print('HIGHEST VALUES:', highest_values)
    print('HIGHEST VALUES INDICES:', highest_values_indices)