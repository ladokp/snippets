from functools import singledispatch
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
def _(data: str) -> str:
    """
    Process string data by converting to uppercase.
    """
    return data.upper()

# Overload for integers
@process_data.register
def _(data: int) -> int:
    """
    Process integer data by returning its square.
    """
    return data ** 2

# Overload for lists
@process_data.register
def _(data: list) -> list:
    """
    Process list data by reversing it.
    """
    return data[::-1]

# Overload for dictionaries
@process_data.register
def _(data: dict) -> dict:
    """
    Process dictionary by swapping keys and values.
    """
    return {v: k for k, v in data.items()}

# Overload for floats
@process_data.register
def _(data: float) -> float:
    """
    Process float data by rounding to two decimal places.
    """
    return round(data, 2)

# Overload for tuples
@process_data.register
def _(data: tuple) -> tuple:
    """
    Process tuple data by sorting it.
    """
    return tuple(sorted(data))

# Overload for sets
@process_data.register
def _(data: set) -> set:
    """
    Process set data by converting it to a sorted list.
    """
    return sorted(data)

# Example usage
def main():
    examples = [
        "hello",
        5,
        [1, 2, 3],
        {"a": 1, "b": 2},
        3.14159,
        (3, 1, 2),
        {3, 1, 2}
    ]
    
    for example in examples:
        try:
            result = process_data(example)
            logging.info(f"Processed data: {result}")
        except TypeError as e:
            logging.error(e)

if __name__ == "__main__":
    main()
