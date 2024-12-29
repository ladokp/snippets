import calendar

def display_year_calendar(year):
    # Erstellen eines Textkalenders
    cal = calendar.TextCalendar(calendar.MONDAY)
    print(f"Kalender für das Jahr {year}:\n")
    
    for month in range(1, 13):
        # Monatstitel ausgeben
        print(cal.formatmonth(year, month))

def main():
    print("Kalender für ein bestimmtes Jahr")
    try:
        # Benutzereingabe für das Jahr
        year = int(input("Bitte geben Sie das Jahr ein (z.B. 2025): "))
        if year < 1:
            raise ValueError("Das Jahr muss positiv sein.")
        display_year_calendar(year)
    except ValueError as e:
        print(f"Fehlerhafte Eingabe: {e}")

if __name__ == "__main__":
    main()