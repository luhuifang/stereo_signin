import warnings

from apps.db.tableService.TableServiceBase import TableServiceBase

class DownloadPath(TableServiceBase):
	def __init__(self, path=None):
		super().__init__('downloadPath')
		if not path is None:
			self.root = path
			self.isAvailable = self.isAvailable(path)

	def add(self):
		if not self.root:
			warnings.warn('No root path, nothing to do')
		elif self.isExists():
			return True
		else:
			return self.insertDB(self.tableName, root=self.root, isAvailable=True)

	def updateAvailable(self, isavailable):
		if not self.root:
			warnings.warn('No root path, nothing to do')
		else:
			return self.DB.updateDB(self.tableName, 'root', self.root, isAvailable=isavailable)

	def isAvailable(self, path):
		sql = 'select isAvailable from {table} where root=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(path,))

	def getAvailablePath(self):
		sql = 'select root from {table} where isAvailable=TRUE'.format(table=self.tableName)
		return self._getSingleField(sql)

	def isExists(self):
		if not self.root:
			return False
		else:
			return self.exists(root=self.root)