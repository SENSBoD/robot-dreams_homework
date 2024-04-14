/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
WITH t
AS(
    SELECT c.name, f.film_id
        FROM film_category f
            JOIN category c ON c.category_id = f.category_id
)
SELECT name, COUNT(film_id) as count_films
    FROM t
    GROUP BY name
    ORDER BY count_films DESC;
/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
SELECT CONCAT(a.first_name, ' ', a.last_name) AS actor_name,
    COUNT(r.rental_id) AS total_rent
    FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_actor fa ON f.film_id = fa.film_id
        JOIN actor a ON fa.actor_id = a.actor_id
    GROUP BY actor_name
    ORDER BY total_rent DESC
    LIMIT 10;
/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
SELECT c.name AS category,
    SUM(p.amount) AS total_sales
    FROM payment p
        JOIN rental r ON p.rental_id = r.rental_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
    GROUP BY category
    ORDER BY total_sales DESC;
/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
SELECT DISTINCT(f.title) as film_titles
FROM film f
WHERE NOT EXISTS
    (SELECT NULL
        FROM inventory i
        WHERE f.film_id = i.film_id
    );
/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
SELECT CONCAT(a.first_name, ' ', a.last_name) as actor_name,
    COUNT(fa.film_id) as total_films
    FROM category c
        JOIN film_category fc ON c.category_id = fc.category_id
        JOIN film_actor fa ON fc.film_id = fa.film_id
        JOIN actor a ON fa.actor_id = a.actor_id
    WHERE c.name = 'Children'
    GROUP BY actor_name
    ORDER BY total_films DESC
    LIMIT 3;