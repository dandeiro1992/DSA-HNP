from DSA_attack import *

path_parameters = os.getcwd() + "\\nygma_keys.txt"
path_results = os.getcwd() + "\\nygma_results.txt"
dimension = 30
number_of_bits_known = 5
message_length=25
number_of_signatures=100
p_length = 64
q_length = 10
# przygotowanie parametrów
p, q = parameters(p_length, q_length)
p, q, g = params(path_parameters, p, q)
x, y = key_pair_for_user(path_parameters, p, q, g)

# przygotowanie podpisów w pliku
results_in_file(path_results, p, q, g, x, message_length, number_of_signatures)
t, u = attack(path_results, dimension, number_of_bits_known, q)
basis=create_basis_2(t, u ,dimension,number_of_bits_known, q)
output=get_new_basic_lll(basis)
print(output)

print(u[0:dimension-1])
