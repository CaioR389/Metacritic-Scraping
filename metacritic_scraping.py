from bs4 import BeautifulSoup
import requests

import config

# Adquire as notas de críticos e usuários
def notas(url):
    html = requests.get(url, headers=config.headers).text
    soup = BeautifulSoup(html, "html.parser")

    notas = soup.find_all("span", {"data-testid" : "global-score-value"})

    return {"metascore":int(notas[0].text), "userscore":float(notas[1].text)}


def escrever_csv(nome_arquivo, cabeçalho: list, dados: dict):
    # Sobrescreve o arquivo anterior e cria o cabeçalho
    with open(nome_arquivo, 'w') as arquivo:
        for atributo in cabeçalho:
            if atributo != cabeçalho[-1]: arquivo.write(f"{atributo}, ")
            else: arquivo.write(atributo + '\n')

    with open(nome_arquivo, 'a') as arquivo:
        with open(nome_arquivo, 'w') as arquivo:
            for atributo in cabeçalho:
                if atributo != cabeçalho[-1]: arquivo.write(f"{dados[atributo]}, ")
                else: arquivo.write(dados[atributo] + '\n')

#TODO: browse_scrapping escreve os dados em arquivos com escrever_csv
# Procura na página de browse global do Metacritic
def browse_scrapping(url, ano: str):
    html = requests.get(url, headers=config.headers).text
    soup = BeautifulSoup(html, "html.parser")

    qnt_jogos = soup.find("span", {"class" : "hidden lg:inline text-base text-gray-500"}).text[0:-8]
    qnt_paginas = int(soup.find_all("span", {"class" : "c-navigation-pagination__item-content"})[3].text)

    # Página em que ele vai começar a colocar &page= no link
    pagina_atual = 2

    progresso = 0

    while qnt_paginas > 0:

        nomes = soup.find_all("h3", {"data-testid" : "product-title"})
        jogos = soup.find_all("div", {"data-testid" : "filter-results"})

        for i in range(len(jogos)):
            # URL do game atual
            nome_jogo = nomes[i].find_all("span")[1].text

            link_jogo = "https://www.metacritic.com" + jogos[i].find('a')["href"]

            print(f"Nome: {nome_jogo}\nlink: {link_jogo}")

            print(notas(link_jogo))

            progresso += 1
            print(str(progresso) + '/' + qnt_jogos)

        # Executa todas as operações para o próximo loop while
        qnt_paginas -= 1
        html = requests.get(url + f"&page={pagina_atual}", headers=config.headers).text
        soup = BeautifulSoup(html, "html.parser")
        pagina_atual += 1