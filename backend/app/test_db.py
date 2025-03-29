from app import create_app, db
from models import Variety
from sqlalchemy import text  # ����������� text ��� ����� SQL-��������

app = create_app()

with app.app_context():
    try:
        print("Testing connection...")
        # ������� 1: ����� connection
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("OK: Connection successful. Result:", result.scalar())
        
        # ������� 2: ����� session
        # result = db.session.execute(text("SELECT 1"))
        # print("OK: Connection successful. Result:", result.scalar())
        
        print("\nTable structure:")
        inspector = db.inspect(db.engine)
        if 'varieties' in inspector.get_table_names():
            print([col['name'] for col in inspector.get_columns('varieties')])
        else:
            print("Table 'varieties' doesn't exist!")
        
        print("\nFirst 2 records:")
        if db.session.query(Variety).first():  # ��������, ��� ������� �� ������
            print(db.session.query(Variety.id, Variety.name_main).limit(2).all())
        else:
            print("No records found or table doesn't exist")
            
    except Exception as e:
        print("ERROR:", str(e))
        # �������������� �����������
        print("\nDebug info:")
        print("Tables in DB:", inspector.get_table_names())

