from ctypes import *

libc = cdll.LoadLibrary("./linear_threshold_function/test.so")
libc.get_cost.restype = c_double
libc.get_cost.argtypes = (c_int, c_int, POINTER(c_double))
k = 4
n = 7
p_with_order = [0.01,0.01,0.01,0.5,0.99,0.99,0.99]
c = libc.get_cost(k, n, (c_double * len(p_with_order))(*p_with_order))
print(c)

