import random
import time

inicio = (time.time())  # em segundos

arq = open('FlyFood/matriz2.txt', 'r')
matriz = (arq.readlines())

tam_populacao = 100
taxa_mutacao = 0.05
parada = 800

def pontos(matriz):
    pontos = []
    linha = 0
    for i in matriz:
        coluna = 0
        for j in i:
            if j not in [" ", "0", "\n"]:
                pontos.append([j, linha, coluna])
            if j != " ":
                coluna += 1
        linha += 1
    return pontos

lista = pontos(matriz)

def separa_R(lista):
    for i in lista:
        if i[0] == 'R':
            lista.remove(i)
            return (i, lista)

r, individuo = separa_R(lista)

def distancia_entre_dois_pontos(ponto1, ponto2):
    distancia = abs(ponto1[1] - ponto2[1]) + abs(ponto1[2] - ponto2[2])
    return distancia

# quanto menor a distancia, mais apto é o indivíduo
def avaliar_individuo(individuo):
    dist = 0
    inicio = r
    for i in individuo:
        dist = dist + distancia_entre_dois_pontos(inicio, i)
        inicio = i
    dist = dist + distancia_entre_dois_pontos(inicio, r)
    return dist

def gerar_pop_inicial(individuo):
    populacao = []
    for i in range(tam_populacao):
        lista = random.sample(individuo, len(individuo))
        populacao.append(lista)
    return populacao

def torneio(populacao):
    selecionados = []
    for i in range(len(populacao)):
        ind1 = random.choice(populacao)
        ind2 = random.choice(populacao)
        if avaliar_individuo(ind1) < avaliar_individuo(ind2):
            selecionados.append(ind1)
        else:
            selecionados.append(ind2)
    return selecionados

def torneiocomelitismo(populacao):
    selecionados = []
    pop = len(populacao)
    i = 0
    j = 1
    while(i < pop and j < pop):

        ind1 = populacao[i]
        ind2 = populacao[j]

        if avaliar_individuo(ind1) < avaliar_individuo(ind2):
            selecionados.append(ind1)
        else:
            selecionados.append(ind2)
        i += 1
        j += 1

    menor_dist = avaliar_individuo(populacao[0])
    menor_cam = [populacao[0]]

    for n in populacao:
        if avaliar_individuo(n) <= menor_dist:
            menor_dist = avaliar_individuo(n)
            menor_cam = n
    selecionados.append(menor_cam)

    return selecionados


def cruzamento_ordenado(populacao):
    filhos = []

    for i in range(0, len(populacao), 2):
        # Seleciona dois pais aleatórios da população
        pai1 = random.choice(populacao)
        pai2 = random.choice(populacao)

        # Seleciona um ponto de corte aleatório
        corte = random.randint(1, len(pai1) - 1)

        # Realiza o cruzamento ordenado
        filho1 = [-1] * len(pai1)
        filho2 = [-1] * len(pai2)
        for j in range(corte, len(pai1)):
            filho1[j] = pai1[j]
            filho2[j] = pai2[j]
        for j in range(corte, len(pai1)):
            # Para o filho 1, copia os valores do pai 2 que ainda não estão no filho
            if pai2[j] not in filho1:
                index = filho1.index(-1)
                filho1[index] = pai2[j]
            # Para o filho 2, copia os valores do pai 1 que ainda não estão no filho
            if pai1[j] not in filho2:
                index = filho2.index(-1)
                filho2[index] = pai1[j]
        for j in range(0, corte):
            # Para o filho 1, copia os valores do pai 2 que ainda não estão no filho
            if pai2[j] not in filho1:
                index = filho1.index(-1)
                filho1[index] = pai2[j]
            # Para o filho 2, copia os valores do pai 1 que ainda não estão no filho
            if pai1[j] not in filho2:
                index = filho2.index(-1)
                filho2[index] = pai1[j]

        # Adiciona os filhos na nova população
        filhos.append(filho1)
        filhos.append(filho2)

    return filhos

def mutacao(populacao):
        
        for i in range(len(populacao)):
            if random.random() < taxa_mutacao:
                # Seleciona dois genes aleatórios para trocar
                index1 = random.randint(0, len(populacao[i]) - 1)
                index2 = random.randint(0, len(populacao[i]) - 1)
                # Troca os valores dos genes selecionados
                populacao[i][index1], populacao[i][index2] = populacao[i][index2], populacao[i][index1]

        return populacao

def rota_e_dist(populacao):
    menor_dist = avaliar_individuo(populacao[0])
    menor_cam = [populacao[0]]
    for i in populacao:
        if avaliar_individuo(i) <= menor_dist:
            menor_dist = avaliar_individuo(i)
            menor_cam = i
    return (menor_cam, menor_dist)


def pegaLocais(caminho):
    rota = []
    for i in caminho:
        rota.append(i[0])
    return "".join(rota)


def main():
    pop = gerar_pop_inicial(individuo)

    for geracao in range(parada):
        selecionados = torneiocomelitismo(pop)
        pop = cruzamento_ordenado(selecionados)
        mutacao(pop)

    caminho, distancia = rota_e_dist(pop)
    print(f"A menor rota eh {pegaLocais(caminho)}, com distancia de {distancia} dronometros")

main()

final = (time.time())  # em segundos
tempo = final - inicio

# Print do tempo que demorou para rodar o código
print(tempo)
