class Player:

    def __init__(self, nome, idade, peso, vivo):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.vivo = vivo

    def mostrar_dados(self):
        print("nome: " + self.nome, "idade: " + self.idade, "peso: " + self.peso, self.vivo)

# player1 = Player("nicholas", 21, 124, True) OBJETO 1
# player2 = Player("Edelcio", 48, 78, False) OBJETO 2
# player1.mostrar_dados()
# player2.mostrar_dados()
