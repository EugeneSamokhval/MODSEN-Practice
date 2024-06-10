# Return an array with the same shape as the input
def bounding_box(image_array):
    if not len(image_array):
        return image_array
    left, right, top, bottom = len(image_array[0]), 0, len(image_array), 0
    empty = True
    for row in image_array:
        if 1 in row:
            empty = False
            break
    if empty:
        return image_array
    else:
        rows_counter = 0
        for row in image_array:
            back_pointer = len(row)-1
            for i in range(len(row)):
                if row[i] and i < left:
                    left = i
                if row[i] and i > right:
                    right = i
                if row[i] and rows_counter < top:
                    top = rows_counter
                if row[i] and rows_counter > bottom:
                    bottom = rows_counter
                back_pointer -= 1
            rows_counter += 1
        box = [[0 for j in range(len(image_array[0]))]
               for i in range(len(image_array))]
        for i in range(right-left):
            box[top][left+i] = 1
            box[bottom][left+i] = 1
        for i in range(bottom-top):
            box[top+i][left] = 1
            box[top+i][right] = 1
        box[bottom][right] = 1
        return box


for row in bounding_box(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]
):
    print(row)
