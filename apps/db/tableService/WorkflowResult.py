import warnings
import pandas as pd

from apps.db.tableService.TableServiceBase import TableServiceBase

class WorkflowResult(TableServiceBase):
	def __init__(self, task_id=None):
		super().__init__('workflowResult')
		if task_id is not None:
			self.task_id = task_id

	def setNo(self, no):
		self.no = no

	def setUser_name(self, name):
		self.user_name = name

	def setStatus(self, status):
		self.status = status

	def setChip_2(self, chip_2):
		self.chip_2 = chip_2

	def setResultPath(self, result_path):
		self.result_path = result_path

	def setRemarks(self, remarks):
		self.Remarks = remarks

	def addResult(self, **kwargs):
		if not 'task_id' in kwargs:
			warnings.warn('Field required "task_id", nothing to do')
		else:
			return self.DB.insertDB(self.tableName, **kwargs)

	def update(self, **kwargs):
		if not self.task_id:
			warnings.warn('Field required "task_id", nothing to do')
		else:
			return self.DB.updateDB(self.tableName, 'task_id', self.task_id, **kwargs)

	def delete(self):
		if not self.task_id:
			warnings.warn('Field required "task_id", nothing to do')
		else:
			return self.DB.deleteDB(self.tableName, task_id=self.task_id)

	def getAllRecords(self):
		sql = 'select * from {0} order by create_time desc'.format(self.tableName)
		return self.getAllDataFromQuery(sql)

	def isExists(self):
		if not self.task_id:
			return False
		return self.exists(task_id=self.task_id)
	
	def getSNByPath(self, path):
		sql = 'select no from {table} where result_path=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(path,))
	
	def getDataByPath(self, path):
		sql = 'select * from {table} where result_path=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(path,))
