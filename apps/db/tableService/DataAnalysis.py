import pandas as pd
import warnings

from apps.db.tableService.TableServiceBase import TableServiceBase

class DataAnalysis(TableServiceBase):
	def __init__(self, chip_id=None):
		super().__init__('secondSequences')

		if chip_id is not None:
			self.chip_id = chip_id

	def setNo(self, no):
		self.no = no

	def setSpecies(self, spec):
		self.species = spec

	def setTissue(self, tissue):
		self.tissue = tissue

	def setChip_id(self, chip_id):
		self.chip_id = chip_id

	def setLibrary_type(self, lib):
		self.library_type = lib

	def setBarcode_len(self, barcode_len):
		self.barcode_len = barcode_len
	
	def setBarcode_start(self, barcode_start):
		self.barcode_start = barcode_start

	def setRead_len(self, read_len):
		self.read_len = read_len

	def setUMI_len(self, umi_len):
		self.umi_len = umi_len

	def setUMI_start_pos(self, umi_start_pos):
		self.UMI_start_pos = umi_start_pos

	def setUMI_location(self, umi_location):
		self.UMI_location = umi_location

	def setRemarks(self, remarks):
		self.Remarks = remarks

	def setFastq1(self, fq1):
		self.fastq1 = fq1

	def setFastq2(self, fq2):
		self.fastq2 = fq2

	def add(self):
		if not self.chip_id:
			warnings.warn('Field required "chip_id", nothing to do')
		else:
			values = self.getAllField()
			return self.DB.insertDB(self.tableName, **values)

	def addSecondSequences(self, **kwargs):
		if not 'chip_id' in kwargs:
			warnings.warn('Field required "chip_id", nothing to do')
		else:
			return self.DB.insertDB(self.tableName, **kwargs)

	def update(self, **kwargs):
		if not self.chip_id:
			warnings.warn('Field required "chip_id", nothing to do')
		else:
			return self.DB.updateDB(self.tableName, 'chip_id', self.chip_id, **kwargs)

	def delete(self, **kwargs):
		return self.DB.deleteDB(self.tableName, **kwargs)

	def getAllRecords(self):
		sql = 'select * from {0} order by create_time desc'.format(self.tableName)
		return self.getAllDataFromQuery(sql)
	
	def getDataByChipID(self, chip_id):
		sql = 'select * from {table} where chip_id=%s'.format(table = self.tableName)
		return self.getAllDataFromQuery(sql, args=(chip_id,))
	
	def getData(self):
		if self.chip_id:
			return self.getDataByChipID(self.chip_id)
		return pd.DataFrame()

	def isExists(self):
		if not self.chip_id:
			return False
		return self.exists(chip_id=self.chip_id)