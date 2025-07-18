from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("mongodb://localhost:27017/")

db = client["test"]

collection_names = db.list_collection_names()

print("Collections in the database:")
for name in collection_names:
    print(name)

collection = db["cats"]


def get_all_records():
    records = collection.find()
    for record in records:
        print(record)


def get_cat_info_by_name():
    cat_name = input("Введіть ім'я кота: ")
    # Пошук кота за ім'ям
    cat_info = collection.find_one({"name": cat_name})

    if cat_info:
        print("Інформація про кота:")
        print(f"Ім'я: {cat_info['name']}")
        print(f"Вік: {cat_info['age']}")
        print(f"Особливості: {', '.join(cat_info['features'])}")
    else:
        print("Кота з таким ім'ям не знайдено.")


def update_cat_age(cat_name, new_age):
    result = collection.update_one({"name": cat_name}, {"$set": {"age": new_age}})

    if result.modified_count > 0:
        print(f"Вік кота '{cat_name}' успішно оновлено на {new_age}.")
    else:
        print(f"Кота з ім'ям '{cat_name}' не знайдено або вік вже такий самий.")


def add_cat_feature(cat_name, new_feature):
    result = collection.update_one(
        {"name": cat_name},
        {"$addToSet": {"features": new_feature}},
    )

    if result.modified_count > 0:
        print(f"Характеристика '{new_feature}' успішно додана до кота '{cat_name}'.")
    else:
        print(f"Кота з ім'ям '{cat_name}' не знайдено або характеристика вже існує.")


def delete_cat_by_name(cat_name):
    result = collection.delete_one({"name": cat_name})

    if result.deleted_count > 0:
        print(f"Запис про кота '{cat_name}' успішно видалено.")
    else:
        print(f"Кота з ім'ям '{cat_name}' не знайдено.")


def delete_all_cats():
    result = collection.delete_many({})

    print(
        f"Усі записи про котів успішно видалено. Видалено записів: {result.deleted_count}."
    )


if __name__ == "__main__":
    # Читання (Read)
    get_all_records()
    get_cat_info_by_name()
    # Оновлення (Update)
    update_cat_age("barsik", 4)
    add_cat_feature("barsik", "мурчить")
    # Видалення (Delete)
    delete_cat_by_name("barsik")
    delete_all_cats()
