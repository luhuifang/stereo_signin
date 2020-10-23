import warnings
import datetime
import pandas as pd

from apps.db.tableService.Utils import get_randstr
from apps.db.tableService.TableServiceBase import TableServiceBase

class Data(TableServiceBase):
	def __init__(self, sn=None, chip_list=None, data_id=None):
		super().__init__('Data')
		self.SN = sn
		self.DataID = data_id
		self.setChipID(chip_list)
		self._checkExists()

	def _checkExists(self):
		self.Species = ''
		self.Tissue = ''
		self.Status = ''
		self.ResultPath = ''
		self.IsPublic = False
		self.IsExample = False
		self.data = pd.DataFrame()

		if self.DataID:
			single_data = self.getDataByID(self.DataID)
			self.__initValues(single_data)
		elif not self.ChipID: ## all records
			self.data = self.getDataBySN(self.SN)
		else: ## single record
			single_data = self.getDataBySNandChip(self.SN, self.ChipID)
			self.__initValues(single_data)

	def __initValues(self, single_data):
		if not single_data.empty:
			self.data = single_data
			self.ChipID = single_data['ChipID'][0]
			self.DataID = single_data['DataID'][0]
			self.Species = single_data['Species'][0]
			self.Tissue = single_data['Tissue'][0]
			self.Status = single_data['Status'][0]
			self.ResultPath = single_data['ResultPath'][0]
			self.IsPublic = single_data['IsPublic'][0]
			self.PublicTime = single_data['PublicTime'][0]
			self.IsExample = single_data['IsExample'][0]
			if not self.SN :
				self.SN = single_data['SN'][0]
			return True
		return False
				
	def setChipID(self, chip_list):
		if isinstance(chip_list, list):
			self.ChipID = ', '.join(chip_list)
		elif isinstance(chip_list, str):
			self.ChipID = chip_list
		else:
			self.ChipID = ''
		self.data = self.getDataBySNandChip(self.SN, self.ChipID)

	def setSpecies(self, species):
		self.Species = species

	def updateSpecies(self, species):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, Species=species)
		if updated:
			self.setSpecies(species)
		return updated

	def setTissue(self, tissue):
		self.Tissue = tissue

	def updateTissue(self, tissue):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, Tissue=tissue)
		if updated:
			self.setTissue(tissue)
		return updated

	def setStatus(self, status):
		self.Status = status

	def updateStatus(self, status):
		if not self.ChipID: ## 
			warnings.warn('No chip id, nothing to do')
		else:
			condition = { 'SN': self.SN, 'ChipID': self.ChipID }
			updated = self.DB.updateDBbyCondition(self.tableName, condition, Status=status)
			if updated:
				self.setStatus(status)
			return updated

	def setResultPath(self, resultpath):
		self.ResultPath = resultpath

	def updateResultPath(self, resultpath):
		if not self.ChipID:
			warnings.warn('No chip id, nothing to do')
		else:
			condition = { 'SN': self.SN, 'ChipID': self.ChipID }
			updated = self.DB.updateDBbyCondition(self.tableName, condition, ResultPath=resultpath)
			if updated:
				self.setResultPath(resultpath)
			return updated

	def isPublic(self):
		return self.IsPublic

	def isExample(self):
		return self.IsExample

	def public(self):
		if self.data is not None: ## exists in db
			condition={'SN': self.SN}
			if self.ChipID:
				condition['ChipID'] = self.ChipID
			now = datetime.datetime.now()
			values = {'IsPublic':True, 'PublicTime':now}
			updated = self.DB.updateDBbyCondition(self.tableName, condition, **values)
			if updated:
				self.IsPublic = True
				self.PublicTime = now
			return updated
		else:
			self.IsPublic = True
			self.PublicTime = now
			return True

	def revertPublic(self):
		if self.data is not None:
			condition={'SN': self.SN}
			if self.ChipID:
				condition['ChipID'] = self.ChipID
			values = {'IsPublic':False}
			updated = self.DB.updateDBbyCondition(self.tableName, condition, **values)
			if updated:
				self.IsPublic = False
			return updated
		else:
			self.IsPublic = False
		return True

	def setExample(self, isExample):
		self.IsExample = isExample

	def updateExample(self, isExample):
		updated = self.DB.updateDB(self.tableName, 'SN', self.SN, IsExample=isExample)
		if updated :
			self.setExample(isExample)
		return updated

	def add(self):
		if not self.ChipID: 
			warnings.warn('No chip id, nothing to do')
		else:
			if not self.DataID: ## not exists
				data_id = get_randstr('DATA')
				all_field = self.getAllField()
				all_field['DataID'] = data_id
				del all_field['data']
				inserted = self.DB.insertDB(self.tableName, **all_field)
				if inserted:
					self.DataID = data_id
					self.data = self.getDataBySNandChip(self.SN, self.ChipID)
			return self.DataID

	def delete(self):
		if not self.ChipID: 
			warnings.warn('No chip id, nothing to do')
		else:
			deleted = self.DB.deleteDB(self.tableName, SN=self.SN, ChipID=self.ChipID)
			if deleted:
				self.data=None
			return deleted

	def getData(self):
		return self.data

	def getResultPath(self):
		return self.ResultPath
	
	def getSNByPath(self, path):
		sql = 'select SN from {table} where ResultPath=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(path,))

	def getDataByPath(self, path):
		sql = 'select * from {table} where ResultPath=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(path,))

	def getDataByID(self, data_id):
		sql = 'select * from {table} where DataID=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(data_id,))

	def getDataBySN(self, sn):
		sql = 'select * from {table} where SN=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(sn, ))

	def getDataBySNandChip(self, sn, chip_id):
		sql = 'select * from {table} where SN=%s and ChipID=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(sn, chip_id,))

	def getExampleData(self):
		sql = 'select * from {table} where IsExample=TRUE order by CreateTime desc'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql)[['DataID', 'SN', 'Species', 'Tissue', 'ChipID', 'Status', 'ResultPath']]

	def getPublicData(self):
		sql = 'select * from {table} where IsPublic=TRUE order by CreateTime desc'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql)[['DataID', 'SN', 'Species', 'Tissue', 'ChipID', 'Status', 'ResultPath']]
	
	def getSNByID(self, data_id):
		sql = 'select SN from {table} where DataID=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(data_id,))

