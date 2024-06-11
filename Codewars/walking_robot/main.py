def robot_transfer(matrix, k):
    matrix_conv = [[i.split(',')
                    for i in row] for row in matrix]
    matrix_conv = [[[int(j) for j in i] for i in row] for row in matrix_conv]

    def walk(matrix, starting_point, current_step, k, beginig):
        if current_step < k:
            if (starting_point != beginig) or (current_step == 0):
                return walk(matrix, matrix[starting_point[0]]
                            [starting_point[1]], current_step+1, k, beginig)
            else:
                return 0
        elif (current_step == k) and (starting_point == beginig):
            return 1
        else:
            return 0
    result = 0
    i = 0
    for row in matrix_conv:
        j = 0
        for entry in row:
            result += walk(matrix_conv, [i, j], 0, k, [i, j])
            j += 1
        i += 1
    return result


print(robot_transfer([['1,0', '1,1', '2,1'], [
      '0,0', '1,0', '0,2'], ['2,1', '1,1', '1,1']], 2))
