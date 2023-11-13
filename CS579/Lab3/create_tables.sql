#Jiankun Dong
create database HouseForSale;
use houseforsale;

CREATE TABLE realtor (
    RID VARCHAR(30) PRIMARY KEY,
    `Name` VARCHAR(30) NOT NULL,
    Company VARCHAR(30),
    BuyerFee TINYINT,
    SellerFee TINYINT
);
CREATE TABLE buyer (
    BID VARCHAR(30) PRIMARY KEY,
    Preapproved BOOLEAN,
    `Name` VARCHAR(30) NOT NULL,
    Phone VARCHAR(15),
    RID VARCHAR(30),
    FOREIGN KEY (RID)
        REFERENCES realtor (RID)
        ON UPDATE CASCADE ON DELETE SET NULL
);
CREATE TABLE seller (
    SID VARCHAR(30) PRIMARY KEY,
    Motivated BOOL,
    `Name` VARCHAR(30) NOT NULL,
    Phone VARCHAR(15),
    RID VARCHAR(30),
    FOREIGN KEY (RID)
        REFERENCES realtor (RID)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE property (
    PID VARCHAR(30) PRIMARY KEY,
    City VARCHAR(15),
    `Type` VARCHAR(15),
    Room TINYINT,
    Bath TINYINT,
    SF INT,
    Allowrance INT,
    ListDate DATE,
    SID VARCHAR(30),
    FOREIGN KEY (SID)
        REFERENCES seller (SID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE BID_HISTORY (
    PID VARCHAR(30),
    BID VARCHAR(30),
    `Date` DATE,
    Price INT,
    CloseDate DATE,
    ClosePrice INT,
    PRIMARY KEY (PID , BID , `Date`),
    FOREIGN KEY (PID)
        REFERENCES property (PID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (BID)
        REFERENCES buyer (BID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CHECK (CloseDate >= `Date`)
);