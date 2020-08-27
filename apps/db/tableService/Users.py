import warnings
import hashlib

from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from apps.db.tableService.Utils import get_randstr
from apps.db.tableService.TableServiceBase import TableServiceBase

class Users(TableServiceBase, UserMixin):
	def __init__(self, username='', userid = '', realname='', email='', phone='', district='', country='', city='', org=''):
		super().__init__('Users')

		if username:
			self.LoginName = username
			self.UserID = self.getUserIdByName(username)
		elif userid:
			self.UserID = userid
			self.LoginName = self.getUserNameById(userid)
		else:
			self.UserID = userid
			self.LoginName = username

		self.RealName = realname
		self.Email = email
		self.Phone = phone
		self.District = district
		self.Country = country
		self.City = city
		self.Organization = org
		self.UserRoleID = 1
		self._checkUserName(self.LoginName)

	def _checkUserName(self, username):
		u = self.getUserByName(username)
		if not u.empty:
			self.RealName = u['RealName'][0]
			self.Email = u['Email'][0]
			self.Phone = u['Phone'][0]
			self.District = u['District'][0]
			self.Country = u['Country'][0]
			self.City = u['City'][0]
			self.Organization = u['Organization'][0]
			self.UserRoleID = u['UserRoleID'][0]

	def checkExists(self):
		return self.exists(LoginName=self.LoginName)

	def checkEmailExists(self):
		return self.exists(Email=self.Email)

	def getUserIdByName(self, username):
		sql = 'select UserID from {table} where LoginName=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(username,))

	def getUserNameById(self, userid):
		sql = 'select LoginName from {table} where UserID=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(userid,))

	def getUserByName(self, username):
		sql = 'select * from {table} where LoginName=%s'.format(table=self.tableName)
		return self.getAllDataFromQuery(sql, args=(username,))

	def getUser(self):
		all_field = self.getAllField()
		if 'LoginPasswd' in all_field:
			del all_field['LoginPasswd']
		return all_field

	def getName(self):
		return self.LoginName

	def getId(self):
		return self.UserID
	
	def getKey(self):
		if self.LoginName :
			return self.getKeyByName(self.LoginName)
		elif self.UserID:
			return self.getKeyById(self.UserID)
		return ''

	def getKeyByName(self, name):
		sql = 'select HashKey from {table} where LoginName=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(name,))

	def getKeyById(self, userid):
		sql = 'select HashKey from {table} where UserID=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(userid,))

	def add(self):
		if not self.LoginName:
			warnings.warn('No Username, nothing to do')
		elif not self.UserID: ## not exists
			user_id = get_randstr('USER')
			row_str = user_id.split('_')[1]
			hashkey = hashlib.md5(row_str.encode(encoding='utf-8')).hexdigest()
			all_field = self.getAllField()
			all_field['UserID'] = user_id
			all_field['HashKey'] = hashkey
			if self.DB.insertDB(self.tableName , **all_field):
				self.UserID = user_id
		return self.UserID

	def delete(self):
		if not self.UserID:
			warnings.warn('Not exists, nothing to do')
		else:
			deleted = self.DB.deleteDB(self.tableName, LoginName=self.LoginName)
			if deleted :
				self.UserID = ''
			return deleted

	def update(self):
		if not self.UserID:
			warnings.warn('Not exists, nothing to do')
		else:
			all_field = self.getAllField()
			del all_field['LoginName']
			return self.DB.updateDB(self.tableName, 'LoginName', self.LoginName, **kwargs)

	def existsUser(self):
		return self.exists(LoginName=self.LoginName)

	def setRealName(self, realname):
		self.RealName = realname

	def updateRealName(self, realname):
		updated = self.DB.updateDB(self.tableName, 'LoginName', self.LoginName, RealName=realname)
		if updated:
			self.setRealName(realname)
		return updated

	def setEmail(self, email):
		self.Email = email

	def updateEmail(self, email):
		updated = self.DB.updateDB(self.tableName, 'LoginName', self.LoginName, Email=email)
		if updated:
			self.setEmail(email)
		return updated

	def setPhone(self, phone):
		self.Phone = phone

	def updatePhone(self, phone):
		updated = self.DB.updateDB(self.tableName, 'LoginName', self.LoginName, Phone=phone)
		if updated:
			self.setPhone(phone)
		return updated

	def setDistrict(self, district):
		self.District = district

	def updateDistrict(self, district):
		updated = self.DB.updateDB(self.tableName, 'LoginName', self.LoginName, District=district)
		if updated:
			self.setDistrict(district)
		return updated

	def setCountry(self, country):
		self.Country = country

	def updateCountry(self, country):
		updated = self.DB.updateDB(self.tableName, 'LoginName', self.LoginName, Country=country)
		if updated:
			self.setCountry(country)
		return updated

	def setCity(self, city):
		self.City = city

	def updateCity(self, city):
		updated = self.DB.updateDB(self.tableName, 'LoginName', self.LoginName, City=city)
		if updated:
			self.setCity(city)
		return updated

	def setOrg(self, org):
		self.Organization = org

	def updateOrg(self, org):
		updated = self.DB.updateDB(self.tableName, 'LoginName', self.LoginName, Organization=org)
		if updated:
			self.setOrg(org)
		return updated

	def setUserRole(self, role_id):
		self.UserRoleID = role_id

	def updateUserRole(self, role_id):
		updated = self.DB.updateDB(self.tableName, 'LoginName', self.LoginName, UserRoleID=role_id)
		if updated:
			self.setUserRole(role_id)
		return updated
	
	def getFieldByName(self, username, fieldname):
		sql = 'select {field} from {table} where LoginName=%s'.format(field=fieldname, table=self.tableName)
		return self._getSingleField(sql, args=(username,))
	
	def getFieldById(self, userid, fieldname):
		sql = 'select {field} from {table} where UserID=%s'.format(field=fieldname, table=self.tableName)
		return self._getSingleField(sql, args=(userid,))

	def __getPasswd(self):
		sql = 'select LoginPasswd from {table} where LoginName=%s'.format(table=self.tableName)
		return self._getSingleField(sql, args=(self.LoginName,))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		"""save user name, id and password hash to json file"""
		self.LoginPasswd = generate_password_hash(password)
		if not self.UserID: ## not exists
			self.add()
		else: ## exists, modify passwd
			self.DB.updateDB(self.tableName, 'LoginName', self.LoginName, LoginPasswd=self.LoginPasswd)

	def verifyPassword(self, password):
		password_hash = self.__getPasswd()
		if not password_hash :
			return False
		return check_password_hash(password_hash, password)
