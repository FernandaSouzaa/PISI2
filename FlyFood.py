arq = open('arquivo.txt', 'r')
matriz = (arq.readlines())

def pontos(matriz):
    pontos = []
    linha = 0
    for i in matriz:
        coluna = 0
        for j in i:
            if j not in [" ", "0", "\n"]:
                pontos.append([j,linha,coluna])
            if j != " ":
                coluna += 1
        linha += 1
    return pontos

lista = pontos(matriz)

def separa_R(lista):
    for i in lista:
        if i[0] == 'R':
            lista.remove(i)
            return (i,lista)

r,lista_p = separa_R(lista)

def permuta(lista_p):
    if len(lista_p) == 0:
        return []
    if len(lista_p) == 1:
        return [lista_p]
    lista_aux = []
    for indice in range(len(lista_p)):
        primeiro_elem = lista_p[indice]
        lista_restante = lista_p[:indice] + lista_p[indice + 1:]
        for p in permuta(lista_restante):
            lista_aux.append([primeiro_elem] + p)
    return lista_aux

def distancia_entre_dois_pontos(ponto1,ponto2):
    distancia = abs(ponto1[1] - ponto2[1]) + abs(ponto1[2] - ponto2[2])
    return distancia

def dist_total(r,lista_p):
    cont = 0
    inicio = r
    for i in lista_p:
        cont = cont + distancia_entre_dois_pontos(inicio,i)
        inicio = i
    cont = cont + distancia_entre_dois_pontos(inicio,r)
    return cont

def rota_e_dist(r,lista_aux):
    menor_dist = dist_total(r,lista_aux[0])
    menor_cam = [lista_aux[0]]
    inicio = r
    for i in lista_aux:
        if dist_total(inicio,i) <= menor_dist:
            menor_dist = dist_total(inicio,i)
            menor_cam = i
    return (menor_cam,menor_dist)

caminho,distancia = rota_e_dist(r,permuta(lista_p))

def pegaLocais(caminho):
    rota = []
    for i in caminho:
        rota.append(i[0])
    return "".join(rota)

print(f"A menor rota é {pegaLocais(caminho)}, com distância de {distancia} dronômetros")