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

    # Relacionamento com Professor
    professor = relationship("Professor", back_populates="alunos")

    # Relacionamento com Notas
    notas = relationship("Nota", back_populates="aluno", cascade="all, delete, delete-orphan")

    def __init__(self, nome: str, sobrenome: str, professor_id: int):
        self.nome = nome
        self.sobrenome = sobrenome
        self.professor_id = professor_id  # Atribuindo professor_id


class Nota(Base):
    __tablename__ = "notas"

    # Definindo variáveis da tabela
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID para identificar cada nota
    nota1 = Column("Nota I", Float)  # Definindo a coluna corretamente
    matricula_aluno = Column(Integer, ForeignKey('alunos.Matricula'))  # Chave estrangeira para 'alunos'

    # Relacionamento com Aluno
    aluno = relationship("Aluno", back_populates="notas")


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
2 - EDITAR NOTAS E CALCULAR MEDIA
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

def media (notas):
    qtd = len(notas)
    total = sum(notas)
    med = total/qtd
    return med

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

                        case 2:
                            lista_notas = []
                            matricula_alun =input("MATRICULA DO ALUNO: ")
                            alun = session.query(Aluno).filter(Aluno.matricula == matricula_alun).first()
                            notas=Nota(
                                nota1 = float(input("Nota I: ")),
                                nota2 = float(input("Nota II: ")),
                                nota3 = float(input("Nota III: ")),
                                nota4 = float(input("Nota IV: ")),
                                matricula_aluno = matricula_alun
                            )
                            lista_notas.append(notas)
                            media_notas = media(lista_notas)
                            print(f"A MEDIA É: {media_notas}")