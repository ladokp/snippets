import random
from collections import Counter, namedtuple
from itertools import cycle, islice
from statistics import mean, median, mode, stdev

# Define a named tuple for data insights
DataInsights = namedtuple('DataInsights', 'mean median mode stdev most_common')

def generate_data(size=100, range_start=1, range_end=50):
    """Generates a random dataset."""
    return [random.randint(range_start, range_end) for _ in range(size)]

def analyze_data(data):
    """Analyzes the dataset and provides statistical insights."""
    data_counter = Counter(data)
    return DataInsights(
        mean=mean(data),
        median=median(data),
        mode=mode(data),
        stdev=stdev(data),
        most_common=data_counter.most_common(3)  # Top 3 most common elements
    )

def visualize_data(data):
    """Creates a simple text-based histogram."""
    data_counter = Counter(data)
    for value, count in data_counter.most_common():
        print(f"{value:2}: {'#' * count}")

def create_cyclic_pattern(data, pattern_size=10):
    """Creates a cyclic pattern from the dataset."""
    pattern = list(islice(cycle(data), pattern_size))
    return pattern

# Main Program
if __name__ == "__main__":
    # Step 1: Generate random data
    dataset = generate_data()

    # Step 2: Analyze the dataset
    insights = analyze_data(dataset)
    print("Data Insights:")
    print(f"  Mean: {insights.mean:.2f}")
    print(f"  Median: {insights.median}")
    print(f"  Mode: {insights.mode}")
    print(f"  Standard Deviation: {insights.stdev:.2f}")
    print(f"  Top 3 Most Common: {insights.most_common}")

    # Step 3: Visualize the dataset
    print("\nHistogram:")
    visualize_data(dataset)

    # Step 4: Create and display a cyclic pattern
    cyclic_pattern = create_cyclic_pattern(dataset, pattern_size=10)
    print("\nCyclic Pattern (10 elements):", cyclic_pattern)
