"""Menu:
1. Show flight by ID
2. Show flights by date
3. Delayed flights by airline
4. Delayed flights by origin airport
5. Exit
"""
from data import FlightData

def display_results(results):
    if not results:
        print("No results found.\n")
        return

    for row in results:
        print("-" * 40)
        for key, value in row.items():
            print(f"{key}: {value}")
    print("-" * 40 + "\n")


def main():
    db_uri = "sqlite:///data/flights.sqlite3"  # Update this if your DB file name is different
    flight_data = FlightData(db_uri)

    while True:
        print("Menu:")
        print("1. Show flight by ID")
        print("2. Show flights by date")
        print("3. Delayed flights by airline")
        print("4. Delayed flights by origin airport")
        print("5. Exit")

        choice = input("Select an option (1-5): ")

        if choice == "1":
            flight_id = input("Enter Flight ID: ")
            results = flight_data.get_flight_by_id(flight_id)
            display_results(results)

        elif choice == "2":
            date = input("Enter date (YYYY-MM-DD): ")
            results = flight_data.get_flights_by_date(date)
            display_results(results)

        elif choice == "3":
            airline = input("Enter airline name: ")
            results = flight_data.get_delayed_flights_by_airline(airline)
            display_results(results)

        elif choice == "4":
            origin = input("Enter origin airport code (e.g. JFK): ")
            results = flight_data.get_delayed_flights_by_origin(origin)
            display_results(results)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose between 1 and 5.\n")


if __name__ == "__main__":
    main()
