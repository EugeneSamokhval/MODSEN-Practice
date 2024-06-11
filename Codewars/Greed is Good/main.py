def score(dice):
    solo_ones = 0
    solo_fives = 0
    dice_counter = [0 for i in range(0, 6)]
    for entry in dice:
        dice_counter[entry-1] += 1
    results = 0
    results += (dice_counter[0]//3)*1000
    dice_counter[0] = dice_counter[0] % 3
    for entry in range(5):
        results += (dice_counter[entry+1]//3)*(200+entry*100)
        dice_counter[entry+1] = dice_counter[entry+1] % 3
    results += dice_counter[0]*100 + dice_counter[4]*50
    return results


print(score([5, 1, 3, 4, 1]))
