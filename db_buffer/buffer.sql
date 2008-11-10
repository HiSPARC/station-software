DROP DATABASE IF EXISTS `buffer`;
CREATE DATABASE `buffer`;
USE `buffer`;

CREATE TABLE `device` (
  `device_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `device_serial` VARCHAR(40) DEFAULT NULL,
  `sensor_password` varchar(20) DEFAULT NULL,
  PRIMARY KEY  (`device_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `message` (
  `message_id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `device_id` INT(10) UNSIGNED DEFAULT NULL,
  `message_type_id` INT(10) UNSIGNED DEFAULT '1',
  `message_status_id` INT(10) UNSIGNED NOT NULL DEFAULT '1',
  `message` BLOB,
  `timestamp` TIMESTAMP DEFAULT NOW(),
  `upload_status` INTEGER UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY  (`message_id`),
  KEY `i_upload_status` (`device_id`,`message_type_id`,`upload_status`,`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `message_status` (
  `message_status_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `description` varchar(40) DEFAULT NULL,
  PRIMARY KEY  (`message_status_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `message_type` (
  `message_type_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `description` varchar(40) DEFAULT NULL,
  PRIMARY KEY  (`message_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `settings` (
  `code` VARCHAR(3) NOT NULL,
  `description` VARCHAR(40) NULL,
  `value` TEXT NULL,
  PRIMARY KEY(`code`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


-- Adding users 
-- First make sure the user exists before dropping it. Braindamage: there
-- is no DROP USER IF EXISTS statement.
GRANT USAGE ON *.* TO `buffer`@`%` IDENTIFIED BY 'foo';
GRANT USAGE ON *.* TO `buffer`@`localhost` IDENTIFIED BY 'foo';
DROP USER `buffer`@`%`;
DROP USER `buffer`@`localhost`;
CREATE USER `buffer`@`%` IDENTIFIED BY 'PLACEHOLDER';
CREATE USER `buffer`@`localhost` IDENTIFIED BY 'PLACEHOLDER';
GRANT ALL ON `buffer`.* TO `buffer`@`%`;
GRANT ALL ON `buffer`.* TO `buffer`@`localhost`;
