import psycopg2
from faker import Faker
import random

DATABASE_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "mysecretpassword",
    "host": "localhost",
    "port": "5432",
}

fake = Faker()


def fill_users(cursor, num_users=10):
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.unique.email()
        cursor.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email)
        )


def fill_tasks(cursor, num_tasks=20):
    cursor.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_tasks):
        title = fake.sentence(nb_words=4)
        description = fake.text(max_nb_chars=200)
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cursor.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id),
        )


def main():
    try:
        # connect to db
        connection = psycopg2.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        # fill db
        fill_users(cursor)
        fill_tasks(cursor)

        # save changes
        connection.commit()
        print("Tables filled with data successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
