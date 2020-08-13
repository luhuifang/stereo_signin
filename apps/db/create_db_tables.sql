/*create database*/
CREATE DATABASE Bioinfo;
use Bioinfo;

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
    PRIMARY KEY (`LoginName`),
    UNIQUE KEY `LoginName_UNIQUE` (`LoginName`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `UserRole`;
create table `UserRole`(
    `UserRoleID` int NOT NULL AUTO_INCREMENT,
    `UserRoleName` varchar(100) NOT NULL,
    `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`UserRoleID`),
    UNIQUE KEY `UserRoleID_UNIQUE` (`UserRoleID`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;