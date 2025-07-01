-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: snmp
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `filedata`
--

DROP TABLE IF EXISTS `filedata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filedata` (
  `f_id` int unsigned NOT NULL AUTO_INCREMENT,
  `f_name` varchar(30) NOT NULL,
  `fdata` longblob,
  `create_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `added_by` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`f_id`),
  KEY `added_by` (`added_by`),
  CONSTRAINT `filedata_ibfk_1` FOREIGN KEY (`added_by`) REFERENCES `users` (`useremail`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filedata`
--

LOCK TABLES `filedata` WRITE;
/*!40000 ALTER TABLE `filedata` DISABLE KEYS */;
INSERT INTO `filedata` VALUES (1,'otp.py',_binary 'import random\r\nucase_letter=[chr(i) for i in range(ord(\'A\'),ord(\'Z\')+1)]\r\nlcase_letter=[chr(i) for i in range(ord(\'a\'),ord(\'z\')+1)]\r\ndef genotp():\r\n    otp=\'\'\r\n\r\n    for i in range(2):\r\n        otp=otp+random.choice(ucase_letter)\r\n        otp=otp+random.choice(lcase_letter)\r\n        otp=otp+str(random.randint(0,9))\r\n    return otp\r\n   \r\n\r\n\r\n','2025-06-29 16:29:50','nsuchi3@gmail.com'),(2,'stoken.py',_binary 'from itsdangerous import URLSafeTimedSerializer\r\nfrom keys import secret_key,salt\r\ndef entoken(data):\r\n    serializer=URLSafeTimedSerializer(secret_key)\r\n    return  serializer.dumps(data,salt=salt)\r\ndef dctoken(data):\r\n    serializer=URLSafeTimedSerializer(secret_key)\r\n    return  serializer.loads(data,salt=salt)     \r\n','2025-06-29 20:15:50','nsuchi3@gmail.com');
/*!40000 ALTER TABLE `filedata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notes` (
  `n_id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `added_by` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`n_id`),
  KEY `added_by` (`added_by`),
  CONSTRAINT `notes_ibfk_1` FOREIGN KEY (`added_by`) REFERENCES `users` (`useremail`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notes`
--

LOCK TABLES `notes` WRITE;
/*!40000 ALTER TABLE `notes` DISABLE KEYS */;
INSERT INTO `notes` VALUES (3,'html','ssfgfh','2025-06-28 23:32:35','nsuchi3@gmail.com'),(4,'python','easy and high level programming languages','2025-06-28 23:40:54','nsuchi3@gmail.com'),(9,'flask','flask is framework','2025-07-01 11:12:46','nsuchi3@gmail.com');
/*!40000 ALTER TABLE `notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `useremail` varchar(30) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(15) NOT NULL,
  PRIMARY KEY (`useremail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('nsuchi3@gmail.com','suchitra','123');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-01 12:37:17
