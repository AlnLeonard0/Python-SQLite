from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from os import system
from time import sleep

system("cls||clear")

# Criando Banco de dados:
BD = create_engine("sqlite:///sistema_rh.db")

# Conectando ao banco de dados:
Session = sessionmaker(bind=BD)
session = Session()

# Criando Tabela e Classe:
Base = declarative_base()

class Funcionario(Base):
    __tablename__ = "funcionarios"
    
    nome = Column(String)
    sobrenome = Column(String)
    idade = Column(Integer)
    cpf = Column(String, primary_key=True)
    setor = Column(String)
    funcao = Column(String)
    salario = Column(Float)
    telefone = Column(String)
    sexo = Column(String)

    def __init__(self, nome: str, sobrenome: str, idade: int, cpf: str, setor: str, funcao: str, salario: float, telefone: str, sexo: str):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade                                                                                            
        self.cpf = cpf
        self.setor = setor
        self.funcao = funcao
        self.salario = salario
        self.telefone = telefone
        self.sexo = sexo                                     

# Criando tabela de dados, no banco de dados:
Base.metadata.create_all(bind=BD)

def menu_principal():
    limpar_tela()
    print("""   === RH System ===
        1 - Adicionar um funcionário
        2 - Consultar um funcionário
        3 - Atualizar os dados de um funcionário
        4 - Excluir um funcionário
        5 - Listar todos os funcionários
        0 - Sair do sistema.
        """)

def limpar_tela():
    system("cls||clear")
    sleep(1)

def logo_empresa():
    print("="*20)
    print(f"{'SENAI':^20}")
    print("="*20)

def verificar_cpf(cpf):
    return session.query(Funcionario).filter(Funcionario.cpf == cpf).first()

def add_funcionario():
    while True:
        cpf = input("Insira o CPF: ")
        if verificar_cpf(cpf):
            print("CPF já cadastrado. Tente novamente.")
        else:
            break
    
    funcionario = Funcionario(
        nome = input("Insira o nome: "),
        sobrenome = input("Insira o sobrenome: "),
        idade = int(input("Insira a idade: ")),
        cpf = cpf,
        setor = input("Insira o setor: "),
        funcao = input("Insira a função: "),
        salario = float(input("Insira o salário: ")),
        telefone = input("Insira o telefone: "),
        sexo = input("Insira o sexo (M/F): ").upper()
    )
    
    session.add(funcionario)
    session.commit()
    print("Funcionário adicionado com sucesso!")
    return funcionario

def pesquisa_funcionario(usuario_id):
    funcionario = session.query(Funcionario).filter(Funcionario.cpf == usuario_id).first()
    if not funcionario:
        print("Funcionário não encontrado.")
        return None
    return funcionario

def exibir_dados_funcionario(funcionario):
    print(f"Nome: {funcionario.nome} {funcionario.sobrenome}")
    print(f"Idade: {funcionario.idade}")
    print(f"CPF: {funcionario.cpf}")
    print(f"Setor: {funcionario.setor}")
    print(f"Função: {funcionario.funcao}")
    print(f"Salario: {funcionario.salario} R$")
    print(f"Telefone: {funcionario.telefone}")
    print(f"Sexo: {funcionario.sexo}")

def atualizar_dados(usuario_id, opcao2):
    funcionario = pesquisa_funcionario(usuario_id)
    if not funcionario:
        return

    match opcao2:
        case 1:
            funcionario.nome = input("Nome: ")
            funcionario.sobrenome = input("Sobrenome: ")
        case 2:
            funcionario.idade = int(input("Idade: "))
        case 3:
            novo_cpf = input("Novo CPF: ")
            if verificar_cpf(novo_cpf):
                print("CPF já cadastrado. Não é possível alterar.")
                return
            funcionario.cpf = novo_cpf
        case 4:
            funcionario.setor = input("Setor: ")
        case 5:
            funcionario.funcao = input("Função: ")
        case 6:
            funcionario.salario = float(input("Salario: "))
        case 7:
            funcionario.telefone = input("Telefone: ")
        case 8:
            funcionario.sexo = input("Sexo: ").upper()    
    
    session.commit()
    print("Dados atualizados com sucesso!")

def excluir_um_funcionario():
    cpf_funcionario = input("Informe o CPF do funcionário para ser excluído: ")
    funcionario = pesquisa_funcionario(cpf_funcionario)
    
    if funcionario:
        session.delete(funcionario)
        session.commit()
        print("Usuário excluído com sucesso.")
    else:
        print("Funcionário não encontrado.")

def listar_todos_funcionarios():
    lista_funcionarios = session.query(Funcionario).all()
    for funcionario in lista_funcionarios:
        exibir_dados_funcionario(funcionario)
        print("-" * 40)

# Execução do sistema
while True:
    menu_principal()
    opcao = int(input("Insira a opção desejada: "))
    if opcao in [1, 2, 3, 4, 5, 0]:
        match opcao:
            case 1:
                while True:
                    limpar_tela()
                    logo_empresa()
                    add_funcionario()
                    opcao1 = int(input("Deseja adicionar outro funcionário? \n1 - Sim\n2 - Não\nInsira a opção desejada: "))
                    if opcao1 == 2:
                        break
            case 2:
                limpar_tela()
                logo_empresa()
                cpf_funcionario = input("Informe o CPF do funcionário desejado: ")
                funcionario = pesquisa_funcionario(cpf_funcionario)
                if funcionario:
                    limpar_tela()
                    logo_empresa()
                    exibir_dados_funcionario(funcionario)
                sleep(5)
            case 3:
                limpar_tela()
                cpf_funcionario = input("Informe o CPF do funcionário que deseja atualizar: ")
                while True:
                    print("""Quais dados deseja atualizar:
1 - Nome
2 - Idade
3 - CPF
4 - Setor
5 - Função
6 - Salário
7 - Telefone
8 - Sexo""")
                    opcao2 = int(input("Insira a opção desejada: "))
                    if opcao2 in range(1, 9):
                        atualizar_dados(cpf_funcionario, opcao2)
                        opcao3 = input("Deseja atualizar outro dado? \n1 - Sim \n2 - Não\nInsira a opção desejada: ")
                        if opcao3 == "2":
                            break
                    limpar_tela()
            case 4:
                limpar_tela()
                logo_empresa()
                excluir_um_funcionario()
                sleep(2)
            case 5:
                limpar_tela()
                print("\nTodos os funcionários:")
                listar_todos_funcionarios()
                sleep(5)
            case 0:
                print("Saiu do sistema com sucesso.")
                sleep(1)
                break
    else:
        print("Opção inválida. Tente novamente.")
