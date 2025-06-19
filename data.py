from sqlalchemy import create_engine, text
from datetime import datetime

QUERY_FLIGHT_BY_ID = """
SELECT
  flights.*,
  airlines.AIRLINE   AS airline,
  flights.ID         AS FLIGHT_ID,
  flights.DEPARTURE_DELAY AS DELAY
FROM flights
JOIN airlines ON flights.AIRLINE = airlines.ID
WHERE flights.ID = :id
"""

class FlightData:
    """
    DAL for flights.sqlite3. Keeps a single SQLAlchemy engine alive
    for all queries, and exposes methods for each report.
    """
    def __init__(self, db_uri):
        """
        Initialize a new engine using the given database URI.
        """
        self._engine = create_engine(db_uri)

    def _execute_query(self, query, params):
        """
        Execute an SQL query with the params provided in a dictionary,
        and return a list of dictionary-like results.
        """
        try:
            with self._engine.connect() as conn:
                result = conn.execute(text(query), params)
                return list(result.mappings())  # 🔥 FIXED here
        except Exception as e:
            print("Query failed:", e)
            return []

    def get_flight_by_id(self, flight_id):
        """
        Menu 1: Show flight by its ID.
        Returns a list with one dict (or [] if not found).
        """
        return self._execute_query(QUERY_FLIGHT_BY_ID, {'id': flight_id})

    def get_flights_by_date(self, date_str):
        """
        Menu 2: Show all flights on a given date (YYYY-MM-DD).
        Splits into YEAR, MONTH, DAY to match your schema.
        """
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return []

        query = """
        SELECT
          flights.*,
          airlines.AIRLINE   AS airline,
          flights.ID         AS FLIGHT_ID,
          flights.DEPARTURE_DELAY AS DELAY
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE flights.YEAR  = :year
          AND flights.MONTH = :month
          AND flights.DAY   = :day
        """
        params = {
            'year':  str(dt.year),
            'month': str(dt.month),
            'day':   dt.day
        }
        return self._execute_query(query, params)

    def get_delayed_flights_by_airline(self, airline_name):
        """
        Menu 3: All flights (DEP_DELAY >= 20) for a given airline name.
        """
        query = """
        SELECT
          flights.*,
          airlines.AIRLINE   AS airline,
          flights.ID         AS FLIGHT_ID,
          flights.DEPARTURE_DELAY AS DELAY
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE airlines.AIRLINE     = :airline
          AND flights.DEPARTURE_DELAY >= 20
        """
        return self._execute_query(query, {'airline': airline_name})

    def get_delayed_flights_by_origin(self, origin_code):
        """
        Menu 4: All flights (DEP_DELAY >= 20) departing from given origin airport code.
        """
        query = """
        SELECT
          flights.*,
          airlines.AIRLINE   AS airline,
          flights.ID         AS FLIGHT_ID,
          flights.DEPARTURE_DELAY AS DELAY
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE flights.ORIGIN_AIRPORT   = :origin
          AND flights.DEPARTURE_DELAY  >= 20
        """
        return self._execute_query(query, {'origin': origin_code})

    def __del__(self):
        """
        Dispose of the engine when this object is garbage-collected.
        """
        self._engine.dispose()
