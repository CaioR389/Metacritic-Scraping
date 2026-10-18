from bs4 import BeautifulSoup
import requests

import config

# Adquire as notas de críticos e usuários
# Notas iguais (metascore = userscore) significa que não tem dados de um deles, e substitui pelo outro
def adquirir_dados(url):
    html = requests.get(url, headers=config.headers).text
    soup = BeautifulSoup(html, "html.parser")

    notas = soup.find_all("span", {"data-testid" : "global-score-value"})
    qnt_avaliações = soup.find_all("a", {"data-testid" : "global-score-review-count-link"})

    # A bagunça dos or é por causa que algumas desenvolvedoras pequenas não tem link no Metacritic
    return {"metascore" : notas[0].text,
            "qnt_críticos" : qnt_avaliações[0].text[9:-15],
            "userscore" : notas[1].text,
            "qnt_usuários" : qnt_avaliações[1].text[9:-13],
            "gênero" : soup.find("span", {"class" : "global-link-button__label"}).text,
            "desenvolvedora" : ( soup.find("a", {"class" : "text-gray-800 underline"}) or soup.find_all("span", {"class" : "text-gray-800"})[1] ).text,
            "publisher" : (soup.find("a", {"class" : "c-product-detail-link"}) or soup.find_all("span", {"class" : "c-product-details__section__value"})[1]).text
            }

# Sobrescreve o arquivo anterior e cria o cabeçalho
def criar_csv(nome_arquivo, cabeçalho):
    with open(nome_arquivo, 'w') as arquivo:
        for atributo in cabeçalho:
            if atributo != cabeçalho[-1]: arquivo.write(atributo + ", ")
            else: arquivo.write(atributo + '\n')

# Adiciona os jogos ao arquivo CSV
def append_csv(nome_arquivo, cabeçalho, dados: dict):
    with open(nome_arquivo, 'a') as arquivo:
        for atributo in cabeçalho:
            if atributo != cabeçalho[-1]: arquivo.write(dados[atributo] + ", ")
            else: arquivo.write(dados[atributo] + '\n')

# Procura na página de browse global do Metacritic
def browse_scrapping(url, ano: str):
    html = requests.get(url, headers=config.headers).text
    soup = BeautifulSoup(html, "html.parser")

    # Nome do CSV em que será armazenado os dados
    nome_arquivo = "dados/jogos_por_ano/jogos" + str(ano) + ".csv"
    # Cabeçalho para organização. A ordem importa. Todos os atributos listados aqui devem estar contidos na variável dados passada ao append_csv
    cabeçalho = ["nome", "url", "ano", "metascore", "qnt_críticos", "userscore", "qnt_usuários", "gênero", "desenvolvedora", "publisher"]

    qnt_jogos = soup.find("span", {"class" : "hidden lg:inline text-base text-gray-500"}).text[0:-8]
    qnt_paginas = int(soup.find_all("span", {"class" : "c-navigation-pagination__item-content"})[3].text)

    criar_csv(nome_arquivo, cabeçalho)

    pagina_atual = 1
    progresso = 0

    while pagina_atual <= qnt_paginas:

        nomes = soup.find_all("h3", {"data-testid" : "product-title"})
        jogos = soup.find_all("div", {"data-testid" : "filter-results"})

        for i in range(len(jogos)):
            nome_jogo = nomes[i].find_all("span")[1].text

            link_jogo = "https://www.metacritic.com" + jogos[i].find('a')["href"]

            dados = adquirir_dados(link_jogo)
            dados_basicos = {"nome" : nome_jogo, "url" : link_jogo, "ano" : ano}

            # Termina de organizar os dados para enfim escrevê-los
            for chave in dados_basicos:
                dados[chave] = dados_basicos[chave]

            # Escreve no CSV os dados do jogo atual
            append_csv(nome_arquivo, cabeçalho, dados)            

            progresso += 1
            print(str(progresso) + '/' + qnt_jogos)

        # Executa todas as operações para o próximo loop while
        pagina_atual += 1
        html = requests.get(url + f"&page={pagina_atual}", headers=config.headers).text
        soup = BeautifulSoup(html, "html.parser")