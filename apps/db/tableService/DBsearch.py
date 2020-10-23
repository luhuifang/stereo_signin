import pandas as pd
from apps.db.tableService.ConnectMYSQL import ConnectMYSQL
from db.database_settings import MYSQL_LOCAL as MYSQL

class DBsearch(ConnectMYSQL):
	def __init__(self):
		super().__init__(**MYSQL)
	
	def searchUserData(self, username):
		query = '''
			select distinct d.DataID, d.SN, d.Species, d.Tissue, d.ChipID, d.Status, d.ResultPath, d.CreateTime
			from Data as d 
			inner join Product as p 
			on d.SN=p.SN
			left join GroupMember as gm 
				on p.SharedGroup = gm.GroupID
				where 
					p.CustomerName = %s
				or p.SharedUser = %s
				or (
					gm.MemberName = %s
					and gm.MemberRoleName = 'Maintainer'
				)
			order by d.CreateTime desc;
		'''
		data = self.searchDB(query, args=(username, username, username))
		colname = ['DataID', 'SN', 'Species', 'Tissue', 'ChipID', 'Status', 'ResultPath', 'CreateTime']
		return pd.DataFrame(data, columns=colname)[['DataID', 'SN', 'Species', 'Tissue', 'ChipID', 'Status', 'ResultPath']]

	def searchSharedData(self, username):
		query = '''
			select distinct d.DataID, d.SN, d.Species, d.Tissue, d.ChipID, d.Status, d.ResultPath, d.CreateTime
			from Data as d
			left join DataPrivilege as dp
			on d.DataID = dp.DataSource
			where (
				dp.ExpirationDate > now()
				or dp.ExpirationDate is NULL
			) and (
				(dp.Type='User' and dp.MasterName=%s)
				or (dp.Type='Group' and dp.MasterID in 
					(select GroupID from GroupMember as gm where gm.MemberName=%s)
				)
			) 
			order by d.CreateTime desc;
		'''
		data = self.searchDB(query, args=(username,username))
		colname = ['DataID', 'SN', 'Species', 'Tissue', 'ChipID', 'Status', 'ResultPath', 'CreateTime']
		return pd.DataFrame(data, columns=colname)[['DataID', 'SN', 'Species', 'Tissue', 'ChipID', 'Status', 'ResultPath']]

	def searchYourGroup(self, username):
		query = '''
			select distinct g.GroupID, g.GroupName, g.CreateUserName, g.GroupDescription
			from Team as g
			inner join GroupMember as gm
			on g.GroupID = gm.GroupID
			where (
				gm.MemberName = %s
				or g.CreateUserName = %s
			)
		'''
		data = self.searchDB(query, args=(username, username))
		colname = ['GroupID', 'GroupName', 'CreateUserName', 'GroupDescription']
		return pd.DataFrame(data, columns=colname)

