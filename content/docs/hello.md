---
title: Hello World
weight: 2
---

## Hello World

### Example code (SQL)

```sql
SELECT
    customer_id,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY customer_id;
```

