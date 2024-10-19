import pandas as pd
import re
import csv

# Função para limpar as colunas, mantendo apenas a coluna 'texto'
def limpar_csv(caminho_entrada, caminho_saida):
    # Lê o arquivo CSV
    df = pd.read_csv(caminho_entrada)

    # Exibe as colunas originais para referência
    print("Colunas originais:", df.columns.tolist())

    # Aplica uma regex para substituir todo o texto nas colunas, exceto na coluna 'texto'
    for coluna in df.columns:
        if coluna != 'texto':
            # Aplica regex para substituir o conteúdo da coluna por uma string vazia
            df[coluna] = df[coluna].apply(lambda x: re.sub(r'.*', '', str(x)))

    # Salvando o resultado em um novo arquivo com tratamento de espaços usando strip()
    with open(caminho_saida, 'w', newline='', encoding='utf-8') as f_out:
        for linha in df.to_csv(index=False, sep='\t', quoting=csv.QUOTE_NONE).splitlines():
            # Usando strip() para remover espaços em branco no início e fim de cada linha
            f_out.write(linha.strip() + '\n')

# Ajuste os caminhos conforme necessário
caminho_csv_entrada = r"C:\Users\Loryn\Documents\Bruno\Sistemas baseados em conhecimento\projeto\datasets\biblia_almeida_completa.csv"
caminho_txt_saida = r"C:\Users\Loryn\Documents\Bruno\Sistemas baseados em conhecimento\projeto\datasets\biblia_REGEX.txt"

# Chama a função para limpar o CSV
limpar_csv(caminho_csv_entrada, caminho_txt_saida)

print("Arquivo limpo salvo em:", caminho_txt_saida)
