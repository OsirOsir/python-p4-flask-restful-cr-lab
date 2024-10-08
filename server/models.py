from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# Plant Model
class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    # Define the columns of the Plant model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Define which columns to serialize
    serialize_only = ('id', 'name', 'image', 'price')
