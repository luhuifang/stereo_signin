import pymysql
import pandas as pd

class ConnectMYSQL(object):
	def __init__(self, **dbConfig):
		self.config = dbConfig

	def connectDB(self):
		connection = pymysql.connect(**self.config)
		return connection

	def searchDB(self, query, args=None):
		connection = self.connectDB() ## 
		cursor = connection.cursor()
		try:
			cursor.execute(query, args)
			out_result = cursor.fetchall()
			return out_result
		except Exception as e:
			raise RuntimeError(e)
		finally:
			self.__closeCursor(cursor)
			self.__closeDB(connection)
		
	def searchColumnNames(self, **kwargs):
		query = 'select column_name from information_schema.COLUMNS ' \
			'where {query} ' \
			'order by ORDINAL_POSITION'.format(query=' and '.join('{0}=%s'.format(k) for k in kwargs))
		col_tmp = self.searchDB(query, args=tuple(kwargs.values()))
		return [c[0] for c in col_tmp]

	def fetchAll(self, table, query=None, db_name = None, args=None):
		if query is None:
			query = 'select * from {0}'.format(table)
		try:
			data = self.searchDB(query, args)

			conditions = {'table_name':table}
			if db_name is not None:
				conditions['table_schema'] = db_name
			colname = self.searchColumnNames(**conditions)
			
			return pd.DataFrame(data, columns=colname)
		except Exception as e:
			raise RuntimeError(e)

	def changeDB(self, query, args=None):
		connection = self.connectDB()
		cursor = connection.cursor()
		try:
			cursor.execute(query, args) # 执行sql语句
			connection.commit() # 执行sql语句
			return True
		except Exception as e:
			print(e)
			connection.rollback() # 发生错误时回滚
			return False
		finally:
			self.__closeCursor(cursor)
			self.__closeDB(connection)

	def insertDB(self, table, **kwargs):
		keys = ','.join(kwargs.keys())
		values = ','.join(['%s'] * len(kwargs))
		sql = 'INSERT INTO {table}({keys})values ({values})'.format(table=table, keys=keys, values=values)
		return self.changeDB(sql, args=tuple(kwargs.values()))

	def deleteDB(self, table, **kwargs):
		sql = 'DELETE FROM {table} WHERE {query}'.format(table=table, query=' and '.join('{}=%s'.format(k) for k in kwargs))
		return self.changeDB(sql, args=tuple(kwargs.values()))

	def updateDB(self, table, on_col, on_value, **kwargs):
		sql = 'UPDATE {table} SET {query} WHERE {col_name}=%s'.format(
			table=table, query=', '.join('{}=%s'.format(k) for k in kwargs), col_name=on_col)
		return self.changeDB(sql, args=tuple(kwargs.values())+(on_value,) )

	def updateDBbyCondition(self, table, condition, **kwargs):
		sql = 'UPDATE {table} SET {query} WHERE {rule}'.format(
			table=table, query=', '.join('{}=%s'.format(k) for k in kwargs),
			rule=' and '.join('{0}=%s'.format(k) for k in condition))
		return self.changeDB(sql, args=tuple(kwargs.values())+tuple(condition.values()) )

	def __closeDB(self, connection):
		return connection.close()

	def __closeCursor(self, cursor):
		return cursor.close()

