import pandas as pd
from apps.db.tableService.TableServiceBase import TableServiceBase

class Menu(TableServiceBase):
	def __init__(self, MenuName=None, MenuID=None, MenuUrl='', MenuIcon='', MenuOrder=1,  MenuClassName='', MenuIdName='', IsVisible=True):
		super().__init__('Menu')

		self._checkMenuName(MenuID, MenuName)
		self.MenuUrl = MenuUrl
		self.MenuOrder = MenuOrder
		self.MenuIcon = MenuIcon
		self.MenuClassName = MenuClassName
		self.MenuIdName = MenuIdName
		self.IsVisible = IsVisible
		self._checkExists()

	def _checkMenuName(self, mid, mname):
		if mname:
			self.MenuID = self.getIdByName(mname)
			self.MenuName = mname
		elif mid:
			self.MenuID = mid
			self.MenuName = self.getNameById(mid)
		else:
			self.MenuID = mid
			self.MenuName = mname

	def _checkExists(self):
		if not self.MenuName or not self.MenuID:
			pass
		else:
			m = self.getMenuByName(self.MenuName)
			if not m.empty:
				self.MenuUrl = m['MenuUrl'][0]
				self.MenuOrder = m['MenuOrder'][0]
				self.MenuIcon = m['MenuIcon'][0]
				self.MenuClassName = m['MenuClassName'][0]
				self.MenuIdName = m['MenuIdName'][0]
				self.IsVisible = m['IsVisible'][0]

	def updateMenuUrl(self, url):
		self.MenuUrl = url
		if self.MenuID: ## exists
			return self.DB.updateDB(self.tableName, 'MenuID', self.MenuID, MenuUrl=url)
		return True

	def setMenuIcon(self, icon):
		self.MenuIcon = icon
		if self.MenuID: ## exists
			return self.DB.updateDB(self.tableName, 'MenuID', self.MenuID, MenuIcon=icon)
		return True

	def setMenuClassName(self, classname):
		self.MenuClassName = classname
		if self.MenuID: ## exists
			return self.DB.updateDB(self.tableName, 'MenuID', self.MenuID, MenuClassName = classname)
		return True

	def setMenuOrder(self, order):
		self.MenuOrder = order
		if self.MenuID: ## exists
			return self.DB.updateDB(self.tableName, 'MenuID', self.MenuID, MenuOrder = order)
		return True

	def setMenuIdName(self, idname):
		self.MenuIdName = idname
		if self.MenuID: ## exists
			return self.DB.updateDB(self.tableName, 'MenuID', self.MenuID, MenuIdName = idname)
		return True

	def setIsVisiable(self, isvisible):
		self.IsVisible = isvisible
		if self.MenuID: ## exists
			return self.DB.updateDB(self.tableName, 'MenuID', self.MenuID, IsVisible = isvisible)
		return True

	def getMenuId(self):
		return self.MenuID

	def getIdByName(self, menuName):
		sql = 'select MenuID from {table} WHERE MenuName=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(menuName,))

	def getNameById(self, menuId):
		sql = 'select MenuName from {table} WHERE MenuID=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(menuId,))

	def getMenuById(self, menuId):
		sql = 'select * from {table} WHERE MenuID=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(menuId,))

	def getMenuByName(self, menuName):
		sql = 'select * from {table} WHERE MenuName=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(menuName,))

	def getMenuByIdList(self, idList):
		if not idList:
			return pd.DataFrame()
		sql = 'select * from {table} WHERE MenuID in %s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(tuple(idList),))

	def getMenuByNameList(self, nameList):
		if not nameList:
			return pd.DataFrame()
		sql = 'select * from {table} WHERE MenuName in %s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(tuple(nameList),))


	def delete(self):
		if self.MenuID: ## exists
			return self.DB.deleteDB(self.tableName , MenuID=self.MenuID, MenuName=self.MenuName)
		else: ## not exists
			return True

	def add(self):
		if not self.MenuID: ## not exists
			all_field = self.getAllField()
			del all_field['MenuID']
			if self.DB.insertDB(self.tableName , **all_field):
				self.MenuID = self.getIdByName(self.MenuName)
		return self.MenuID

	def update(self):
		if self.MenuID: ## exists
			all_field = self.getAllField()
			del all_field['MenuID']
			return self.DB.updateDB(self.tableName, 'MenuID', self.MenuID, **all_field)
		else:
			raise RuntimeError('The database cannot be updated because it does not exist')
