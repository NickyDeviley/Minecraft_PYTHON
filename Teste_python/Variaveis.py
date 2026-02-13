nome = "Nicholas" #Variável string nome
idade = 21 #Variável int idade
peso = 122 #variável int peso
pi = 3.14 #variável float pi
pi_dois = 3.141592 #variável double pi
vivo = True #variável bool vivo
posicao = (200, 50, 30) #vetor de valores inteiros

def qual_sua_idade(): #função em python é declarada com def

    idade = int(input("digite sua idade: ")) #o comando "input" é para receber um valor do usuário

    if idade < 20: # if
        print("Você tem menos de vinte anos!") #Print para imprimir
    elif idade >= 20: # else if
        print("você tem vinte ou mais!")
    else: # else
        print("não sei sua idade!")

while nome == "Nicholas":
    qual_sua_idade()