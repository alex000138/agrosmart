import json
import psycopg2

# ���� � JSON-�����
file_path = r'C:\json_test_import.json'

# ����������� � PostgreSQL
conn = psycopg2.connect(
    dbname="agrosmart2",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

try:
    # �������� ��������� �������
    cursor.execute("""
    CREATE TEMP TABLE temp_json_data (
        json_data JSONB
    );
    """)
    conn.commit()

    print("Table temp_json_data created.")

    # ��������� � ������ JSON-����
    with open(file_path, 'r', encoding='utf-8') as file:
        # ���������, ����� ��� JSON-��������� � �����
        try:
            # ���������, ���� ���� �������� ������ JSON-��������
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
            # ���������, ���� ���� �������� ���� JSON-������ �� ������
            file.seek(0)  # ���������� ��������� ����� � ������
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

    # ��������� ���������
    conn.commit()

    print("Success.")

    # ��������� ���������� ������� � �������
    cursor.execute("SELECT COUNT(*) FROM temp_json_data;")
    count = cursor.fetchone()[0]
    print(f"Load {count} value in tables temp_json_data.")

    # ������� ������ 5 ������� ��� ��������
    cursor.execute("SELECT * FROM temp_json_data LIMIT 5;")
    rows = cursor.fetchall()
    print("First 5 value in table temp_json_data:")
    for row in rows:
        print(row)

except psycopg2.Error as e:
    print(f"Error with PostgreSQL: {e}")
    conn.rollback()

finally:
    # ������� ������ � ����������
    cursor.close()
    conn.close()
