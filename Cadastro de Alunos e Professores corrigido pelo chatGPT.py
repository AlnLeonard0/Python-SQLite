from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from os import system
from time import sleep

# Definindo banco de dados
BD = create_engine("sqlite:///bancodedadosescolar.bd")

# Conectando ao banco de dados
Session = sessionmaker(bind=BD)
session = Session()

Base = declarative_base()

class Professor(Base):
    __tablename__ = "professores"

    # Definindo variáveis da tabela
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome = Column("Nome", String)
    sobrenome = Column("Sobrenome", String)
    senha = Column("Senha", String)

    def __init__(self, nome: str, sobrenome: str, senha: str):
        self.nome = nome
        self.sobrenome = sobrenome
        self.senha = senha

    # Relacionamento com Alunos
    alunos = relationship("Aluno", back_populates="professor")

class Aluno(Base):
    __tablename__ = "alunos"

    # Definindo variáveis da tabela
    matricula = Column("Matricula", Integer, primary_key=True, autoincrement=True)
    nome = Column("Nome", String)
    sobrenome = Column("Sobrenome", String)
    professor_id = Column(Integer, ForeignKey('professores.ID'))  # Chave estrangeira para 'professores'

    # Notas associadas ao aluno
    notas = relationship("Nota", back_populates="aluno")

    def __init__(self, nome: str, sobrenome: str, professor_id: int):
        self.nome = nome
        self.sobrenome = sobrenome
        self.professor_id = professor_id  # Atribuindo professor_id

class Nota(Base):
    __tablename__ = "notas"

    # Definindo variáveis da tabela
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID para identificar cada nota
    nota1 = Column("Nota I", Float)
    nota2 = Column("Nota II", Float)
    nota3 = Column("Nota III", Float)
    nota4 = Column("Nota IV", Float)
    matricula_aluno = Column(Integer, ForeignKey('alunos.Matricula'))  # Chave estrangeira para 'alunos'

    aluno = relationship("Aluno", back_populates="notas")

    def __init__(self, nota1: float, nota2: float, nota3: float, nota4: float, matricula_aluno: int):
        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3
        self.nota4 = nota4
        self.matricula_aluno = matricula_aluno  # Atribuindo a matrícula do aluno

# Código para criar as tabelas no banco de dados
if __name__ == "__main__":
    Base.metadata.create_all(bind=BD)  # Cria as tabelas no banco de dados

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
                prof = prof.id #Para receber o ID que foi gerado logo após ter sido adicionado
                print(f"ID DE REGISTRO: {prof}")
                print("""
DESEJA ADICIONAR OUTRO PROFESSOR ?
1- SIM
2- NÃO\n""")
                sleep(5)
                opcao0=int(input(": "))
                if opcao0 == 2:
                    break
        case 2:
            while True:
                prof_id=int(input("INFORME SEU NUMERO ID PARA CONTINUAR: "))
                prof = session.query(Professor).filter(Professor.id == prof_id).first()
                prof_senha = input("Senha: ")
                if prof_senha == prof.senha:
                    limpa_tela()
                    print("="*40)
                    print(f"SEJA BEM VINDO {prof.nome} {prof.sobrenome}")
                    print("="*40)
                    menu_aluno()
                    while True:
                        opcao1=int(input(": "))
                        if opcao1 == 1 or 2 or 3:
                            break
                    match (opcao1):
                        case 1:
                            aluno = Aluno(
                                nome = input("Nome: "),
                                sobrenome = input("Sobrenome: "),
                                professor_id = prof_id 
                            )
                            session.add(aluno)
                            session.commit()
                            print("Aluno salvo com sucesso")
