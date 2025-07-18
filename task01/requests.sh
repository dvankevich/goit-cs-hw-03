#!/bin/bash

CONTAINER_NAME="task01-postgres"

declare -a queries=(
    "SELECT * FROM tasks WHERE user_id = 1;"
    "SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');"
    "UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 10;"
    "SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);"
    "INSERT INTO tasks (title, description, status_id, user_id) VALUES ('New Task Title', 'Task description here.', (SELECT id FROM status WHERE name = 'new'), 1);"
    "SELECT * FROM tasks WHERE status_id <> (SELECT id FROM status WHERE name = 'completed');"
    "DELETE FROM tasks WHERE id = 13;"
    "SELECT * FROM users WHERE email = 'staceymoore@example.org';"
    "UPDATE users SET fullname = 'New Full Name' WHERE id = 1;"
    "SELECT s.name, COUNT(t.id) AS task_count FROM status s LEFT JOIN tasks t ON s.id = t.status_id GROUP BY s.name;"
    "SELECT t.* FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE '%@example.net';"
    "SELECT * FROM tasks WHERE description IS NULL OR description = '';"
    "SELECT u.*, t.* FROM users u INNER JOIN tasks t ON u.id = t.user_id WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress');"
    "SELECT u.*, COUNT(t.id) AS task_count FROM users u LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.id;"
)

for query in "${queries[@]}"; do
    echo "Executing query: $query"
    docker exec -it "$CONTAINER_NAME" psql -U postgres -c "$query"

    read -n 1 -s -r -p "Press any key to continue..."
done