from DSA_attack import *

path_parameters = os.getcwd() + "/nygma_keys.txt"
path_results = os.getcwd() + "/nygma_results.txt"
dimension = 12
number_of_bits_known = 7
message_length = 100
number_of_signatures = 100
p_length = 100
q_length = 40
# przygotowanie parametrów
p, q = parameters(p_length, q_length)
p, q, g = params(path_parameters, p, q)
x, y = key_pair_for_user(path_parameters, p, q, g)

# przygotowanie podpisów w pliku
results_in_file(path_results, p, q, g, x, message_length, number_of_signatures)
t, u = attack(path_results, dimension, number_of_bits_known, q)
basis = create_basis(t, u, dimension, number_of_bits_known, q)
output = get_new_basic_lll(basis)
get_secret_key(output, find_second(output), dimension, q)
print("q: ", q)
print("x: ", x)

# # print(output)
# # sum = []
# # for i in output:
# #     suma=0
# #     for k in i:
# #         suma=suma+k*k
# #     sum.append(suma)
# # print(sum)
# # print(list(zip(output,sum)))
# # print(u[0:dimension + 2])
# # print(q)
# # print(x)
# # for i in output:
# #     print(str(i[dimension-1]%q)+"\n")
# #
# # print(find_second(output))
# # print(get_secret_key(output,find_second(output),dimension,q))
# dimension=14
# basis = [[26385864255373312, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 26385864255373312, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 26385864255373312, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 26385864255373312, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 26385864255373312, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 26385864255373312, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 26385864255373312, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 26385864255373312, 0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0, 26385864255373312, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0, 0, 26385864255373312, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26385864255373312, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26385864255373312, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26385864255373312, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26385864255373312, 0, 0],
#          [228561596134, 205775004408, 794408716733, 479752040156, 87728974275, 680399626135, 255902343203, 360058597374,
#           333431288176, 59361477700, 287953918046, 625233622554, 680333190207, 717290012402, 1, 0],
#          [130522716854, 64816177718, 681542212515, 10922969654, 434636689732, 366394835170, 618885095178, 552718237541,
#           628711217394, 393193633719, 201915326982, 782634435932, 509388878192, 462311240559, 0, 805232673809]]
# output = olll.reduction(basis, 0.75)
# print(output)
# q=805232673809
# sum = []
# for i in output:
#     suma=0
#     for k in i:
#         suma=suma+k*k
#     sum.append(suma)
# print(sum)
# print(list(zip(output,sum)))
#
# for i in output:
#     print(str(i[dimension-1]%q)+"\n")
#
# print(find_second(output))
# print(get_secret_key(output,find_second(output),dimension,q))