SELECT payment_status, SUM(total_amount) as total_payment, AVG(total_amount) as avg_payment
FROM orders
GROUP BY payment_status
ORDER BY SUM(total_amount) DESC

/*

payment_status|total_payment     |avg_payment       |
--------------+------------------+------------------+
paid          |11198.989990234375|1119.8989990234375|
pending       |            3049.5|           762.375|
cancelled     |             120.0|              60.0|

*/

SELECT count(DISTINCT item_id) AS items_cnt, sum(product_price) AS items_total_cost, avg(product_price) AS avg_item_cost
FROM `default`.order_items

/*

items_cnt|items_total_cost|avg_item_cost|
---------+----------------+-------------+
       16|          6144.0|        384.0|
*/



SELECT CAST(order_date AS date) AS stat_order_date, count(order_id) AS orders_cnt, sum(total_amount) AS revenue
FROM orders
GROUP BY CAST(order_date AS date)


stat_order_date|orders_cnt|revenue          |
---------------+----------+-----------------+
     2023-03-01|         5|           4149.5|
     2023-03-02|         6|           4769.0|
     2023-03-03|         5|5449.989990234375|


SELECT DISTINCT o.user_id, sum(total_amount) AS total_spend, count(order_id) AS total_orders
FROM orders o
INNER JOIN (
    SELECT user_id
    FROM orders
    GROUP BY  user_id
    ORDER BY sum(total_amount) DESC
    LIMIT 2

    UNION ALL

    SELECT user_id
    FROM orders
    GROUP BY  user_id
    ORDER BY count(order_id) DESC
    LIMIT 2
) t ON t.user_id = o.user_id
GROUP BY o.user_id;
/*
user_id|total_spend      |total_orders|
-------+-----------------+------------+
     15|1799.989990234375|           3|
     10|           6900.0|          10|
     13|           4100.0|           2|

*/