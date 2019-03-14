DROP TABLE IF EXISTS `bp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bp` (
  `name` varchar(255) NOT NULL,
  `description` varchar(255) default NULL,
  `priority` varchar(5) default NULL,
  `type` varchar(3) NOT NULL,
  `command` varchar(255) default NULL,
  `url` varchar(255) default NULL,
  `min_value` varchar(5) default NULL,
  `is_define` tinyint(1) default '0',
  PRIMARY KEY  (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bp_links`
--

DROP TABLE IF EXISTS `bp_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bp_links` (
  `id` mediumint(9) NOT NULL auto_increment,
  `bp_name` varchar(255) NOT NULL,
  `bp_link` varchar(255) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bp_services`
--

DROP TABLE IF EXISTS `bp_services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bp_services` (
  `id` mediumint(9) NOT NULL auto_increment,
  `bp_name` varchar(255) NOT NULL,
  `host` varchar(255) NOT NULL,
  `service` varchar(255) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;