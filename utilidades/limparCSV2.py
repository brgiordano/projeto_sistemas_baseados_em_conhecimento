import re

# Função para remover palavras com mais de 46 caracteres
def remover_palavras_grandes(texto, limite):
    palavras = texto.split()  # Divide o texto em palavras
    palavras_filtradas = [palavra for palavra in palavras if len(palavra) <= limite]
    return ' '.join(palavras_filtradas)

# Função para limpar os espaços em excesso
def limpar_espacos(texto):
    texto = texto.strip()  # Remove espaços no início e no fim
    texto = re.sub(r'\s+', ' ', texto)  # Substitui múltiplos espaços por um só
    return texto

# Caminho do arquivo original
arquivo_txt = 'nerd_cast_transcricao.txt'  # Substitua pelo caminho do seu arquivo .txt

# Caminho para o novo arquivo filtrado
novo_arquivo_txt = 'nerd_cast_transcricao_REGEX.txt'

# Lê o arquivo original, remove as palavras grandes e os espaços em excesso, e salva no novo arquivo
with open(arquivo_txt, 'r', encoding='utf-8') as file:
    conteudo = file.read()

# Remove palavras maiores que 46 caracteres
conteudo_filtrado = remover_palavras_grandes(conteudo, 46)

# Limpa espaços em excesso
conteudo_limpo = limpar_espacos(conteudo_filtrado)

# Salva o conteúdo final no novo arquivo
with open(novo_arquivo_txt, 'w', encoding='utf-8') as file:
    file.write(conteudo_limpo)

print(f'Novo arquivo TXT criado: {novo_arquivo_txt}')
