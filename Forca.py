from random import choice
from os import system

def limpar_tela():
    system("cls||clear")

palavras = ["ELEFANTE","GOLFINO","FOCA","LEÃO",'TARTARUGA','JAGUATIRICA','ONÇA','GIRAFA','TIGRE','BALEIA' ]
palavra = choice(palavras)
qtd_letra = len(palavra)
chute = []

print(f"A PALAVRA TEM {qtd_letra} LETRAS\n")
for i in range (0,qtd_letra):
    letra = input("INFORME A LETRA: ").upper()
    if letra in palavra:
        posicao=palavra.index(letra)
        print(f"A LETRA {letra} ESTÁ NA POSIÇÃO {posicao+1}")
    chute.append(letra)
for letra in chute:
    print("\n",letra, end=" ")
print("QUAL A PALAVRA ?")
palavra_final = input("").upper()
if palavra_final == palavra:
    print(f"VOCÊ ACERTOU")
else:
    print(f"VOCÊ ERROU, A PALAVRA É CERTA É {palavra}")
    