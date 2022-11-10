-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: localhost    Database: website
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '獨立編號',
  `name` varchar(255) NOT NULL COMMENT '姓名',
  `username` varchar(255) NOT NULL COMMENT '帳戶名稱',
  `password` varchar(255) NOT NULL COMMENT '帳戶密碼',
  `follower_count` int unsigned NOT NULL DEFAULT '0' COMMENT '追蹤者數量',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '註冊時間',
  PRIMARY KEY (`id`),
  KEY `username_index` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,'123','test','test',130,'2022-10-19 16:55:14'),(2,'UU','uutest','uucode',87,'2022-10-15 16:55:14'),(3,'YY','yytest','yycode',90,'2022-10-15 13:55:14'),(4,'DUNKY','dtest','dcode',88,'2022-10-20 16:55:14'),(5,'GiantFish','Ftest','Fcode',67,'2022-10-10 16:55:14'),(7,'測試六的名字就叫測試六','test6','test6',0,'2022-10-25 14:42:13'),(8,'嵐','lan','lan',0,'2022-10-25 16:18:59'),(10,'測試1號','test1','test1',0,'2022-10-25 16:56:49'),(11,'十二','12','12',0,'2022-10-25 22:45:02');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '獨立編號',
  `member_id` bigint NOT NULL COMMENT '留言者會員編號',
  `content` varchar(255) NOT NULL COMMENT '留言內容',
  `like_count` int unsigned NOT NULL DEFAULT '0' COMMENT '按讚的數量',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '留言時間',
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,1,'YA! 我是頭香',66,'2022-10-15 10:34:22'),(2,5,'沙發～我來了！',12,'2022-10-16 10:34:22'),(3,3,'走過路過不能錯過',87,'2022-10-16 23:59:59'),(4,4,'可惡剛下班',7,'2022-10-17 03:12:44'),(5,2,'什麼？加一就對了',90,'2022-10-17 10:08:08'),(6,1,'快完成了嗎！？',100,'2022-10-18 10:34:22'),(7,2,'大家快來加一啊！',56,'2022-10-18 16:59:59'),(8,1,'有一種 feeling',10,'2022-10-18 20:12:44'),(9,3,'我又路過了！',7,'2022-10-19 10:08:08');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-10 15:33:21
