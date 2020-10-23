from apps.db.tableService.TableServiceBase import TableServiceBase

class GroupRole(TableServiceBase):
	def __init__(self, GroupRoleName=None, GroupRoleID=None):
		super().__init__('GroupRole')

		if GroupRoleName is not None:
			self.GroupRoleName = GroupRoleName
		elif GroupRoleID is not None:
			self.GroupRoleName = self.getRoleNameById(GroupRoleID)
		else:
			self.GroupRoleName = ''

		if GroupRoleID is not None:
			self.GroupRoleID = GroupRoleID
		elif GroupRoleName is not None:
			self.GroupRoleID = self.getRoleIdByName(GroupRoleName)
		else:
			self.GroupRoleID = ''

	def getRoleIdByName(self, role_name):
		query = 'select GroupRoleID from {0} where GroupRoleName=%s'.format(self.tableName)
		return self._getSingleField(query, args=(role_name,))

	def getRoleNameById(self, role_id):
		query = 'select GroupRoleName from {0} where GroupRoleID=%s'.format(self.tableName)
		return self._getSingleField(query, args=(role_id))

	def getId(self):
		return self.GroupRoleID

	def getName(self):
		return self.GroupRoleName

	def add(self):
		if not self.GroupRoleName:
			raise RuntimeError('No RoleName')
		elif not self.GroupRoleID: ## not exists
			if self.DB.insertDB(self.tableName, GroupRoleName=self.GroupRoleName):
				self.GroupRoleID = self.getRoleIdByName(self.GroupRoleName)
		return self.GroupRoleID