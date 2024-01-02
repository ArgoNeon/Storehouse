import random as rand

def rand_choice(range_list, weights):
    lower_border    = 0
    higher_border   = 1
    sum_weights     = 0
    weight_border   = 0

    first_list_element = range_list[0]

    borders = []
    choice  = first_list_element

    random_number = rand.random()

    for weight in weights:
        sum_weights = sum_weights + weight

    for weight in weights:
        weight_border = weight_border + weight / sum_weights
        borders.append(weight_border)

    for i in range(len(borders)):
        if (random_number < borders[i]):
            choice = range_list[i]
            break
    return choice
