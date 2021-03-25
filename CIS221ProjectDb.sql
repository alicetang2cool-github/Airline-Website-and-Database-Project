-- MySQL dump 10.13  Distrib 8.0.21, for macos10.15 (x86_64)
--
-- Host: cis221projectdb.ckdslcdwovmx.us-west-1.rds.amazonaws.com    Database: cis221projectdb
-- ------------------------------------------------------
-- Server version	8.0.20

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

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `Accounts`
--

DROP TABLE IF EXISTS `Accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Accounts` (
  `Email` varchar(45) NOT NULL,
  `Account_Creation_Date` date DEFAULT NULL,
  `Password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Accounts`
--

LOCK TABLES `Accounts` WRITE;
/*!40000 ALTER TABLE `Accounts` DISABLE KEYS */;
INSERT INTO `Accounts` VALUES ('',NULL,''),('6918270@gmail.com',NULL,'yanhuo1124'),('aaa@gmail.com',NULL,'123'),('admin@admin.com',NULL,'admin'),('alicetang@email.com',NULL,'password'),('chris18@gmail.com',NULL,'password123'),('darthvader@email.com',NULL,'iamyourfather'),('makai23allbert@gmail.com',NULL,'hello123'),('notmyaddress@gmail.com',NULL,'Admin123'),('rumiadmin@admin.com',NULL,'admin123'),('rumiallbert@gmail.com',NULL,'password'),('test@test.com',NULL,'test'),('truemanwu@email.com',NULL,'password');
/*!40000 ALTER TABLE `Accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Airlines`
--

DROP TABLE IF EXISTS `Airlines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Airlines` (
  `Airline_ID` char(2) NOT NULL,
  `Airline_Name` char(20) NOT NULL,
  PRIMARY KEY (`Airline_ID`),
  CONSTRAINT `Airlines_chk_1` CHECK ((char_length(`Airline_ID`) = 2))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Airlines`
--

LOCK TABLES `Airlines` WRITE;
/*!40000 ALTER TABLE `Airlines` DISABLE KEYS */;
INSERT INTO `Airlines` VALUES ('AA','Trueman Airlines'),('AB','Wu Airlines'),('AD','Alice Airlines'),('AE','Hartsfield–Jackson A'),('AF','Los Angeles Airline'),('AG','O\'Hare Airline'),('AH','Dallas/Fort Worth Ai'),('AI','Denver Airline');
/*!40000 ALTER TABLE `Airlines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Airports`
--

DROP TABLE IF EXISTS `Airports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Airports` (
  `Airport_ID` char(3) NOT NULL,
  `Airport_Name` char(20) NOT NULL,
  `City` char(20) DEFAULT NULL,
  `Country` char(20) DEFAULT NULL,
  PRIMARY KEY (`Airport_ID`),
  CONSTRAINT `Airports_chk_1` CHECK ((char_length(`Airport_ID`) = 3))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Airports`
--

LOCK TABLES `Airports` WRITE;
/*!40000 ALTER TABLE `Airports` DISABLE KEYS */;
INSERT INTO `Airports` VALUES ('AAA','Trueman','Trueman','Trueman'),('AAB','Wu','Wu','Wu'),('AAC','Alice','Alice','Trueman'),('AAD','Rumi','Rumi','Wu'),('AAE','Lehan','Lehan','Trueman'),('AAF','April','Melly','Wu'),('AAH','Hartsfield–Jackson A','Atlanta','USA'),('AAI','Los Angeles Internat','Los Angeles','USA'),('AAJ','O\'Hare International','Chicago','USA'),('AAK','Dallas/Fort Worth I','Dallas','USA'),('AAL','Denver International','Denver','USA');
/*!40000 ALTER TABLE `Airports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking`
--

DROP TABLE IF EXISTS `Booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking` (
  `Reservation_Number` int NOT NULL,
  `SSN` char(11) DEFAULT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `Booking_Fee` double DEFAULT NULL,
  PRIMARY KEY (`Reservation_Number`),
  KEY `SSN` (`SSN`),
  KEY `Email` (`Email`),
  CONSTRAINT `Booking_ibfk_2` FOREIGN KEY (`SSN`) REFERENCES `Employees` (`SSN`),
  CONSTRAINT `Booking_ibfk_3` FOREIGN KEY (`Email`) REFERENCES `Accounts` (`Email`),
  CONSTRAINT `Booking_ibfk_4` FOREIGN KEY (`Reservation_Number`) REFERENCES `Reservations` (`Reservation_Number`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking`
--

LOCK TABLES `Booking` WRITE;
/*!40000 ALTER TABLE `Booking` DISABLE KEYS */;
INSERT INTO `Booking` VALUES (2,NULL,'test@test.com',10),(3,NULL,'test@test.com',10),(4,NULL,'test@test.com',10),(5,NULL,'test@test.com',10),(6,NULL,'test@test.com',10),(7,NULL,'test@test.com',10),(8,NULL,'test@test.com',10),(9,NULL,'test@test.com',10),(10,NULL,'test@test.com',10),(11,NULL,'rumiadmin@admin.com',10),(13,NULL,'test@test.com',10),(14,NULL,'test@test.com',10),(15,NULL,'test@test.com',10),(16,NULL,'test@test.com',10),(17,NULL,'test@test.com',10),(21,NULL,'chris18@gmail.com',10);
/*!40000 ALTER TABLE `Booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customers`
--

DROP TABLE IF EXISTS `Customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Customers` (
  `SSN` char(11) NOT NULL,
  `Email_Address` char(45) DEFAULT NULL,
  `Credit_Card_Number` char(20) DEFAULT NULL,
  `Preferences` char(20) DEFAULT NULL,
  PRIMARY KEY (`SSN`),
  CONSTRAINT `Customers_ibfk_1` FOREIGN KEY (`SSN`) REFERENCES `People` (`SSN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customers`
--

LOCK TABLES `Customers` WRITE;
/*!40000 ALTER TABLE `Customers` DISABLE KEYS */;
INSERT INTO `Customers` VALUES ('123456789','test@test.com','1234567890','American'),('192847562','alicetang@email.com','1937382737','Chinese'),('987654321','captainjack@pirates.com','0987654321','Chinese');
/*!40000 ALTER TABLE `Customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Employees`
--

DROP TABLE IF EXISTS `Employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Employees` (
  `SSN` char(11) NOT NULL,
  `Start_Date` date DEFAULT NULL,
  `Hourly_Rate` double DEFAULT NULL,
  PRIMARY KEY (`SSN`),
  CONSTRAINT `Employees_ibfk_1` FOREIGN KEY (`SSN`) REFERENCES `People` (`SSN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Employees`
--

LOCK TABLES `Employees` WRITE;
/*!40000 ALTER TABLE `Employees` DISABLE KEYS */;
INSERT INTO `Employees` VALUES ('192837455','2020-05-04',20);
/*!40000 ALTER TABLE `Employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Flights`
--

DROP TABLE IF EXISTS `Flights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Flights` (
  `Flight_Number` int NOT NULL,
  `Airline_ID` char(2) NOT NULL,
  `From_airport` varchar(45) DEFAULT NULL,
  `To_airport` varchar(45) DEFAULT NULL,
  `Number_of_Seats` int DEFAULT NULL,
  `Days_of_Week` varchar(20) DEFAULT NULL,
  `Associated_Fare` int DEFAULT NULL,
  `Fare_Restriction` char(200) DEFAULT NULL,
  `Advanced_Purchase` char(200) DEFAULT NULL,
  `Length_of_Stay` char(200) DEFAULT NULL,
  `Local_arrivial` time DEFAULT NULL,
  `Local_departure` time DEFAULT NULL,
  PRIMARY KEY (`Flight_Number`,`Airline_ID`),
  KEY `Airline_ID` (`Airline_ID`),
  CONSTRAINT `Flights_ibfk_1` FOREIGN KEY (`Airline_ID`) REFERENCES `Airlines` (`Airline_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Flights`
--

LOCK TABLES `Flights` WRITE;
/*!40000 ALTER TABLE `Flights` DISABLE KEYS */;
INSERT INTO `Flights` VALUES (111,'AA','AAA','AAB',NULL,'1,4,5,6',100,NULL,NULL,NULL,'06:30:00','08:30:00'),(112,'AB','AAA','AAB',NULL,'1,2,3',150,NULL,NULL,NULL,'04:30:00','06:30:00'),(113,'AA','AAB','AAA',NULL,'1,2,3,4',200,NULL,NULL,NULL,'06:30:00','12:30:00'),(114,'AD','AAC','AAE',NULL,'1,4,6',300,NULL,NULL,NULL,'05:00:00','07:00:00'),(115,'AA','AAA','AAC',NULL,'1,4,5',150,NULL,NULL,NULL,'08:00:00','10:00:00'),(116,'AB','AAA','AAE',NULL,'1,4,5,6',350,NULL,NULL,NULL,'20:00:00','22:00:00'),(117,'AF','AAF','AAH',NULL,'2,4,6',120,NULL,NULL,NULL,'01:30:00','02:20:00'),(118,'AI','AAK','AAL',NULL,'5,6,7',150,NULL,NULL,NULL,'04:20:00','06:30:00'),(119,'AG','AAF','AAD',NULL,'6,7',200,NULL,NULL,NULL,'12:00:00','06:00:00'),(120,'AF','AAI','AAJ',NULL,'6,7',300,NULL,NULL,NULL,'01:00:00','04:30:00');
/*!40000 ALTER TABLE `Flights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Have`
--

DROP TABLE IF EXISTS `Have`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Have` (
  `SSN` char(11) NOT NULL,
  `Email` varchar(45) NOT NULL,
  PRIMARY KEY (`SSN`,`Email`),
  KEY `Email` (`Email`),
  CONSTRAINT `Have_ibfk_1` FOREIGN KEY (`SSN`) REFERENCES `Customers` (`SSN`),
  CONSTRAINT `Have_ibfk_2` FOREIGN KEY (`Email`) REFERENCES `Accounts` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Have`
--

LOCK TABLES `Have` WRITE;
/*!40000 ALTER TABLE `Have` DISABLE KEYS */;
/*!40000 ALTER TABLE `Have` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Legs`
--

DROP TABLE IF EXISTS `Legs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Legs` (
  `Reservation_Number` int NOT NULL,
  `Flight_Number` int NOT NULL,
  `Airline_ID` char(2) NOT NULL,
  `Seat_type` char(10) DEFAULT NULL,
  `Class` char(20) DEFAULT NULL,
  `Departure_Time` time DEFAULT NULL,
  `Arrival_Time` time DEFAULT NULL,
  `Special_Meal` char(20) DEFAULT NULL,
  PRIMARY KEY (`Reservation_Number`,`Flight_Number`,`Airline_ID`),
  KEY `Legs_ibfk_1` (`Flight_Number`,`Airline_ID`),
  CONSTRAINT `Legs_ibfk_1` FOREIGN KEY (`Flight_Number`, `Airline_ID`) REFERENCES `Flights` (`Flight_Number`, `Airline_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Legs_ibfk_2` FOREIGN KEY (`Reservation_Number`) REFERENCES `Reservations` (`Reservation_Number`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Legs`
--

LOCK TABLES `Legs` WRITE;
/*!40000 ALTER TABLE `Legs` DISABLE KEYS */;
INSERT INTO `Legs` VALUES (2,111,'AA','Center','First','08:30:00','06:30:00','Mexican'),(3,111,'AA','Window','First','08:30:00','06:30:00','American'),(4,111,'AA','Window','First','08:30:00','06:30:00','American'),(5,111,'AA','Window','First','08:30:00','06:30:00','American'),(6,111,'AA','Window','First','08:30:00','06:30:00','American'),(7,111,'AA','Window','First','08:30:00','06:30:00','American'),(8,112,'AB','Window','First','06:30:00','04:30:00','American'),(9,111,'AA','Window','First','08:30:00','06:30:00','American'),(9,113,'AA','Window','First','12:30:00','06:30:00','American'),(10,111,'AA','Window','First','08:30:00','06:30:00','American'),(10,112,'AB','Window','First','06:30:00','04:30:00','American'),(10,113,'AA','Window','First','12:30:00','06:30:00','American'),(11,112,'AB','Aisle','First','06:30:00','04:30:00','Mexican'),(11,113,'AA','Aisle','First','12:30:00','06:30:00','Mexican'),(13,115,'AA','Window','First','10:00:00','08:00:00','American'),(14,112,'AB','Center','First','06:30:00','04:30:00','Chinese'),(14,113,'AA','Center','First','12:30:00','06:30:00','Chinese'),(15,111,'AA','Window','First','08:30:00','06:30:00','American'),(16,111,'AA','Window','First','08:30:00','06:30:00','American'),(17,111,'AA','Window','First','08:30:00','06:30:00','American'),(17,113,'AA','Window','First','12:30:00','06:30:00','American'),(18,111,'AA','Window','First','08:30:00','06:30:00','American'),(19,118,'AI','Window','First','06:30:00','04:20:00','American'),(20,118,'AI','Window','First','06:30:00','04:20:00','American'),(21,118,'AI','Window','Business','06:30:00','04:20:00','Mexican'),(22,118,'AI','Center','First','06:30:00','04:20:00','American'),(23,118,'AI','Window','First','06:30:00','04:20:00','Mexican');
/*!40000 ALTER TABLE `Legs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `People`
--

DROP TABLE IF EXISTS `People`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `People` (
  `SSN` char(11) NOT NULL,
  `Last_Name` char(20) DEFAULT NULL,
  `First_Name` char(20) DEFAULT NULL,
  `Address` char(20) DEFAULT NULL,
  `City` char(20) DEFAULT NULL,
  `State` char(2) DEFAULT NULL,
  `Zip_Code` int DEFAULT NULL,
  `Telephone` char(11) DEFAULT NULL,
  PRIMARY KEY (`SSN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `People`
--

LOCK TABLES `People` WRITE;
/*!40000 ALTER TABLE `People` DISABLE KEYS */;
INSERT INTO `People` VALUES ('123456789','Vader','Darth','qwer','qwer','qw',10980,'1234567890'),('192837455','Dave','Donald','34 Homes','Catar','Ma',19232,'1432434332'),('192847562','Tang','Alice','43 Pineapple','Bottoms','Pa',10298,'1383947582'),('987654321','Sparrow','Jack','Black Pearl','Atlantis','At',0,'8008008000');
/*!40000 ALTER TABLE `People` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Reservations`
--

DROP TABLE IF EXISTS `Reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Reservations` (
  `Reservation_Number` int NOT NULL,
  `Date` date DEFAULT NULL,
  `Passengers` int DEFAULT NULL,
  `Total_Fare` int DEFAULT NULL,
  `Fare_Restriction` char(200) DEFAULT NULL,
  `Email` varchar(45) NOT NULL,
  PRIMARY KEY (`Reservation_Number`),
  KEY `Reservations_ibfk_2` (`Email`),
  CONSTRAINT `Reservations_ibfk_2` FOREIGN KEY (`Email`) REFERENCES `Accounts` (`Email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reservations`
--

LOCK TABLES `Reservations` WRITE;
/*!40000 ALTER TABLE `Reservations` DISABLE KEYS */;
INSERT INTO `Reservations` VALUES (2,'2020-11-23',2,2147483647,NULL,'test@test.com'),(3,'2020-11-21',1,2147483647,NULL,'test@test.com'),(4,'2020-11-24',1,2147483647,NULL,'test@test.com'),(5,'2020-11-24',2,2147483647,NULL,'test@test.com'),(6,'2020-11-24',3,2147483647,NULL,'test@test.com'),(7,'2020-11-24',4,2147483647,NULL,'test@test.com'),(8,'2020-11-24',10,2147483647,NULL,'test@test.com'),(9,'2020-11-24',2,2147483647,NULL,'test@test.com'),(10,'2020-11-24',3,1350,NULL,'test@test.com'),(11,'2020-11-24',4,1400,NULL,'rumiadmin@admin.com'),(13,'2020-11-24',1,150,NULL,'test@test.com'),(14,'2020-11-26',1,350,NULL,'test@test.com'),(15,'2020-11-26',1,100,NULL,'test@test.com'),(16,'2020-11-26',1,100,NULL,'test@test.com'),(17,'2020-11-27',2,600,NULL,'test@test.com'),(18,'2020-12-06',1,100,NULL,'test@test.com'),(19,'2020-12-06',1,150,NULL,'alicetang@email.com'),(20,'2020-12-06',1,150,NULL,'alicetang@email.com'),(21,'2020-12-09',200,30000,NULL,'chris18@gmail.com'),(22,'2020-12-15',3,450,NULL,'test@test.com'),(23,'2020-12-19',8,600,NULL,'test@test.com');
/*!40000 ALTER TABLE `Reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Stops`
--

DROP TABLE IF EXISTS `Stops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Stops` (
  `Flight_Number` int NOT NULL,
  `Airline_ID` char(2) NOT NULL,
  `Airport_ID` char(3) NOT NULL,
  `Local_arrival` time DEFAULT NULL,
  `Local_departure` time DEFAULT NULL,
  PRIMARY KEY (`Airport_ID`,`Flight_Number`,`Airline_ID`),
  KEY `Flight_Number` (`Flight_Number`),
  KEY `Airline_ID` (`Airline_ID`),
  CONSTRAINT `Stops_ibfk_1` FOREIGN KEY (`Airport_ID`) REFERENCES `Airports` (`Airport_ID`),
  CONSTRAINT `Stops_ibfk_2` FOREIGN KEY (`Flight_Number`) REFERENCES `Flights` (`Flight_Number`),
  CONSTRAINT `Stops_ibfk_3` FOREIGN KEY (`Airline_ID`) REFERENCES `Airlines` (`Airline_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Stops`
--

LOCK TABLES `Stops` WRITE;
/*!40000 ALTER TABLE `Stops` DISABLE KEYS */;
INSERT INTO `Stops` VALUES (111,'AA','AAA','02:30:00','08:00:00'),(112,'AB','AAA','05:30:00','12:30:00'),(112,'AB','AAB','05:30:00','12:30:00');
/*!40000 ALTER TABLE `Stops` ENABLE KEYS */;
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

-- Dump completed on 2020-12-19 14:05:32
