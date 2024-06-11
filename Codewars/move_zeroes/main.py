def move_zeros(lst: list):
    zeroes_count = lst.count(0)
    for i in range(zeroes_count):
        lst.remove(0)
        lst.append(0)
    return lst


print(move_zeros([1, 0, 1, 2, 0, 1, 3]))
