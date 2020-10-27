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
    `CreateTime`    datetime DEFAULT CURRENT_TIMESTAMP,
    `CurrentStatus` int DEFAULT 1,
    `NextStatus`    int DEFAULT 2,
    `ContractNo`    varchar(32) DEFAULT NULL,
    `Accessory` varchar(1000) DEFAULT NULL,
    `LoginName` varchar(100) DEFAULT NULL,
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