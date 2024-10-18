from os import system
from time import sleep
from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

BD = create_engine("sqlite:///Servidor_pagamenos.db")

Session = sessionmaker(bind=BD)
session = Session()

Base = declarative_base()

class Trabalhador(Base):
    __tablename__ = "trabalhadores"

    id = Column(Integer, autoincrement=True, primary_key=True)
    valor = Column(Float)
    nome = Column(String)
    senha = Column(String)
    
    
