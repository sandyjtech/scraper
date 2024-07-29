from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import db, bcrypt

# Models go here!
class ScoreCard(db.Model, SerializerMixin):
 __tablename__ ="scorecards"
 id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)   
     
