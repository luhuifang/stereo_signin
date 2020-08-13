from apps.db.tableService.TableServiceBase import TableServiceBase

class UserRole(TableServiceBase):
	def __init__(self, UserRoleName=None, UserRoleID=None):
		super().__init__('UserRole')

		if UserRoleName is not None:
			self.UserRoleName = UserRoleName
		elif UserRoleID is not None:
			self.UserRoleName = self.getRoleNameById(UserRoleID)
		else:
			self.UserRoleName = ''

		if UserRoleID is not None:
			self.UserRoleID = UserRoleID
		elif UserRoleName is not None:
			self.UserRoleID = self.getRoleIdByName(UserRoleName)
		else:
			self.UserRoleID = ''

	def getRoleIdByName(self, role_name):
		query = 'select UserRoleID from {0} where UserRoleName=%s'.format(self.tableName)
		return self._getSingleField(query, args=(role_name,))

	def getRoleNameById(self, role_id):
		query = 'select UserRoleName from {0} where UserRoleID=%s'.format(self.tableName)
		return self._getSingleField(query, args=(role_id,))

	def getId(self):
		return self.UserRoleID

	def getName(self):
		return self.UserRoleName

	def add(self):
		if not self.UserRoleName:
			raise RuntimeError('No RoleName')
		if not self.UserRoleID:
			if self.DB.insertDB(self.tableName, UserRoleName=self.UserRoleName):
				self.UserRoleID = self.getRoleIdByName(self.UserRoleName)
		return self.UserRoleID