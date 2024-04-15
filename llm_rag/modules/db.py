import psycopg2
from psycopg2 import pool
import os

from .. import logger

class Database:
	def __init__(self):
		# Configure the connection parameters
		self.db_params = {
			'database': os.environ.get('DB_NAME'),
			'user': os.environ.get('DB_USER'),
			'password': os.environ.get('DB_PASSWORD'),
			'host': os.environ.get('DB_HOST'),
			'port': os.environ.get('DB_PORT')
		}
		# Create a connection pool
		self.connection_pool = self._create_connection_pool()

	def _create_connection_pool(self):
		# Define connection pool parameters
		min_conn = 1
		max_conn = 5
		try:
			return pool.SimpleConnectionPool(min_conn, max_conn, **self.db_params)
		except psycopg2.Error as e:
			print("Error creating connection pool:", e)
			raise

	def get_connection(self):
		try:
			# Get a connection from the pool
			connection = self.connection_pool.getconn()
			logger.info("DB: Connection established successfully")
			return connection
		except psycopg2.Error as e:
			print("Error getting connection from pool:", e)
			raise

	def return_connection(self, conn):
		try:
			# Return the connection to the pool
			self.connection_pool.putconn(conn)
			logger.info("DB: Connection closed successfully")
		except psycopg2.Error as e:
			print("Error returning connection to pool:", e)
			raise

	def close_all_connections(self):
		try:
			# Close all connections in the pool
			self.connection_pool.closeall()
			logger.info("DB: All connections closed successfully")
		except psycopg2.Error as e:
			print("Error closing connections in the pool:", e)
			raise