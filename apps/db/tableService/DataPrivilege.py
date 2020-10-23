import warnings
from apps.db.tableService.TableServiceBase import TableServiceBase
from apps.db.tableService.Groups import Groups
from apps.db.tableService.Users import Users

class DataPrivilege(TableServiceBase):
	"""docstring for DataPrivilege"""
	def __init__(self, dataID):
		super().__init__('DataPrivilege')
		self.DataSource = dataID
		self.DataPrivilege = self.getDataPrivilegeBySourceId(dataID)

	def getDataPrivilege(self):
		return self.DataPrivilege
		
	def getDataPrivilegeBySourceId(self, sourceId):
		sql = 'select * from {table} where DataSource=%s order by CreateTime desc'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(sourceId,))

	def addPrivilege(self, MasterRole, MasterID=None, MasterName=None, Type='User', ExpirationDate=None):
		if MasterID is None and MasterName is None:
			warnings.warn('No MasterID or MasterName, nothing to do')
		else:
			values = locals().copy()
			del values['self']
			values = self.__getParam(**values)
			
			m_id, m_name = self.__getIDandName(MasterID, MasterName, Type)
			values['MasterID'] = m_id
			values['MasterName'] = m_name
			if not m_id or not m_name:
				return False, 1 
			if self.isExists(m_id):
				return False, 2

			inserted = self.DB.insertDB(self.tableName, **values)
			if inserted:
				self.DataPrivilege = self.getDataPrivilegeBySourceId(self.DataSource)
			return inserted, 3

	def deletePrivilege(self, MasterID=None, MasterName=None):
		if MasterID is None and MasterName is None:
			warnings.warn('No MasterID or MasterName, nothing to do')
		else:
			conditions = locals().copy()
			del conditions['self']
			conditions = {k: v for k, v in conditions.items() if v}
			deleted = self.DB.deleteDB(self.tableName, **conditions)
			if deleted:
				self.DataPrivilege = self.getDataPrivilegeBySourceId(self.DataSource)
			return deleted

	def updateRole(self, MasterRole, MasterID=None, MasterName=None):
		if MasterID is None and MasterName is None:
			warnings.warn('No MasterID or MasterName, nothing to do')
		else:
			conditions = locals().copy()
			del conditions['self']
			conditions = self.__getParam(**conditions)
			del conditions['MasterRole']
			updated = self.DB.updateDBbyCondition(self.tableName, conditions, MasterRole=MasterRole)
			if updated:
				self.DataPrivilege = self.getDataPrivilegeBySourceId(self.DataSource)
			return updated

	def updateExpDate(self, ExpDate, MasterID=None, MasterName=None):
		if MasterID is None and MasterName is None:
			warnings.warn('No MasterID or MasterName, nothing to do')
		else:
			conditions = locals().copy()
			del conditions['self']
			conditions = self.__getParam(**conditions)
			if 'ExpDate' in conditions:
				del conditions['ExpDate']

			updated = self.DB.updateDBbyCondition(self.tableName, conditions, ExpirationDate=ExpDate)
			if updated:
				self.DataPrivilege = self.getDataPrivilegeBySourceId(self.DataSource)
			return updated

	def getUserRole(self, user_name):
		sql = 'select MasterRole from {table} where MasterName=%s and DataSource=%s'.format(table=self.tableName)
		uRole = self._getSingleField(sql, args=(user_name, self.DataSource))
		if not uRole:
			sql = '''
				select MasterRole from {table}
				where DataSource = %s
				and Type = 'Group'
				and MasterID in(
					select GroupID from GroupMember
					where MemberName = %s
				)
				order by MasterRole desc;
			'''.format(table=self.tableName)
			uRole = self._getSingleField(sql, args=(self.DataSource, user_name))
		return uRole

	def isExists(self, MasterID):
		return self.exists(MasterID=MasterID, DataSource=self.DataSource)


	def __getIDandName(self, MasterID, MasterName, Type):
		if MasterID is not None:
			if Type=='User':
				return MasterID, Users(userid=MasterID).getName()
			elif Type=='Group':
				return MasterID, Groups(GroupID=MasterID).getName()
		elif MasterName is not None:
			if Type == 'User':
				return Users(MasterName).getId(), MasterName
			elif Type == 'Group':
				return Groups(GroupName=MasterName).getId(), MasterName
		else:
			return MasterID, MasterName


	def __getParam(self, **kwargs):
		conditions = {k: v for k, v in kwargs.items() if v is not None}
		conditions['DataSource'] = self.DataSource
		return conditions

