-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: qlkhachsan
-- ------------------------------------------------------
-- Server version	8.0.26

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
-- Table structure for table `bill`
--

DROP TABLE IF EXISTS `bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sum_price` float DEFAULT '0',
  `costs` float DEFAULT '0',
  `deposit` float DEFAULT '0',
  `phi_phu` float DEFAULT '0',
  `employee_id` int DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `status` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `room_number_date` int DEFAULT NULL,
  `customer_id` int NOT NULL,
  `room_book_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  KEY `employee_id` (`employee_id`),
  KEY `room_book_id` (`room_book_id`),
  CONSTRAINT `bill_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `user` (`id`),
  CONSTRAINT `bill_ibfk_2` FOREIGN KEY (`employee_id`) REFERENCES `user` (`id`),
  CONSTRAINT `bill_ibfk_3` FOREIGN KEY (`room_book_id`) REFERENCES `room_book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill`
--

LOCK TABLES `bill` WRITE;
/*!40000 ALTER TABLE `bill` DISABLE KEYS */;
INSERT INTO `bill` VALUES (24,37.5,20,0,17.5,3,'2021-11-27 21:05:18','Đã thanh toán',1,8,73),(25,75,25,25,25,3,'2021-11-27 21:05:21','Đã thanh toán',2,8,74);
/*!40000 ALTER TABLE `bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_information`
--

DROP TABLE IF EXISTS `book_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_information` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CMND` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `address` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `room_book_id` int NOT NULL,
  `category_customer_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `room_book_id` (`room_book_id`),
  KEY `category_customer_id` (`category_customer_id`),
  CONSTRAINT `book_information_ibfk_1` FOREIGN KEY (`room_book_id`) REFERENCES `room_book` (`id`),
  CONSTRAINT `book_information_ibfk_2` FOREIGN KEY (`category_customer_id`) REFERENCES `category_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_information`
--

LOCK TABLES `book_information` WRITE;
/*!40000 ALTER TABLE `book_information` DISABLE KEYS */;
INSERT INTO `book_information` VALUES (32,'Huỳnh Đình Thông','206123123','Hồ Chí Minh ',73,1),(33,'Nguyễn Văn A','123091931','Hồ Chí Minh',73,2),(34,'Mạnh Thắng','206367 ','Thủ Đức ',74,2),(35,'Nguyễn Văn B','12313e','Thủ Đức',74,1);
/*!40000 ALTER TABLE `book_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category_customer`
--

DROP TABLE IF EXISTS `category_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category_customer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `percent` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_customer`
--

LOCK TABLES `category_customer` WRITE;
/*!40000 ALTER TABLE `category_customer` DISABLE KEYS */;
INSERT INTO `category_customer` VALUES (1,'nội địa',0),(2,'nước ngoài',150);
/*!40000 ALTER TABLE `category_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category_room`
--

DROP TABLE IF EXISTS `category_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category_room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `number_people` int NOT NULL,
  `max_people` int DEFAULT NULL,
  `surcharge` float DEFAULT NULL,
  `price` float DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `number_people` (`number_people`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_room`
--

LOCK TABLES `category_room` WRITE;
/*!40000 ALTER TABLE `category_room` DISABLE KEYS */;
INSERT INTO `category_room` VALUES (1,1,2,25,20),(2,2,3,25,25),(3,3,5,25,30);
/*!40000 ALTER TABLE `category_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_label_room`
--

DROP TABLE IF EXISTS `group_label_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_label_room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_label_room`
--

LOCK TABLES `group_label_room` WRITE;
/*!40000 ALTER TABLE `group_label_room` DISABLE KEYS */;
INSERT INTO `group_label_room` VALUES (1,'Kiểu phòng'),(2,'Loại giường'),(4,'Tầm nhìn');
/*!40000 ALTER TABLE `group_label_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `label_room`
--

DROP TABLE IF EXISTS `label_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `label_room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `percent` float DEFAULT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `label_room_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `group_label_room` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `label_room`
--

LOCK TABLES `label_room` WRITE;
/*!40000 ALTER TABLE `label_room` DISABLE KEYS */;
INSERT INTO `label_room` VALUES (1,'Phòng Standard',0,1),(2,'Phòng Superior ',5,1),(3,'Phòng Deluxe',20,1),(4,'Phòng Suite ',50,1),(5,'Giường Đơn',0,2),(6,'Giường Đôi Nhỏ',2,2),(7,'Giường Đôi Lớn',5,2),(8,'Giường Cỡ Lớn',5,2),(9,'Hướng núi',4,4),(10,'Hướng biển',9,4),(11,'Trên cao',2,4),(12,'Hướng phố',3,4),(13,'Không có',0,4);
/*!40000 ALTER TABLE `label_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'admin'),(2,'staff'),(3,'user');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `image` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `status` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `room_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category_room` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES (1,'Phòng 1','https://d2ile4x3f22snf.cloudfront.net/wp-content/uploads/sites/174/2017/08/10060639/Deluxe-3092-700x490.jpg','trống',1),(2,'Phòng 2','https://www.hoteljob.vn/files/Anh-HTJ-Hong/mau-tam-trang%20tri-giuong-khach-san-dep-nhat-19.jpg','trống',1),(3,'Phòng 3','https://vinapad.com/wp-content/uploads/2019/01/Phong-ngu-khach-san-mini.jpg','trống',1),(4,'Phòng 4','https://thietkenoithat.com/Portals/0/DNNGo_PhotoAlbums/53503/9883/ks5.jpg','trống',1),(5,'Phòng 5','https://noithathunggiaphat.vn/uploaded/Danh-muc-noi-that/noi-that-phong-ngu/noi-that-2-phong-ngu-dep/noi-that-phong-ngu-hien-dai.jpg','trống',1),(6,'Phòng 6','https://uniquedecor.com.vn/wp-content/uploads/2018/03/noi_that_khach_san_002.png','trống',2),(7,'Phòng 7','http://giasangocongnghiep.com/wp-content/uploads/2018/07/thiet-ke-noi-that-khach-san.png','trống',2),(8,'Phòng 8','http://giasangocongnghiep.com/wp-content/uploads/2018/07/thiet-ke-noi-that-khach-san.png','trống',2),(9,'Phòng 9','https://phuchoa.com.vn/wp-content/uploads/2021/04/cac-loai-phong-trong-khach-san-5-sao.jpg','trống',2),(10,'Phòng 10','https://lotushotel.vn/wp-content/uploads/2021/06/quy-trinh-ve-sinh-phong-khach-san-doi-voi-phong-khach.jpg','trống',2),(11,'Phòng 11','https://vnn-imgs-f.vgcloud.vn/2020/02/19/19/goi-khach-san-5.jpg','trống',3),(12,'Phòng 12','https://noithathoangha.com.vn/upload/news/1-thiet-ke-phong-ngu-khach-san-1-6289.jpg','trống',3),(13,'Phòng 13','https://thietkenoithatkhachsan.com/Portals/88/xNews/uploads/2017/12/26/noi-that-phong-ngu-khach-san-3-sao.jpg','trống',3),(14,'Phòng 14','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStnJ8YsxyaCWb3vIlIAVBk6-LoFF2Zndr7EA&usqp=CAU','trống',3),(15,'Phòng 15','https://pix10.agoda.net/hotelImages/1637964/-1/c57b69367732bd81c3bc87a22f6d35fd.jpg?s=1024x768','trống',3),(16,'Phòng 16','https://smjahome.com/wp-content/uploads/2021/07/HkyxKOSlL-capture.jpg','trống',1),(17,'Phòng 17','https://bizweb.dktcdn.net/100/396/288/articles/52c2e14f642fba03f175f548c3a3265f.jpg?v=1600999074960','trống',1),(18,'Phòng 18','https://www.hoteljob.vn/files/Anh-HTJ-Hong/tieu-chi-can-co-trong-thiet-ke-phong-khach-san-1.jpg','trống',1),(19,'Phòng 19','https://noithatduonggia.vn/wp-content/uploads/2017/03/mau-thiet-ke-noi-that-khach-san-ksdg02.jpg','trống',1);
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room_book`
--

DROP TABLE IF EXISTS `room_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room_book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `date_out` datetime DEFAULT NULL,
  `status` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `room_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `room_id` (`room_id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `room_book_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`),
  CONSTRAINT `room_book_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `room_book_ibfk_3` FOREIGN KEY (`book_id`) REFERENCES `type_book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_book`
--

LOCK TABLES `room_book` WRITE;
/*!40000 ALTER TABLE `room_book` DISABLE KEYS */;
INSERT INTO `room_book` VALUES (73,'2021-11-27 00:00:00','2021-11-28 00:00:00','Đã trả phòng',1,8,1),(74,'2021-11-28 00:00:00','2021-11-30 00:00:00','Đã trả phòng',6,8,2);
/*!40000 ALTER TABLE `room_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type_book`
--

DROP TABLE IF EXISTS `type_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `type_book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `percent_cost` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type_book`
--

LOCK TABLES `type_book` WRITE;
/*!40000 ALTER TABLE `type_book` DISABLE KEYS */;
INSERT INTO `type_book` VALUES (1,'online_fast',0),(2,'online_detail',50),(3,'direct',0);
/*!40000 ALTER TABLE `type_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type_room`
--

DROP TABLE IF EXISTS `type_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `type_room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_id` int NOT NULL,
  `label_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `room_id` (`room_id`),
  KEY `label_id` (`label_id`),
  CONSTRAINT `type_room_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`),
  CONSTRAINT `type_room_ibfk_2` FOREIGN KEY (`label_id`) REFERENCES `label_room` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type_room`
--

LOCK TABLES `type_room` WRITE;
/*!40000 ALTER TABLE `type_room` DISABLE KEYS */;
INSERT INTO `type_room` VALUES (1,1,1),(2,1,5),(3,1,13),(4,2,1),(5,2,5),(6,2,13),(7,3,2),(8,3,5),(9,3,11),(10,4,3),(11,4,8),(12,4,10),(13,4,11),(14,5,4),(15,5,8),(16,5,9),(17,5,12),(18,5,11),(19,16,1),(20,16,5),(21,16,13),(22,17,1),(23,17,5),(24,17,13),(25,18,1),(26,18,5),(27,18,13),(28,19,1),(29,19,5),(30,19,13),(32,6,1),(33,6,5),(34,6,13),(35,7,2),(36,7,6),(37,7,10),(38,8,1),(39,8,5),(40,8,13),(41,9,1),(42,9,8),(43,9,11),(44,10,4),(45,10,7),(46,10,9),(47,10,11),(48,11,1),(49,11,5),(50,11,13),(51,12,1),(52,12,5),(53,12,13),(55,13,3),(56,13,6),(57,13,12),(58,14,3),(59,14,8),(60,14,10),(61,14,11),(62,15,4),(63,15,7),(64,15,10),(65,15,11);
/*!40000 ALTER TABLE `type_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `joined_date` datetime DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `name` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `image` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `birthdate` datetime DEFAULT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','b\' ,\\xb9b\\xacY\\x07[\\x96K\\x07\\x15-#Kp\'',NULL,1,'Hoang Minh Thang     ','minhhoangthang75@gmail.com','Linh Trung, Thủ Đức  ','0942895938','https://res.cloudinary.com/ho-chi-minh-city-of-technology-and-education/image/upload/v1637941479/fsje9kigthxgiwkhy3tm.jpg','2001-11-03 00:00:00',1),(3,'haiduong','b\' ,\\xb9b\\xacY\\x07[\\x96K\\x07\\x15-#Kp\'','2021-11-24 09:28:27',1,'Lê Hải Dương','HaiDuong@gmail.com','Thủ Đức','0923123112',NULL,'2001-04-11 09:36:00',2),(6,'ducthang','b\' ,\\xb9b\\xacY\\x07[\\x96K\\x07\\x15-#Kp\'','2021-11-26 15:33:48',1,'Duong Duc Thang','nhoclun31101@gmail.com',NULL,NULL,NULL,NULL,3),(8,'dinhthong','b\' ,\\xb9b\\xacY\\x07[\\x96K\\x07\\x15-#Kp\'','2021-11-27 20:31:44',1,'Đình Thông   ','cnpmute@gmail.com','Hồ Chí Minh','0923128313','https://res.cloudinary.com/ho-chi-minh-city-of-technology-and-education/image/upload/v1638020898/rfihtggzipho3idlebul.jpg','2001-11-02 00:00:00',3);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-28 21:01:20
