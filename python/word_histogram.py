def word_histogram(text):
    """Generates a word frequency histogram using Python's built-in functions."""
    # Split text into words
    words = text.lower().split()

    # Remove punctuation using `str.strip`
    words = map(lambda w: w.strip('.,!?;:"'), words)

    # Count word frequencies using `dict` and `set`
    word_counts = {word: words.count(word) for word in set(words)}

    # Sort the dictionary by frequency using `sorted`
    sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Display as a histogram
    for word, count in sorted_counts:
        print(f"{word:10}: {'#' * count}")


if __name__ == "__main__":
    # Example usage
    text = """
    Python is amazing! Amazing tools, amazing community, and amazing code.
    Python is simple and elegant, yet powerful.
    """
    print("Word Frequency Histogram:")
    word_histogram(text)
