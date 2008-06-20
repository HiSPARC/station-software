DROP TABLE IF EXISTS `device`;
CREATE TABLE `device` (
  `device_id` int(10) unsigned NOT NULL auto_increment,
  `device_serial` varchar(40) default NULL,
  `sensor_uploadcode` varchar(3) default NULL,
  `sensor_password` varchar(20) default NULL,
  PRIMARY KEY  (`device_id`),
  UNIQUE KEY `i_device_serial` (`device_serial`)
) DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
  `message_id` bigint(20) NOT NULL auto_increment,
  `device_id` int(10) unsigned default NULL,
  `message_type_id` int(10) unsigned default '1',
  `message_status_id` int(10) unsigned NOT NULL default '1',
  `message` blob,
  `timestamp` datetime default '0000-00-00 00:00:00',
  `upload_status` integer unsigned not null default '0',
  PRIMARY KEY  (`message_id`),
  UNIQUE KEY `i_message_type` (`message_type_id`,`message_status_id`,`message_id`),
  KEY `i_device_id` (`device_id`,`message_id`)
) DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `message_status`;
CREATE TABLE `message_status` (
  `message_status_id` int(10) unsigned NOT NULL auto_increment,
  `description` varchar(40) default NULL,
  PRIMARY KEY  (`message_status_id`)
) DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `message_type`;
CREATE TABLE `message_type` (
  `message_type_id` int(10) unsigned NOT NULL auto_increment,
  `description` varchar(40) default NULL,
  PRIMARY KEY  (`message_type_id`)
) DEFAULT CHARSET=latin1;


