
from app import db
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Time,Boolean


class TelModel(db.Model):
    __tablename__ = "telefones"

    id          = Column(Integer,primary_key=True)
    numero      = Column(String,unique=True,nullable=False)
    status   = Column(Boolean,nullable=False)

    def __init__(self,numero,status):
        self.numero     = numero
        self.status  = status

    def __repr__(self):
        return "<Tel %r>" % self.id
