WITH Spend AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.email,
        SUM(oi.quantity * oi.price_per_unit) AS total_spent
    FROM
        Customers c
    JOIN
        Orders o ON c.customer_id = o.customer_id
    JOIN
        Order_Items oi ON o.order_id = oi.order_id
    WHERE
        o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    GROUP BY
        c.customer_id, c.customer_name, c.email
),
Category AS (
    SELECT
        c.customer_id,
        p.category,
        SUM(oi.quantity * oi.price_per_unit) AS category_spent
    FROM
        Customers c
    JOIN
        Orders o ON c.customer_id = o.customer_id
    JOIN
        Order_Items oi ON o.order_id = oi.order_id
    JOIN
        Products p ON oi.product_id = p.product_id
    WHERE
        o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    GROUP BY
        c.customer_id, p.category
),
TopCustomerCategory AS (
    SELECT
        c.customer_id,
        c.category,
        c.category_spent,
        ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY c.category_spent DESC) AS rank
    FROM
        Category c
)
SELECT
    s.customer_id,
    s.customer_name,
    s.email,
    s.total_spent,
    tcc.category AS most_purchased_category
FROM
    Spend s
JOIN
    TopCustomerCategory tcc ON s.customer_id = tcc.customer_id
WHERE
    tcc.rank = 1
ORDER BY
    s.total_spent DESC
LIMIT 5;
