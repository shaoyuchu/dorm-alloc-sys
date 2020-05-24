


#first choice, second choice, third choice, not my choice
cost_table = [1, 5, 10, 100]
# all_rooms = [ [room_type+"_"+str(i) for room_type in all_room_types] for i in range(4) ]

# def compute_cost_matrix(students):
#     cost_matrix = []
#     for i in range(len(students)):
#         prefs_lis = list(students.iloc[i][1:4])
#         #init a student's cost_lis with no matching costs
#         cost_lis = [cost_table[3] for i in range(len(all_room_types_symbol))]
#         for j in range(len(prefs_lis)):
#             if prefs_lis[j] == all_room_types_symbol[0]:
#                 cost_lis[0] = cost_table[j]
#             elif prefs_lis[j] == all_room_types_symbol[1]:
#                 cost_lis[1] = cost_table[j]
#             elif prefs_lis[j] == all_room_types_symbol[2]:
#                 cost_lis[2] = cost_table[j]
#             elif prefs_lis[j] == all_room_types_symbol[3]:
#                 cost_lis[3] = cost_table[j]
#             elif prefs_lis[j] == all_room_types_symbol[4]:
#                 cost_lis[4] = cost_table[j]
#             elif prefs_lis[j] == all_room_types_symbol[5]:
#                 cost_lis[5] = cost_table[j]
#         cost_matrix.append(cost_lis)
#     return cost_matrix


# m = Munkres()

# cost_matrix = compute_cost_matrix(students)
# indexes = m.compute(cost_matrix)
# print_matrix(cost_matrix, msg='Lowest cost through this matrix:')
# total = 0
# for row, column in indexes:
#     value = cost_matrix[row][column]
#     total += value
#     print ("(%d, %d) -> %d"%(row, column, value))
# print ("total cost: %d"% (total))
