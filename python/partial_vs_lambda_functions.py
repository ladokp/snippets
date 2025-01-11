from functools import partial

# Base function to demonstrate differences
def operation(x, y, z):
    return (x + y) * z

# Using functools.partial to create specialized versions
add_and_double = partial(operation, z=2)  # Pre-fills z=2
add_10_and_multiply = partial(operation, x=10)  # Pre-fills x=10

# Using lambda to achieve similar functionality
add_and_double_lambda = lambda x, y: (x + y) * 2  # Dynamic version of add_and_double
add_10_and_multiply_lambda = lambda y, z: (10 + y) * z  # Dynamic version of add_10_and_multiply

# Test values
x, y, z = 5, 3, 4

print("=== Using functools.partial ===")
print(f"add_and_double({x}, {y}): {add_and_double(x, y)}")  # Output: (5 + 3) * 2 = 16
print(f"add_10_and_multiply({y}, {z}): {add_10_and_multiply(y, z)}")  # Output: (10 + 3) * 4 = 52

print("\n=== Using lambda ===")
print(f"add_and_double_lambda({x}, {y}): {add_and_double_lambda(x, y)}")  # Output: (5 + 3) * 2 = 16
print(f"add_10_and_multiply_lambda({y}, {z}): {add_10_and_multiply_lambda(y, z)}")  # Output: (10 + 3) * 4 = 52

# Showing flexibility of lambda
print("\n=== Custom behavior with lambda ===")
custom_behavior = lambda x, y: (x + y) ** 2  # New logic not tied to the original function
print(f"custom_behavior({x}, {y}): {custom_behavior(x, y)}")  # Output: (5 + 3)^2 = 64

# Attempting invalid use cases
print("\n=== Invalid use cases ===")
try:
    # partial cannot define new logic
    invalid_partial = partial(operation, x=lambda a: a ** 2)
    print(f"Invalid partial: {invalid_partial(3, z)}")  # Will raise a TypeError
except Exception as e:
    print(f"Invalid partial raised: {e}")

try:
    # Lambda allows errors if improperly defined
    error_lambda = lambda a, b: b / a  # Division by zero
    print(f"Error lambda: {error_lambda(0, 5)}")  # Will raise a ZeroDivisionError
except Exception as e:
    print(f"Error lambda raised: {e}")
