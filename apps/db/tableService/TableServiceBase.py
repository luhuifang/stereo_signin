from apps.db.tableService.ConnectMYSQL import ConnectMYSQL
from apps.db.database_settings import MYSQL_LOCAL as MYSQL

class TableServiceBase(object):
	def __init__(self, tableName):
		self.DB = ConnectMYSQL(**MYSQL)
		self.tableName = tableName
		self.dbName = MYSQL['database']

	def _getSingleField(self, query, args=None):
		res = self.DB.searchDB(query, args)
		if res:
			return res[0][0]
		else:
			return ''

	def _getAllAttr(self):
		return vars(self)

	def getAllField(self):
		all_field= self._getAllAttr().copy()
		del all_field['DB']
		del all_field['tableName']
		del all_field['dbName']
		return all_field

	def getAllData(self):
		return self.DB.fetchAll(self.tableName, db_name=self.dbName)

	def getTableName(self):
		return self.tableName

	def getAllDataFromQuery(self, query, args=None):
		return self.DB.fetchAll(self.tableName, query=query, db_name=self.dbName, args=args)

	def exists(self, **kwargs):
		sql = 'select 1 from {table} where {query} limit 1;'.format(table=self.tableName, query=' and '.join('{0}=%s'.format(k) for k in kwargs))
		return self._getSingleField(sql, args=tuple(kwargs.values()))

	def getTableColumns(self):
		return self.searchColumnNames(table_name=self.tableName, table_schema=self.dbName)