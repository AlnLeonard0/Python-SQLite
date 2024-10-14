from sqlalchemy import create_engine, Column,String, Float, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from os import system
from time import sleep

#Definindo banco de dados
BD = create_engine("sqlite:///bancodedadosescolar.bd")

#Conectando ao banco de dados
Session = sessionmaker(bind=BD)
session = Session()

Base = declarative_base()

class Professor(Base):
    __tablename__ = "professores"

    #Definindo variaveis da tabela:
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome = Column("Nome", String)
    sobrenome = Column("Sobrenome", String)
    senha = Column("Senha", String)

    def __init__(self, nome: str, sobrenome: str, senha:str):
        self.nome = nome
        self.sobrenome = sobrenome
        self.senha = senha

class Aluno(Professor):
    __tablename__ = "alunos"

    #Definindo variaveis da SUB - Tabela
    matricula = Column("Matricula", Integer, primary_key=True, autoincrement=True)
    nome = Column("Nome", String)
    sobrenome = Column("Sobrenome", String)
    nota1 = Column("Nota I", Float)
    nota2 = Column("Nota II", Float)
    nota3 = Column("Nota III", Float)
    nota4 = Column("Nota IV", Float)
    professor_id = Column(Integer, ForeignKey('professores.id'))
    professor = relationship("Professor", back_populates="alunos")
    
    def __init__(self, nome: str, sobrenome: str, nota1: float, nota2:float, nota3:float,nota4):
        super().__init__(nome, sobrenome)
        self.nome = nome
        self.sobrenome = sobrenome
        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3
        self.nota4 = nota4
Professor.alunos = relationship("Aluno", order_by=Aluno.id, back_populates="professor")

Base.metadata.creat_all(bind=BD)

def limpa_tela():
    system("cls||clear")

def menu_professor():
    print("="*30)
    print("""
1 - CADASTRAR PROFESSOR
2 - FAZER LOGIN
3 - EXCLUIR PROFESSOR
          """)
    print("="*30)

def menu_aluno():
    print("="*30)
    print("""
1 - ADCIONAR ALUNO
2 - EDITAR NOTAS
3 - EXCLUIR ALUNO
""")
    print("="*30)

def criando_senha():
    while True:
        senha = int(input("Crie uma senha: "))
        senha1 = int(input("Digite a senha novamente: "))
        if senha == senha1:
            break
        print("As precisam ser iguais")
    return senha

while True:
    limpa_tela()
    while True:
        menu_professor()
        opcao = int(input(": "))
        if opcao == 1 or 2 or 3:
            break
    match (opcao):
        case 1:
            while True:
                prof = Professor(
                    nome = input("Nome: ").upper (),
                    sobrenome = input("Sobrenome: ").upper(),
                    senha= criando_senha()
                )
                session.add(prof)
                session.commit()
                prof = prof.id#Para receber o ID que foi gerado logo após ter sido adicionado
                print(f"ID DE REGISTRO: {prof.id}")
                print("""
DESEJA ADICIONAR OUTRO USUÁRIO ?
1- SIM
2- NÃO\n""")
                sleep(5)
                opcao0=int(input(": "))
                if opcao0 == 2:
                    break

