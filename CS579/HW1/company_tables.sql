/* -------------------------------------------------------------- */
/* company_tables.sql                                             */
/* on MySQL                                                       */
/* This file creates tables of COMPANY database.                  */
/* Uses database "company "                                       */
/* ---------------------------------------------------------------*/

use company;

create table employee
  (	fname		varchar(15)	not null,
	minit		char,
	lname		varchar(15)	not null,
	ssn			char(9)		primary key,
	bdate		date,
	address		varchar(30),
	sex			char,
	salary		decimal(10,2),
	superssn	char(9),
	dno			tinyint
  );

create table department
  (	dname		varchar(15)	unique not null,
	dnumber		tinyint		primary key,
	mgrssn		char(9),
	mgrstartdate	date,
	foreign key (mgrssn) references employee(ssn)
  );

create table dept_locations
  (	dnumber		tinyint not null,
	dlocation	varchar(15) not null,
	primary key (dnumber, dlocation),
	foreign key (dnumber) references department(dnumber)
  );

create table project
  (	pname		varchar(15)	unique not null,
	pnumber		tinyint		primary key,
	plocation	varchar(15),
	dnum		tinyint, 
	foreign key (dnum) references department(dnumber)
  );

create table works_on
  (	essn		char(9)	not null,
	pno		tinyint not null,
	hours	decimal(3,1),
	primary key (essn, pno),
	foreign key (essn) references employee(ssn),
	constraint proj_number
	  foreign key (pno) references project (pnumber)
  );

create table dependent
  (	essn		char(9) not null,
	dependent_name	varchar(15) not null,
	sex		char,
	bdate	date,
	relationship	varchar(8),
	primary key (essn, dependent_name),
	foreign key (essn) references employee(ssn)
  );

alter table employee add foreign key (superssn) references employee(ssn);
alter table employee add foreign key (dno) references department(dnumber);






