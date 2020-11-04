import warnings

from apps.db.tableService.Utils import get_randstr
from apps.db.tableService.TableServiceBase import TableServiceBase
from apps.db.tableService.GroupMember import GroupMember
from apps.db.tableService.Users import Users

class Groups(TableServiceBase):
	def __init__(self, GroupName='', GroupID='', CreateUserName='', GroupDescription='', CreateUserID=''):
		super().__init__('Team')

		self._checkGroupId(GroupID, GroupName)
		self.GroupDescription = GroupDescription
		self._checkUsername(CreateUserName, CreateUserID)
		self._checkExists()
		self.GroupMember = GroupMember(self.GroupID)

	def _checkGroupId(self, gid, group_name):
		if gid:
			self.GroupID = gid
			self.GroupName = self.getNameById(gid)
		elif group_name:
			self.GroupName = group_name
			self.GroupID = self.getIdByName(group_name)
		else:
			self.GroupID = gid
			self.GroupName = group_name

	def _checkUsername(self, CreateUserName, CreateUserID):
		if CreateUserName:
			u = Users(username=CreateUserName)
			self.CreateUserName = u.getName()
			self.CreateUserID = u.getId()
		elif CreateUserID:
			u = Users(userid=CreateUserID)
			self.CreateUserID = u.getId()
			self.CreateUserName = u.getName()
		else:
			self.CreateUserID = CreateUserID
			self.CreateUserName = CreateUserName

	def _checkExists(self):
		if not self.GroupID or not self.GroupName:
			pass
		else:
			g = self.getGroupById(self.GroupID)
			if not g.empty :
				if not g['IsDelete'][0]:  ## exists and not delete
					self.GroupDescription = g['GroupDescription'][0]
					self.CreateUserID = g['CreateUserID'][0]
					self.CreateUserName = g['CreateUserName'][0]
				self.IsDelete = g['IsDelete'][0]

	def checkExists(self):
		return self.exists(GroupName=self.GroupName)


	def isDelete(self):
		if self.isExists():
			return self.IsDelete
		else:
			return True

	def getGroupById(self, gid):
		sql = 'select * from {table} WHERE GroupID=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(gid,))

	def getGroupByName(self, g_name):
		sql = 'select * from {table} WHERE GroupName=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(g_name,))

	def setGroupDescription(self, description):
		self.GroupDescription = description

	def updateGroupDescription(self, description):
		if not self.GroupID:
			warnings.warn('Not exists in db, nothing to do')
		else:
			updated = self.DB.updateDB(self.tableName, 'GroupID', self.GroupID, GroupDescription=description)
			if updated:
				self.setGroupDescription(description)
			return updated

	def setCreateUserName(self, name):
		self.CreateUserName = name

	def updateCreateUserName(self, name):
		if not self.GroupID:
			warnings.warn('Not exists in db, nothing to do')
		else:
			updated = self.DB.updateDB(self.tableName, 'GroupID', self.GroupID, CreateUserName=name)
			if updated:
				self.setCreateUserName(name)
			return updated

	def setCreateUserID(self, id):
		self.CreateUserID = id

	def updateCreateUserID(self, id):
		if not self.GroupID:
			warnings.warn('Not exists in db, nothing to do')
		else:
			updated = self.DB.updateDB(self.tableName, 'GroupID', self.GroupID, CreateUserID=id)
			if updated:
				self.setCreateUserID(id)
			return updated

	def setIsDelete(self, isdelete):
		self.IsDelete = isdelete

	def updateIsDelete(self, isdelete):
		if not self.GroupID:
			warnings.warn('Not exists in db, nothing to do')
		else:
			updated = self.DB.updateDB(self.tableName, 'GroupID', self.GroupID, IsDelete=isdelete)
			if updated:
				self.IsDelete = isdelete
			return updated

	def add(self):
		if not self.GroupID: ## not exists
			group_id = get_randstr('GROUP')
			all_field = self.getAllField()
			all_field['GroupID'] = group_id
			del all_field['GroupMember']
			if self.DB.insertDB(self.tableName , **all_field):
				self.GroupID = group_id
				self.GroupMember = GroupMember(self.GroupID)
				self.GroupMember.addMember(
					MemberID=self.CreateUserID, 
					MemberName=self.CreateUserName, 
					MemberRoleID=1 , 
					MemberRoleName='Creator',
				)
		else:
			if self.IsDelete:
				self.setIsDelete(False)
				if self.update():
					self.GroupMember.addMember(
						MemberID=self.CreateUserID, 
						MemberName=self.CreateUserName, 
						MemberRoleID=1 , 
						MemberRoleName='Creator',
					)
		return self.GroupID

	def delete(self):
		if self.GroupID: ## exists
			if GroupMember(self.GroupID).deleteAllMembers():
				#deleted = self.DB.deleteDB(self.tableName, GroupID=self.GroupID)
				deleted = self.updateIsDelete(True)
				self.GroupMember = GroupMember(self.GroupID)
				return deleted
			return False
		else: ## not exists
			return True

	def update(self):
		if self.GroupID: ## exists
			all_field = self.getAllField()
			del all_field['GroupID']
			del all_field['GroupMember']
			return self.DB.updateDB(self.tableName, 'GroupID', self.GroupID, **all_field)
		else:
			raise RuntimeError('The database cannot be updated because it does not exist')

	def getMember(self):
		return self.GroupMember.getMembers()

	def addMember(self,  MemberID, MemberName, MemberRoleID , MemberRoleName):
		return self.GroupMember.addMember( MemberID, MemberName, MemberRoleID , MemberRoleName)

	def deleteMember(self, MemberID=None, MemberName=None):
		return self.GroupMember.deleteMember(MemberID, MemberName)

	def updateMemberRoleById(self, MemberID, MemberRoleID=None, MemberRoleName=None):
		return self.GroupMember.updateMemberRoleById(MemberID, MemberRoleID=MemberRoleID, MemberRoleName=MemberRoleName)

	def updateMemberRoleByName(self, MemberName, MemberRoleID=None, MemberRoleName=None):
		return self.GroupMember.updateMemberRoleByName(MemberName, MemberRoleID=MemberRoleID, MemberRoleName=MemberRoleName)

	def getIdByName(self, group_name):
		sql = 'select GroupID from {table} WHERE GroupName=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(group_name,))

	def getNameById(self, group_id):
		sql = 'select GroupName from {table} WHERE GroupID=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(group_id,))

	def getName(self):
		return self.GroupName

	def getId(self):
		return self.GroupID

	def getOwnGroupByUserName(self, username):
		sql = 'select * from {table} WHERE GreateUserName=%s'.format(self.tableName)
		return self.getAllDataFromQuery(sql, args=(username,))

	def getOwnGroupByUserId(self, user_id):
		sql = 'select * from {table} WHERE GreateUserId=%s'.format(self.tableName)
		return self.getAllDataFromQuery(sql, args=(user_id,))

	def getGroupByIdList(self, group_ids):
		sql = 'select * from {table} WHERE GroupID in %s'.format(self.tableName)
		return self.getAllDataFromQuery(sql, args=(tuple(group_ids),))

	def getGroupByNameList(self, group_names):
		sql = 'select * from {table} WHERE GroupName in %s'.format(self.tableName)
		return self.getAllDataFromQuery(sql, args=(tuple(group_names),))

	def isExists(self):
		return self.exists(GroupName=self.GroupName)