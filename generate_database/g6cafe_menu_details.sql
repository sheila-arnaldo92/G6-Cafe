-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: g6cafe
-- ------------------------------------------------------
-- Server version	8.0.39

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

--
-- Table structure for table `menu_details`
--

DROP TABLE IF EXISTS `menu_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_details` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_details`
--

LOCK TABLES `menu_details` WRITE;
/*!40000 ALTER TABLE `menu_details` DISABLE KEYS */;
INSERT INTO `menu_details` VALUES (1,'Espresso','Americano','americano.jpeg',150.00),(2,'Espresso','Cappuccino','cappucino.png',150.00),(3,'Espresso','Double Espresso','double espresso.png',125.00),(4,'Espresso','Latte','latte.png',175.00),(5,'Espresso','Macchiato','macchiato.png',175.00),(6,'Espresso','Mocha','mocha.png',180.00),(7,'Espresso','White Mocha','white mocha.png',150.00),(8,'Tea','Earl Grey','earl grey.png',120.00),(9,'Tea','English Breakfast','english breakfast.png',110.00),(10,'Tea','Green Tea','green tea.png',110.00),(11,'Tea','Jasmine Tea','jasmine tea.png',115.00),(12,'Tea','Black Tea','black tea.png',125.00),(13,'Tea','Red Tea','red tea.png',130.00),(14,'Ice Blended','Caramel','caramel.png',125.00),(15,'Ice Blended','Coffee Jelly','coffee jelly.png',130.00),(16,'Ice Blended','Cookies and Cream','cookies and cream.png',150.00),(17,'Ice Blended','Hazelnut Mocha','hazel nut mocha.png',155.00),(18,'Ice Blended','Matcha Cream','matcha cream.png',135.00),(19,'Ice Blended','Mint Chocolate Chip','mint chocolate chips.png',150.00),(20,'Ice Blended','Strawberry Cream','strawberry cream.png',150.00),(21,'Ice Blended','Vanilla Bean','vanilla bean.jpg',135.00),(22,'Pastries','Bagels','bagels.jpg',90.00),(23,'Pastries','Donut','donut.jpg',70.00),(24,'Pastries','Muffins','muffin.jpg',75.00),(25,'Pastries','Biscotto','biscotto.jpg',80.00),(26,'Pasta','Spaghetti Bolognaise','Spaghetti Bolognese.jpg\"',185.00),(27,'Pasta','Lasagne','lasagna.jpg\"',190.00),(28,'Pasta','Pasta Carbonara','Pasta Carbonara.jpg',150.00),(29,'Pasta','Ravioli','ravioli.jpg',200.00),(30,'Pasta','Spaghetti alle Vongole','Spaghetti alle Vongole.jpg',200.00),(31,'Pasta','Macaroni Cheese','Macaroni Cheese.jpg',190.00);
/*!40000 ALTER TABLE `menu_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-05 23:13:56
