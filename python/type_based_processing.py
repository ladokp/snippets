from functools import singledispatch

# Base function using @singledispatch
@singledispatch
def process_data(data):
    """
    Default function for processing data.
    Raises an error if the type is unsupported.
    """
    raise TypeError(f"Unsupported data type: {type(data)}")

# Overload for strings
@process_data.register
def _(data: str):
    """
    Process string data by converting to uppercase.
    """
    return data.upper()

# Overload for integers
@process_data.register
def _(data: int):
    """
    Process integer data by returning its square.
    """
    return data ** 2

# Overload for lists
@process_data.register
def _(data: list):
    """
    Process list data by reversing it.
    """
    return data[::-1]

# Overload for dictionaries
@process_data.register
def _(data: dict):
    """
    Process dictionary by swapping keys and values.
    """
    return {v: k for k, v in data.items()}

# Example usage
if __name__ == "__main__":
    print(process_data("hello"))       # Output: "HELLO"
    print(process_data(5))            # Output: 25
    print(process_data([1, 2, 3]))    # Output: [3, 2, 1]
    print(process_data({"a": 1, "b": 2}))  # Output: {1: "a", 2: "b"}
    
    try:
        print(process_data(3.14))  # Unsupported type
    except TypeError as e:
        print(e)  # Output: Unsupported data type: <class 'float'>
    