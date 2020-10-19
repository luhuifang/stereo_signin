from apps.db.tableService.Utils import get_randstr
from apps.db.tableService.TableServiceBase import TableServiceBase

class Orders(TableServiceBase):
	def __init__(self,orderid='',currentstatus='',chipplat='',createtime=''):
		super().__init__('orderform')
		self.orderid = orderid

	def getAllData(self):
		sql = 'select * from {table}'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql)

	def getDataByStatus(self, currentstatus):
		sql = 'select * from {table} where CurrentStatus=(select OrderStatusID from orderStatus where OrderStatusName=%s);'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(currentstatus,))

	def getDataByOrderID(self, orderid):
		sql = 'select * from {table} where OrderID=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(orderid,))

	def getDataBySearch(self, orderid,ChipPlat,DateStart,DateEnd):
		orderid = str(orderid) + '.*'
		ChipPlat = '^' + str(ChipPlat) + '.*'
		# Date = '^' + Date + '.*'
		if not DateStart and not DateEnd:
			Date = '.*'
			sql = 'select * from {table} where OrderID rlike %(orderid)s and ChipPlat rlike %(ChipPlat)s and CreateTime rlike %(date)s'.format(table=self.tableName)
			value = {'orderid':orderid,'ChipPlat':ChipPlat,'date':Date}
		elif DateStart and not DateEnd:
			Date = DateStart + ' 00:00:00'
			sql = 'select * from {table} where OrderID rlike %(orderid)s and ChipPlat rlike %(ChipPlat)s and CreateTime >= %(date)s'.format(table=self.tableName)
			value = {'orderid':orderid,'ChipPlat':ChipPlat,'date':Date}
		elif DateEnd and not DateStart:
			Date = DateEnd + ' 23:59:59'
			sql = 'select * from {table} where OrderID rlike %(orderid)s and ChipPlat rlike %(ChipPlat)s and CreateTime < %(date)s'.format(table=self.tableName)
			value = {'orderid':orderid,'ChipPlat':ChipPlat,'date':Date}
		else:
			DateStart = DateStart + ' 00:00:00'
			DateEnd = DateEnd + ' 23:59:59'
			sql = 'select * from {table} where OrderID rlike %(orderid)s and ChipPlat rlike %(ChipPlat)s and CreateTime between %(datestart)s and %(dateend)s'.format(table=self.tableName)
			value = {'orderid':orderid,'ChipPlat':ChipPlat,'datestart':DateStart,'dateend':DateEnd}
		return self.getAllDataFromQuery(sql, args=(value))

	def setCurrentStatus(self, currentstatus):
		self.currentstatus = currentstatus

	def updateCurrentStatus(self, currentstatus, OrderID):
		updated = self.DB.updateDB(self.tableName, 'OrderID', OrderID, CurrentStatus=currentstatus)
		if updated:
			self.setCurrentStatus(currentstatus)
		return updated

	def setNextStatus(self, nextstatus):
		self.nextstatus = nextstatus

	def updateNextStatus(self, nextstatus, OrderID):
		updated = self.DB.updateDB(self.tableName, 'OrderID', OrderID, NextStatus=nextstatus)
		if updated:
			self.setNextStatus(nextstatus)
		return updated
