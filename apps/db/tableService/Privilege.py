import warnings

import pandas as pd
from apps.db.tableService.Utils import get_randstr
from apps.db.tableService.TableServiceBase import TableServiceBase

class Privilege(TableServiceBase):
	def __init__(self, PrivilegeMaster=None, PrivilegeMasterValue=None, 
				PrivilegeAccess=None, PrivilegeAccessValue=None, PrivilegeOperation=None):
		super().__init__('Privilege')

		self.PrivilegeMaster = PrivilegeMaster
		self.PrivilegeMasterValue = PrivilegeMasterValue
		self.PrivilegeAccess = PrivilegeAccess
		self.PrivilegeAccessValue = PrivilegeAccessValue
		self.PrivilegeOperation = PrivilegeOperation
		self.PrivilegeID = self._getId()

	def delete(self):
		if self.PrivilegeID:
			all_field = self.getAllField()
			return self.DB.deleteDB(self.tableName , **all_field)
		else:
			return True

	def add(self):
		if not self.PrivilegeID: ## not exists in db
			pri_id = get_randstr('PRI')
			#all_field = self.getAllField()
			all_field = self.__getNonNullField()
			all_field['PrivilegeID'] = pri_id

			if len(all_field) != 6:
				warnings.warn('Nothing to do')
			elif self.DB.insertDB(self.tableName , **all_field):
				self.PrivilegeID = pri_id
		return self.PrivilegeID

	def updatePrivilegeOperation(self, operation):
		if self.PrivilegeID:
			if self.DB.updateDB(self.tableName, 'PrivilegeID', self.PrivilegeID, PrivilegeOperation=operation):
				self.PrivilegeOperation = operation
				return True
			else:
				return False
		else:
			raise RuntimeError('The database cannot be updated because it does not exist')

	def _getId(self):
		all_field = self.getAllField()
		del all_field['PrivilegeOperation']
		sql = 'select PrivilegeID from {table} WHERE {query}'.format(table=self.tableName, query=' and '.join('{0}=%s'.format(k) for k in all_field))
		return self._getSingleField(sql, args=tuple(all_field.values()))

	def getPrivilegeId(self):
		return self.PrivilegeID

	def getPrivilegeById(self, pri_id):
		query = 'select * from {table} where PrivilegeID=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(query, args=(pri_id,))

	def getPrivilege(self):
		not_null_field = self.__getNonNullField()
		sql = 'select * from {table} ' \
			'where {query}'.format(table=self.tableName, query=' and '.join('{}=%s'.format(k) for k in not_null_field))
		alldata = self.getAllDataFromQuery(sql, args=tuple(not_null_field.values()))
		return alldata[['PrivilegeAccess', 'PrivilegeAccessValue', 'PrivilegeOperation']]

	def __getNonNullField(self):
		all_field = self.getAllField()
		return {k:v for k,v in all_field.items() if v}
