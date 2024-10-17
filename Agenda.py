from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import arrow
import pytz
from os import system

def menu ():
    print("="*30)
    print("""
1 - CHECAR AGENDA
2 - ADCIONAR EVENTO
3 - EXCLUIR EVENTO
""")
    print("="*30)

def limpa ():
    system("cls||clear")

def data_horas ():
    agora = arrow.now('America/Sao_Paulo')
    data_formatada = agora.format('DD/MM/YYYY HH:mm:ss')
    return data_formatada

BD = create_engine("sqlite:///agendabd.bd")

Session = sessionmaker(bind=BD)
session = Session()

Base = declarative_base()

class Agenda(Base):
    __tablename__ = "agendas"
    data_atual = Column(String)
    evento = Column(String)

    def __init__(self, data_atual:str, evento:str):
        self.data_atual = data_atual
        self.evento = evento

Base.create_engine_all(bind=BD)

while True:
    while True:
        menu()
        menu_selec = int(input(": "))
        if menu_selec == 1 or 2 or 3:
            break
    match (menu_selec):
        case 1:
            datahoras = data_horas()
            for evento in lista_evento:
                print()
        case 2:
            datahoras = data_horas()

        case 3:

