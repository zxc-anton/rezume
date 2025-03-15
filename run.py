import sqlalchemy as sa
import sqlalchemy.orm as so
from main import application, db

if __name__ == '__main__':
    with application.app_context():
       db.create_all()
    application.run(host='0.0.0.0')