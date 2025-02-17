import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import os
from pprint import pprint

def process_function_input():
    try:
        equation_str = input("Enter the equation with single variable 'x' (e.g., x*sin(x) - x^2 + 1): ")

        x = sym.symbols('x')
        equation = sym.sympify(equation_str)

        interval_start = float(input("Enter the interval start: "))
        interval_end = float(input("Enter the interval end: "))

        degree = int(input("Enter the degree of the polynomial: "))

        x_vals = np.linspace(interval_start, interval_end, 200)
        y_vals = np.array([equation.subs(x, val) for val in x_vals], dtype=float)

        selected_x_vals = np.linspace(interval_start, interval_end, degree)
        selected_y_vals = np.array([equation.subs(x, val) for val in selected_x_vals], dtype=float)

        return x_vals, y_vals, selected_x_vals, selected_y_vals, interval_start, interval_end, degree
    except Exception as e:
        print(f"Error: {e}")


def process_file_input():
    try:
        file_path = input("Input your file path (CSV format): ")

        degree = int(input("Enter the number of points for interpolation: "))

        data = np.loadtxt(file_path, delimiter=',')

        data_sorted = data[data[:, 0].argsort()]

        x_vals = data_sorted[:, 0]
        y_vals = data_sorted[:, 1]

        interval_start = np.min(x_vals)
        interval_end = np.max(x_vals)

        selected_x_vals = np.linspace(interval_start, interval_end, degree)

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
    x = sym.symbols('x')
    A = np.vander(x_vals, degree + 1)  
    b = np.array(y_vals)
    coeffs = np.linalg.solve(A, b) 
    return sum(c * x**i for i, c in enumerate(coeffs))

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
      print("Select interpolation option:")
      print("    [0] Interpolation Polynomial solving SLE")
      print("    [1] Interpolation Polynomial using Lagrange")
      print("    [2] Parametric Interpolation")
      
      option = int(input("Option: "))
      
      if option == 0:
          # Solve using SLE
          poly = interpolate_sle(selected_x_vals, selected_y_vals, degree)
          print(f"Interpolation Polynomial (SLE): {poly}")
          return poly
      elif option == 1:
          # Solve using Lagrange
          poly = interpolate_lagrange(selected_x_vals, selected_y_vals)
          print(f"Interpolation Polynomial (Lagrange): {poly}")
          return poly
      elif option == 2:
          # Parametric interpolation (for x(t) and y(t))
          x_poly, y_poly = interpolate_parametric(selected_x_vals, selected_y_vals, degree)
          print(f"Parametric Interpolation Polynomials (x(t), y(t)): \n{x_poly}\n{y_poly}")
          return x_poly, y_poly
      else:
          print("Invalid option. Please select 0, 1, or 2.")
          continue








if __name__ == "__main__":
    pass