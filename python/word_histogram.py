def word_histogram(text):
    """
    Generates a word frequency histogram from the given text.

    Args:
        text (str): The input text to analyze.

    Prints:
        A histogram displaying the frequency of each word in the text.
    """
    words = text.lower().split()
    words = tuple(map(lambda w: w.strip('.,!?;:"'), words))
    word_counts = {word: words.count(word) for word in set(words)}
    sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    for word, count in sorted_counts:
        print(f"{word:10}: {'#' * count}")


if __name__ == "__main__":
    text = input("Text: ") or """
    Python is amazing! Amazing tools, amazing community, and amazing code.
    Python is simple and elegant, yet powerful.
    """
    print("Word Frequency Histogram:")
    word_histogram(text)
