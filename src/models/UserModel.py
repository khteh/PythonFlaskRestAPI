from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from .BlogModel import BlogSchema
class UserModel(db.Model):
    """
    User Model
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=True)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    blogs = db.relationship("BlogModel", backref="users", lazy=True)
    # Class constructor
    def __init__(self, data):
        """
        Class Constructor
        """
        self.firstname = data.get("firstname")
        self.lastname = data.get("lastname")
        self.email = data.get("email")
        self.phone = data.get("phone")
        self.password = self.__generate_hash(data.get("password"))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
    def save(self):
        db.session.add(self)
        db.session.commit()
    def update(self, data):
        for key, item in data.items():
            if key == "password":
                self.password = self.__generate_hash(value)
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)
    @staticmethod
    def get_user(id):
        return UserModel.query.get(id)
    @staticmethod
    def get_user_by_email(email):
        return UserModel.query.filter_by(email=email).first()
    @staticmethod
    def get_users():
        return UserModel.query.all()
    def __repl__(self): # return a printable representation of UserModel object, in this case we're only returning the id
        return "<id {}>".format(self.id)
class UserSchema(Schema):
    """
    User Schema
    """
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=False)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    blogs = fields.Nested(BlogSchema, many=True)