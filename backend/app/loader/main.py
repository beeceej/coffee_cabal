from coffee_cabal.coffee import load_coffee_into_db
from coffee_cabal.db import connection

if __name__ == "__main__":
    load_coffee_into_db(connection)
