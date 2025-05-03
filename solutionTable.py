solution_table = [                                      #Players Hand Value
    #Dealers Card Value
    # 2    3    4    5    6    7    8    9    10   11
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"], #4
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"], #5
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"], #6
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"], #7
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"], #8
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"], #9
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"], #10
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"], #11
    ["D", "D", "S", "S", "S", "D", "D", "D", "D", "D"], #12
    ["S", "S", "S", "S", "S", "D", "D", "D", "D", "D"], #13
    ["S", "S", "S", "S", "S", "D", "D", "D", "D", "D"], #14
    ["S", "S", "S", "S", "S", "D", "D", "D", "D", "D"], #15
    ["S", "S", "S", "S", "S", "D", "D", "D", "D", "D"], #16
    ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"], #17
    ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"], #18
    ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"], #19
    ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"], #20
    ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"]  #21
]

soft_solution_table = [
    #  2    3    4    5    6    7    8    9    10   A
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],  # "Soft 12" (A+A)
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],  # Soft 13 (A+2)
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],  # Soft 14 (A+3)
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],  # Soft 15 (A+4)
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],  # Soft 16 (A+5)
    ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],  # Soft 17 (A+6)
    ["D", "S", "S", "S", "S", "D", "D", "D", "D", "D"],  # Soft 18 (A+7)
    ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # Soft 19 (A+8)
    ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # Soft 20 (A+9)
]
#Example if Dealers Card is 10 and Players Hand is 15
# You would access it by solution_table[15-4][10-2]
# Generic Formula for acessing
# solution_table[player_hand_value - 4][dealer_card_value - 2]


s = solution_table
