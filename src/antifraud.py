from graph_algorithms import Graph
from read_processing_files import read_into_list_of_tuples
import sys

###############################
# read files
###############################

# folder names
input_dir = "../paymo_input/"
output_dir = "../paymo_output/"

# input files
batch_name  = input_dir + sys.argv [1]
stream_name = input_dir + sys.argv [2]
# output files
out1 = output_dir + sys.argv [3]
out2 = output_dir + sys.argv [4]
out3 = output_dir + sys.argv [5]
# verbosity
if len (sys.argv) >= 7 and sys.argv [6] == "True":
        verbose = True
else:
    verbose = False
    
# def function that prints only if verbose is turned on
def print_if_verbose (message, end = '\n'):
    if verbose:
        print (message, end = end)
    else:
        None
    return None

print_if_verbose ('\ninput files: {}, {}'.format (batch_name, stream_name))
print_if_verbose ('\noutput files: {}, {}, {}'.format (out1, out2, out3))


# read batch
print_if_verbose ("\nparsing {} into a list to tuples...".format (batch_name), end = '')
batch0 = read_into_list_of_tuples (batch_name)
print_if_verbose ("finished")

# converting batch into a graph
print_if_verbose ("\ncreating a graph of transactions based on {}...".format (batch_name), end = '')
batch = Graph (batch0)
print_if_verbose ("finished")

# read stream
print_if_verbose ("\nparsing {} into a list to tuples...".format (stream_name), end = '')
stream = read_into_list_of_tuples (stream_name)
print_if_verbose ("finished")






###############################
# process stream file according to the different features
###############################
end = '\n'
msg_true = "trusted" + end
msg_false = "unverified" + end

## Feature 1
print_if_verbose ("\nBeginning feature 1: transactions separated by no more than 1 degree is considered verified")

# Make deep copy of the batch graph
feature = batch.copy ()

with open (out1, 'w') as output:
    for pair in stream:
        # First, check if prior transaction exists. If so, no need to add edge to graph
        if feature.degree_lte (pair, degree = 1): # transaction existed
            output.write (msg_true)
        else:
            output.write (msg_false)
            
            # add edge after determining degree of separation
            feature.add_edge (pair)
print_if_verbose ('finished')
        
## Feature 2
print_if_verbose ("\nBeginning feature 2: transactions separated by no more than 2 degree is considered verified")
# Make deep copy of the batch graph
feature = batch.copy ()

with open (out2, 'w') as output:
    for pair in stream:
        # First, check if prior transaction exists. If so, no need to add edge to graph
        if feature.degree_lte (pair, degree = 1):
            output.write (msg_true)
        else:
            # determine if <= 2 degrees of separation
            lte = feature.degree_lte (pair, degree = 2)
            output.write (msg_true if lte else msg_false)
            
            # add edge after determining degree of separation
            feature.add_edge (pair)
print_if_verbose ('finished')



## Feature 3
print_if_verbose ("\nBeginning feature 3: transactions separated by no more than 4 degree is considered verified")
# Make deep copy of the batch graph
feature = batch.copy ()

with open (out3, 'w') as output:
    for pair in stream:
        # First, check if prior transaction exists. If so, no need to add edge to graph
        if feature.degree_lte (pair, degree = 1):
            output.write (msg_true)
        else:
            # determine if <= 4 degrees of separation
            lte = feature.degree_lte (pair, degree = 4)
            output.write (msg_true if lte else msg_false)

            # add edge after determining degree of separation
            feature.add_edge (pair)
print_if_verbose ('finished')
