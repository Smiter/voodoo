# SQL Manager 2010 for MySQL 4.5.0.9
# ---------------------------------------
# Host     : localhost
# Port     : 3306
# Database : django_db


#
# Structure for the `admin_center_menu` table : 
#

CREATE TABLE `admin_center_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `title` varchar(30) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

#
# Structure for the `admin_center_supplier` table : 
#

CREATE TABLE `admin_center_supplier` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `delivery_time` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

#
# Structure for the `admin_center_orderstatus` table : 
#

CREATE TABLE `admin_center_orderstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(120) NOT NULL,
  `color` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Structure for the `admin_center_itemstatus` table : 
#

CREATE TABLE `admin_center_itemstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(120) NOT NULL,
  `color` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Structure for the `admin_center_currency` table : 
#

CREATE TABLE `admin_center_currency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `code` varchar(120) NOT NULL,
  `ratio` decimal(20,1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

