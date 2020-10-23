import warnings
import pandas as pd

from apps.db.tableService.TableServiceBase import TableServiceBase
from apps.db.tableService.Data import Data
from apps.db.tableService.WorkflowResult import WorkflowResult
from apps.exampleData.pitch_settings import PITCH

class ChipSequences(TableServiceBase):
	def __init__(self, sn=None):
		super().__init__('firstSequences')

		if not sn is None:
			self.no = sn

	def setNo(self, no):
		self.no = no

	def setChip_id(self, chip_id):
		self.chip_id = chip_id

	def setPlatform(self, platform):
		self.platform = platform

	def setPrimer_type(self, primer_type):
		self.primer_type = primer_type

	def setBarcode_segment(self, barcode_segment):
		self.barcode_segment = barcode_segment

	def setBarcode_len(self, barcode_len):
		self.barcode_len = barcode_len
	
	def setBarcode_start(self, barcode_start):
		self.barcode_start = barcode_start

	def setRC(self, rc):
		self.RC = rc

	def setQC(self, qc):
		self.QC = qc

	def setFOV_row(self, row):
		self.FOV_row = row

	def setFOV_col(self, col):
		self.FOV_col = col

	def setFastq_path(self, fq_path):
		self.fastq_path = fq_path

	def setBarcode_pos_file(self, f):
		self.barcode_pos_file = f

	def addChipSequences(self, **kwargs):
		if not 'no' in kwargs:
			warnings.warn('Field required "no", nothing to do')
		else:
			return self.DB.insertDB(self.tableName, **kwargs)

	def update(self, **kwargs):
		if not self.no:
			warnings.warn('Field required "no", nothing to do')
		else:
			return self.DB.updateDB(self.tableName, 'no', self.no, **kwargs)

	def delete(self):
		if not self.no:
			warnings.warn('Field required "no", nothing to do')
		else:
			return self.DB.deleteDB(self.tableName, no=self.no)

	def getAllRecords(self):
		sql = 'select * from {0} order by create_time desc'.format(self.tableName)
		return self.getAllDataFromQuery(sql)

	def getData(self):
		if not self.no:
			return pd.DataFrame()
		else:
			sql = 'select * from {0} where no=%s'.format(self.tableName)
			return self.getAllDataFromQuery(sql, args=(self.no))

	def getDataByConditions(self, **kwargs):
		sql = 'select * from {0} where {query}'.format(self.tableName, query=' and '.join('{0}=%s'.format(k) for k in kwargs))
		return self.getAllDataFromQuery(sql, args=tuple(kwargs.values()))

	def isExists(self):
		if not self.no:
			return False
		return self.exists(no=self.no)

	def getChipBySN(self, sn):
		sql = 'select chip_id from {table} where no=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(sn,))

	def getPitchByPath(self, path):
		sn = Data().getSNByPath(path)
		if not sn:
			sn = WorkflowResult().getSNByPath(path)
		return self.getPitchBySN(sn)
	
	def getPitchBySN(self, sn):
		if not sn:
			return -1
		chip_id = self.getChipBySN(sn)
		if chip_id:
			for p in PITCH:
				if chip_id.startswith(p):
					return PITCH[p]
		return -1