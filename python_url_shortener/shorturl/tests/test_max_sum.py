

def max_sum_walk(matrix):
    """ Computes the maximal sum walk from the left top corner to the bottom right corner, as the numbers are
    "collected", assumes the numbers can be summed only once. b) hints at that we should memoize the intermediate
    results, in general as we can only move to the right or down, the resulting matrix would be:
    maxsum[y][x] = max(maxsum[y-1][x], maxsum[y][x-1]) + matrix[y][x], with the special cases at y=0 and x=0,
    where we are only able to arrive from the cell to the left or the one above, respectively.
    @:param matrix: n by m list of lists with positive integers """

    ydim = len(matrix)
    xdim = len(matrix[0])

    # empty matrix special case, returns 0
    if not (ydim and xdim):
        return 0

    max_sum_matrix = [[0] * xdim for _ in range(ydim)]
    max_sum_matrix[0][0] = matrix[0][0]

    for x in range(1, xdim):
        max_sum_matrix[0][x] = max_sum_matrix[0][x-1] + matrix[0][x]

    for y in range(1, ydim):
        max_sum_matrix[y][0] = max_sum_matrix[y-1][0] + matrix[y][0]

    for y in range(1, ydim):
        for x in range(1, xdim):
            max_sum_matrix[y][x] = max(max_sum_matrix[y-1][x], max_sum_matrix[y][x-1]) + matrix[y][x]

    return max_sum_matrix[ydim-1][xdim-1]

def test_max_sum_walk():
    matrix = [[1, 5, 7, 10], [3, 13, 14, 15], [6, 16, 19, 25]]
    print("max for matrix {}".format(matrix))
    print(max_sum_walk(matrix))
    matrix = [[1]]
    print("max for matrix {}".format(matrix))
    print(max_sum_walk(matrix))
    matrix = [[]]
    print("max for matrix {}".format(matrix))
    print(max_sum_walk(matrix))


test_max_sum_walk()
