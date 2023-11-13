#Jiankun Dong
use houseforsale;
SET GLOBAL local_infile=1;
insert into realtor values(12345,"Thomas H. Jefferson","Zillow",5,3);
insert into realtor values(114514,"Tadokoro","COAT CORP",6,9);
insert into realtor values(88888,"Fugui Wang","Royal",8,8);
insert into realtor values(7761,"Jeff T. Jeff","Progressive",1,99);
insert into realtor values(7251213,"Ian Chelminski","HyMan & Friends",2,2);
insert into realtor values(5142,"Richard Dickenson","Shaft CO.",11,8);

insert into buyer values (1,True,"Jiankun Dong","797-123-4567",7251213);
insert into buyer values (2,False, "Richard Jackson", "812-812-8182", 7761);
insert into buyer values (3,True, "Jack Billie", "111-111-1111", 12345);
insert into buyer values (4,True, "Ako Bko", "987-675-2222", 5142);
insert into buyer values (5,False, "J.J. Jefferson", "123-456-7890", 7761);

insert into seller values (0,False,"Jack","999-999-9999",7761);
insert into seller values (1,False, "Tom", "111-111-1112",88888);
insert into seller values (2,True,"Josh","444-444-4441",12345);
insert into seller values (3,False,"James","555-555-5556",7251213);
insert into seller values (4,True,"Mike","000-000-0001",5142);

insert into property values (1, "Boston", "Condo", 5,3,3000,100000,'1999-05-22',0);
insert into property values (2, "Boston", "Apartment", 2,1,2100,0,'2000-07-22',1);
insert into property values (3, "Boston", "Apartment", 2,2,2200,100,'2007-05-22',2);
insert into property values (4, "Boston", "ranch", 8,6,8000,100000,'2009-01-22',3);
insert into property values (5, "NewYork", "Apartment", 1,1,800,0,'2022-09-22',4);
insert into property values (6, "NewYork", "Apartment", 2,1,1200,100,'2022-06-01',0);
insert into property values (7, "NewYork", "Apartment", 3,2,1500,100000,'2022-06-02',1);
insert into property values (8, "NewYork", "Condo", 2,0,700,0,'2021-06-01',2);
insert into property values (9, "NewYork", "Condo", 2,2,800,100,'2021-06-23',3);
insert into property values (10, "Tokyo", "Apartment", 3,2,300,100000,'2004-05-22',4);
insert into property values (11, "Tokyo", "Apartment", 2,2,200,0,'2004-05-22',0);
insert into property values (12, "Tokyo", "Apartment", 1,1,83,100,'2004-05-22',1);
insert into property values (13, "Tokyo", "Apartment", 2,1,150,100000,'2004-05-22',2);
insert into property values (14, "Tokyo", "Condo", 3,2,400,0,'2004-05-22',3);
insert into property values (15, "Cedar Rapids", "ranch", 5,3,15123,100,'2021-05-22',4);
insert into property values (16, "Cedar Rapids", "ranch", 5,4,25123,100000,'2021-05-22',0);
insert into property values (17, "Cedar Rapids", "ranch", 8,8,35123,0,'2021-05-22',1);
insert into property values (18, "Cedar Rapids", "Condo", 3,2,5123,100,'2021-05-22',2);
insert into property values (19, "Cedar Rapids", "Apartment", 2,2,2300,100000,'2021-05-22',3);
insert into property values (20, "Cedar Rapids", "Apartment", 1,1,923,0,'2021-05-22',4);
insert into property values (21, "Beijing", "Apartment", 3,2,4123,100,'2013-09-23',0);
insert into property values (22, "Beijing", "Apartment", 2,1,1123,100000,'1997-12-31',1);
insert into property values (23, "Beijing", "Apartment", 3,2,2823,0,'2003-01-22',2);
insert into property values (24, "Shanghai", "Apartment", 4,3,3123,100,'2020-05-21',3);
insert into property values (25, "Shanghai", "Apartment", 2,1,2378,100000,'2023-01-02',4);
insert into property values (26, "Shanghai", "Apartment", 1,1,523,0,'2022-04-23',0);
insert into property values (27, "Shanghai", "Apartment", 1,1,623,100,'2022-06-09',1);

LOAD DATA LOCAL INFILE "C:/BU/CSSE/CS579/Lab3/bid_history.csv" INTO TABLE bid_history
fields terminated by ','
lines terminated by '\n'
ignore 1 lines
(PID, BID,@'Date',Price,@CloseDate,ClosePrice)
set `Date` = str_to_date(@`Date`,'%m/%d/%Y'), CloseDate = str_to_date(@CloseDate,'%m/%d/%Y');
