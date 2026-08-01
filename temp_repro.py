from aitexttosqlengine.db import DatabaseManager
import os

url = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/dvdrental'
db = DatabaseManager(url)
try:
    db.initialize_schema()
    print('schema ok')
    db.seed_data()
    print('seed ok')
except Exception as e:
    import traceback
    traceback.print_exc()
    print('ERROR:', repr(e))
finally:
    db.close()
