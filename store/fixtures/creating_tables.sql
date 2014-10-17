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

ALTER TABLE good ADD COLUMN vendor INT NOT NULL DEFAULT 0;
CREATE TABLE vendor (
  id integer AUTO_INCREMENT PRIMARY KEY,
  name varchar(100),
  alias varchar(50),
  flags bigint not null default 0
);

CREATE TABLE good_consist (
  id INT AUTO_INCREMENT PRIMARY KEY,
  alias varchar(50) NOT NULL,
  name varchar(100) NOT NULL
);

ALTER TABLE good ADD COLUMN consists INT NOT NULL DEFAULT 0;

CREATE TABLE colour (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name varchar(100) NOT NULL,
  code varchar(20) NOT NULL
);

CREATE TABLE good_colour (
  id INT AUTO_INCREMENT PRIMARY KEY,
  good int not null,
  colour int not null
);

ALTER TABLE good_colour ADD COLUMN vendor_colour varchar(150);
ALTER TABLE good_colour ADD COLUMN img varchar(150);
ALTER TABLE good_colour CHANGE colour unified_colour int;

ALTER TABLE good_colour ADD COLUMN `width` varchar(7),
   ADD COLUMN `height` varchar(7);

CREATE TABLE cart (
  id INT AUTO_INCREMENT PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user INT,
  session varchar(255),
  product int not null,
  product_code varchar(100),
  amount INT NOT NULL
);

RENAME TABLE good_colour TO product_sku;
ALTER TABLE product_sku ADD COLUMN left_amount INT NOT NULL DEFAULT 0;


ALTER TABLE good MODIFY consist int unsigned DEFAULT 0;
ALTER TABLE good MODIFY vendor int unsigned DEFAULT 0;
ALTER TABLE good MODIFY descr TEXT DEFAULT '';
ALTER TABLE good_consist ADD COLUMN good_category int unsigned not null; // обновить всем составам это поле (проставить категорию пряжи)
ALTER TABLE good ADD COLUMN left_amount int unsigned  DEFAULT 0;


CREATE TABLE smodel1 (
  id INT AUTO_INCREMENT PRIMARY KEY,
  field_one varchar(255),
  field_two  varchar(255),
  field_three  varchar(255)
);

CREATE TABLE smodel2 (
  id INT AUTO_INCREMENT PRIMARY KEY,
  parent_model int,
  field_one varchar(255),
  field_two  varchar(255),
  field_three  varchar(255)
);


CREATE TABLE `order` (
  id INT AUTO_INCREMENT PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status SMALLINT UNSIGNED NOT NULL,
  fname VARCHAR(100) DEFAULT  '',
  phone VARCHAR (15) DEFAULT '',
  email VARCHAR(100) DEFAULT  '',
  delivery SMALLINT UNSIGNED NOT NULL,
  payment  SMALLINT UNSIGNED NOT NULL,
  comment TINYTEXT DEFAULT '',
  ip varchar(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE order_product (
  id INT AUTO_INCREMENT PRIMARY KEY,
  `order` INT UNSIGNED NOT NULL,
  product INT UNSIGNED NOT NULL,
  sku VARCHAR (100) DEFAULT NULL,
  amount INT UNSIGNED NOT NULL,
  price DECIMAL(9,2) unsigned NOT NULL
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE good_consist_unified (
  id INT AUTO_INCREMENT PRIMARY KEY,
  alias varchar(50) NOT NULL,
  name varchar(100) NOT NULL,
  good_category int unsigned not null
);

ALTER TABLE good_consist DROP COLUMN good_category;
ALTER TABLE good ADD COLUMN consist_unified  INT UNSIGNED;