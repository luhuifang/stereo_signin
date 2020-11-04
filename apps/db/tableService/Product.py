import warnings

from apps.db.tableService.TableServiceBase import TableServiceBase

class Product(TableServiceBase):
	def __init__(self, sn=''):
		super().__init__('Product')
		self.SN = sn
		self._checkExists(sn)

	def _checkExists(self, sn):
		p = self.getProductBySN(sn)
		if not p.empty:
			self.ProductID = p['ProductID'][0]
			self.ProductionDate = p['ProductionDate'][0]
			self.Price = p['Price'][0]
			self.Status = p['Status'][0]
			self.CustomerName = p['CustomerName'][0]
			self.OrderID = p['OrderID'][0]
			self.SoldDate = p['SoldDate'][0]
			self.SharedUser = p['SharedUser'][0]
			self.SharedGroup = p['SharedGroup'][0]
		else:
			self.ProductID = ''
			self.ProductionDate = ''
			self.Price = ''
			self.Status = ''
			self.CustomerName = ''
			self.OrderID = ''
			self.SoldDate = ''
			self.SharedUser = ''
			self.SharedGroup = ''

	def setProductionDate(self, date):
		self.ProductionDate = date

	def updateProductionDate(self, date):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, ProductionDate = date)
		if updated:
			self.setProductionDate(date)
		return updated

	def setPrice(self, price):
		self.Price = price

	def updatePrice(self, price):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, Price = price)
		if updated:
			self.setPrice(price)
		return updated

	def setStatus(self, status):
		self.Status = status

	def updateStatus(self, status):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, Status=status)
		if updated:
			self.setStatus(status)
		return updated

	def setCustomerName(self, name):
		self.CustomerName = name

	def updateCustomerName(self, name):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, CustomerName=name)
		if updated:
			self.setCustomerName(name)
		return updated
	
	def setOrderId(self, order_id):
		self.OrderID = order_id
	
	def updateOrderId(self, order_id):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, OrderID=order_id)
		if updated:
			self.setOrderId(order_id)
		return updated

	def setSoldDate(self, date):
		self.SoldDate = date

	def updateSoldDate(self, date):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, SoldDate=date)
		if updated:
			self.setSoldDate(date)
		return updated

	def setSharedUser(self, user):
		self.SharedUser = user

	def updateSharedUser(self, user):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, SharedUser=user)
		if updated:
			self.setSharedUser(user)
		return updated

	def setSharedGroup(self, group):
		self.SharedGroup = group

	def updateSharedGroup(self, group):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, SharedGroup=group)
		if updated:
			self.setSharedGroup(group)
		return updated

	def delete(self):
		if self.ProductID: ## exists in db
			return self.DB.deleteDB(self.tableName , ProductID=self.ProductID, SN=self.SN)
		else:
			return True

	def add(self):
		if not self.ProductID: ## not exists in db
			values = self.__getValue()
			if self.DB.insertDB(self.tableName , **values):
				self.ProductID = self.getIdBySN(self.SN)
		else:
			warnings.warn('This product already exists, nothing to do')
		return self.ProductID

	'''
	def update(self):
		if self.ProductID: 
			values = self.__getValue()
			del values['SN']
			return self.DB.updateDB(self.tableName, 'SN', self.SN, **values)
		else:
			raise RuntimeError('The database cannot be updated because it does not exist')
	'''

	def getIdBySN(self, sn):
		sql = 'select ProductID from {table} where SN=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(sn,))

	def getProductBySN(self, sn):
		sql = 'select * from {table} where SN=%s;'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(sn,))
	
	def getProductByOrderId(self, order_id):
		sql = 'select * from {table} where OrderID=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(order_id,))

	def __getValue(self):
		all_field = self.getAllField()
		del all_field['ProductID']
		values = {k: v for k, v in all_field.items() if v}
		return values
