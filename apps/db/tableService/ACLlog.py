import warnings

from apps.db.tableService.TableServiceBase import TableServiceBase
from apps.db.tableService.Groups import Groups
from apps.db.tableService.Data import Data

class ACLlog(TableServiceBase):
	def __init__(self, operator=None, OperationSource='', OperationSourceValue=''):
		super().__init__('ACLlog')
		self.Operator = operator
		self.OperationSource = OperationSource
		self.OperationSourceValue = OperationSourceValue
		self.OperationSourceValueName = self.__checkSourceName(OperationSourceValue)

	def __checkSourceName(self, opSourceValue):
		if opSourceValue.startswith('GROUP_'):
			return Groups(GroupID=opSourceValue).getName()
		elif opSourceValue.startswith('DATA_'):
			data = Data(data_id=opSourceValue)
			return '{0} ({1})'.format(data.SN, data.ChipID)
		else:
			return ''

	def setOperationSource(self, opSource):
		self.OperationSource = opSource

	def setOperationSourceValue(self, opSourceValue):
		self.OperationSourceValue = opSourceValue

	def setOperationType(self, opType):
		self.OperationType = opType

	def setOperationField(self, opField):
		self.OperationField = opField

	def setOperationValue(self, opValue):
		self.OperationValue = opValue

	def add(self):
		if not self.OperationSource or not self.OperationSourceValue or not self.OperationType:
			warnings.warn('Nothing to do')
			return False
		all_field = self.__getNonNullField()
		print(all_field)
		return self.DB.insertDB(self.tableName, **all_field)

	def getLogBySourceList(self, source_list):
		if not source_list or not isinstance(source_list, list):
			return pd.DataFrame()
		sql = 'select * from {table} WHERE OperationSourceValue in %s order by OperationTime desc'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(tuple(source_list),))

	def __getNonNullField(self):
		all_field = self.getAllField()
		return {k:v for k,v in all_field.items() if v}

