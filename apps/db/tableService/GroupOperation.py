from apps.db.tableService.TableServiceBase import TableServiceBase

class GroupOperation(TableServiceBase):
	def __init__(self, OperationName=None, OperationID=None):
		super().__init__('GroupOperation')

		if OperationName is not None:
			self.OperationName = OperationName
		elif OperationID is not None:
			self.OperationName = self.getRoleNameById(OperationID)
		else:
			self.OperationName = ''

		if OperationID is not None:
			self.OperationID = OperationID
		elif OperationName is not None:
			self.OperationID = self.getRoleIdByName(OperationName)
		else:
			self.OperationID = ''

	def getRoleIdByName(self, role_name):
		query = 'select OperationID from {0} where OperationName=%s'.format(self.tableName)
		return self._getSingleField(query, args=(role_name,))

	def getRoleNameById(self, role_id):
		query = 'select OperationName from {0} where OperationID=%s'.format(self.tableName, role_id)
		return self._getSingleField(query, args=(role_id,))

	def getId(self):
		return self.OperationID

	def getName(self):
		return self.OperationName

	def add(self):
		if not self.OperationName:
			raise RuntimeError('No RoleName')
		if not self.OperationID: ## not exists
			if self.DB.insertDB(self.tableName, OperationName=self.OperationName):
				self.OperationID = self.getRoleIdByName(self.OperationName)
		return self.OperationID