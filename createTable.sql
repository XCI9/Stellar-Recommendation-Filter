/*
\encoding UTF8
\copy school FROM 'D:\program\python\20220604DBFinalProject\school.csv' with (format csv, delimiter ',');
*/
create table school(
id varchar(3) primary key,
name varchar(64) not null
);

/*
\encoding UTF8
\copy Department FROM 'D:\program\python\20220604DBFinalProject\department.csv' with (format csv, delimiter ',');
*/
create table department(
/*It original Id differ in different year, so I use may own id.*/
id smallint primary key,
schoolId varchar(3) references school(id),
name varchar(64) not null
);


/*
\encoding UTF8
\copy Standard FROM 'D:\program\python\20220604DBFinalProject\standard.csv' with (format csv, delimiter ',');
*/
create table Standard(
year smallint,
subject varchar(3),
highest smallint not null,    /*0~15*/
higher  smallint not null,   /*0~15*/
mid     smallint not null,/*0~15*/
lower   smallint not null,  /*0~15*/
lowest  smallint not null,   /*0~15*/
primary key(year, subject)
);
/*Drop TABLE standard
select * from standard*/
/*
\encoding UTF8
\copy Main FROM 'D:\program\python\20220604DBFinalProject\main.csv' with (format csv, delimiter ',');
*/
create table Main(
year smallint,
departmentId smallint references department(id),
isAddition boolean, /*外加*/
primary key(year, departmentId, isAddition),
wantCount smallint not null,
finalCount smallint not null,
chineseTheshold smallint check (chineseTheshold >= 0 and chineseTheshold <= 5),
englishTheshold smallint check (englishTheshold >= 0 and englishTheshold <= 5),
mathTheshold    smallint check (mathTheshold    >= 0 and mathTheshold    <= 5),
societyTheshold smallint check (societyTheshold >= 0 and societyTheshold <= 5),
scienceTheshold smallint check (scienceTheshold >= 0 and scienceTheshold <= 5),
totalTheshold   smallint check (totalTheshold   >= 0 and totalTheshold   <= 5),
listeningTheshold smallint check (listeningTheshold >= 0 and listeningTheshold <= 3),
CompareRule1 varchar(10),
CompareRule2 varchar(10),
CompareRule3 varchar(10),
CompareRule4 varchar(10),
CompareRule5 varchar(10),
CompareRule6 varchar(10),
CompareRule7 varchar(10),
firstStageCount smallint,
firstStageRule1 varchar(5),
firstStageRule2 varchar(5),
firstStageRule3 varchar(5),
firstStageRule4 varchar(5),
firstStageRule5 varchar(5),
firstStageRule6 varchar(5),
firstStageRule7 varchar(5),
secondStageCount smallint,
secondStageRule1 varchar(5),
secondStageRule2 varchar(5),
secondStageRule3 varchar(5),
secondStageRule4 varchar(5),
secondStageRule5 varchar(5),
secondStageRule6 varchar(5),
secondStageRule7 varchar(5)
);

create index departmentIndex on Main(departmentId);