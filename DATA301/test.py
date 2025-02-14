#import the dask and bag library
import dask
import dask.bag as db
import math

# First, let's create some simple data, say the integers from 1 to 1000.
# We use the python command range to do this.
# Note that in practice our data will most likely come from data files.
A = range(1000)

# Let us start with a simple task of computing the sum of the values in the array:
print(sum(A))
# Because A is in memory in our Google Colab python instance and sum is a built in python function
# this computation is not distributed and instead runs sequentially.

# Now let us distribute this data across our processes in a dask bag
bA = db.from_sequence(A)

# # To sum our distributed array, we call the reduce function with the sum function
# print(bA.reduction(sum, sum).compute())
# # Because the data structure bA was distributed across the available processes, the computation for reduction was also distributed.

# Because summing along an array axis is very common, we could simply call the built-in function that does the reduction efficiently
print(bA.sum().compute())

