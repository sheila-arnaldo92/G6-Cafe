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
-- Temporary view structure for view `vwmonthlysales`
--

DROP TABLE IF EXISTS `vwmonthlysales`;
/*!50001 DROP VIEW IF EXISTS `vwmonthlysales`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vwmonthlysales` AS SELECT 
 1 AS `Monthly_Sales`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vwyearlysales`
--

DROP TABLE IF EXISTS `vwyearlysales`;
/*!50001 DROP VIEW IF EXISTS `vwyearlysales`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vwyearlysales` AS SELECT 
 1 AS `SUM(net_amount)`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vwdaily_sales_report`
--

DROP TABLE IF EXISTS `vwdaily_sales_report`;
/*!50001 DROP VIEW IF EXISTS `vwdaily_sales_report`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vwdaily_sales_report` AS SELECT 
 1 AS `date_time`,
 1 AS `receipt_number`,
 1 AS `item_name`,
 1 AS `quantity`,
 1 AS `subtotal`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vwmonthlysales`
--

/*!50001 DROP VIEW IF EXISTS `vwmonthlysales`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`devuser`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vwmonthlysales` AS select sum(`orders`.`net_amount`) AS `Monthly_Sales` from `orders` where (month(`orders`.`date_time`) = month(now())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vwyearlysales`
--

/*!50001 DROP VIEW IF EXISTS `vwyearlysales`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`devuser`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vwyearlysales` AS select sum(`orders`.`net_amount`) AS `SUM(net_amount)` from `orders` where (year(`orders`.`date_time`) = year(now())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vwdaily_sales_report`
--

/*!50001 DROP VIEW IF EXISTS `vwdaily_sales_report`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`devuser`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vwdaily_sales_report` AS select `o`.`date_time` AS `date_time`,`o`.`receipt_number` AS `receipt_number`,`md`.`item_name` AS `item_name`,`od`.`quantity` AS `quantity`,`od`.`subtotal` AS `subtotal` from ((`order_details` `od` left join `orders` `o` on((`o`.`order_id` = `od`.`order_id`))) left join `menu_details` `md` on((`md`.`item_id` = `od`.`item_id`))) where (cast(`o`.`date_time` as date) = cast(now() as date)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-05 23:13:58
