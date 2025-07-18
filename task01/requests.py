import psycopg2
from psycopg2 import sql

DATABASE_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "mysecretpassword",
    "host": "localhost",
    "port": "5432",
}


def execute_query(query, params=None):
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        cursor.execute(query, params)

        # if SELECT - return results
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results

        # INSERT, UPDATE, DELETE - commit changes
        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    queries = [
        # 1. Отримати всі завдання певного користувача
        "SELECT * FROM tasks WHERE user_id = 1;",
        # 2. Вибрати завдання за певним статусом
        "SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');",
        # 3. Оновити статус конкретного завдання
        "UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 10;",
        # 4. Отримати список користувачів, які не мають жодного завдання
        "SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);",
        # 5. Додати нове завдання для конкретного користувача
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES ('New Task Title', 'Task description here.', (SELECT id FROM status WHERE name = 'new'), 1);",
        # 6. Отримати всі завдання, які ще не завершено
        "SELECT * FROM tasks WHERE status_id <> (SELECT id FROM status WHERE name = 'completed');",
        # 7. Видалити конкретне завдання
        "DELETE FROM tasks WHERE id = 13;",
        # 8. Знайти користувачів з певною електронною поштою
        "SELECT * FROM users WHERE email = 'staceymoore@example.org';",
        # 9. Оновити ім'я користувача
        "UPDATE users SET fullname = 'New Full Name' WHERE id = 1;",
        # 10. Отримати кількість завдань для кожного статусу
        "SELECT s.name, COUNT(t.id) AS task_count FROM status s LEFT JOIN tasks t ON s.id = t.status_id GROUP BY s.name;",
        # 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
        "SELECT t.* FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE '%@example.net';",
        # 12. Отримати список завдань, що не мають опису
        "SELECT * FROM tasks WHERE description IS NULL OR description = '';",
        # 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
        "SELECT u.*, t.* FROM users u INNER JOIN tasks t ON u.id = t.user_id WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress');",
        # 14. Отримати користувачів та кількість їхніх завдань
        "SELECT u.*, COUNT(t.id) AS task_count FROM users u LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.id;",
    ]

    for i, query in enumerate(queries):
        print(f"Executing Query {i + 1}: {query}")
        results = execute_query(query)

        if results is not None:
            print(results)
