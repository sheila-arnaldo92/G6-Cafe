USE g6cafe;

DROP VIEW IF EXISTS vwdaily_sales_report;
CREATE ALGORITHM=UNDEFINED DEFINER=`admin`@`localhost` 
SQL SECURITY DEFINER VIEW `g6cafe`.`vwdaily_sales_report` AS 
select `o`.`date_time` AS `date_time`,
`o`.`receipt_number` AS `receipt_number`,
`md`.`item_name` AS `item_name`,
`od`.`quantity` AS `quantity`,
`od`.`subtotal` AS `subtotal` 
from ((`g6cafe`.`order_details` `od` 
left join `g6cafe`.`orders` `o` on((`o`.`order_id` = `od`.`order_id`))) 
left join `g6cafe`.`menu_details` `md` on((`md`.`item_id` = `od`.`item_id`))) 
where (cast(`o`.`date_time` as date) = cast(now() as date));

DROP VIEW IF EXISTS vwmonthlysales;
CREATE ALGORITHM=UNDEFINED DEFINER=`admin`@`localhost` 
SQL SECURITY DEFINER VIEW `g6cafe`.`vwmonthlysales` AS 
select sum(`g6cafe`.`orders`.`net_amount`) AS `Monthly_Sales` 
from `g6cafe`.`orders` 
where (month(`g6cafe`.`orders`.`date_time`) = month(now()));


DROP VIEW IF EXISTS vwyearlysales;
CREATE ALGORITHM=UNDEFINED DEFINER=`admin`@`localhost` 
SQL SECURITY DEFINER VIEW `g6cafe`.`vwyearlysales` AS 
select sum(`g6cafe`.`orders`.`net_amount`) AS `SUM(net_amount)` 
from `g6cafe`.`orders` 
where (year(`g6cafe`.`orders`.`date_time`) = year(now()));
