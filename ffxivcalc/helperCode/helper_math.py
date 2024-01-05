import math

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0): # Helper function to compare float
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def roundDown(x, precision):
    print("hello : " + str(x))
    return math.floor(x * 10**precision)/10**precision

def roundUp(x, precision):
    return math.ceil(x * 10**precision)/10**precision