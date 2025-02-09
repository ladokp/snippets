def analyse_temperature_trend(temperatures: list[float]) -> str:
    """
    Analyzes the temperature trend.
    
    :param temperatures: List of temperature values
    :return: "increasing", "decreasing" or "inconsistent"
    """
    increasing = all(temperatures[i] < temperatures[i + 1] for i in range(len(temperatures) - 1))
    decreasing = all(temperatures[i] > temperatures[i + 1] for i in range(len(temperatures) - 1))
    
    if increasing:
        return "increasing"
    elif decreasing:
        return "decreasing"
    else:
        return "inconsistent"
