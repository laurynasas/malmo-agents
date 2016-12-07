def _convert_grid_arr_to_3x3matrix(grid):
    matrix = [[],[],[]]
    row = []
    for i in xrange(len(grid)):
    	print len(grid)-1-i
        matrix[i/3] += [grid[len(grid)-1-i]]

    return matrix

print _convert_grid_arr_to_3x3matrix(range(9))