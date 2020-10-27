from apps.db.tableService.Utils import get_randstr
from apps.db.tableService.TableServiceBase import TableServiceBase

class OrderStatus(TableServiceBase):
	def __init__(self,orderstatusid=''):
		super().__init__('orderstatus')
		self.orderstatusid = orderstatusid

	def getAllStatus(self):
		sql = 'select * from {table}'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql)