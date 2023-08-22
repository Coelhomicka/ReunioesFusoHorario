from pulp import *
import pytz
import pycountry
from datetime import datetime

# Coletar entrada do usuário
num_usuarios = int(input("Quantos usuários vão para a reunião (máximo 6): "))
if num_usuarios < 2 or num_usuarios > 6:
    print("Número inválido de usuários.")
    exit(1)

usuarios = []
for _ in range(num_usuarios):
    nome = input(f"Informe o nome do usuário {_ + 1}: ")
    pais_origem = input(f"Informe o país de origem para {nome}: ")
    opcoes_horario = input(f"Informe as opções de horário em comum para {nome} (ex: 9-12,14-16): ")
    usuarios.append((nome, pais_origem, opcoes_horario))


# Criar um dicionário para armazenar a disponibilidade de cada usuário
disponibilidade_usuarios = {}
for nome, _, _ in usuarios:
    disponibilidade_usuarios[nome] = [0] * 24

# Calcular a disponibilidade para cada usuário
for nome, _, opcoes_horario in usuarios:
    opcoes = opcoes_horario.split(',')
    for opcao in opcoes:
        inicio, fim = map(int, opcao.split('-'))
        for i in range(inicio, fim + 1):
            disponibilidade_usuarios[nome][i] = 1

# Criar o problema de Programação Linear
prob = LpProblem("AgendamentoDeReuniao", LpMaximize)

# Variáveis de decisão: x[i] = 1 se o intervalo de tempo i é escolhido
x = LpVariable.dicts("Intervalo", range(24), cat='Binary')

# Função objetivo: Maximizar a soma das variáveis de decisão
prob += lpSum([x[i] for i in range(24)]), "MaximizarSobreposicao"

# Restrições: Intervalos escolhidos devem estar disponíveis para todos os participantes
for i in range(24):
    for nome, _, _ in usuarios:
        prob += x[i] <= disponibilidade_usuarios[nome][i]

# Resolver o problema
prob.solve()

# Imprimir resultados
print("Status:", LpStatus[prob.status])
print("Horários escolhidos:")
for i in range(24):
    if x[i].value() == 1:
        print(f"Horário {i}:00 - {i + 1}:00")

print("Valor da Função Objetivo:", value(prob.objective))
