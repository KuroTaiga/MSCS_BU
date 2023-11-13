create database temp_db;

use temp_db;

create table dept(
	dnumber int primary key default 1,
	dname varchar(64)
);

create table emp(
	eid int primary key,
	ename varchar(64),
	dno int,
	foreign key(dno) references dept(dnumber) on update cascade
);
	
create table pjt(
	pnumber int primary key,
	pname varchar(64),
	dnum int,
	foreign key(dnum) references dept(dnumber) on update set null
);

create table car(
	vin int primary key,
	make varchar(32),
	owner int,
	foreign key(owner) references dept(dnumber) on update set default
);

insert into dept values(1, 'HR');
insert into dept values(2, 'Production');
insert into dept values(3, 'Sales');

insert into emp values(1, 'John', 1);
insert into emp values(2, 'Susan', 1);
insert into emp values(3, 'Kelsey', 2);

insert into pjt values(1, 'Truck', 1);
insert into pjt values(2, 'Sedan', 2);
insert into pjt values(3, 'Wagon', 2);

insert into car values(1, 'GM', 3);
insert into car values(2, 'Ford', 3);
insert into car values(3, 'Chevy', 3);


	
	
