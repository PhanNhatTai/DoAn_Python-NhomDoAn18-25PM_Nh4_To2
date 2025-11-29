	create database QLBH
on (
	name = QLBH_mdf,
	filename = 'D:\QLBH.mdf',
	size = 10,
	maxsize = 50,
	filegrowth = 5)
log on (
	name = QLBH_log,
	filename = 'D:\QLBH.ldf',
	size = 10,
	maxsize = 50,
	filegrowth = 5)
use QLBH
create table THELOAI(
	matheloai char(5) primary key not null,
	tentheloai nvarchar(40),
)
create table BAIHAT (
	maso char(5) primary key not null ,
	tencasi nvarchar (30),
	tenbaihat nvarchar(30),
	ngayramat Date,
	matheloai char (5),
	foreign key (matheloai) references THELOAI(matheloai),
)
INSERT INTO THELOAI (matheloai, tentheloai) VALUES ('TLBH1', N'RAP');
INSERT INTO THELOAI (matheloai, tentheloai) VALUES ('TLBH2', N'Trữ tình');
INSERT INTO THELOAI (matheloai, tentheloai) VALUES ('TLBH3', N'Dân ca');
INSERT INTO THELOAI (matheloai, tentheloai) VALUES ('TLBH4', N'POP');
INSERT INTO THELOAI (matheloai, tentheloai) VALUES ('TLBH5', N'Rock');
INSERT INTO THELOAI (matheloai, tentheloai) VALUES ('TLBH6', N'Ballad');

