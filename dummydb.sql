-- MySQL dump 10.13  Distrib 5.7.31, for Linux (x86_64)
--
-- Host: localhost    Database: inventory
-- ------------------------------------------------------
-- Server version	5.7.31-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `affair`
--

DROP TABLE IF EXISTS `affair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `affair` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) DEFAULT 'Waiting',
  `close_date` date DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `probability` int(11) DEFAULT NULL,
  `origin` varchar(100) DEFAULT NULL,
  `description` text,
  `responsible_user` int(11) DEFAULT NULL,
  `company` int(11) DEFAULT NULL,
  `type_` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affair`
--

LOCK TABLES `affair` WRITE;
/*!40000 ALTER TABLE `affair` DISABLE KEYS */;
INSERT INTO `affair` VALUES (19,'nice sale','2020-07-24 21:17:10','Waiting',NULL,NULL,80,'','qsd',4,4,'Sale'),(20,'bad sale','2020-07-24 21:18:40','Waiting',NULL,15,10,'','ee',4,NULL,'Sale'),(21,'Amazing sale','2020-07-24 21:31:54','Waiting','2020-07-25',501,100,'fb','qsd',4,4,'Sale'),(24,'sss','2020-07-24 21:53:12','Waiting',NULL,NULL,NULL,'','dsq',4,4,'Sale'),(25,'s','2020-07-24 22:23:45','Waiting',NULL,NULL,NULL,'','s',4,4,'Sale'),(31,'qsdqdqds','2020-07-25 15:30:05','In Progress',NULL,NULL,NULL,'','ddd',4,4,'Purchase'),(32,'ddd','2020-07-25 15:35:34','Waiting',NULL,NULL,NULL,'','dd',4,-1,'Purchase'),(33,'a','2020-07-25 15:36:32','Waiting',NULL,NULL,NULL,'','a',4,-1,'Purchase'),(34,'a','2020-07-25 15:37:09','Waiting',NULL,NULL,NULL,'','a',4,4,'Sale'),(35,'aaaa','2020-07-25 15:42:03','Waiting',NULL,500,NULL,'','aaaaq qsdqsd qsdqsdqsd qsd qsdqsd qsd qsdqsd qsd qsdqsd ',4,NULL,'Sale'),(36,'qdqsd','2020-07-26 11:14:39','Waiting','2020-07-26',200,50,'','qdfqfsq',4,NULL,'Sale'),(37,'hehe','2020-07-26 12:42:41','Waiting','2020-07-26',10,100,'','a',4,NULL,'Sale'),(38,'qsd','2020-07-26 12:43:36','Waiting','2020-07-26',NULL,NULL,'','ds',4,NULL,'Sale'),(39,'aze','2020-07-26 12:44:57','Waiting','2020-07-26',NULL,100,'','a',4,NULL,'Sale'),(40,'qq','2020-07-26 12:45:23','Done',NULL,NULL,NULL,'','a',4,NULL,'Sale'),(42,'aaa','2020-07-26 13:01:48','Waiting','2020-07-26',NULL,NULL,'','aa',4,NULL,'Sale'),(43,'aaa','2020-07-26 13:02:24','Done','2020-07-26',NULL,NULL,'','a',4,NULL,'Sale'),(44,'aaaaaa','2020-07-26 13:02:53','Done','2020-07-26',NULL,NULL,'','a',4,NULL,'Sale'),(45,'azaa','2020-07-26 13:03:23','Done','2020-07-26',NULL,NULL,'','aa',4,NULL,'Purchase'),(46,'sdf','2020-07-26 13:04:00','Done','2020-07-26',NULL,NULL,'','sdf',4,NULL,'Purchase'),(47,'aaa','2020-07-27 18:23:27','Done','2020-07-27',NULL,NULL,'','aa',4,NULL,'Sale'),(48,'qsd','2020-07-27 18:23:54','Waiting',NULL,NULL,NULL,'','qsd',4,5,'Purchase'),(49,'qds','2020-07-27 18:24:11','Done','2020-07-27',NULL,NULL,'','dd',4,5,'Purchase'),(50,'aaaa','2020-07-30 11:39:54','Waiting',NULL,NULL,NULL,'','a',6,5,'Purchase');
/*!40000 ALTER TABLE `affair` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `affairService`
--

DROP TABLE IF EXISTS `affairService`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `affairService` (
  `affair_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`affair_id`,`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affairService`
--

LOCK TABLES `affairService` WRITE;
/*!40000 ALTER TABLE `affairService` DISABLE KEYS */;
INSERT INTO `affairService` VALUES (1,11,19),(2,7,19),(20,7,1),(20,13,1),(21,7,26),(21,10,4),(21,11,99),(21,12,12),(21,13,2),(24,7,1),(24,11,78),(24,13,11),(25,11,12),(25,12,1),(26,10,3),(27,7,6),(27,12,13),(30,7,1),(31,10,1),(32,11,50),(33,7,5),(34,7,0),(34,14,1),(35,10,12),(36,7,11),(36,11,1),(37,7,2),(37,14,1),(38,7,2),(38,14,2),(39,7,2),(39,14,2),(40,7,2),(40,14,2),(42,7,2),(42,14,2),(43,7,2),(43,13,22),(43,14,2),(44,7,5),(44,13,30),(44,14,15),(45,7,33),(45,13,60),(46,12,10),(47,7,3),(48,7,3),(49,7,9),(50,7,2);
/*!40000 ALTER TABLE `affairService` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (3,'Certex'),(4,'ACER'),(5,'DELL');
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `companyContact`
--

DROP TABLE IF EXISTS `companyContact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `companyContact` (
  `cid` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`company_id`,`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companyContact`
--

LOCK TABLES `companyContact` WRITE;
/*!40000 ALTER TABLE `companyContact` DISABLE KEYS */;
INSERT INTO `companyContact` VALUES (5,3),(7,4),(8,5);
/*!40000 ALTER TABLE `companyContact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `companyService`
--

DROP TABLE IF EXISTS `companyService`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `companyService` (
  `product_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`company_id`,`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companyService`
--

LOCK TABLES `companyService` WRITE;
/*!40000 ALTER TABLE `companyService` DISABLE KEYS */;
INSERT INTO `companyService` VALUES (10,3),(7,4),(11,4),(12,4),(13,4),(7,5),(11,5),(13,5);
/*!40000 ALTER TABLE `companyService` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `surname` varchar(25) DEFAULT NULL,
  `name` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (4,'sampleuser@gmail.com',NULL,'Admin'),(5,'certex@email.com','thelastname','thename'),(6,'test@gmail.com','King','Burger'),(7,'noemail@email.com','Labrie','james'),(8,'rogeremail@email.com','Seagate','Roger');
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contactTelephone`
--

DROP TABLE IF EXISTS `contactTelephone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contactTelephone` (
  `num` varchar(20) NOT NULL,
  `uid` int(11) NOT NULL,
  PRIMARY KEY (`uid`,`num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contactTelephone`
--

LOCK TABLES `contactTelephone` WRITE;
/*!40000 ALTER TABLE `contactTelephone` DISABLE KEYS */;
INSERT INTO `contactTelephone` VALUES ('+216 94 445587',5),('+216 12345678',6),('+216 99999999',6),('94342211',7),('95 001 145',8);
/*!40000 ALTER TABLE `contactTelephone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operationRole`
--

DROP TABLE IF EXISTS `operationRole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operationRole` (
  `operation` varchar(150) NOT NULL,
  `role_name` varchar(15) NOT NULL,
  PRIMARY KEY (`role_name`,`operation`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operationRole`
--

LOCK TABLES `operationRole` WRITE;
/*!40000 ALTER TABLE `operationRole` DISABLE KEYS */;
INSERT INTO `operationRole` VALUES ('Add users','Accountant'),('Check users list','Accountant'),('Add affairs','Admin'),('Add company','Admin'),('Add products','Admin'),('Add tasks','Admin'),('Add users','Admin'),('Check affairs list','Admin'),('Check companies list','Admin'),('Check products list','Admin'),('Check tasks list','Admin'),('Check users list','Admin'),('Edit affairs','Admin'),('Edit company','Admin'),('Edit products','Admin'),('Edit tasks','Admin'),('Postpone tasks','Admin'),('Update affair status','Admin'),('Update parameters','Admin'),('Update task status','Admin'),('Check affairs list','Engineer'),('Check companies list','Engineer'),('Check products list','Engineer'),('Check users list','Engineer');
/*!40000 ALTER TABLE `operationRole` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` int(11) DEFAULT NULL,
  `sku` varchar(20) DEFAULT NULL,
  `ean_upc` varchar(13) DEFAULT NULL,
  `location` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (7,NULL,'','53FA12'),(11,'9541167713','6191234567895',''),(12,'3042088734','',''),(13,'7558859006','',''),(14,'7486909514','','');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_family`
--

DROP TABLE IF EXISTS `product_family`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_family` (
  `name` varchar(150) NOT NULL,
  `family` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_family`
--

LOCK TABLES `product_family` WRITE;
/*!40000 ALTER TABLE `product_family` DISABLE KEYS */;
INSERT INTO `product_family` VALUES ('Computer Equipment','None'),('Instruments','None'),('None','None'),('Technologie','None');
/*!40000 ALTER TABLE `product_family` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_information`
--

DROP TABLE IF EXISTS `product_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_information` (
  `service_id` int(11) NOT NULL,
  `dat` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `quantity` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  PRIMARY KEY (`dat`,`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_information`
--

LOCK TABLES `product_information` WRITE;
/*!40000 ALTER TABLE `product_information` DISABLE KEYS */;
INSERT INTO `product_information` VALUES (4,'2020-07-22 18:02:01',0,200),(5,'2020-07-23 12:48:33',0,25),(7,'2020-07-23 12:54:31',0,11),(8,'2020-07-23 13:01:47',0,25),(9,'2020-07-23 13:02:34',0,25),(7,'2020-07-24 09:11:17',0,12),(10,'2020-07-24 09:28:04',0,50),(11,'2020-07-24 09:30:49',0,23),(12,'2020-07-24 11:05:08',0,200),(13,'2020-07-24 11:05:27',0,5),(7,'2020-07-25 19:46:41',0,10),(14,'2020-07-26 12:35:21',0,300),(7,'2020-07-26 13:05:24',0,10),(14,'2020-07-26 13:05:24',-1,300),(11,'2020-07-26 13:08:34',-12,23),(12,'2020-07-26 13:08:34',-1,200),(11,'2020-07-26 13:09:44',38,23),(7,'2020-07-26 13:41:58',5,10),(7,'2020-07-26 14:02:24',3,10),(13,'2020-07-26 14:02:24',-22,5),(14,'2020-07-26 14:02:24',-3,300),(7,'2020-07-26 14:02:53',-2,10),(13,'2020-07-26 14:02:53',-52,5),(14,'2020-07-26 14:02:53',-18,300),(7,'2020-07-26 14:03:23',31,10),(13,'2020-07-26 14:03:23',8,5),(12,'2020-07-26 14:05:16',9,200),(7,'2020-07-26 14:07:42',64,10),(13,'2020-07-26 14:07:42',68,5),(7,'2020-07-26 14:08:00',59,10),(13,'2020-07-26 14:08:00',38,5),(14,'2020-07-26 14:08:00',-33,300),(7,'2020-07-27 19:22:38',57,10),(13,'2020-07-27 19:22:39',16,5),(14,'2020-07-27 19:22:39',-35,300),(7,'2020-07-27 19:23:02',55,10),(14,'2020-07-27 19:23:02',-37,300),(7,'2020-07-27 19:23:27',52,10),(7,'2020-07-27 19:24:11',61,10),(15,'2020-08-04 12:06:38',0,25);
/*!40000 ALTER TABLE `product_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `type` varchar(15) NOT NULL,
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES ('Accountant'),('Admin'),('Engineer'),('Moderator'),('Secretary');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `description` varchar(250) DEFAULT NULL,
  `estimated_cost` double DEFAULT NULL,
  `tax_category` varchar(20) DEFAULT NULL,
  `family` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
INSERT INTO `service` VALUES (7,'Mousepad','aaa',5,'Normal','Computer Equipment'),(10,'AC Installation','air conditionner installation',25,'Normal','None'),(11,'Keyboard A12','dqsd',NULL,'Normal','Computer Equipment'),(12,'Screen','screen',NULL,'Normal','Computer Equipment'),(13,'Cable RJ45 ','5m',NULL,'Normal','Computer Equipment'),(14,'Flute','zs',250,'Normal','Instruments'),(15,'installation matériel','aa',NULL,'Normal','Technologie');
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `description` text,
  `creator` int(11) DEFAULT NULL,
  `assigned_user` int(11) DEFAULT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `due_date` date DEFAULT NULL,
  `due_hour` char(5) DEFAULT NULL,
  `priority` varchar(15) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Waiting',
  `progress` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task`
--

LOCK TABLES `task` WRITE;
/*!40000 ALTER TABLE `task` DISABLE KEYS */;
INSERT INTO `task` VALUES (1,'test taska','foqsdqsssssssssssssss',4,4,'2020-07-19 13:28:07','2020-11-07','17:00','High','Waiting',20),(2,'qzz','a',4,4,'2020-07-19 13:31:17','2021-01-05','15:20','Medium','Waiting',0),(3,'task2','this is a tes ttask',4,4,'2020-07-19 17:25:08','2020-07-20','15:20','Low','In Progress',50),(4,'get the light fixed','qsdqsd',4,4,'2020-07-19 17:28:53','2020-07-23','15:20','Low','Done',100),(5,'go home','go sleep',4,4,'2020-07-20 11:15:42','2020-08-03','15:20','Low','Done',100),(6,'close one','aa',4,4,'2020-07-26 09:26:39','2020-07-31','','Medium','Waiting',0);
/*!40000 ALTER TABLE `task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taskAwait`
--

DROP TABLE IF EXISTS `taskAwait`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taskAwait` (
  `waitingTaskId` int(11) DEFAULT NULL,
  `awaitedTaskId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taskAwait`
--

LOCK TABLES `taskAwait` WRITE;
/*!40000 ALTER TABLE `taskAwait` DISABLE KEYS */;
INSERT INTO `taskAwait` VALUES (5,1),(5,2),(5,3);
/*!40000 ALTER TABLE `taskAwait` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tax_category`
--

DROP TABLE IF EXISTS `tax_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tax_category` (
  `name` varchar(20) NOT NULL,
  `value` double DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tax_category`
--

LOCK TABLES `tax_category` WRITE;
/*!40000 ALTER TABLE `tax_category` DISABLE KEYS */;
INSERT INTO `tax_category` VALUES ('Normal',19),('Transport',7);
/*!40000 ALTER TABLE `tax_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `telephone`
--

DROP TABLE IF EXISTS `telephone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `telephone` (
  `num` varchar(20) NOT NULL,
  PRIMARY KEY (`num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telephone`
--

LOCK TABLES `telephone` WRITE;
/*!40000 ALTER TABLE `telephone` DISABLE KEYS */;
INSERT INTO `telephone` VALUES ('+216 12345678'),('+216 94342410'),('+216 99999999');
/*!40000 ALTER TABLE `telephone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `image_file` char(20) NOT NULL DEFAULT 'default.jpg',
  `password` char(60) NOT NULL,
  `lang` char(2) DEFAULT 'FR'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_role`
--

DROP TABLE IF EXISTS `user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_role` (
  `uid` int(11) NOT NULL,
  `role` varchar(15) NOT NULL,
  PRIMARY KEY (`uid`,`role`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role`
--

LOCK TABLES `user_role` WRITE;
/*!40000 ALTER TABLE `user_role` DISABLE KEYS */;
INSERT INTO `user_role` VALUES (4,'Admin'),(6,'Accountant');
/*!40000 ALTER TABLE `user_role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-04 12:29:19
