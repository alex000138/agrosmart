import json
import psycopg2

# Путь к JSON-файлу
file_path = r'C:\json_test_import.json'

# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname="agrosmart2",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

try:
    # Создание временной таблицы
    cursor.execute("""
    CREATE TEMP TABLE temp_json_data (
        json_data JSONB
    );
    """)
    conn.commit()

    print("Table temp_json_data created.")

    # Открываем и читаем JSON-файл
    with open(file_path, 'r', encoding='utf-8') as file:
        # Проверяем, какой тип JSON-документа в файле
        try:
            # Проверяем, если файл содержит массив JSON-объектов
            data = json.load(file)
            if isinstance(data, list):
                print("JSON massive data object")
                for record in data:
                    cursor.execute(
                        """
                        INSERT INTO temp_json_data (json_data)
                        VALUES (%s)
                        """,
                        (json.dumps(record),)
                    )
            else:
                raise ValueError("JSON need MASSIV.")
        except json.JSONDecodeError:
            # Проверяем, если файл содержит один JSON-объект на строку
            file.seek(0)  # Возвращаем указатель файла в начало
            print("JSON string data object")
            for line in file:
                record = json.loads(line)
                cursor.execute(
                    """
                    INSERT INTO temp_json_data (json_data)
                    VALUES (%s)
                    """,
                    (json.dumps(record),)
                )
        except Exception as e:
            print(f"Error read JSON file: {e}")

    # Применяем изменения
    conn.commit()

    print("Success.")

    # Проверяем количество записей в таблице
    cursor.execute("SELECT COUNT(*) FROM temp_json_data;")
    count = cursor.fetchone()[0]
    print(f"Load {count} value in tables temp_json_data.")

    # Выводим первые 5 записей для проверки
    cursor.execute("SELECT * FROM temp_json_data LIMIT 5;")
    rows = cursor.fetchall()
    print("First 5 value in table temp_json_data:")
    for row in rows:
        print(row)

except psycopg2.Error as e:
    print(f"Error with PostgreSQL: {e}")
    conn.rollback()

finally:
    # Закрыть курсор и соединение
    cursor.close()
    conn.close()
