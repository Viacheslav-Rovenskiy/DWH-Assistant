import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

dotenv_path = '.env'
load_dotenv(dotenv_path)


def execute_sql_query(sql_query: str):
    """
    Executes an SQL query in Postgres database and returns the results in a dictionary.

    Parameters
    ----------
    sql_query : str
        SQL query string.

    Returns
    -------
    dict
        A dictionary with two keys 
        - 'result' as a pandas DataFrame containing the query results, 
        - 'error' with an error message if the execution failed.
    """

    host = os.getenv("PG_HOST")
    port = os.getenv("PG_PORT")
    dbname = os.getenv("PG_DBNAME")
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")

    # Initialize the result and error variables
    result = None
    error = None

    # Connection to the database
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(sql_query)

        columns = [desc[0] for desc in cursor.description] # Get column names
        data = cursor.fetchall() # Fetch all rows

        result = pd.DataFrame(data, columns=columns)

    except Exception as e:
        # Capture any errors and set the error message
        error = str(e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return {'result': result, "error": error}
