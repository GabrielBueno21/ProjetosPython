# Importando algumas bibliotecas

import random
import sqlite3
import math
import numpy as np


# Definindo a classe Adivinha

class Adivinha():

    def __init__(self, limite_inf = 0, limite_sup = 100):
        # Fazendo um if para previnir caso o usuário digite os limites em ordens trocadas

        if limite_inf < limite_sup: # Caso o usuário tenha digitado os limites na ordem contrária, faz a correção
            self.limite_inf = limite_inf
            self.limite_sup = limite_sup
        else:
            self.limite_inf = limite_sup
            self.limite_sup = limite_inf
        self.aleatorio = random.randint(self.limite_inf, self.limite_sup) #cria um número aleatório
        self.tentativas = 0 # quantidade de tentativas do usuário
        self.max_tentativas = int(np.ceil(math.log(self.limite_sup - self.limite_inf + 1, 2))) # quantidade de de tentativas máximas
        self.acerto = 0 # variável que define se o usuário acertou ou não / Inicialmente recebe 0 - Serve como uma variável de controle

    # Comparando o número digitado pelo usuário com o número aleatóro gerado
    def compara_numeros(self, numero):
        if self.aleatorio == numero:
            self.tentativas += 1
            self.acerto = 1 #Caso o usuário tenha acertado, acerto vale 1
        elif numero > self.aleatorio:
            print('Você chutou muito alto!')  # Dá dicas ao usuário sobre como andam os chutes caso o valor for MAIOR que o valor aleatório
            self.tentativas += 1
        else:
            print('Você chutou muito baixo!') # Dá dicas ao usuário sobre como andam os chutes caso o valor for MENOR que o valor aleatório
            self.tentativas += 1
    def mensagem_derrota(self):
        print('Eu lamento ! Você perdeu, mas vamos tentar mais uma vez?!')

    def mensagem_vitoria(self):
        print('Parabéns! Você acertou! Foram {} tentativa(s) até aqui!'.format(self.tentativas))

class Banco_dados():
    # Criando uma conexão com o banco de dados bd_game_advin sempre que um objeto da classe Banco_dados for criado
    def __init__(self):
        self.conn = sqlite3.connect('bd_game_advin.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS logs_jogos
                    (id_jogo INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    numero_aleatorio INTEGER NOT NULL,
                    tentativas INTEGER NOT NULL,
                    max_tentativas INTEGER NOT NULL,
                    vitoria INT(1) NOT NULL)
            '''
        self.c.execute(sql)

    def insere_dados(self, numero_aleatorio,tentativas, max_tentativas, vitoria):
        sql = '''INSERT INTO logs_jogos (numero_aleatorio,tentativas,max_tentativas,vitoria)
        VALUES({},{},{},{})
        '''.format(numero_aleatorio, tentativas, max_tentativas, vitoria)

        self.c.execute(sql)
        self.conn.commit()
        self.c.close()
        self.conn.close()




# Imprime boas vindas
print('*'*100)
print(' '*34 + 'Bem vindo ao jogo da adivinhação' + ' '*34)
print('*'*100)

# Pergunta ao usuário se ele deseja jogar
jogar = str(input('Deseja jogar o jogo da adivinhação (S/N)? '))

# Garantindo que mesmo que o usuário digite 'S' ou 's', não irá afetar o resultado do programa
while (jogar.lower() == 's'):
    lim_inf = int(input('Digite o limite inferior para o possível número que será gerado:'))
    lim_sup = int(input('Digite o limite superior para o possível número que será gerado:'))

    obj = Adivinha(lim_inf, lim_sup) #cria o objeto da Classe Adivinha

    print(obj.aleatorio)
    while obj.tentativas < obj.max_tentativas: #Enquanto o número de tentativas não for igual ao número máximo, o usuário pode chutar
        try:
            chute = int(input('Chute um número: '))
        except:
            print('Você digitou um número inválido e perdeu uma tentativa!') #Caso o usuário digite uma letra ou algo que não seja um inteiro, ocorre uma exceção
            obj.tentativas += 1
            continue
        else:
            obj.compara_numeros(chute) #Se o chute for feito com um inteiro, faz a comparação dos números
        finally:
            if obj.acerto == 1:  # Se o usuário tiver êxito, então imprime a mensagem de vitória
                obj.mensagem_vitoria()
                break

    if obj.acerto == 0:
        obj.mensagem_derrota()

    dados = Banco_dados()
    dados.insere_dados(obj.aleatorio, obj.tentativas, obj.max_tentativas, obj.acerto)

    jogar = str(input('Deseja jogar novamente (S/N)? '))







