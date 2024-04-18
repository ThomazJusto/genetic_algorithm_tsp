import math
import random
from dataset import berlin52, eil51, pr152, rat99

#objeto cidade
class ponto:
    def __init__(self, id, x, y):
        self.x = float(x)
        self.y = float(y)
        self.id = int(id)

def gerador_de_lista_de_objetos_pontos(lista):
    data = []
    for item in lista:
        id, x, y = item
        data.append(ponto(id=id, x=x, y=y))
    return data

#fitness de uma lista de pontos (consideramos a ordem dos pontos na lista como a ordem de conexao entre cada um)
def fitness(lista_de_pontos_no_mapa):
    
    custo_total = 0.0
    num_pontos = len(lista_de_pontos_no_mapa)
    
    for i in range(1, num_pontos):
        ponto_atual = lista_de_pontos_no_mapa[i-1]
        proximo_ponto = lista_de_pontos_no_mapa[(i)]
        custo_total += calcular_distancia(ponto_atual, proximo_ponto)
    custo_total += calcular_distancia(lista_de_pontos_no_mapa[len(lista_de_pontos_no_mapa)-1], lista_de_pontos_no_mapa[0])
        
    return custo_total

def calcular_distancia(p1, p2):
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

# FUNCAO DE SELECAO 1(ELISTISMO -> SELECIONA O MELHOR DA LISTA QUE RECEBEU)
# elitismo (recebe uma lista de mapas, ou seja, a posicao 0 conterá uma lista de pontos). Por isso utilizamos a funcao fitness para calculo de custo em cada iteracao
# exemplo de estrutura que sera recebida: (ponto = objeto)
# [
#    [ponto, ponto, ponto...],
#    [ponto, ponto, ponto...],
#    [ponto, ponto, ponto...]
#    ...
#]
def selecao(lista_de_direcoes):
    custo = 9999999999999999999999999999.00
    selecionado = []
    for i in (lista_de_direcoes):
        parametro = fitness(i)
        if parametro < custo:
            selecionado = i
            custo = parametro
    return selecionado

# FUNCAO DE SELECAO 2(TORNEIO -> SELECIONA UM ALEATORIO DA LISTA QUE RECEBEU)
def selecao_torneio(lista_de_direcoes):
    return lista_de_direcoes[random.randint(0, len(lista_de_direcoes))-1]

# FUNCAO DE SELECAO CUSTOMIZADA 3(SELECIONA O 1 MELHOR E O SEGUNDO MELHOR E RETORNA OS DOIS NA MESMA CHAMADA)
def selecao_dois_melhores(lista_de_direcoes):
    lista_de_direcoes_auxiliar = lista_de_direcoes.copy()

    selecionado1 = selecao(lista_de_direcoes_auxiliar)
    lista_de_direcoes_auxiliar.remove(selecionado1)

    selecionado2 = selecao(lista_de_direcoes_auxiliar)
    lista_de_direcoes_auxiliar.remove(selecionado2)
    
    return selecionado1, selecionado2

def geracao_de_caminho_randomico(lista_de_pontos):
    nova_ordem = lista_de_pontos[:]  # Cria uma cópia da lista original
    random.shuffle(nova_ordem)  # Embaralha a nova lista
    return nova_ordem

# FUNCAO DE MUTACAO 1(MUTACAO DO TIPO SWAP ALEATORIO)
def mutate(lista_de_pontos):
    # Seleciona aleatoriamente um índice válido na lista
    indice_aleatorio = random.randint(0, len(lista_de_pontos) - 1)
    
    # Seleciona aleatoriamente outro índice diferente do primeiro
    novo_indice_aleatorio = random.randint(0, len(lista_de_pontos) - 1)
    while novo_indice_aleatorio == indice_aleatorio:
        novo_indice_aleatorio = random.randint(0, len(lista_de_pontos) - 1)
    
    # Troca os pontos de posição
    lista_de_pontos[indice_aleatorio], lista_de_pontos[novo_indice_aleatorio] = lista_de_pontos[novo_indice_aleatorio], lista_de_pontos[indice_aleatorio]

    return lista_de_pontos
    #retorna [ponto, ponto, ponto...]

# FUNCAO DE MUTATE 2(MUTACAO DO TIPO INVERSAO)
def mutate2(lista_de_pontos):
    nova_lista_de_pontos = lista_de_pontos.copy()  # Copia a lista original para não modificar a original

    # Escolhe aleatoriamente dois índices diferentes na lista de pontos
    indice1 = random.randint(0, len(nova_lista_de_pontos) - 1)
    indice2 = random.randint(0, len(nova_lista_de_pontos) - 1)
    while indice1 == indice2:
        indice2 = random.randint(0, len(nova_lista_de_pontos) - 1)

    # Garante que indice1 seja menor que indice2
    if indice1 > indice2:
        indice1, indice2 = indice2, indice1

    # Inverte a ordem dos pontos entre os índices escolhidos
    nova_lista_de_pontos[indice1:indice2 + 1] = reversed(nova_lista_de_pontos[indice1:indice2 + 1])

    return nova_lista_de_pontos

# FUNÇÃO DE CRUZAMENTO 1 (N-POINT STYLE)
def crossover(lista_de_pontos1, lista_de_pontos2):
    nova_lista = []
    genes_utilizados = set()  # Conjunto para armazenar os genes já utilizados

    # Adiciona os pontos de lista_de_pontos1 até o ponto de crossover
    random_number = random.randint(0, len(lista_de_pontos2))
    for i in range(0, random_number):
        ponto = lista_de_pontos1[i]
        if ponto not in nova_lista:
            nova_lista.append(ponto)
            genes_utilizados.add(ponto)

    # Adiciona os pontos de lista_de_pontos2 que não estão na nova lista
    i=0
    while len(nova_lista) < len(lista_de_pontos2):
        ponto = lista_de_pontos2[i]
        if ponto not in genes_utilizados:
            nova_lista.append(ponto)
            genes_utilizados.add(ponto)
        i = i + 1 

    return nova_lista

# FUNÇÃO DE CRUZAMENTO 2 (DOUBLE POINT STYLE)
def crossover_doublepoint(lista_de_pontos1, lista_de_pontos2):
    nova_lista = []
    genes_utilizados = set()
    
    # Seleciona aleatoriamente dois pontos de corte
    corte1 = random.randint(0, len(lista_de_pontos1) - 1)
    corte2 = random.randint(corte1 + 1, len(lista_de_pontos1))

    # Troca os segmentos entre os dois pontos de corte
    i=0
    while len(nova_lista) < corte1:
        if lista_de_pontos1[i] not in genes_utilizados:
            nova_lista.append(lista_de_pontos1[i])
            genes_utilizados.add(lista_de_pontos1[i])
        i = i +1

    i=0
    while len(nova_lista) < corte2:
        if lista_de_pontos2[i] not in genes_utilizados:
            nova_lista.append(lista_de_pontos2[i])
            genes_utilizados.add(lista_de_pontos2[i])
        i = i +1

    i=0
    while len(nova_lista) < len(lista_de_pontos2):
        if lista_de_pontos1[i] not in genes_utilizados:
            nova_lista.append(lista_de_pontos1[i])
            genes_utilizados.add(lista_de_pontos1[i])
        i = i +1

    return nova_lista
    

# FUNÇÃO DE CRUZAMENTO ESTADO DA ARTE 3
# UM OPERADOR DE CRUZAMENTO EFICIENTE PARA O PROBLEMA DO CAIXEIRO VIAJANTE
def crossover_perfect(lista_de_pontos1, lista_de_pontos2):
    offspring = []

    # Step 1: Choose initial city randomly
    initial_city = random.choice(lista_de_pontos1)
    offspring.append(initial_city)

    visited_cities = set([initial_city.id])

    while len(offspring) < len(lista_de_pontos1):
        current_city = offspring[-1]
        index1 = lista_de_pontos1.index(current_city)
        index2 = lista_de_pontos2.index(current_city)

        # Find the nearest unvisited city
        min_distance = float('inf')
        nearest_city = None
        for index, lista_de_pontos in [(index1, lista_de_pontos1), (index2, lista_de_pontos2)]:
            for i in range(1, len(lista_de_pontos)):
                next_city = lista_de_pontos[(index + i) % len(lista_de_pontos)]
                if next_city.id not in visited_cities:
                    distance = calcular_distancia(current_city, next_city)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_city = next_city

        # Add the nearest unvisited city to offspring
        if nearest_city not in offspring:
            offspring.append(nearest_city)
            visited_cities.add(nearest_city.id)

    return offspring


def distinct_check(lista_de_pontos, valor_soma):
    soma = 0

    for i in range(len(lista_de_pontos)):
        soma += lista_de_pontos[i].id
    
    if soma == valor_soma:
        return True
    return False

def fitness_threshold(fitness, fn_thres, population):
    if not fn_thres:
        return None

    fittest_individual = min(population, key=fitness)
    if fitness(fittest_individual) <= fn_thres:
        return fittest_individual

    return None

def impressao_solucao(data):
    for i in range(len(data) - 1):
        distancia = calcular_distancia(data[i], data[i+1])
        print(f"ID: {data[i].id}, Distância até próximo ponto: {distancia}")
    
    # Imprimindo o último ponto
    print(f"ID: {data[-1].id}, Distância até próximo ponto: Último ponto da lista")
    print(f"Pontos unicos: {ids_unicos(data)}!!!")
    print(f"Tamanho da lista: {len(data)}!!!")
    print(f"Custo total: {fitness(data)}!!!")

def ids_unicos(data):
    ids = set()
    for ponto in data:
        if ponto.id in ids:
            return False
        else:
            ids.add(ponto.id)
    return True

def escrever_em_arquivo(lista, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for i, elemento in enumerate(lista):
            arquivo.write(f'Posição {i+1}: {elemento}\n')

def algoritmo_genetico_completo(operador_selecao, operador_mutacao, operador_cruzamento, quantidade_inicial_populacao, quantidade_de_geracoes, taxa_de_mutacao, dataset, fitness_thresh=None):
    # Antes de tudo, vamos criar uma lista com objetos pontos, que foi a lista teste passada. 
    # O parametro 'data' é exatamente uma lista de pontos (NAO objetos)

    data_sample = gerador_de_lista_de_objetos_pontos(dataset)

    # Criar uma lista de tamanho caminhos_randomicos_quantidade, contendo listas de pontos, baseado no sample que temos
    data_population = []
    for i in range(quantidade_inicial_populacao):
        data_population.append(geracao_de_caminho_randomico(data_sample))

    for i in range(quantidade_de_geracoes):
        new_population = []

        for i in range(quantidade_inicial_populacao):
            if(operador_selecao == 1):
                pai = selecao(data_population)
                mae = selecao(data_population)
            elif(operador_selecao == 2):
                pai = selecao_torneio(data_population)
                mae = selecao_torneio(data_population)
            elif(operador_selecao == 3):
                pai, mae = selecao_dois_melhores(data_population)

            if(operador_cruzamento == 1):
                crianca = crossover(pai, mae)
            elif(operador_cruzamento == 2):
                crianca = crossover_doublepoint(pai, mae)
            elif(operador_cruzamento == 3):
                crianca = crossover_perfect(pai, mae)

            if(operador_mutacao == 1):
                if random.random() <= taxa_de_mutacao: 
                    crianca = mutate(crianca)
            elif(operador_mutacao == 2):
                if random.random() <= taxa_de_mutacao: 
                    crianca = mutate2(crianca)
            
            new_population.append(crianca)

        data_population = new_population

        fittest_individual = fitness_threshold(fitness, fitness_thresh, data_population)

        if fittest_individual:
            return fittest_individual

    return min(data_population, key=fitness)

# caminhos_randomicos_quantidade = quanitidade de caminhos randomicos que vao servir de populacao inicial
# numero_geracoes = quantidade de geracoes que o algoritmo vai criar
# rate_de_mutacao = rate de mutacao
# data = input de pontos (testdata)

# SELECAO
#   1 -> ELITISMO
#   2 -> TORNEIO
#   3 -> CUSTOM (1 E 2 melhores) (opcional)

# MUTACAO
#   1 -> SWAP
#   2 -> INVERSAO

# CRUZAMENTO
#   1 -> N-POINT
#   2 -> DOUBLE-POINT
#   3 -> ESTADO DA ARTE

# QUANTIDADE INICIAL DE POPULACAO(numero inteiro)
# QUANTIDADE DE GERACOES(numero inteiro)
# TAXA DE MUTACAO(float entre 0.0 e 0.99)
# DATASET (berlin52, eil51, pr152, rat99)
# FITNESS THRESHOLD (valor inteiro)

#operador_selecao = 1
#operador_mutacao = 1
#operador_cruzamento = 2
#quantidade_inicial_populacao = 100
#quantidade_de_geracoes = 200
#taxa_de_mutacao = 0.1
#dataset = eil51
#fitness_thresh = 425

#impressao_solucao(algoritmo_genetico_completo(operador_selecao, operador_mutacao, operador_cruzamento, quantidade_inicial_populacao, quantidade_de_geracoes, taxa_de_mutacao, dataset, fitness_thresh))
lista_eil51 = []
lista_berlin52 = []
lista_pr152 = []
lista_rat99 = []

lista_eil51.append(fitness(algoritmo_genetico_completo(1, 1, 1, 100, 200, 0.2, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 1, 1, 100, 200, 0.3, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.1, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.2, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.3, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.1, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.2, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.3, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.1, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.2, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.3, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.1, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.2, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.3, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 300, 0.3, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 2, 3, 200, 300, 0.3, eil51, 426)))
lista_eil51.append(fitness(algoritmo_genetico_completo(1, 2, 3, 300, 400, 0.3, eil51, 426)))
escrever_em_arquivo(lista_eil51, 'lista_eil51.txt')

lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 1, 1, 100, 200, 0.2, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 1, 1, 100, 200, 0.3, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.1, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.2, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.3, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.1, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.2, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.3, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.1, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.2, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.3, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.1, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.2, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.3, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 300, 0.3, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 2, 3, 200, 300, 0.3, berlin52, 7542)))
lista_berlin52.append(fitness(algoritmo_genetico_completo(1, 2, 3, 300, 400, 0.3, berlin52, 7542)))
escrever_em_arquivo(lista_berlin52, 'lista_berlin52.txt')

lista_pr152.append(fitness(algoritmo_genetico_completo(1, 1, 1, 100, 200, 0.1, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 1, 1, 100, 200, 0.2, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 1, 1, 100, 200, 0.3, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.1, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.2, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.3, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.1, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.2, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.3, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.1, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.2, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.3, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.1, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.2, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.3, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 300, 0.3, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 2, 3, 200, 300, 0.3, pr152, 73682)))
lista_pr152.append(fitness(algoritmo_genetico_completo(1, 2, 3, 300, 400, 0.3, pr152, 73682)))
escrever_em_arquivo(lista_pr152, 'lista_pr152.txt')

lista_rat99.append(fitness(algoritmo_genetico_completo(1, 1, 1, 100, 200, 0.1, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 1, 1, 100, 200, 0.2, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 1, 1, 100, 200, 0.3, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.1, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.2, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 1, 2, 100, 200, 0.3, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.1, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.2, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 1, 3, 100, 200, 0.3, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.1, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.2, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 200, 0.3, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.1, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.2, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(2, 2, 3, 100, 200, 0.3, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 2, 3, 100, 300, 0.3, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 2, 3, 200, 300, 0.3, rat99, 1211)))
lista_rat99.append(fitness(algoritmo_genetico_completo(1, 2, 3, 300, 400, 0.3, rat99, 1211)))
escrever_em_arquivo(lista_rat99, 'lista_rat99.txt')