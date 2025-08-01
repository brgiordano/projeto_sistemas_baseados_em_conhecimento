#-------------------------------------------------------------------------------------------------------------------
#Função para criar a cadeia de Markov
def criar_cadeia_markov(dataset, n_grama=2):
    """
    Esta função recebe um texto (dataset) e cria uma cadeia de Markov.
    A cadeia de Markov usa 'n_grama' (número de palavras usadas como chave) para prever a próxima palavra.
    """
    # Separa o texto em uma lista de palavras
    palavras = dataset.split()

    # Dicionário para armazenar as cadeias de Markov
    cadeia_markov = {}

    # Percorre as palavras e cria as sequências de n-gramas
    for i in range(len(palavras) - n_grama):
        # Define a chave como uma sequência de n palavras
        chave = tuple(palavras[i:i + n_grama])

        # Define o valor como a palavra que vem depois da chave no texto
        proxima_palavra = palavras[i + n_grama]

        # Adiciona a chave e a palavra seguinte ao dicionário da cadeia
        if chave not in cadeia_markov:
            cadeia_markov[chave] = []

        # Adiciona a próxima palavra à lista associada à chave
        cadeia_markov[chave].append(proxima_palavra)

    return cadeia_markov


# Função para gerar texto usando a cadeia de Markov
def gerar_texto(cadeia_markov, comprimento_texto, n_grama=2):
    """
    Esta função recebe uma cadeia de Markov e gera um texto de tamanho 'comprimento_texto'.
    Começa com uma chave aleatória e, a partir daí, gera palavras seguindo a cadeia de Markov.
    """
    # Escolhe uma chave aleatória para começar (sequência de n-gramas)
    chave_atual = random.choice(list(cadeia_markov.keys()))

    # Inicia o texto com as palavras da chave escolhida
    texto_gerado = list(chave_atual)

    # Gera as palavras seguintes até atingir o comprimento desejado
    for _ in range(comprimento_texto - n_grama):
        # Verifica se a chave atual está no dicionário de cadeias
        if chave_atual in cadeia_markov:
            # Escolhe aleatoriamente a próxima palavra associada à chave atual
            proxima_palavra = random.choice(cadeia_markov[chave_atual])

            # Adiciona a próxima palavra ao texto gerado
            texto_gerado.append(proxima_palavra)

            # Atualiza a chave para as próximas n palavras
            chave_atual = tuple(texto_gerado[-n_grama:])
        else:
            # Se a chave não estiver no dicionário, para de gerar o texto
            break

    # Retorna o texto gerado como uma string
    return ' '.join(texto_gerado)


# Dataset de exemplo (você pode substituir por qualquer texto)
dataset = """
Dois motivos me levam a falar do livro do Sr. A. E. Zaluar; o primeiro, é o próprio
merecimento dele, a confirmação que essas novas páginas trazem ao talento do
poeta; o segundo, é ser o autor das Revelações um dos que conservam mais viva
a fé poética e acreditam realmente na poderosa influência das musas.
Parece, à primeira vista, coisa impossível um poeta que condene a sua própria
missão, não acreditando nos efeitos dela; mas, se se perscrutar cuidadosamente,
ver-se-á que este fenômeno é, não só possível, como até não raro.
O tom sinceramente elegíaco da poesia de alguns dos mestres contemporâneos
deu em resultado uma longa enfiada desses filhos das musas, aliás, talentosos,
em cuja lira a desconfiança e o abatimento tomam o lugar da fé e da aspiração.
Longe a idéia de condenar os que, após longa e dolorosa provação, sem negarem
a grandeza de sua missão moral, soluçam por momentos desconsolados e
desesperançados. Desses sabe-se que a cada gota de sangue que lhes tinge os
lábios corresponde um rompimento de fibras interiores; mas entre esses
sofrimentos, muitas vezes não conhecidos de todos, e o continuado lama
sabactani dos pretendidos infelizes, há uma distância que a credulidade dos
homens não deve preencher.
Não se contesta às almas poéticas certa sensibilidade fora do comum e mais
exposta por isso ao choque das paixões humanas e das contrariedades da vida;
mas não se estenda essa faculdade até à sensiblerie, nem se confunda a dor
espontânea com o sofrimento calculado. A nossa língua tem exatamente dois
termos para exprimir e definir essas duas classes de poetas; uns serão a
sensibilidade, outros a suscetibilidade.
Destes últimos não é o autor das Revelações, o que no tempo presente é um
verdadeiro mérito e um dos primeiros a serem apontados na conta da análise.
Análise escapa-me aqui, sem indicar de minha parte intuito determinado de
examinar detida e profundamente a obra do Sr. Zaluar. Em matéria de crítica o
poeta e o leitor têm direito a exigir do escritor mais valiosos documentos que os
meus; esta confissão, que eu sempre tenho o cuidado de repetir, deve relevar-me
dos erros que cometer e dispensar-me de um longo exame. É como um
companheiro da mesma oficina que eu leio os versos do poeta, e indico as minhas
impressões. Nada mais.
O primeiro volume com que o Sr. Zaluar se estreou na poesia intitulava-se Dores e
Flores; foi justamente apreciado como um primeiro ensaio; mas desde então a
crítica reconheceu no poeta um legítimo talento e o admitiu entre as esperanças
que começavam a florir nesse tempo.
As torturas de Bossuet para descrever o sonho da heroína servem-me de aviso
nesta conjuntura, mas tiram-me uma das mais apropriadas figuras, com que eu
poderia definir o resultado mau e o resultado bom dessas esperanças nascentes.
Direi em prosa simples que o autor das Dores e Flores foi das esperanças que
vingaram, e pode atravessar os anos dando provas do seu talento sempre
desenvolvido.
O que é pena (e é essa a principal censura a fazer às Revelações) é que durante o
longo período que separa os dois livros o poeta não acompanhasse o
desenvolvimento do seu estro com maior cópia de produções, e que no fim de tão
longa espera o novo livro não traga com que fartar largamente tantos desejos.
Mas, sendo assim, o que resta aos apreciadores do talento do poeta é buscar no
insuficiente do livro as sensações a que ele os acostumou.
Para ser franco cumpre declarar que há reservas a fazer, e tanto mais notáveis,
quanto se destacam sensivelmente no fundo irrepreensível do livro. Mais de uma
vez o poeta, porque escrevesse em horas de cansaço ou fastio, sai com a sua
musa das regiões etéreas para vir jogar terra a terra com a frieza das palavras;
esses abatimentos, que, por um singular acaso, na divisão do livro acham-se
exatamente em ordem a indicar as alternativas dos vôos da sua musa, servem, é
certo, para pôr mais em relevo as suas belezas incontestáveis e as elevações
periódicas do seu estro.
Pondo de parte esses fragmentos menos cuidados, detenho-me no que me parece
traduzir o poeta. Aí, reconhecem-se as suas qualidades, sente-se a sua poesia
melodiosa, simples, terna; a sua expressão conceituosa e apropriada; a
abundância contida do seu estro. Sempre que o poeta dá passagem às comoções
de momento, a sua poesia traz o verdadeiro e primitivo sabor, como na Casinha
de sapê e outras.
A parte destinada à família e ao lar, que é por onde começa o livro, traz
fragmentos de poesia melancólica, mas não dessa melancolia que anula toda a
ação do poeta e faz ver na hora presente o começo de continuadas catástrofes. É
esse um assunto eterno de poesia; a recordação da vida de criança, na intimidade
do lar paterno, onde as mágoas e os dissabores, como os raios, não chegam até
às plantas rasteiras, não passando dos carvalhos; essa recordação na vida do
homem feito é sempre causa de lágrimas involuntárias e silenciosas; as do poeta
são assim, e tão medrosas de aparecer, que essa parte do livro é a menos farta.
Efêmeras é o título da segunda parte do livro. Aí reuniu o poeta as poesias de
assunto diverso, as que traduzem afetos e observações, os episódios íntimos e
rápidos da vida.
Arrufos é uma das poesias mais notáveis dessa parte; é inspirada visivelmente da
musa fácil de Garret, mas com tal felicidade, que o leitor, lembrando-se do grande
mestre, nem por isso deixa de lhe achar um especial perfume.
Não acompanharei as outras efêmeras de merecimento, como sejam A Confissão,
Perdão, etc. O livro contém mais duas partes; uma, onde se acham algumas boas
traduções do autor, e versos que lhe são dedicados por poetas amigos; outra que
toma por título Harpa Brasileira, onde estão as poesias A casinha de sapê, O ouro,
O Filho das florestas, A flor do mato, os Rios, etc.
Da Casinha de sapê já disse que é uma das melhores do livro; acrescentarei que
ela basta para indicar a existência do fogo sagrado no espírito do poeta; a
melancolia do lugar é traduzida em versos que deslizam suave, espontânea e
naturalmente, e a descrição não pode ser mais verdadeira.
Para apreciação detida do leitor, dou aqui algumas dessas estrofes:
No cimo de um morro agreste,
Por entre uns bosques sombrios,
Onde conduz uma senda
De emaranhados desvios,
Uma casinha se vê
Toda feita de sapê!
Suave estância! Parece,
Circundada de verdura,
Como um templo recatado
No seio da espessura;
Naqueles ermos tão sós
Não chega do mundo a voz!
Apenas uma torrente,
Que brota lá dos rochedos,
Murmura galgando as penhas,
Suspira entre os arvoredos!
Tem ali a natureza
A primitiva beleza!
Lá distante... inda se escuta
Ao longe o bramir do mar!
Ouvem-se as vagas frementes
Nos alcantis rebentar!
Aquele eterno lamento
Chora nas asas do vento!
Mas na casinha, abrigada
Pelos ramos das mangueiras,
Protegida pelas sombras,
Dos leques das bananeiras,
Aquele triste clamor
É como um gênio de amor!
Eu e Júlia nos perdemos
Na senda, uma vez, do monte;
Ao sol-posto — cor de lírio
Era a barra do horizonte
Toda a terra se cobria
D'um véu de melancolia!
O meu braço segurava
O seu corpo já pendido
Às emoções, ao cansaço,
Como que desfalecido.
Seus olhos com que doçura
Se banhavam de ternura!
Paramos no tosco ang'lo
Da montanha verdejante.
Era deserto. Não tinha
A ninguém por habitante!
Só no lar abandonadas
Algumas pedras tisnadas!
"""

# Cria a cadeia de Markov usando o dataset
cadeia_markov = criar_cadeia_markov(dataset, n_grama=2)

# Gera um texto de exemplo com 20 palavras
texto_gerado = gerar_texto(cadeia_markov, comprimento_texto=20)

# Exibe o texto gerado
print("Texto gerado:\n", texto_gerado)