import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import os
from pprint import pprint

LAZY_NAME = None



def process_function_input():
    try:
        equation_str = input("Enter the equation with single variable 'x' (e.g., x*sin(x) - x^2 + 1): ")
        global LAZY_NAME 
        LAZY_NAME = equation_str

        x = sym.symbols('x')
        equation = sym.sympify(equation_str)

        interval_start = float(input("Enter the interval start: "))
        interval_end = float(input("Enter the interval end: "))

        degree = int(input("Enter the degree of the polynomial (We need a lot): "))

        x_vals = np.linspace(interval_start, interval_end, 200)
        y_vals = np.array([equation.subs(x, val) for val in x_vals], dtype=float)

        selected_x_vals = np.linspace(interval_start, interval_end, degree + 1)
        selected_y_vals = np.array([equation.subs(x, val) for val in selected_x_vals], dtype=float)

        return x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree
    except Exception as e:
        print(f"Error: {e}")


def process_file_input():
    try:
        file_path = input("Input your file path (CSV format): ")
        global LAZY_NAME        
        LAZY_NAME = f"DATA: {file_path}"

        degree = int(input("Enter the number of points for interpolation: "))

        data = np.loadtxt(file_path, delimiter=',')

        data_sorted = data[data[:, 0].argsort()]

        x_vals = data_sorted[:, 0]
        y_vals = data_sorted[:, 1]

        interval_start = np.min(x_vals)
        interval_end = np.max(x_vals)

        selected_x_vals = np.linspace(interval_start, interval_end, degree + 1)

        selected_y_vals = np.interp(selected_x_vals, x_vals, y_vals)

        return x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree

    except FileNotFoundError:
        print("Error: The file was not found. Please check the file path.")
    except ValueError as e:
        print(f"Error: Invalid data in the file. Please ensure the file contains numeric data. ({e})")
    except Exception as e:
        print(f"Error: {e}")


def call_input_options():
    while True:
        print("Types of input")
        print("    [0] String ")
        print("    [1] File (.csv)")

        option = input("Option: ")

        x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree = None, None, None, None, None, None, None

        if option == "0":
            x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree = process_function_input()
        elif option == "1":
            x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree = process_file_input()
        else:
            continue

        print("\n\n\n\n\n")

        break

    return x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree






def interpolate_sle(x_vals, y_vals, degree):
    pprint(x_vals)
    pprint(len(x_vals))
    x = sym.symbols('x')
    
    A = np.vander(x_vals, len(x_vals))
    pprint(A)
    
    b = np.array(y_vals)

    pprint(b)
    
    coeffs = np.linalg.solve(A, b)

    pprint(coeffs)
    
    poly = sum(c * x**i for i, c in enumerate(coeffs))
    
    return poly


def interpolate_lagrange(x_vals, y_vals):
    x = sym.symbols('x')
    n = len(x_vals)
    L = 0
    for i in range(n):
        term = y_vals[i]
        for j in range(n):
            if i != j:
                term *= (x - x_vals[j]) / (x_vals[i] - x_vals[j])
        L += term
    return L

def interpolate_parametric(x_vals, y_vals, degree):
    t = sym.symbols('t')
    x_poly = interpolate_lagrange(np.linspace(0, 1, len(x_vals)), x_vals)
    y_poly = interpolate_lagrange(np.linspace(0, 1, len(y_vals)), y_vals)
    return x_poly, y_poly

def call_interpolation_options(selected_x_vals, selected_y_vals, degree):
    while True:
      print("\n\n\n\n\n")
      print("Select interpolation option:")
      print("    [0] Interpolation Polynomial solving SLE")
      print("    [1] Interpolation Polynomial using Lagrange")
      print("    [2] Parametric Interpolation")
      
      option = int(input("Option: "))
      
      if option == 0:
          # Solve using SLE
          poly = interpolate_sle(selected_x_vals, selected_y_vals, degree)
          print(f"Interpolation Polynomial (SLE): {poly}")
          return poly, None
      elif option == 1:
          # Solve using Lagrange
          poly = interpolate_lagrange(selected_x_vals, selected_y_vals)
          print(f"Interpolation Polynomial (Lagrange): {poly}")
          return poly, None
      elif option == 2:
          # Parametric interpolation (for x(t) and y(t))
          x_poly, y_poly = interpolate_parametric(selected_x_vals, selected_y_vals, degree)
          print(f"Parametric Interpolation p_x (x(t), y(t)): \n{x_poly}\n{y_poly}")
          return x_poly, y_poly
      else:
          print("Invalid option. Please select 0, 1, or 2.")
          continue





def calculate_interpolation_at(poly, x_val):
    return poly.subs(sym.symbols('x'), x_val)

def calculate_interpolation_all(poly, interval_start, interval_end):
    x_vals = np.linspace(interval_start, interval_end, 200)
    y_vals = np.array([calculate_interpolation_at(poly, x) for x in x_vals], dtype=float)
    return x_vals, y_vals

def calculation():
    x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree = call_input_options()

    while True:
        print("Select calculation type:")
        print("    [0] Plot")
        print("    [1] Single point")
        option = input("Option: ")

        p_x, p_y = call_interpolation_options(selected_x_vals, selected_y_vals, degree)

        if option == "0":
            
            if p_y != None:
                x_poly, y_poly = p_x, p_y
                t, intp_x_vals = calculate_interpolation_all(x_poly, interval_start, interval_end)
                t, intp_y_vals = calculate_interpolation_all(y_poly, interval_start, interval_end)
                # plt.plot(intp_x_vals, intp_y_vals, label="Interpolated Curve")
                # plt.scatter(selected_x_vals, selected_y_vals, color='red', label="Data Points")
                # plt.legend()
                # plt.show()
            else:
                intp_x_vals, intp_y_vals = calculate_interpolation_all(p_x, interval_start, interval_end)
                # plt.plot(intp_x_vals, intp_y_vals, label="Interpolated Curve")
                # plt.scatter(selected_x_vals, selected_y_vals, color='red', label="Data Points")
                # plt.legend()
                # plt.show()

            print("\n\n\n\n\n")
        
            return intp_x_vals, intp_y_vals, x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree
        
        if option == "1":
            print(f"Calculate interpolation from {interval_start} to {interval_end}")
            input_x = float(input("Calculate interpolation at x = "))
            intp_x_vals, intp_y_vals, x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree = None, None, None, None, None, None, None, None, None
            degree = "RETURN VALUE"
            intp_x_vals = input_x
            intp_y_vals = calculate_interpolation_at(p_x, input_x)

            
            print("\n\n\n\n\n")

            return intp_x_vals, intp_y_vals, x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree
        
        else:
            print("Invalid option. Please select 0, or 1.")
       
        print("\n\n\n\n\n")






def plot_original(x_vals, y_vals):
    plt.plot(x_vals, y_vals, label="Original Data")

def plot_interpolation(intp_x_vals, intp_y_vals):
    plt.plot(intp_x_vals, intp_y_vals, label="Interpolated Curve") 

def plot_master(intp_x_vals, intp_y_vals, x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end):
    plt.title(f"{LAZY_NAME} from [{interval_start}, {interval_end}]")
    plt.scatter(selected_x_vals, selected_y_vals, color='red', label="Data Points")

    plot_original(x_vals, y_vals)
    plot_interpolation(intp_x_vals, intp_y_vals)

    plt.legend()
    plt.show()




def run_master():
    intp_x_vals, intp_y_vals, x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree = calculation()

    if degree == "RETURN VALUE":
        print(f"Interpolation of {LAZY_NAME}")
        print(f"At x = {intp_x_vals} is {intp_y_vals}")
    else:
        plot_master(intp_x_vals, intp_y_vals, x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end)


if __name__ == "__main__":
    run_master()