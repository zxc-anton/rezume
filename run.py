import sqlalchemy as sa
import sqlalchemy.orm as so
from main import app, db

#$env:FLASK_APP = "run.py"
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so}
if __name__ == '__main__':
    with app.app_context():
       db.create_all()
    app.run(debug=True)