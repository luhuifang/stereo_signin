import warnings
import pandas as pd

from apps.db.tableService.Utils import get_randstr
from apps.db.tableService.TableServiceBase import TableServiceBase

class OrderForm(TableServiceBase):
    def __init__(self, OrderID='', ChipPlat='', ContactName='', ZipCode='', Address='', Quantity = '',
                Email='', Phone='', CurrentStatus='', NextStatus='', ContractNo='', LoginName='',
                Org='', Res=''):
        super().__init__('orderForm')

        self.OrderID = OrderID
        if self.checkExists():
            order = self.getOrder()
            self.ContactName = order['ContactName'][0]
            self.ChipPlat = order['ChipPlat'][0]
            self.ZipCode = order['ZipCode'][0]
            self.Address = order['Address'][0]
            self.Quantity = order['Quantity'][0]
            self.Email = order['Email'][0]
            self.Phone = order['Phone'][0]
            self.CurrentStatus = order['CurrentStatus'][0]
            self.NextStatus = order['NextStatus'][0]
            self.ContractNo = order['ContractNo'][0]
            self.LoginName = order['LoginName'][0]
            self.Organization = order['Organization'][0]
            self.ResearchInterests = order['ResearchInterests'][0]
        else:
            self.ContactName = ContactName
            self.ChipPlat = ChipPlat
            self.ZipCode = ZipCode
            self.Address = Address
            self.Quantity = Quantity
            self.Email = Email
            self.Phone = Phone
            self.CurrentStatus = CurrentStatus
            self.NextStatus = NextStatus
            self.ContractNo = ContractNo
            self.LoginName = LoginName
            self.Organization = Org
            self.ResearchInterests = Res
    
    def setContactName(self, ContactName):
        self.ContactName = ContactName

    def setOrganization(self, org):
        self.Organization = org
    
    def setResearchInterests(self, res):
        self.ResearchInterests = res

    def setChipPlat(self, ChipPlat):
        self.ChipPlat = ChipPlat
    
    def setQuantity(self, Quantity):
        self.Quantity = Quantity
    
    def setZipCode(self, ZipCode):
        self.ZipCode = ZipCode
    
    def setAddress(self, Address):
        self.Address = Address
    
    def setEmail(self, Email):
        self.Email = Email
    
    def setPhone(self, Phone):
        self.Phone = Phone
    
    def setCurrentStatus(self, CurrentStatus):
        self.CurrentStatus = CurrentStatus
    
    def setNextStatus(self, NextStatus):
        self.NextStatus = NextStatus

    def setContractNo(self, ContractNo):
        self.ContractNo = ContractNo
    
    def setLoginName(self, LoginName):
        self.LoginName = LoginName
        
    def getOrderById(self, order_id):
        sql = 'select * from {table} where OrderID=%s'.format(table=self.tableName)
        return self.getAllDataFromQuery(sql, args=(order_id,))
    
    def getOrderByContactName(self, ContactName):
        sql = 'select * from {table} where ContactName=%s'.format(table=self.tableName)
        return self.getAllDataFromQuery(sql, args=(ContactName,))
    
    def getOrderByLoginName(self, loginname):
        sql = 'select * from {table} where LoginName=%s'.format(table=self.tableName)
        return self.getAllDataFromQuery(sql, args=(loginname, ))

    def getOrder(self):
        return self.getOrderById(self.OrderID)
    
    def checkExists(self):
        return self.exists(OrderID=self.OrderID)
    
    def add(self):
        if not self.checkExists():
            order_id = get_randstr('ORDER')
            all_filed = self.getNonNullField()
            all_filed['OrderID'] = order_id
            if self.DB.insertDB(self.tableName, **all_filed):
                self.OrderID = order_id
        return self.OrderID
	
    def delete(self):
        if not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            deleted = self.DB.deleteDB(self.tableName, OrderID=self.OrderID)
            if deleted:
                self.OrderID = ''
            return deleted
    
    def update(self):
        if not self.OrderID or not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            all_filed = self.getAllField()
            del all_filed['OrderID']
            return self.DB.updateDB(self.tableName, 'OrderID', self.OrderID, **all_filed)
    
    def updateContactName(self):
        return self.updateByContactName(self.ContactName)
    
    def updateByContactName(self, contactname):
        if not self.OrderID or not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            updated = self.DB.updateDB(self.tableName, 'OrderID', self.OrderID, ContactName=contactname)
            if updated:
                self.ContactName = contactname
            return updated
    
    def updateZipCode(self):
        return self.updateByZipCode(self.ZipCode)
    
    def updateByZipCode(self, zipcode):
        if not self.OrderID or not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            updated = self.DB.updateDB(self.tableName, 'OrderID', self.OrderID, ZipCode=zipcode)
            if updated:
                self.ZipCode = zipcode
            return updated
    
    def updateAddress(self):
        return self.updateByAddress(self.Address)
    
    def updateByAddress(self, addr):
        if not self.OrderID or not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            updated = self.DB.updateDB(self.tableName, 'OrderID', self.OrderID, Address=addr)
            if updated:
                self.Address = addr
            return updated

    def updateEmail(self):
        return self.updateByEmail(self.Email)
    
    def updateByEmail(self, email):
        if not self.OrderID or not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            updated = self.DB.updateDB(self.tableName, 'OrderID', self.OrderID, Email=email)
            if updated:
                self.Email = email
            return updated
    
    def updatePhone(self):
        return self.updateByPhone(self.Phone)

    def updateByPhone(self, phone):
        if not self.OrderID or not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            updated = self.DB.updateDB(self.tableName, 'OrderID', self.OrderID, Phone=phone)
            if updated:
                self.Phone = phone
            return updated
    
    def updateCurrentStatus(self):
        return self.updateByCurrentStatus(self.CurrentStatus)

    def updateByCurrentStatus(self, currStatus):
        if not self.OrderID or not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            updated = self.DB.updateDB(self.tableName, 'OrderID', self.OrderID, CurrentStatus=currStatus)
            if updated:
                self.CurrentStatus = currStatus
            return updated
    
    def updateNextStatus(self):
        return self.updateByNextStatus(self.NextStatus)

    def updateByNextStatus(self, nextStatus):
        if not self.OrderID or not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            updated = self.DB.updateDB(self.tableName, 'OrderID', self.OrderID, NextStatus=nextStatus)
            if updated:
                self.NextStatus = nextStatus
            return updated
    
    def updateContractNo(self):
        return self.updateByContractNo(self.ContractNo)

    def updateByContractNo(self, ContractNo):
        if not self.OrderID or not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            updated = self.DB.updateDB(self.tableName, 'OrderID', self.OrderID, ContractNo=ContractNo)
            if updated:
                self.ContractNo = ContractNo
            return updated
    
    def updateLoginName(self):
        return self.updateByLoginName(self.LoginName)
    
    def updateByLoginName(self, username):
        if not self.OrderID or not self.checkExists():
            warnings.warn('Not exists, nothing to do')
        else:
            updated = self.DB.updateDB(self.tableName, 'OrderID', self.OrderID, LoginName=username)
            if updated:
                self.LoginName = username
            return updated
    

    