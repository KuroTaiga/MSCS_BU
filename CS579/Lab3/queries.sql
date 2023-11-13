#Jiankun Dong
use houseforsale;
#Q1
SELECT 
    p.PID, r.`Name`
FROM
    property AS p,
    realtor AS r,
    seller AS s
WHERE
    s.RID = r.RID AND p.SID = s.SID
        AND p.city = 'NewYork'
        AND p.room >= 2
        AND P.Bath >= 2;
#Q2
SELECT 
    b.BID, b.`Name`, h.Price
FROM
    buyer AS b,
    bid_history AS h
WHERE
    b.BID = h.BID AND h.PID = '1';
#Q3 only property 4 and 24 sold within 15 days, this also include properties with no bids
select p.PID, r.`Name`,r.Company
from property as p, realtor as r, seller as s
where s.RID = r.RID and s.SID = p.SID
and PID in ((select h.PID
from bid_history as h
where h.PID in (select p.PID
				  From property as p, bid_history as h
                  where p.PID = h.PID and (h.CloseDate-p.listdate) > 15)
	or h.PID not in (select PID
					From bid_history
					Where CloseDate is not null))
UNION
(select p.PID
from property as p
where p.PID not in (select PID
					from bid_history)));

#Q4
SELECT 
    p.PID, p.City, r.`Name`
FROM
    property AS p,
    seller AS s,
    realtor AS r
WHERE
    p.SID = s.SID AND r.RID = s.RID
        AND p.PID NOT IN (SELECT 
            PID
        FROM
            bid_history);
#Q5 this value is gonna be large
SELECT 
    AVG(h.CloseDate - p.listdate) as Average_Listing_Time
FROM
    property AS p,
    bid_history AS h
WHERE
    p.PID = h.PID
        AND h.CloseDate IS NOT NULL;