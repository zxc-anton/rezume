
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
from main import login, db


class rezume(UserMixin, db.Model):

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(100))
    citi: so.Mapped[str] = so.mapped_column(sa.String(50))
    user_number: so.Mapped[str] = so.mapped_column(sa.String(60), unique=True) 
    user_email: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True)
    salary: so.Mapped[int] = so.mapped_column()
    progrm_lang: so.Mapped[str] = so.mapped_column(sa.String(500))
    experience: so.Mapped[int] = so.mapped_column()
    body: so.Mapped[str] = so.mapped_column(sa.String(1000))
    remote_work: so.Mapped[str] = so.mapped_column(sa.String(6))
    status: so.Mapped[str] = so.mapped_column(sa.String(15))#no_checked = не просмотрено false = отказано true = разрешено


    def __repr__(self):
        return f'<User {self.username}>'


class Admin(UserMixin, db.Model):
    #login: banan pasw:123
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    login: so.Mapped[str] = so.mapped_column(sa.String(100))
    password: so.Mapped[str] = so.mapped_column(sa.String(400))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
    return db.session.get(Admin, int(id))
