
DROP TABLE IF EXISTS `Orders`;
create table `Orders`(
    `OrderID` varchar(100) NOT NULL,
    `LoginName` varchar(100) DEFAULT NULL,
    `Email` varchar(200) DEFAULT NULL,
    `Phone` varchar(20) DEFAULT NULL,
    `Address` varchar(200) DEFAULT NULL,
	`Postcode` varchar(200) DEFAULT NULL,
    `Research` varchar(200) DEFAULT NULL,
	`States` varchar(200) DEFAULT NULL,
    `Organization` varchar(200) DEFAULT NULL,
    `StatesUpdateDate` date DEFAULT NULL,
    `OrderDate` date DEFAULT NULL,
    PRIMARY KEY (`OrderID`),
    UNIQUE KEY `OrderID_UNIQUE` (`OrderID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;