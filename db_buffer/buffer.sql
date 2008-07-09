DROP TABLE IF EXISTS `device`;
CREATE TABLE `device` (
  `device_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `device_serial` VARCHAR(40) DEFAULT NULL,
  `sensor_uploadcode` varchar(3) DEFAULT NULL,
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
  `upload_status` INTEGER uNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY  (`message_id`),
  UNIQUE KEY `i_message_type` (`message_type_id`,`message_status_id`,`message_id`),
  KEY `i_device_id` (`device_id`,`message_id`)
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
