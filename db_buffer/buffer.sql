DROP DATABASE IF EXISTS `buffer`;
CREATE DATABASE `buffer`;
CONNECT `buffer`;

DROP TABLE IF EXISTS `device`;
CREATE TABLE `device` (
  `device_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `device_serial` VARCHAR(40) DEFAULT NULL,
  `sensor_password` varchar(20) DEFAULT NULL,
  PRIMARY KEY  (`device_id`),
  UNIQUE KEY `i_device_serial` (`device_serial`)
) DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
  `message_id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `device_id` INT(10) UNSIGNED DEFAULT NULL,
  `message_type_id` INT(10) UNSIGNED DEFAULT '1',
  `message_status_id` INT(10) UNSIGNED NOT NULL DEFAULT '1',
  `message` BLOB,
  `timestamp` TIMESTAMP DEFAULT NOW(),
  `upload_status` INTEGER UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY  (`message_id`),
  KEY `i_upload_status` (`device_id`,`message_status_id`,`upload_status`)
) DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `message_status`;
CREATE TABLE `message_status` (
  `message_status_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `description` varchar(40) DEFAULT NULL,
  PRIMARY KEY  (`message_status_id`)
) DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `message_type`;
CREATE TABLE `message_type` (
  `message_type_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `description` varchar(40) DEFAULT NULL,
  PRIMARY KEY  (`message_type_id`)
) DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `settings`;
CREATE TABLE `settings` (
  `code` VARCHAR(3) NOT NULL,
  `description` VARCHAR(40) NULL,
  `value` TEXT NULL,
  PRIMARY KEY(`code`)
);


-- Adding users 
-- First make sure the user exists before dropping it. Braindamage: there
-- is no drop user if exists statemtent.
GRANT USAGE ON *.* TO `buffer`@`%`;
DROP USER `buffer`@`%`;
CREATE USER `buffer`@`%` IDENTIFIED BY 'PLACEHOLDER';
GRANT ALL ON buffer.* TO buffer;
