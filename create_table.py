from models import *
import database
import os

 
if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
        Base.metadata.create_all(database.engine)
 
    admin = User(username='admin', password='fastapi', mail='sample@example.com')
    database.session.add(admin)
    database.session.commit()
 
    task = Task(
        user_id=admin.id,
        content='deadline',
        priority=Priority.a.value,
        category=Category.daily.value,
        deadline=datetime(2021, 12, 25, 12, 00, 00),
    )
    print(task)
    database.session.add(task)
    database.session.commit()
 
    database.session.close()
