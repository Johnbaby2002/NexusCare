CREATE DATABASE  IF NOT EXISTS `ehr_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ehr_system`;
-- MySQL dump 10.13  Distrib 8.0.44, for macos15 (arm64)
--
-- Host: localhost    Database: ehr_system
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '421e7924-ca68-11f0-b4fa-37292950198c:1-13';

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `doctor_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`doctor_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (1,'Dr. Alice','alice@example.com','hashed_pw1','2025-11-26 11:56:37'),(2,'Dr. Bob','bob@example.com','hashed_pw2','2025-11-26 11:56:37'),(3,'Dr. Alice Johnson','alice.johnson@example.com','pw_hash1','2025-11-27 09:30:44'),(4,'Dr. Bob Smith','bob.smith@example.com','pw_hash2','2025-11-27 09:30:44'),(5,'Dr. Carol White','carol.white@example.com','pw_hash3','2025-11-27 09:30:44'),(6,'Dr. David Brown','david.brown@example.com','pw_hash4','2025-11-27 09:30:44'),(7,'Dr. Emma Davis','emma.davis@example.com','pw_hash5','2025-11-27 09:30:44'),(8,'Dr. Frank Miller','frank.miller@example.com','pw_hash6','2025-11-27 09:30:44'),(9,'Dr. Grace Wilson','grace.wilson@example.com','pw_hash7','2025-11-27 09:30:44'),(10,'Dr. Henry Moore','henry.moore@example.com','pw_hash8','2025-11-27 09:30:44'),(11,'Dr. Irene Taylor','irene.taylor@example.com','pw_hash9','2025-11-27 09:30:44'),(12,'Dr. Jack Anderson','jack.anderson@example.com','pw_hash10','2025-11-27 09:30:44');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ehr_records`
--

DROP TABLE IF EXISTS `ehr_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ehr_records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `medical_history` text,
  `medications` text,
  `immunization_date` date DEFAULT NULL,
  `vital_signs` text,
  `lab_results` text,
  `radiology_image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`record_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `ehr_records_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ehr_records`
--

LOCK TABLES `ehr_records` WRITE;
/*!40000 ALTER TABLE `ehr_records` DISABLE KEYS */;
INSERT INTO `ehr_records` VALUES (1,1,'Asthma history','Inhaler','2025-01-01','BP:120/80','Normal','uploads/xray1.png','2025-11-26 11:56:39','2025-11-26 11:56:39'),(2,2,'Diabetes type 2','Metformin','2024-12-10','BP:130/85','Glucose high','uploads/xray2.png','2025-11-26 11:56:39','2025-11-26 11:56:39'),(3,1,'Asthma history','Inhaler','2025-01-01','BP:120/80','Normal','uploads/xray1.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(4,2,'Diabetes type 2','Metformin','2024-12-10','BP:130/85','Glucose high','uploads/xray2.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(5,3,'Seasonal allergies','Antihistamines','2025-03-15','BP:118/76','Normal','uploads/xray3.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(6,4,'Hypertension','Lisinopril','2025-02-20','BP:145/95','High BP','uploads/xray4.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(7,5,'Migraine history','Ibuprofen','2025-04-05','BP:122/80','Normal','uploads/xray5.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(8,6,'Celiac disease','Gluten-free diet','2025-01-25','BP:115/75','Normal','uploads/xray6.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(9,7,'Asthma','Albuterol','2025-05-10','BP:119/78','Normal','uploads/xray7.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(10,8,'Pollen allergy','Cetirizine','2025-06-01','BP:121/79','Normal','uploads/xray8.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(11,9,'Obesity','Diet plan','2025-02-28','BP:135/88','High cholesterol','uploads/xray9.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(12,10,'Anemia','Iron supplements','2025-03-12','BP:110/70','Low iron','uploads/xray10.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(13,11,'Penicillin allergy','Avoid antibiotics','2025-07-07','BP:125/82','Normal','uploads/xray11.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(14,12,'Asthma','Steroid inhaler','2025-08-15','BP:118/77','Normal','uploads/xray12.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(15,13,'Back pain','Physical therapy','2025-09-01','BP:120/80','Normal','uploads/xray13.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(16,14,'Latex allergy','Avoid latex','2025-05-25','BP:116/74','Normal','uploads/xray14.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(17,15,'High cholesterol','Statins','2025-06-18','BP:128/84','Elevated cholesterol','uploads/xray15.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(18,16,'Asthma','Inhaler','2025-07-20','BP:117/76','Normal','uploads/xray16.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(19,17,'None','None','2025-08-30','BP:124/81','Normal','uploads/xray17.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(20,18,'Dust allergy','Antihistamines','2025-09-10','BP:122/80','Normal','uploads/xray18.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(21,19,'Knee injury','Physiotherapy','2025-10-05','BP:120/80','Normal','uploads/xray19.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(22,20,'Peanut allergy','Avoid peanuts','2025-11-01','BP:115/75','Normal','uploads/xray20.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(23,21,'None','None','2025-11-15','BP:123/82','Normal','uploads/xray21.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(24,22,'Asthma','Inhaler','2025-01-10','BP:119/78','Normal','uploads/xray22.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(25,23,'None','None','2025-02-14','BP:121/79','Normal','uploads/xray23.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(26,24,'None','None','2025-03-19','BP:118/76','Normal','uploads/xray24.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(27,25,'Hypertension','Amlodipine','2025-04-22','BP:140/90','High BP','uploads/xray25.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(28,26,'None','None','2025-05-30','BP:120/80','Normal','uploads/xray26.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(29,27,'None','None','2025-06-12','BP:122/81','Normal','uploads/xray27.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(30,28,'None','None','2025-07-25','BP:119/78','Normal','uploads/xray28.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(31,29,'None','None','2025-08-08','BP:123/82','Normal','uploads/xray29.png','2025-11-27 09:35:08','2025-11-27 09:35:08'),(32,30,'None','None','2025-09-15','BP:120/80','Normal','uploads/xray30.png','2025-11-27 09:35:08','2025-11-27 09:35:08');
/*!40000 ALTER TABLE `ehr_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `date_of_birth` date NOT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `allergies` text,
  PRIMARY KEY (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,1,'John Doe','Male','1990-05-12',75.50,'Peanuts'),(2,1,'Jane Smith','Female','1985-03-20',62.00,'None'),(3,2,'Mark Lee','Male','2000-07-15',80.00,'Dust'),(4,1,'John Doe','Male','1990-05-12',75.50,'Peanuts'),(5,1,'Jane Smith','Female','1985-03-20',62.00,'None'),(6,1,'Michael Green','Male','2002-07-15',80.00,'Dust'),(7,2,'Sophia Brown','Female','1993-09-10',68.00,'Shellfish'),(8,2,'Daniel Lee','Male','1988-11-25',85.00,'None'),(9,2,'Olivia Clark','Female','1995-01-05',55.00,'Gluten'),(10,3,'Ethan Hall','Male','1991-04-18',72.00,'None'),(11,3,'Ava Lewis','Female','1999-06-30',60.00,'Pollen'),(12,3,'Noah Young','Male','1987-12-22',90.00,'None'),(13,4,'Mia King','Female','1994-08-14',58.00,'None'),(14,4,'Lucas Scott','Male','1982-03-09',82.00,'Penicillin'),(15,4,'Isabella Adams','Female','2000-10-01',65.00,'None'),(16,5,'James Baker','Male','1996-02-17',70.00,'None'),(17,5,'Emily Carter','Female','1989-07-25',63.00,'Latex'),(18,5,'Benjamin Perez','Male','1992-05-11',78.00,'None'),(19,6,'Charlotte Rivera','Female','1997-09-03',59.00,'None'),(20,6,'William Cox','Male','1984-12-19',88.00,'None'),(21,6,'Amelia Ward','Female','1990-01-29',66.00,'Dust'),(22,7,'Alexander Torres','Male','1998-06-07',74.00,'None'),(23,7,'Harper Brooks','Female','1993-11-12',61.00,'Peanuts'),(24,7,'Elijah Sanders','Male','1986-04-02',83.00,'None'),(25,8,'Abigail Price','Female','1995-08-21',57.00,'None'),(26,8,'Matthew Foster','Male','1981-10-30',92.00,'None'),(27,8,'Ella Bell','Female','2001-12-05',64.00,'None'),(28,9,'Henry Murphy','Male','1983-07-16',86.00,'None'),(29,9,'Victoria Hughes','Female','1990-09-28',60.00,'None'),(30,9,'Samuel Ward','Male','1994-02-11',77.00,'None'),(31,10,'Zoe Coleman','Female','1992-03-23',62.00,'None'),(32,10,'Jack Reed','Male','1987-05-19',84.00,'None'),(33,10,'Lily Morgan','Female','1999-01-07',58.00,'None');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-27 10:51:07
