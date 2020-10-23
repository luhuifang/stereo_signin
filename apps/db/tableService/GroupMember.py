import warnings

from apps.db.tableService.TableServiceBase import TableServiceBase
from apps.db.tableService.GroupRole import GroupRole

class GroupMember(TableServiceBase):
	def __init__(self, GroupID):
		super().__init__('GroupMember')
		if self.__checkGroupId(GroupID):
			self.GroupID = GroupID 
		else:
			self.GroupID = ''

		self.Members = self.getMemberById(self.GroupID) ##DataFrame

	def __checkGroupId(self, group_id):
		sql = 'select 1 from Team where GroupID=%s limit 1;'
		return self._getSingleField(sql, args=(group_id,))

	def getMemberById(self, group_id):
		sql = 'select * from {table} where GroupID=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(group_id,))

	def getMembers(self):
		return self.Members

	def addMember(self, MemberID, MemberName, MemberRoleID , MemberRoleName):
		if not self.GroupID:
			return False
		args = locals().copy()
		del args['self']
		conditions = self.__getParam(**args)

		if self.exists(**conditions):
			return True
		else:
			inserted = self.DB.insertDB(self.tableName, **conditions)
			if inserted:
				self.Members = self.getMemberById(self.GroupID)
			return inserted

	def deleteAllMembers(self):
		if not self.GroupID: ## not exists
			warnings.warn('Nothing to do')
		deleted = self.DB.deleteDB(self.tableName, GroupID=self.GroupID)
		if deleted:
			self.Members = self.getMemberById(self.GroupID)
			self.GroupID = ''
		return deleted

	def deleteMember(self, MemberID=None, MemberName=None):
		args = locals().copy()
		del args['self']
		conditions = self.__getParam(**args)
		
		deleted = self.DB.deleteDB(self.tableName, **conditions)
		if deleted:
			self.Members = self.getMemberById(self.GroupID)
		return deleted

	def updateMemberRoleById(self, MemberID, MemberRoleID=None, MemberRoleName=None):
		if not self.GroupID:
			return False

		values = self.__getValues(MemberRoleID, MemberRoleName)
		if not values:
			return False

		conditions = {'MemberID':MemberID, 'GroupID':self.GroupID}
		updated = self.DB.updateDBbyCondition(self.tableName, conditions, **values)
		if updated:
			self.Members = self.getMemberById(self.GroupID)
		return updated

	def updateMemberRoleByName(self, MemberName, MemberRoleID=None, MemberRoleName=None):
		if not self.GroupID:
			return False

		values = self.__getValues(MemberRoleID, MemberRoleName)
		if not values:
			return False
		conditions = {'MemberName':MemberName, 'GroupID':self.GroupID}
		updated = self.DB.updateDBbyCondition(self.tableName, conditions, **values)
		if updated:
			self.Members = self.getMemberById(self.GroupID)
		return updated

	def isExists(self, username):
		return self.exists(GroupID=self.GroupID, MemberName=username)

	def __getValues(self, MemberRoleID, MemberRoleName):
		values = {}
		if MemberRoleID is None and MemberRoleName is None:
			warnings.warn('No MemberRoleID or MemberRoleName')
		elif MemberRoleID is not None:
			values['MemberRoleID'] = MemberRoleID
			groupRole = GroupRole(GroupRoleID = MemberRoleID)
			values['MemberRoleName'] = groupRole.getName()
		elif MemberRoleName is not None:
			values['MemberRoleName'] = MemberRoleName
			groupRole = GroupRole(GroupRoleName = MemberRoleName)
			values['MemberRoleID'] = groupRole.getId()
		return values

	def __getParam(self, **kwargs):
		conditions = {k: v for k, v in kwargs.items() if v is not None}
		conditions['GroupID'] = self.GroupID
		return conditions


