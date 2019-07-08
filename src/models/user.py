import bcrypt

from .base import BaseModel
from ..core import db
from ..utils import Generator


class User(db.Model, BaseModel):
    __tablename__ = "user"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.Text, nullable=True)

    # relationships
    rel_favorite_movies = db.relationship("FavoriteMovie", cascade="all, delete-orphan", backref="rel_user",
                                          lazy="joined")

    def __init__(self, name, email, password, **kwargs):
        super(User, self).__init__(**kwargs)
        """ Create a new User """
        self.name = name
        self.email = email
        self._password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.avatar_url = kwargs.get("avatar_url", Generator.gravatar_url(self.email))

    def __repr__(self):
        return "User::{}".format(self.id)

    def check_password(self, password: str):
        return bcrypt.checkpw(password=password.encode(), hashed_password=self._password.encode())


class FavoriteMovie(db.Model, BaseModel):
    __tablename__ = "favorite_movie"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"))
    imdb_movie_id = db.Column(db.String(20), nullable=False, index=True)

    def __init__(self, user_id, imdb_id):
        super(FavoriteMovie, self).__init__()
        self.user_id = user_id
        self.imdb_movie_id = imdb_id
