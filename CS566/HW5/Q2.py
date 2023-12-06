"""
Theta: (k*log(k)), k is the number of polynomial terms (due to sorting)
HW5 Problem 2
Author: Jiankun Dong
Adding 2 polynomials in string form
"""
import re
def parse_polynomial(poly_str):
    # the default regex for python 
    # because the pattern is fixed (Cx**n), the function has
    # theta(n)
    monomials = re.findall(r'(-?\d*)x\*?\*?(\d*)', poly_str)
    poly_dict = {}
    for coef, exp in monomials:
        ## special case for '-X**n'
        if coef == '-':
            coef = -1
        coef = int(coef) if coef else 1
        exp = int(exp) if exp else 1 #'Cx' term
        poly_dict[exp] = poly_dict.get(exp, 0) + coef
    ## handle constant term:
    # constant term does exsist if the last one is 'x' or '*constant'
    if (poly_str[-1] != 'x') and (poly_str[-2]!='*'):
        ##constant exsist
        poly_dict[0] = int(re.findall(r'(-?\d*)',poly_str)[-2])
    return poly_dict
def polynomial_dict_to_string(poly_dict):
    terms = []
    # sorting takes O(klogk), k is the number of polynomials
    for exp, coef in sorted(poly_dict.items(), reverse=True):
        if coef != 0:
            term = f"{coef:+d}" if coef >= 0 else f"{coef:-d}"
            if term == '+1':
                term = '+'
            term += f"x**{exp}" if exp > 1 else "" if exp == 0 else "x"
            terms.append(term)
    if terms[0][0] == '+':
        terms[0]=terms[0][1:]
    return ''.join(terms) if terms else "0"

def add_polynomials(poly1, poly2):
    result_dict = poly1.copy()
    for exp, coef in poly2.items():
        result_dict[exp] = result_dict.get(exp, 0) + coef
    return result_dict
def subtract_polynomials(poly1, poly2):
    result_dict = poly1.copy()
    for exp, coef in poly2.items():
        result_dict[exp] = result_dict.get(exp, 0) - coef
    return result_dict
def simplify_polynomials(inputStr):
    inputLS = inputStr.split(',')
    poly1 = inputLS[0] 
    poly2 = inputLS[2] 
    operator = inputLS[1]
    # Parse input polynomials
    poly1_dict = parse_polynomial(poly1)
    poly2_dict = parse_polynomial(poly2)
    # Perform the operation
    if operator == '+':
        result_dict = add_polynomials(poly1_dict, poly2_dict)
    elif operator == '-':
        result_dict = subtract_polynomials(poly1_dict, poly2_dict)
    else:
        return "Invalid operator. Use '+' or '-'."
    # Convert the result back to a polynomial string
    result_poly = polynomial_dict_to_string(result_dict)
    return result_poly

if __name__ == "__main__":
    #testing 
    #1
    expected1 = "4x**5+x**3+3x**2-3x+4"
    r1 = simplify_polynomials("x**3+5x**2-3x+3,+,4x**5-2x**2+1")
    if r1 == expected1:
        print("Test 1 passed!")
    print(f"Result: {r1}")
    2
    expected2 = "2x**5+2x**2-3x+4"
    r2 = simplify_polynomials("x**6+5x**5-3x+3,-,x**6+3x**5-2x**2-1")
    if r2 == expected2:
        print("Test 2 passed!")
    print(f"Result: {r2}")
    3
    expected3 = "8x**5-2x**2-3x-4"
    r3 = simplify_polynomials("x**6+5x**5-3x-3,+,-x**6+3x**5-2x**2-1")
    if r3 == expected3:
        print("Test 3 passed!")
    print(f"Result: {r3}")
