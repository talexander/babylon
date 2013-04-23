create table store(
	id int unsigned not null AUTO_INCREMENT PRIMARY KEY ,
	name varchar(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

create table store_good(
	id int unsigned not null AUTO_INCREMENT PRIMARY KEY ,
	store  int unsigned not null,
	good int unsigned not null,
	amount int unsigned not null,
	price DECIMAL(9,2) unsigned NOT NULL,
	flags bigint unsigned not null default 0

) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE good_category (
	id  int unsigned not null AUTO_INCREMENT PRIMARY KEY,
	name varchar(255) not null,
	ns_left int unsigned not null,
	ns_right int unsigned not null,
	flags bigint unsigned not null default 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE good(
	id   int unsigned not null AUTO_INCREMENT PRIMARY KEY,
	alias varchar(40) not null,
	name varchar (255) not null,
	descr mediumtext default '',
	good_category int unsigned not null,
	flags bigint unsigned not null
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE good_property (
	id  int unsigned not null AUTO_INCREMENT PRIMARY KEY,
	property int unsigned not null,
	val varchar(255) not null,
	flags bigint unsigned not null default 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE property(
	id  int unsigned not null AUTO_INCREMENT PRIMARY KEY,
	name varchar(255) not null,
	alias varchar(40) not null,
	measure int unsigned,
	flags bigint unsigned not null default 0,
	property_group int unsigned
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE property_group(
	id int unsigned not null AUTO_INCREMENT PRIMARY KEY,
	name varchar(255) not null,
	alias varchar(40) not null,
	flags bigint unsigned not null default 0
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE measure (
	id int unsigned not null AUTO_INCREMENT PRIMARY KEY,
	alias varchar(40) not null,
	name varchar(100)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE user (
	id int unsigned not null AUTO_INCREMENT PRIMARY KEY,
	registered timestamp not null default CURRENT_TIMESTAMP,
	last_visit  timestamp,
	last_visit_ip
	login varchar(40) not null,
	first_name varchar(100) default '',
	last_name varchar(100)  default '',
	gender char(1) not null default '',
	password char(32) NOT NULL,
	salt char(4) NOT NULL,
	flags bigint unsigned not null default 0
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

ALTER TABLE measure ADD COLUMN descr varchar(100) NOT NULL;

ALTER TABLE good_property ADD COLUMN good int not null;

CREATE TABLE `good_image` (
   `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
   `good` integer NOT NULL,
   `img` varchar(255) NOT NULL,
   `width` varchar(7),
   `height` varchar(7),
   `kind` integer unsigned NOT NULL,
   `flags` bigint unsigned NOT NULL DEFAULT 0
)
;

ALTER TABLE good_category ADD COLUMN alias VARCHAR(50) NOT NULL DEFAULT '';
ALTER TABLE good_image ADD COLUMN thumb1 varchar(255) NOT NULL, ADD COLUMN thumb2 varchar(255) NOT NULL;

ALTER TABLE good_image DROP COLUMN thumb1, DROP COLUMN thumb2;

ALTER TABLE good ADD COLUMN price DECIMAL(15, 2) NOT NULL DEFAULT 0;
