#Jiankun Dong Lab 4
use HouseForSale;
delimiter //
create trigger earliest_bid_data 
before insert on bid_history 
for each row
begin
	declare list_date date;
	SELECT p.ListDate
	INTO list_date 
    FROM property AS p
	WHERE p.PID = new.PID;
    
	if new.`Date` < list_date then
		signal SQLSTATE '45000'
			set message_text = 'Bid history entries cannot have date earilier than property list date';
	end if;
end //
delimiter ;

delimiter //
create trigger different_realtor
before insert on bid_history
for each row
begin
	declare buyer_RID VARCHAR(30);
    declare seller_RID VARCHAR(30);
    
    SELECT b.RID into buyer_RID
    FROM buyer as b
    WHERE b.BID = new.BID;
    
    select s.RID into seller_RID
    from seller as s, property as p
    where s.SID = p.SID and p.PID = new.PID;
    
    if seller_RID = buyer_RID then
		signal SQLSTATE '45000'
			set message_text = 'Seller and Buyer has the same Realtor ID';
	end if;
end //
delimiter ;

delimiter //
create trigger price_floor
before insert on bid_history
for each row
begin
	declare max_bid INT;
    select max(Price) into max_bid from bid_history as h where h.PID = new.PID;
    if new.Price <= max_bid  then
		signal SQLSTATE '45000'
			set message_text = 'The new bid is not greater than the previous max bid';
	end if;
end //
delimiter ; 

delimiter //
create procedure get_highest_bidder(in PID VARCHAR(30), out s_name VARCHAR(30),out r_name VARCHAR(30),out Price INT)
begin
	select s.`Name`, r.`Name` into s_name, r_name
    from seller as s, property as p, realtor as r
    where s.SID = p.SID and s.RID = r.RID and p.PID = PID;

    select max(bh.Price) into Price
    from bid_history as bh
    where bh.PID = PID;
end //
delimiter ;
#testing:
#1
select * from bid_history where bid_history.PID = 1;
insert into bid_history values (1,1,'1300-01-01',500,Null,0);
#2
#3

#4
call get_highest_bidder(2, @s_name, @r_name, @Price);
select concat(@s_name) as 'Seller Name',
	concat(@r_name) as 'Realtor Name',
    concat(@Price) as 'Property Price';