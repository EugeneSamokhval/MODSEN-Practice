def descending_order(num):
    num_str = str(num)
    num_arr = [int(i) for i in num_str]
    num_arr.sort(reverse=True)
    num_str = ''
    for number in num_arr:
        num_str += str(number)
    return int(num_str)


print(descending_order(214127))
