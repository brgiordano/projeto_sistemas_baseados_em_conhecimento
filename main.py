import os
import numpy as np

# ----------------------------------------------------------------------------------------------------
# Função para abrir o arquivo do dataset(.txt por exemplo)
def carregar_data_set(dataset):
    with open(dataset, 'r', encoding='utf-8') as conjunto_de_treinamento:
        return  conjunto_de_treinamento.read()

# ----------------------------------------------------------------------------------------------------
# Função para gerar a tabela de transição com base no dataset fornecido
# Mapeia cada estado para uma lista de possíveis estados subsequentes e suas respectivas probabilidades de transição.
def gerar_tabela_de_pesquisa(data_set: str, n_grama = 2):

    # Divide o texto em palavras
    palavras = data_set.split()

    # Inicializa a tabela de transição como um dicionário vazio
    tabela = {}

    # Itera sobre o texto para gerar a tabela de transição
    for i in range(len(palavras) - n_grama):
        # Identifica o estado_atual como uma sequência de palavras de tamanho n_gramas
        estado_atual = ' '.join(palavras[i:i + n_grama])

        # identifica a próxima palavra após o estado_atual(estado composto por n_gramas palavras)
        prox_palavra = palavras[i + n_grama]

        # Verifica se o estado_atual inexiste na está na tabela, caso inexista, cria o estado, e já adiciona a prox palavra
        if estado_atual not in tabela:
            tabela[estado_atual] = {}
            tabela[estado_atual][prox_palavra] = 1
        # Se o estado atual já existir, deve-se verificar se a próxima palavra já foi associada a esses estado;
        # se não foi, associa e atribui uma ocorrência dessa palavra à tabela
        else:
            if prox_palavra not in tabela[estado_atual]:
                tabela[estado_atual][prox_palavra] = 1
            # Se já houve ocorrência da palavra para o estado atual, incrementa a ocorrência da palavra.
            tabela[estado_atual][prox_palavra] += 1

    # Retorna a tabela de transição gerada
    return tabela

# ----------------------------------------------------------------------------------------------------
# Função que converte a contagem de frequência em uma tabela de transição para probabilidades de acordo a com a seguinte equação:
# freqência de prox_palavra no estado atual dividido pela quantidade total de todas as prox_palavra do estado atual.
# Assim, teremos, para cada estado, uma média ponderada de cada próxima palavra,
# e não a quantidade a absoluta de ocorrências dessa palavra nesse estado.

def frequencia_para_probabilidade(tabela):
    # percorre cada estado da tabela
    for estado in tabela:
        # Calcula o total de ocorrências de todas as próximas palavras para o estado atual
        total = float(sum(tabela[estado].values()))

        # Itera sobre cada próxima palavra para o estado atual
        for prox_palavra in tabela[estado]:
            # Divide a contagem de frequência da próxima palavra pelo total de ocorrências
            tabela[estado][prox_palavra] /= total

    # Retorna a tabela de transição convertida em probabilidades
    return tabela

# ----------------------------------------------------------------------------------------------------
# Classe que representa o modelo de Markov.
# Treina um modelo de markov dado um determinado dataset e o n-grama;
# É capaz de retornar o modelo treinado e o n-grama usado para o treinamento
# n-grama é opcional, e o default foi definido como 2
# def cadeia_de_markov(data_set, n_grama = 2):

class ModeloMarkov:
    def __init__(self, data_set: str, n_grama=2):
        if not data_set:
            raise ValueError("[ERRO]: O data_set não pode ser vazio.")
        if not isinstance(n_grama, int) or n_grama <= 0:
            raise ValueError("[ERRO]: O n-grama deve ser um inteiro positivo.")

        self.__data_set = data_set
        self.__n_grama = n_grama
        self.__modelo_markov = frequencia_para_probabilidade(gerar_tabela_de_pesquisa(self.__data_set, self.__n_grama))

        #Retorna o valor do n-grama
    def get_n_grama(self):
        return self.__n_grama

        #Retorna o valor o modelo de markov treinado
    def get_modelo(self):
        return self.__modelo_markov


    # função para atualizar o dataset com mais dados;
    # recebe um novo dataset.txt como argumento
    # Carrega o texto do novo arquivo que será utilizado para atualizar o modelo.
    # gera a tabela de pesquisa do modelo de markov para esse novo dataset
    def atualizar_dataset(self, novo_data_set: str):
        novo_texto = carregar_data_set(novo_data_set)
        nova_tabela = gerar_tabela_de_pesquisa(novo_texto, self.__n_grama)

        # inicia uma tabela de frequência para armazenar o total da frequência acumulada das palavras do modelo existente
        # será usado para atualizar o dataset existente com as informações do novo.
        # necessário pois o modelo existente conta com frequências normalizadas, e o novo tem frequências absolutas
        tabela_frequencias = {}

        # Para cada estado na tabela do modelo existente, Calcula o total de ocorrências de todas as próximas palavras.
        # Armazena essas frequências na tabela_frequencias.
        # Itera sob todos od itens de todos os estados
        # pega o total de ocorrências de cada palavra de um estado
        # multiplica o total de ocorrência de cada palavra pela quantidade total de palavras daquele estado
        # isso no dás, novamente, o valor absoluto(frequência) de cada palavra, e não sua probabilidade dentro do modelo
        # armazena isso na tabela de frequências
        for estado, prox_palavras in self.__modelo_markov.items():
            total_ocorrencias = float(sum(prox_palavras.values()))
            tabela_frequencias[estado] = {palavra: contagem * total_ocorrencias for palavra, contagem in
                                          prox_palavras.items()}

        # Atualiza a tabela com os novos dados
        # adiciona as frequências da nova tabela à tabela de frequências
        for estado, prox_palavras in nova_tabela.items():
            if estado not in tabela_frequencias:
                tabela_frequencias[estado] = prox_palavras
            else:
                for prox_palavra, contagem in prox_palavras.items():
                    tabela_frequencias[estado][prox_palavra] = tabela_frequencias[estado].get(prox_palavra,
                                                                                              0) + contagem

        # Recalcula novamente de valores de frequência para probabilidade
        # agora, a tabela existente passa a calcular as probabilidade das palavras já contando
        # com os dados da nova tabela
        self.__modelo_markov = frequencia_para_probabilidade(tabela_frequencias)

# ----------------------------------------------------------------------------------------------------
# Função que retorna a próxima palavra prevista a partir de um texto inicial e no modelo de Markov previamente treinado.
# tamanho do n-grama do modelo é opcional, o default foi definido como 2
def proxima_suposicao(estado_atual, modelo_markov: ModeloMarkov):

    modelo = modelo_markov.get_modelo()
    n_grama = modelo_markov.get_n_grama()

    # Divide o texto inicial em uma lista de palavras
    estado_atual_lista = estado_atual.split()

    # captura as n-grama ultimas palavras do texto e forma o estado atual do modelo
    estado_atual = ' '.join(estado_atual_lista[-n_grama:])

    # Se o estado não estiver no modelo, retorna um espaço em branco
    if estado_atual not in modelo:
        return " "

    # captura as probabilidades das possíveis próximas palavras e suas probabilidades no modelo
    palavras_possiveis = list(modelo[estado_atual].keys())
    probabilidades_palavras_possiveis = list(modelo[estado_atual].values())

    # Se não houver palavras possíveis, retorne uma string vazia ou um espaço
    if not palavras_possiveis:
        return " "

    # Escolhe aleatoriamente a próxima palavra considerando as probabilidades
    # usando random para ser menos determinístico
    palavra_escolhida = np.random.choice(palavras_possiveis, p=probabilidades_palavras_possiveis)

    # Retorna a próxima palavra prevista
    return palavra_escolhida

#-------------------------------------------------------------------------------------------------------------------
# gera o texto a partir de um texto inicial e um modelo de Markov previamente treinado

def gerar_texto(texto_inicial, modelo_markov: ModeloMarkov, tam_max_texto = 50):
    modelo = modelo_markov.get_modelo()
    n_grama = modelo_markov.get_n_grama()

   # Converte o texto inicial em uma lista de palavras
    texto_inicial_lista = texto_inicial.split()

    # verifica se o texto inicial tem menos palavras do que o tamanho do n-grama
    while len(texto_inicial_lista) < n_grama:
        # busca possíveis próximas palavras com base na última palavra do texto inicial
        palavras_possiveis = [key for key in modelo.keys() if key.startswith(texto_inicial_lista[-1])]

        # Se houver possíveis continuações, escolhe uma aleatoriamente e estende a sentença
        if palavras_possiveis:
            estado_escolhido = np.random.choice(palavras_possiveis)
            texto_inicial_lista.extend(estado_escolhido.split()[1:])
        else:
            if n_grama > len(texto_inicial_lista):
                raise ValueError("[Erro]: Forneça um texto inicial maior ou um modelo com menor n-grama")

    # Define o estado atual com base nas últimas n-gramas palavras do inicial
    estado_atual = ' '.join(texto_inicial_lista[-n_grama:])

    # gera um texto de <tam_max_texto> palavras
    for _ in range(tam_max_texto):
        # Obtém a próxima palavra com base no estado atual e no modelo fornecido
        proxima_palavra = proxima_suposicao(estado_atual, modelo_markov)

        # Se a próxima palavra for uma string vazia, finaliza a geração de palavras
        if proxima_palavra.strip() == "":
            break

        # Adiciona a próxima palavra à sentença e atualiza o estado atual
        # que agora considera a palavra gerada no passo anterior
        texto_inicial_lista.append(proxima_palavra)
        estado_atual = ' '.join(texto_inicial_lista[-n_grama:])

    # Junta todas as palavras em um único texto
    texto_final = ' '.join(texto_inicial_lista)

    # Retorna o texto gerado
    return texto_final


# ######################## TREINANDO O MODELO AOS POUCOS [INÍCIO] ######################## #
# definindo os argumentos das funções
fraseDeInicio = "A vida"
tamanhoTexto = 200
n_grama = 4

modeloTeste = ModeloMarkov(carregar_data_set(r"datasets\txt\nerd_cast_transcricao_REGEX.txt"), n_grama)

print("-=-" * 20)
print(gerar_texto(fraseDeInicio, modeloTeste, tamanhoTexto))

# print("-=-" * 20)
# modeloTeste.atualizar_data_set(r"datasets\txt\americanas.txt")
# print(gerar_texto(fraseDeInicio, modeloTeste, tamanhoTexto))
#
# print("-=-" * 20)
# modeloTeste.atualizar_data_set(r"datasets\txt\bukowski.txt")
# print(gerar_texto(fraseDeInicio, modeloTeste, tamanhoTexto))
#
# print("-=-" * 20)
# modeloTeste.atualizar_data_set(r"datasets\txt\bdfala.txt")
# print(gerar_texto(fraseDeInicio, modeloTeste, tamanhoTexto))
#
# print("-=-" * 20)
# modeloTeste.atualizar_data_set(r"datasets\txt\biblia_REGEX.txt")
# print(gerar_texto(fraseDeInicio, modeloTeste, tamanhoTexto))

# ######################## TREINANDO O MODELO AOS POUCOS [FIM] ######################## #

# ######################## CARREGANDO TODOS OS ARQUIVOS [INÍCIO] ######################## #
# fraseDeInicio = "a terra"
# tamanhoTexto = 100
# print("-=-" * 20)
# n_grama = 2
#
# def carregar_nomes_datasets(caminho_pasta):
#     arquivos_txt = []
#     for arq in os.listdir(caminho_pasta):
#         if arq.endswith(".txt"):
#             arquivos_txt.append(os.path.join(caminho_pasta, arq))
#     return arquivos_txt
#
# # define o caminho da pasta .txt da pasta
# pasta_txt = r"datasets\txt"
#
# # lista com os nomes de todos os arquivos da pasta
# todos_os_arquivos = carregar_nomes_datasets(pasta_txt)
#
# # Inicializa o modelo com o primeiro arquivo
# modeloTeste = ModeloMarkov(carregar_data_set(todos_os_arquivos[0]), 2)
# print(gerar_texto(fraseDeInicio, modeloTeste, tamanhoTexto))
# print("-=-" * 20)
#
# # Atualiza o modelo com todos os arquivos carregados
# for arquivo in todos_os_arquivos[1:]:
#     modeloTeste.atualizar_dataset(arquivo)
#     # print(gerar_texto(fraseDeInicio, modeloTeste, tamanhoTexto))
#     # print("-=-" * 20)
# print(gerar_texto(fraseDeInicio, modeloTeste, tamanhoTexto))

# ######################## CARREGANDO TODOS OS ARQUIVOS [FIM] ######################## #

