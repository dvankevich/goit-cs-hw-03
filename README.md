# goit-cs-hw-03

## task01

### run postgres docker container

https://hub.docker.com/_/postgres

```
docker run --name task01-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

```

check is postgress running

```
sudo netstat -tunlp | grep 5432

tcp        0      0 0.0.0.0:5432            0.0.0.0:*               LISTEN      38166/docker-proxy
```

### connect to postgres

-   host: localhost
-   port: 5432
-   user: postgres
-   password: mysecretpassword

### connect to container

```
docker exec -it task01-postgres psql -U postgres
```

### stop container

```
docker stop task01-postgres
```

### start container

```
docker stop task01-postgres
```

### psql

#### show databases

```
postgres=# \l
                                                    List of databases
   Name    |  Owner   | Encoding | Locale Provider |  Collate   |   Ctype    | Locale | ICU Rules |   Access privileges
-----------+----------+----------+-----------------+------------+------------+--------+-----------+-----------------------
 postgres  | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           |
 template0 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           | =c/postgres          +
           |          |          |                 |            |            |        |           | postgres=CTc/postgres
 template1 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           | =c/postgres          +
           |          |          |                 |            |            |        |           | postgres=CTc/postgres
(3 rows)

```

#### show tables

```
\dt

         List of relations
 Schema |  Name  | Type  |  Owner
--------+--------+-------+----------
 public | status | table | postgres
 public | tasks  | table | postgres
 public | users  | table | postgres
(3 rows)

```

```
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

 table_name
------------
 status
 tasks
 users
(3 rows)

```

#### show tables descriptions

```
postgres=# \d status
                                   Table "public.status"
 Column |         Type          | Collation | Nullable |              Default
--------+-----------------------+-----------+----------+------------------------------------
 id     | integer               |           | not null | nextval('status_id_seq'::regclass)
 name   | character varying(50) |           | not null |
Indexes:
    "status_pkey" PRIMARY KEY, btree (id)
    "status_name_key" UNIQUE CONSTRAINT, btree (name)
Referenced by:
    TABLE "tasks" CONSTRAINT "tasks_status_id_fkey" FOREIGN KEY (status_id) REFERENCES status(id)

postgres=# \d tasks
                                      Table "public.tasks"
   Column    |          Type          | Collation | Nullable |              Default
-------------+------------------------+-----------+----------+-----------------------------------
 id          | integer                |           | not null | nextval('tasks_id_seq'::regclass)
 title       | character varying(100) |           | not null |
 description | text                   |           |          |
 status_id   | integer                |           |          |
 user_id     | integer                |           |          |
Indexes:
    "tasks_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "tasks_status_id_fkey" FOREIGN KEY (status_id) REFERENCES status(id)
    "tasks_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE


postgres=# \d users
                                     Table "public.users"
  Column  |          Type          | Collation | Nullable |              Default
----------+------------------------+-----------+----------+-----------------------------------
 id       | integer                |           | not null | nextval('users_id_seq'::regclass)
 fullname | character varying(100) |           | not null |
 email    | character varying(100) |           | not null |
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)
    "users_email_key" UNIQUE CONSTRAINT, btree (email)
Referenced by:
    TABLE "tasks" CONSTRAINT "tasks_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```

#### get information about foreign keys and relationships

```
postgres=# SELECT
    tc.table_name AS child_table,
    kcu.column_name AS child_column,
    ccu.table_name AS parent_table,
    ccu.column_name AS parent_column
FROM
    information_schema.table_constraints AS tc
JOIN
    information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN
    information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE
    constraint_type = 'FOREIGN KEY';

 child_table | child_column | parent_table | parent_column
-------------+--------------+--------------+---------------
 tasks       | status_id    | status       | id
 tasks       | user_id      | users        | id
(2 rows)

```

### DB diagram

![DB diagram](./db-scheme.png)

### create postgresql container and tables

[createdb.sh](./task01/createdb.sh)

### fill tables with faker

```
pip install faker
```

[seed.py](./task01/seed.py)

### DB queries

[DB_queries.md](./task01/DB_queries.md)

## task02

### mongodb docker container

https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/

```
docker pull mongodb/mongodb-community-server:latest

docker run --name task02-mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest
```

### RTSP MongoDB Shell Docker Image

https://hub.docker.com/r/rtsp/mongosh

```
docker pull rtsp/mongosh
```

#### Interactive Mode

```
docker run --rm -it rtsp/mongosh mongosh -- mongodb://localhost:27017
```

### pymongo

```
pip install pymongo
```

### add records to database via mongosh

```
docker run --rm -it rtsp/mongosh mongosh -- mongodb://172.17.0.1:27017
Current Mongosh Log ID:	687a9b9c81a85bc14d32a03b
Connecting to:		mongodb://172.17.0.1:27017/?directConnection=true&appName=mongosh+2.5.5
Using MongoDB:		8.0.11
Using Mongosh:		2.5.5

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/


To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

------
   The server generated these startup warnings when booting
   2025-07-18T19:08:05.458+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2025-07-18T19:08:06.840+00:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
   2025-07-18T19:08:06.840+00:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2025-07-18T19:08:06.840+00:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2025-07-18T19:08:06.840+00:00: We suggest setting the contents of sysfsFile to 0.
   2025-07-18T19:08:06.840+00:00: Your system has glibc support for rseq built in, which is not yet supported by tcmalloc-google and has critical performance implications. Please set the environment variable GLIBC_TUNABLES=glibc.pthread.rseq=0
   2025-07-18T19:08:06.840+00:00: vm.max_map_count is too low
   2025-07-18T19:08:06.841+00:00: We suggest setting swappiness to 0 or 1, as swapping can cause performance problems.
------

test> db.cats.find()
[
  {
    _id: ObjectId('687a9af1b3dfa36b3432a03c'),
    name: 'barsik',
    age: 3,
    features: [ 'ходить в капці', 'дає себе гладити', 'рудий' ]
  }
]
test> db.cats.insertMany([
...     {
...         name: 'Lama',
...         age: 2,
...         features: ['ходить в лоток', 'не дає себе гладити', 'сірий'],
...     },
...     {
...         name: 'Liza',
...         age: 4,
...         features: ['ходить в лоток', 'дає себе гладити', 'білий'],
...     },
...     {
...         name: 'Boris',
...         age: 12,
...         features: ['ходить в лоток', 'не дає себе гладити', 'сірий'],
...     },
...     {
...         name: 'Murzik',
...         age: 1,
...         features: ['ходить в лоток', 'дає себе гладити', 'чорний'],
...     },
... ])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('687aa25a81a85bc14d32a03c'),
    '1': ObjectId('687aa25a81a85bc14d32a03d'),
    '2': ObjectId('687aa25a81a85bc14d32a03e'),
    '3': ObjectId('687aa25a81a85bc14d32a03f')
  }
}
test>

```

### programm example run

```
python main.py
Collections in the database:
cats
{'_id': ObjectId('687a9af1b3dfa36b3432a03c'), 'name': 'barsik', 'age': 3, 'features': ['ходить в капці', 'дає себе гладити', 'рудий']}
{'_id': ObjectId('687aa25a81a85bc14d32a03c'), 'name': 'Lama', 'age': 2, 'features': ['ходить в лоток', 'не дає себе гладити', 'сірий']}
{'_id': ObjectId('687aa25a81a85bc14d32a03d'), 'name': 'Liza', 'age': 4, 'features': ['ходить в лоток', 'дає себе гладити', 'білий']}
{'_id': ObjectId('687aa25a81a85bc14d32a03e'), 'name': 'Boris', 'age': 12, 'features': ['ходить в лоток', 'не дає себе гладити', 'сірий']}
{'_id': ObjectId('687aa25a81a85bc14d32a03f'), 'name': 'Murzik', 'age': 1, 'features': ['ходить в лоток', 'дає себе гладити', 'чорний']}
Введіть ім'я кота: barsik
Інформація про кота:
Ім'я: barsik
Вік: 3
Особливості: ходить в капці, дає себе гладити, рудий
Вік кота 'barsik' успішно оновлено на 4.
Характеристика 'мурчить' успішно додана до кота 'barsik'.
Запис про кота 'barsik' успішно видалено.
Усі записи про котів успішно видалено. Видалено записів: 4.

```
