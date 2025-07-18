from pymongo import MongoClient, errors


client = MongoClient("mongodb://localhost:27017/")
db = client["test"]
collection = db["cats"]


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except errors.PyMongoError as e:
            print(f"Помилка при виконанні '{func.__name__}': {e}")

    return wrapper


@error_handler
def get_all_records():
    records = collection.find()
    for record in records:
        print(record)


@error_handler
def get_cat_info_by_name():
    cat_name = input("Введіть ім'я кота: ")
    cat_info = collection.find_one({"name": cat_name})
    if cat_info:
        print("Інформація про кота:")
        print(f"Ім'я: {cat_info['name']}")
        print(f"Вік: {cat_info['age']}")
        print(f"Особливості: {', '.join(cat_info['features'])}")
    else:
        print("Кота з таким ім'ям не знайдено.")


@error_handler
def update_cat_age(cat_name, new_age):
    result = collection.update_one({"name": cat_name}, {"$set": {"age": new_age}})
    if result.modified_count > 0:
        print(f"Вік кота '{cat_name}' успішно оновлено на {new_age}.")
    else:
        print(f"Кота з ім'ям '{cat_name}' не знайдено або вік вже такий самий.")


@error_handler
def add_cat_feature(cat_name, new_feature):
    result = collection.update_one(
        {"name": cat_name},
        {"$addToSet": {"features": new_feature}},
    )
    if result.modified_count > 0:
        print(f"Характеристика '{new_feature}' успішно додана до кота '{cat_name}'.")
    else:
        print(f"Кота з ім'ям '{cat_name}' не знайдено або характеристика вже існує.")


@error_handler
def delete_cat_by_name(cat_name):
    result = collection.delete_one({"name": cat_name})
    if result.deleted_count > 0:
        print(f"Запис про кота '{cat_name}' успішно видалено.")
    else:
        print(f"Кота з ім'ям '{cat_name}' не знайдено.")


@error_handler
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
