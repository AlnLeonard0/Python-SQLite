from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base 
from os import system
from time import sleep
system("cls||clear")

dados = []
#Criando Banco de dados:
BD = create_engine("sqlite:///bancodedados.db")

#Conectando ao banco de dados:
Session = sessionmaker(bind=BD)
session = Session()

#Criando Tabela e Classe:
Base = declarative_base()

class Pessoa(Base):
    __tablename__ = "usuarios"
    
    #Definindo variaveis da tabela:
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("Nome", String)
    sobrenome = Column("Sobrenome", String)
    idade = Column("Idade", Integer)
    peso = Column("Peso", Float)
    altura = Column("Altura", Float)
    sexo = Column("Sexo", String)
    #Duvida: Como fazer para declarar sub classes. 
    #Ex: Professor > Alunos > Pais
    #E como fazer para acessar elas através da classe principal "Professor"

    #Definindo atributos da classe:
    def __init__(self,nome:str, sobrenome:str, idade:int,peso:float,altura:float,sexo:str):
        self.nome = nome
        self.sobrenome=sobrenome
        self.idade=idade
        self.peso=peso
        self.altura=altura
        self.sexo=sexo

#Criando tabela de dados, no banco de dados:
Base.metadata.create_all(bind=BD)    

#Funções:
def menu_principal ():
    print("="*40)
    print(f"{"MENU":^40}")
    print("="*40)
    print(f"""
1- ADICIONAR USUÁRIO
2- CALCULAR IMC
3- TAXA METABOLICA BASAL
4- PERCENTUAL DE GORDURA
5- PESO IDEAL (FORMULA DIVINE)
6- DELETAR USUÁRIO
7- MOSTRAR TODOS OS USUARIOS CADASTRADOS
          """)

def imc (altura:float, peso:float):
    imc = peso/(altura*altura)
    return imc

def verificando_imc(imc):
    if imc < 18.5:
        print("Abaixo do peso")
    elif imc < 24.9:
        print("Peso normal")
    elif imc < 29.9:
        print("Sobrepeso")
    else:
        print("Obesidade")

def tax_metabolica(sexo,peso,idade,altura):
    if sexo == "MULHER" or sexo == "FEMININO":
        TMB_M = 447.6 + (9.2*peso)+(3.1*(altura*100))-(4.3*idade)
        return TMB_M
    else:
        TMB_H=88.36 + (13.4*peso) + (4.8*(altura*100))-(5.7*idade)
        return TMB_H
    
def percentual_gordura (imc,idade,sexo):
    
    if sexo == "MULHER" or sexo == "FEMININO":
        percentual_mulheres = (1.20*imc)+(0.23*idade)-5.4
        return percentual_mulheres
    else:
        percentual_homens =(1.20*imc)+(0.23*idade)-16.2
        return percentual_homens
    
def peso_ideal(altura,sexo):
    if sexo == "MULHER" or sexo == "FEMININO":
        peso_ideal_mulheres = 45.5+2.3*(((altura*100)/2.54)-60)
        return peso_ideal_mulheres
    else:
        peso_ideal_homens =50+2.3*(((altura*100)/2.54)-60)
        return peso_ideal_homens

#Coletando dados:
while True:
    system("cls||clear")
    menu_principal()
    opcao1=int(input(":"))
    match (opcao1):
        case 1:
            while True:
                system("cls||clear")
                #Dados para salvamento:
                usuario = Pessoa(
                    nome=input("Nome: ").lower(),
                    sobrenome=input("Sobrenome: ").lower(),
                    idade=int(input("Idade: ")),
                    peso=float(input("Peso: ")),
                    altura=float(input("Altura: ")),
                    sexo=input("Sexo (Feminino/Masculino): ").lower()
                )
                #Salvando Usuário que adicionar os dados:
                session.add(usuario)
                session.commit()
                usuario_id = usuario.id#Para receber o ID que foi gerado logo após ter sido adicionado
                print(f"ID DE REGISTRO: {usuario_id}")
                print("""
DESEJA ADICIONAR OUTRO USUÁRIO ?
1- SIM
2- NÃO\n""")
                sleep(5)
                opcao0=int(input(": "))
                if opcao0 == 2:
                    break
        case 2:
            system("cls||clear")
            print("="*40)
            print(f"{"CACULADORA DE IMC":^40}")
            print("="*40)
            usuario_id=int(input("INFORME SEU NUMERO ID PARA CONTINUAR: "))
            usuario = session.query(Pessoa).filter(Pessoa.id == usuario_id).first()#Método de pesquisa detalhada, adcionando com filtro o ID gerado
            #Após utilizando usuario especifico com base o ID chamado:
            resultado = imc(usuario.altura,usuario.peso)
            print(f"ID DIGITADO: {usuario.id}")
            print(f"Nome: {usuario.nome} {usuario.sobrenome}")
            print(f"SEU IMC: {resultado:.2f}")
            verificando_imc(resultado)
            print(f"Peso: {usuario.peso}Kg")
            print(f"Altura: {usuario.altura}m")
            print(f"Idade: {usuario.idade}")
            sleep(10)
        case 3:
            system("cls||clear")
            print("="*40)
            print(f"{"TAXA METABOLICA BASAL":^40}")
            print("="*40)
            usuario_id=int(input("INFORME SEU NUMERO ID PARA CONTINUAR: "))
            usuario = session.query(Pessoa).filter(Pessoa.id == usuario_id).first()
            resultado=tax_metabolica(usuario.sexo,usuario.peso,usuario.idade,usuario.altura)
            print(f"ID DIGITADO: {usuario.id}")
            print(f"Nome: {usuario.nome} {usuario.sobrenome}")
            print(f"SEU TAXA METABOLICA BASAL: {resultado:.2f} kcal/dia")
            print(f"Peso: {usuario.peso}Kg")
            print(f"Altura: {usuario.altura}m")
            print(f"Idade: {usuario.idade}")
            sleep(10)
        case 4:
            system("cls||clear")
            print("="*40)
            print(f"{"PERCENTUAL DE GORDURA":^40}")
            print("="*40)
            usuario_id=int(input("INFORME SEU NUMERO ID PARA CONTINUAR: "))
            usuario = session.query(Pessoa).filter(Pessoa.id == usuario_id).first()
            resultado=percentual_gordura((imc(usuario.altura,usuario.peso)),usuario.idade,usuario.sexo)
            print(f"ID DIGITADO: {usuario.id}")
            print(f"Nome: {usuario.nome} {usuario.sobrenome}")
            print(f"PERCENTUAL DE GORDURA: {resultado:.2f} %")
            print(f"Peso: {usuario.peso}Kg")
            print(f"Altura: {usuario.altura}m")
            print(f"Idade: {usuario.idade}")
            sleep(10)
        case 5:
            system("cls||clear")
            print("="*40)
            print(f"{"PESO IDEAL (DIVINE FORMULA)":^40}")
            print("="*40)
            usuario_id=int(input("INFORME SEU NUMERO ID PARA CONTINUAR: "))
            usuario = session.query(Pessoa).filter(Pessoa.id == usuario_id).first()
            resultado=peso_ideal(usuario.altura, usuario.sexo)
            print(f"ID DIGITADO: {usuario.id}")
            print(f"Nome: {usuario.nome} {usuario.sobrenome}")
            print(f"PESO IDEAL: {resultado:.2f} Kg")
            print(f"Peso: {usuario.peso}Kg")
            print(f"Altura: {usuario.altura}m")
            print(f"Idade: {usuario.idade}")
            sleep(10)
        case 6:
            id_usuario = int(input("INFORME O ID DO USUÁRIO QUE DESEJA DELETAR: "))
            usuario = session.query(Pessoa).filter_by(id = id_usuario).first()
            session.delete(usuario)
            session.commit()
            print(f"{usuario.nome} excluido com sucesso.")
            sleep(10)
        case 7:
            lista_usuarios = session.query(Pessoa).all()
            for usuario in lista_usuarios:
                print(f"{usuario.id} - {usuario.nome} {usuario.sobrenome}")
            sleep(10)