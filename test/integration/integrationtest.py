#!/usr/bin/python3

import sys
import psycopg2

create = """
        CREATE TABLE IF NOT EXISTS testtable (
            test_id SERIAL PRIMARY KEY,
            test_name VARCHAR(255) NOT NULL
        );
        """
insert = """INSERT INTO testtable(test_name) VALUES(%s);"""

try:
    new_conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
    new_cursor = new_conn.cursor()
    new_cursor.execute(create)
    new_cursor.execute(insert, ("some_name",))
    new_conn.commit()
    new_cursor.close()
    print("Integration Test Successful. Database Created And Edited.")
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    print("Integration Test Failed. Error Querying The Database.")
    sys.exit(1)
finally:
    new_conn.close()

