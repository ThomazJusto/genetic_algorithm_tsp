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

# FUNCAO DE MUTATE 2(MUTACAO DO TIPO UNIFORM)
def mutate2(lista_de_pontos, numero_baixo, numero_alto):
    nova_lista_de_pontos = []
    for ponto in lista_de_pontos:
        ponto = random.randint(numero_baixo, numero_alto)  # Gera um novo valor aleatório para o gene (0 ou 1)
        nova_lista_de_pontos.append(nova_lista_de_pontos)
    return nova_lista_de_pontos

# FUNCAO DE CRUZAMENTO 1(N-POINT STYLE, PEGA PARTE DO PAI E PARTE DA MAE)
# LEMBRANDO QUE SE PEGAMOS DOIS INDIVIDUOS DIFERENTES, PODEMOS ESTAR FAZENDO CRUZAMENTO COM PONTOS DUPLICADOS
def crossover(lista_de_pontos1, lista_de_pontos2):
    nova_lista = []
    random_number = random.randint(0, len(lista_de_pontos2))
    for i in range(random_number):
        nova_lista.append(lista_de_pontos1[i])

    for i in range(random_number, len(lista_de_pontos2)):
        nova_lista.append(lista_de_pontos2[i])

    return nova_lista

# FUNCAO DE CRUZAMENTO 2(DOUBLE POINT STYLE, PEGA PARTES DO PAI E PARTES DA MAE - 2 RECORTES NO INDIVIDUO)
# LEMBRANDO QUE SE PEGAMOS DOIS INDIVIDUOS DIFERENTES, PODEMOS ESTAR FAZENDO CRUZAMENTO COM PONTOS DUPLICADOS
def crossover_doublepoint(lista_de_pontos1, lista_de_pontos2):
    nova_lista = []
    
    # Seleciona aleatoriamente dois pontos de corte
    corte1 = random.randint(0, len(lista_de_pontos1) - 1)
    corte2 = random.randint(corte1 + 1, len(lista_de_pontos1))

    # Troca os segmentos entre os dois pontos de corte
    nova_lista.extend(lista_de_pontos1[:corte1])
    nova_lista.extend(lista_de_pontos2[corte1:corte2])
    nova_lista.extend(lista_de_pontos1[corte2:])
    
    return nova_lista
    
# FUNCAO CRUZAMENTO 3(N-POINT POREM VERIFICA POR DUPLICADOS)
def crossover_custom(lista_de_pontos1, lista_de_pontos2):
    nova_lista = []
    nova_lista = set(nova_lista)

    random_number = random.randint(1, 50)

    for i in range(0, random_number):
        nova_lista.add(lista_de_pontos1[i])

    for i in range(0, len(lista_de_pontos2)):
        if nova_lista.__contains__(lista_de_pontos2[i]):
            continue
        else:
            nova_lista.add(lista_de_pontos2[i])

    nova_lista = list(nova_lista)
    return nova_lista

# FUNCAO CROSSOVER ESTADO DA ARTE 4 
# AN EFFICIENT CROSSOVER OPERATOR FOR TRAVELING SALESMAN PROBLEM
# M. Rajabi Bahaabadi, A. Shariat Mohaymany*,† and M. Babaei
# Iran University of Science and Technology, Faculty of Civil Engineering, Narmak, Tehran, Iran
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
    print(f"Custo total: {fitness(data)}!!!")

def ids_unicos(data):
    ids = set()
    for ponto in data:
        if ponto.id in ids:
            return False
        else:
            ids.add(ponto.id)
    return True

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
                crianca = crossover_custom(pai, mae)
            elif(operador_cruzamento == 4):
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

    impressao_solucao(min(data_population, key=fitness))
    return min(data_population, key=fitness)

# caminhos_randomicos_quantidade = quanitidade de caminhos randomicos que vao servir de populacao inicial
# numero_geracoes = quantidade de geracoes que o algoritmo vai criar
# rate_de_mutacao = rate de mutacao
# data = input de pontos (testdata)

# SELECAO
#   1 -> ELITISMO
#   2 -> TORNEIO
#   3 -> CUSTOM (1 E 2 melhores)

# MUTACAO
#   1 -> SWAP
#   2 -> UNIFORM

# CRUZAMENTO
#   1 -> N-POINT
#   2 -> DOUBLE-POINT
#   3 -> N-POINT COM VERIFICACAO DE DUPLICADOS
#   4 -> ESTADO DA ARTE

# QUANTIDADE INICIAL DE POPULACAO(numero inteiro)
# QUANTIDADE DE GERACOES(numero inteiro)
# TAXA DE MUTACAO(float entre 0.0 e 0.99)
# DATASET (berlin52, eil51, pr152, rat99)
# FITNESS THRESHOLD (valor inteiro)

operador_selecao = 1
operador_mutacao = 1
operador_cruzamento = 1
quantidade_inicial_populacao = 500
quantidade_de_geracoes = 200
taxa_de_mutacao = 0.2
dataset = eil51
fitness_thresh = 500

melhor_solucao = algoritmo_genetico_completo(operador_selecao, operador_mutacao, operador_cruzamento, quantidade_inicial_populacao, quantidade_de_geracoes, taxa_de_mutacao, dataset, fitness_thresh)