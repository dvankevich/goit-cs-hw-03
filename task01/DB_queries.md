### 1. Отримати всі завдання певного користувача

```sql
SELECT * FROM tasks WHERE user_id = 1;
```

### 2. Вибрати завдання за певним статусом

```sql
SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');
```

### 3. Оновити статус конкретного завдання

```sql
UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 10;
```

### 4. Отримати список користувачів, які не мають жодного завдання

```sql
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);
```

### 5. Додати нове завдання для конкретного користувача

```sql
INSERT INTO tasks (title, description, status_id, user_id) VALUES ('New Task Title', 'Task description here.', (SELECT id FROM status WHERE name = 'new'), 1);
```

### 6. Отримати всі завдання, які ще не завершено

```sql
SELECT * FROM tasks WHERE status_id <> (SELECT id FROM status WHERE name = 'completed');
```

### 7. Видалити конкретне завдання

```sql
DELETE FROM tasks WHERE id = 13;
```

### 8. Знайти користувачів з певною електронною поштою

```sql
SELECT * FROM users WHERE email = 'staceymoore@example.org';
```

### 9. Оновити ім'я користувача

```sql
UPDATE users SET fullname = 'New Full Name' WHERE id = 1;
```

### 10. Отримати кількість завдань для кожного статусу

```sql
SELECT s.name, COUNT(t.id) AS task_count
FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.name;
```

### 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти

```sql
SELECT t.*
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.net';
```

### 12. Отримати список завдань, що не мають опису

```sql
SELECT * FROM tasks WHERE description IS NULL OR description = '';
```

### 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'

```sql
SELECT u.*, t.*
FROM users u
INNER JOIN tasks t ON u.id = t.user_id
WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress');
```

### 14. Отримати користувачів та кількість їхніх завдань

```sql
SELECT u.*, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id;
```
