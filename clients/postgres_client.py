import os

import psycopg2
from psycopg2 import sql

from config import postgres


class PostgresDB:
    def __init__(self):
        """Initialize connection parameters."""
        self.dbname = postgres.get('database')
        self.user = postgres.get('user')
        self.password = os.environ.get('postgres_password')
        self.host = postgres.get('host')
        self.port = postgres.get('port')
        self.connection = None
        self.cursor = None

    def connect(self):
        """Create a connection to the database."""
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Connection to the database established.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        """Execute a single query with optional parameters."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()

    def insert_query(self, table, data):
        """Insert data into a table. Data should be a dictionary with column names as keys."""
        try:
            columns = data.keys()
            values = [data[col] for col in columns]
            query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
                table=sql.Identifier(table),
                columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
                values=sql.SQL(', ').join(sql.Placeholder() * len(values))
            )
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")
            self.connection.rollback()

    def update_query(self, table, data, where_clause):
        """Update data in a table. Data should be a dictionary with column names as keys."""
        try:
            columns = data.keys()
            values = [data[col] for col in columns]
            set_clause = sql.SQL(', ').join(
                sql.SQL("{} = %s").format(sql.Identifier(col)) for col in columns
            )
            query = sql.SQL("UPDATE {table} SET {set_clause} WHERE {where_clause}").format(
                table=sql.Identifier(table),
                set_clause=set_clause,
                where_clause=sql.SQL(where_clause)
            )
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Data updated successfully.")
        except Exception as e:
            print(f"Error updating data: {e}")
            self.connection.rollback()
