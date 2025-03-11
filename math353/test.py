def Bisection(a, b):
    input("Press Enter to continue...")
    c = (a+b)/2
    print(c)
    if f(c)*f(b)<0:
        Bisection(c, b)
    elif f(c)*f(a)<0:
        Bisection(c, a)
    elif f(c)==0:
        print(c)

def f(x):
    #return pow(x, 3)+ x + 1
    return pow(x, 4) - pow(x,3)- 10
a = 1.5
b = 2.5
#print(f(a)*f(b))
# if f(a)*f(b)<0:
#         Bisection(a, b)
# else:
#     print("Oops! The root of function doesn't belong to the above domain\nPlease try to again:")
    
    

def newton_method(f, f_prime, x0, tol=1e-6, max_iter=100):
    """
    Find a root of a function using Newton's method.

    Parameters:
    f (function): The function whose root is to be found.
    f_prime (function): The derivative of the function f.
    x0 (float): Initial guess for the root.
    tol (float, optional): Tolerance for convergence. Defaults to 1e-6.
    max_iter (int, optional): Maximum number of iterations. Defaults to 100.

    Returns:
    float: The approximated root.

    Raises:
    ValueError: If the derivative is zero at any iteration.
    Exception: If the method does not converge within max_iter iterations.
    """
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        fp = f_prime(x)
        if fp == 0:
            raise ValueError("Derivative is zero. Cannot continue.")
        delta_x = fx / fp
        x -= delta_x
        if abs(delta_x) < tol:
            return x
    raise Exception("Maximum iterations reached. No convergence.")

def f(x):
    return 


import numpy
def test(t):
    a = numpy.array([[1, 2,3,t], [5,6,t,8],[9,t,11,12],[t,14,15,16]])
    return numpy.linalg.det(a)


#E2Q6(4,12)
def E2Q6():

    import numpy as np
    def f(t):
        matrix = np.array([
            [1, 2, 3, t],
            [5, 6, t, 8],
            [9, t, 11, 12],
            [t, 14, 15, 16]
        ])
        return np.linalg.det(matrix) - 1000



    # Initial interval where f(a) and f(b) have opposite signs
    a = 0.0
    b = 20.0
    tolerance = 1e-6
    max_iterations = 100

    # Verify that the initial interval brackets a root
    if f(a) * f(b) >= 0:
        raise ValueError("Initial interval does not bracket a root. Adjust a and b.")

    # Bisection method
    for _ in range(max_iterations):
        c = (a + b) / 2
        fc = f(c)
        if abs(fc) < tolerance:
            break
        if fc * f(a) < 0:
            b = c
        else:
            a = c

    print(f"The value of t is approximately {c:.6f}")




# Week 4 L2 example in class 
#solve exp(x1^2+x2^2)-1
#      exp(x1^2-x2^2)-1

def W4L2():
    from sympy import symbols, exp, diff, solve, Matrix

    # make matrix func
    JF = lambda x: Matrix([[2*x[0]*exp(x[0]**2+x[1]**2), 2*x[1]*exp(x[0]**2+x[1]**2)], [2*x[0]*exp(x[0]**2-x[1]**2), -2*x[1]*exp(x[0]**2-x[1]**2)]])
    F = lambda x : Matrix( [exp(x[0]**2+x[1]**2)-1, exp(x[0]**2-x[1]**2)-1])   
    x = Matrix([[0.1],[ 0.1]]) # starting point
    for i in range(10):
        # Newton's method
        x = x - JF(x).LUsolve(F(x))
        print(F(x).norm())
#W4L2()

