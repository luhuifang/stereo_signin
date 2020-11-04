/*create database*/
CREATE DATABASE Bioinfo;
use Bioinfo;

/*create table 'task'*/

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
SET character_set_client = utf8mb4 ;
CREATE TABLE `task` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(1000) NOT NULL,
  `username` varchar(1000) NOT NULL,
  `path` varchar(1000) NOT NULL,
  `itemnumber` varchar(1000) NOT NULL,
  `subitemnumber` varchar(1000) DEFAULT NULL,
  `state` varchar(100) NOT NULL,
  `starttime` datetime NOT NULL,
  `endtime` datetime DEFAULT NULL,
  `flow` varchar(1000) NOT NULL,
  `samplename` varchar(1000) NOT NULL,
  `parameter` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


/*create table 'exampledata'*/
DROP TABLE IF EXISTS `exampledata`;
create table `exampledata` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `no` varchar(100) DEFAULT NULL,
    `chip_1` varchar(100) DEFAULT NULL,
    `library` varchar(100) DEFAULT NULL,
    `tissue` varchar(100) DEFAULT NULL,
    `nlen` int NOT NULL,
    `platform` varchar(100) DEFAULT NULL,
    `shard` varchar(100) DEFAULT NULL,
    `chip_2` varchar(100) DEFAULT NULL,
    `resultpath` varchar(1000) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `downloadPath`;
create table `downloadPath`(
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `root` varchar(1000) NOT NULL,
    `isAvailable` BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

/*create table 'firstSequences'*/
DROP TABLE IF EXISTS `firstSequences`;
create table `firstSequences`(
    `no` varchar(200) NOT NULL,
    `chip_id` varchar(200) DEFAULT NULL,
    `platform` varchar(200) DEFAULT NULL,
    `primer_type` varchar(100) DEFAULT NULL,
    `FOV_row` varchar(100) DEFAULT NULL,
    `FOV_col` varchar(100) DEFAULT NULL,
    `barcode_segment` int DEFAULT NULL,
    `barcode_len` int DEFAULT NULL,
    `RC` varchar(10) NOT NULL DEFAULT 'False',
    `QC` varchar(10) DEFAULT NULL,
    `report_file` varchar(500) DEFAULT NULL,
    `barcode_start` int DEFAULT 0,
    `fastq_path` varchar(1000) DEFAULT NULL,
    `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
    `barcode_pos_file` varchar(1000) DEFAULT NULL,
    
    PRIMARY KEY (`no`),
    UNIQUE KEY `no_UNIQUE` (`no`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

/*create table 'secondSequences'*/
DROP TABLE IF EXISTS `secondSequences`;
create table `secondSequences`(
    `id` bigint(32) NOT NULL AUTO_INCREMENT,
    `no` varchar(200) NOT NULL,
    `species` varchar(100) DEFAULT NULL,
    `tissue` varchar(200) DEFAULT NULL,
    `chip_id` varchar(200) DEFAULT NULL,
    `library_type` varchar(200) DEFAULT NULL,
    `barcode_len` int DEFAULT NULL,
    `barcode_start` int DEFAULT 0,
    `read_len` int DEFAULT NULL,
    `UMI_len` int DEFAULT NULL,
    `UMI_start_pos` int DEFAULT NULL,
    `UMI_location` varchar(20) DEFAULT 'read1',
    `Remarks` varchar(200) DEFAULT NULL,
    `fastq1` varchar(1000) DEFAULT NULL,
    `fastq2` varchar(1000) DEFAULT NULL,
    `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`),
    CONSTRAINT fk_dataAnal_chip FOREIGN KEY(`no`) REFERENCES firstSequences(`no`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

/*create table 'workflowResult'*/
DROP TABLE IF EXISTS `workflowResult`;
create table `workflowResult`(
    `task_id` varchar(32) NOT NULL,
    `no` varchar(200) NOT NULL,
    `user_name` varchar(200) NOT NULL,
    `status` varchar(100) NOT NULL DEFAULT 'running',
    `chip_2` varchar(500) NOT NUll,
    `Remarks` varchar(200) DEFAULT NULL,
    `result_path` varchar(1000) DEFAULT NULL,
    `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`task_id`),
    UNIQUE KEY `task_id_UNIQUE` (`task_id`),
    CONSTRAINT fk_workflow_chip FOREIGN KEY(`no`) REFERENCES firstSequences(`no`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


/*Data Manager*/
DROP TABLE IF EXISTS `Users`;
create table `Users`(
    `UserID` varchar(100) NOT NULL,
    `LoginName` varchar(100) NOT NULL,
    `LoginPasswd` varchar(200) DEFAULT NULL,
    `RealName` varchar(200) DEFAULT NULL,
    `Email` varchar(200) DEFAULT NULL,
    `Phone` varchar(20) DEFAULT NULL,
    `District` varchar(200) DEFAULT NULL,
    `Country` varchar(200) DEFAULT NULL,
    `City` varchar(200) DEFAULT NULL,
    `Organization` varchar(200) DEFAULT NULL,
    `UserRoleID` int DEFAULT 1,
    `RegisterTime` datetime DEFAULT CURRENT_TIMESTAMP,
    `HashKey` varchar(32) NOT NULL,
    PRIMARY KEY (`LoginName`),
    UNIQUE KEY `LoginName_UNIQUE` (`LoginName`),
    UNIQUE KEY `UserID_UNIQUE` (`UserID`),
    UNIQUE KEY `Email_UNIQUE` (`Email`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `UserRole`;
create table `UserRole`(
    `UserRoleID` int NOT NULL AUTO_INCREMENT,
    `UserRoleName` varchar(100) NOT NULL,
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`UserRoleID`),
    UNIQUE KEY `UserRoleID_UNIQUE` (`UserRoleID`),
    UNIQUE KEY `UserRoleName_UNIQUE` (`UserRoleName`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `Privilege`;
create table `Privilege`(
    `PrivilegeID` varchar(100) NOT NULL,
    `PrivilegeMaster` varchar(100) NOT NULL,
    `PrivilegeMasterValue` int NOT NULL,
    `PrivilegeAccess` varchar(100) NOT NULL,
    `PrivilegeAccessValue` int NOT NULL,
    `PrivilegeOperation` varchar(100) NOT NULL DEFAULT 'disable',
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`PrivilegeID`),
    UNIQUE KEY `PrivilegeID_UNIQUE` (`PrivilegeID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `Menu`;
create table `Menu`(
    `MenuID` int NOT NULL AUTO_INCREMENT,
    `MenuOrder` int DEFAULT NULL,
    `MenuName` varchar(100) DEFAULT NULL,
    `MenuUrl` varchar(1000) DEFAULT NULL,
    `MenuIcon` varchar(1000) DEFAULT NULL,
    `IsVisible` BOOLEAN DEFAULT TRUE,
    `MenuClassName` varchar(500) DEFAULT NULL,
    `MenuIdName` varchar(500) DEFAULT NULL,
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`MenuID`),
    UNIQUE KEY `MenuID_UNIQUE` (`MenuID`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `Team`;
create table `Team`(
    `GroupID` varchar(100) NOT NULL,
    `GroupName` varchar(500) NOT NULL,
    `GroupDescription` longText DEFAULT NULL,
    `CreateUserID` varchar(100) DEFAULT NULL,
    `CreateUserName` varchar(100) DEFAULT NULL,
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    `IsDelete` BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (`GroupID`),
    UNIQUE KEY `GroupID_UNIQUE` (`GroupID`),
    CONSTRAINT fk_team_users FOREIGN KEY(`CreateUserID`) REFERENCES Users(`UserID`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_team_users2 FOREIGN KEY(`CreateUserName`) REFERENCES Users(`LoginName`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `GroupMember`;
create table `GroupMember`(
    `ID` bigint(32) NOT NULL AUTO_INCREMENT, 
    `GroupID` varchar(100) NOT NULL,
    `MemberID` varchar(100) DEFAULT NULL,
    `MemberName` varchar(100) DEFAULT NULL,
    `MemberRoleID` int DEFAULT NULL,
    `MemberRoleName` varchar(100) DEFAULT NULL,
    `JoinTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`ID`),
    UNIQUE KEY `ID_UNIQUE` (`ID`),
    CONSTRAINT fk_gMember_team FOREIGN KEY(`GroupID`) REFERENCES Team(`GroupID`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_gMember_users FOREIGN KEY(`MemberID`) REFERENCES Users(`UserID`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_gMember_users2 FOREIGN KEY(`MemberName`) REFERENCES Users(`LoginName`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_gMember_gRole FOREIGN KEY(`MemberRoleID`) REFERENCES GroupRole(`GroupRoleID`) ON DELETE SET NULL ON UPDATE CASCADE
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `GroupRole`;
create table `GroupRole`(
    `GroupRoleID` int NOT NULL AUTO_INCREMENT, 
    `GroupRoleName` varchar(100) NOT NULL,
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`GroupRoleID`),
    UNIQUE KEY `GroupRoleID_UNIQUE` (`GroupRoleID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `GroupOperation`;
create table `GroupOperation`(
    `OperationID` int NOT NULL AUTO_INCREMENT, 
    `OperationName` varchar(100) NOT NULL,
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`OperationID`),
    UNIQUE KEY `OperationID_UNIQUE` (`OperationID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `Product`;
create table `Product`(
    `ProductID` bigint(20) NOT NULL AUTO_INCREMENT,
    `SN` varchar(200) NOT NULL,
    `ProductionDate` datetime DEFAULT CURRENT_TIMESTAMP,
    `Price` varchar(100) DEFAULT NULL,
    `Status` varchar(100) DEFAULT 'ForSale',
    `CustomerName` varchar(100) DEFAULT NULL,
    `OrderID` varchar(40) DEFAULT NULL,
    `SoldDate` datetime DEFAULT NULL,
    `SharedUser` varchar(100) DEFAULT NULL,
    `SharedGroup` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`ProductID`),
    UNIQUE KEY `ProductID_UNIQUE` (`ProductID`),
    CONSTRAINT fk_product_chip FOREIGN KEY(`SN`) REFERENCES firstSequences(`no`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_product_users FOREIGN KEY(`SharedUser`) REFERENCES Users(`UserID`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_product_team FOREIGN KEY(`SharedGroup`) REFERENCES Team(`GroupID`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_product_order FOREIGN KEY(`OrderID`) REFERENCES orderForm(`OrderID`) ON DELETE SET NULL ON UPDATE CASCADE
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `Data`;
create table `Data`(
    `DataID` varchar(100) NOT NULL,
    `SN` varchar(100) NOT NULL,
    `Species` varchar(200) DEFAULT NULL,
    `Tissue` varchar(200) DEFAULT NULL,
    `ChipID` varchar(1000) NOT NULL,
    `Status` varchar(100) DEFAULT 'panding',
    `ResultPath` varchar(1000) DEFAULT NULL,
    `IsPublic` boolean DEFAULT FALSE,
    `PublicTime` datetime DEFAULT NULL,
    `IsExample` boolean DEFAULT FALSE,
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`DataID`),
    UNIQUE KEY `DataID_UNIQUE` (`DataID`),
    CONSTRAINT fk_data_chip FOREIGN KEY(`SN`) REFERENCES firstSequences(`no`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `DataPrivilege`;
create table `DataPrivilege`(
    `PrivilegeID` bigint(20) NOT NULL AUTO_INCREMENT,
    `DataSource` varchar(100) NOT NULL,
    `MasterID` varchar(100) NOT NULL,
    `MasterName` varchar(500) NOT NULL,
    `MasterRole` varchar(100) DEFAULT 'Guest',
    `Type` varchar(100) NOT NULL,
    `ExpirationDate` datetime DEFAULT NULL,
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`PrivilegeID`),
    UNIQUE KEY `PrivilegeID_UNIQUE` (`PrivilegeID`),
    CONSTRAINT fk_dataPrivilege_data FOREIGN KEY(`DataSource`) REFERENCES Data(`DataID`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `ACLlog`;
create table `ACLlog`(
    `ID`  bigint(20) NOT NULL AUTO_INCREMENT,
    `Operator`    varchar(100) NOT NULl,
    `OperationTime`   datetime DEFAULT CURRENT_TIMESTAMP,
    `OperationSource` varchar(32) NOT NULL,
    `OperationSourceValue`    varchar(100) NOT NULL,
    `OperationSourceValueName` varchar(100) NOT NULL DEFAULT 'No Name',
    `OperationType`   varchar(100) NOT NULL,
    `OperationField`  varchar(500) DEFAULT NULL,
    `OperationValue`  varchar(500) DEFAULT NULL,
    PRIMARY KEY (`ID`),
    UNIQUE KEY `ID_UNIQUE` (`ID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `orderForm`;
create table `orderForm`(
    `OrderID` varchar(40) NOT NULL,
    `ChipPlat` varchar(32) NOT NULL,
    `ContactName`   varchar(100) DEFAULT NULL,
    `Organization` varchar(300) DEFAULT NULL,
    `ResearchInterests` varchar(300) DEFAULT NULL,
    `ZipCode`   varchar(10) DEFAULT NULL,
    `Address`   varchar(1000) DEFAULT NULL,
    `Email` varchar(100) DEFAULT NULL,
    `Phone` varchar(20) DEFAULT NULL,
    `Quantity` int DEFAULT 1,
    `AssignedNum` int DEFAULT 0,
    `CreateTime`  datetime DEFAULT CURRENT_TIMESTAMP,
    `ModifyTime` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    `CurrentStatus` int DEFAULT 1,
    `NextStatus`    int DEFAULT 2,
    `ContractNo`    varchar(32) DEFAULT NULL,
    `Accessory` varchar(1000) DEFAULT NULL,
    `LoginName` varchar(100) DEFAULT NULL,
    `isdelete` boolean not null default 0,
    PRIMARY KEY(`OrderID`),
    UNIQUE KEY `OrderID_UNIQUE` (`OrderID`),
    CONSTRAINT fk_order_status FOREIGN KEY(`CurrentStatus`) REFERENCES orderStatus(`OrderStatusID`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_order_status2 FOREIGN KEY(`NextStatus`) REFERENCES orderStatus(`OrderStatusID`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_order_users FOREIGN KEY(`LoginName`) REFERENCES Users(`LoginName`) ON DELETE SET NULL ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `orderStatus`;
create table `orderStatus`(
    `OrderStatusID` int NOT NULL AUTO_INCREMENT,
    `OrderStatusName` varchar(100) NOT NULL,
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`OrderStatusID`),
    UNIQUE KEY `OrderStatusID_UNIQUE` (`OrderStatusID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `suggestion`;
create table `suggestion`(
    `ID` int NOT NULL AUTO_INCREMENT,
    `Name` varchar(100) NOT NULL,
    `Email` varchar(100) DEFAULT NULL,
    `Organization` varchar(300) DEFAULT NULL,
    `ResearchInterests` varchar(300) DEFAULT NULL,
    `ResearchIdea` longText DEFAULT NULL,
    `Proposal` longText DEFAULT NULL,
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`ID`),
    UNIQUE KEY `ID_UNIQUE` (`ID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;