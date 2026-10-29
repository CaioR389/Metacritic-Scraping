from bs4 import BeautifulSoup
import requests

import config

# Adquire as notas de críticos e usuários
# Notas iguais (metascore = userscore) significa que não tem dados de um deles, e substitui pelo outro
def game_scraping(url):
    def scrap_nome(soup):
        return soup.find("h1", {"class" : "text-4xl font-bold text-[#333]"}).text

    def scrap_data_lancamento(soup):
        tabela_data = {"Jan" : "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", "May" : "05", "Jun" : "06", "Jul" : "07", "Aug" : "08", "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"}

        # Tinha um jogo sem data de lançamento, por isso essa manipulação toda só para pegar a data
        if soup.find("div", {"class" : "hero-release-date__value"}) != None:
            data_lançamento = soup.find("div", {"class" : "hero-release-date__value"}).text
            if len(data_lançamento) == 11:
                data_lançamento = f"0{data_lançamento[4]}/{tabela_data[data_lançamento[0:3]]}/{data_lançamento[-4:]}"
            else:
                data_lançamento = f"{data_lançamento[4:6]}/{tabela_data[data_lançamento[0:3]]}/{data_lançamento[-4:]}"
        else:
            data_lançamento = "tdb"

        return data_lançamento

    def scrap_metascore(soup):
        return soup.find_all("span", {"data-testid" : "global-score-value"})[0].text

    def scrap_qnt_meta(soup):
        return soup.find_all("a", {"data-testid" : "global-score-review-count-link"})[0].text[9:-15]

    def scrap_pmn_meta(soup):
        # Porcentagem de avaliações positivas, mistas e negativas
        positivas = soup.find_all("div", {"class" : "reviews-stats__positive-stats"})
        mistas = soup.find_all("div", {"class" : "reviews-stats__neutral-stats"})
        negativas = soup.find_all("div", {"class" : "reviews-stats__negative-stats"})
                
        return positivas[0].find("span", {"class" : "bold"}).text[:-10] + ':' + mistas[0].find("span", {"class" : "bold"}).text[:-7] + ':' + negativas[0].find("span", {"class" : "bold"}).text[:-10]

    def scrap_userscore(soup):
        return soup.find_all("span", {"data-testid" : "global-score-value"})[1].text

    def scrap_qnt_user(soup):
        return soup.find_all("a", {"data-testid" : "global-score-review-count-link"})[1].text[9:-13]

    def scrap_pmn_user(soup):
        # Porcentagem de avaliações positivas, mistas e negativas
        positivas = soup.find_all("div", {"class" : "reviews-stats__positive-stats"})
        mistas = soup.find_all("div", {"class" : "reviews-stats__neutral-stats"})
        negativas = soup.find_all("div", {"class" : "reviews-stats__negative-stats"})
        
        return positivas[1].find("span", {"class" : "bold"}).text[:-10] + ':' + mistas[1].find("span", {"class" : "bold"}).text[:-7] + ':' + negativas[1].find("span", {"class" : "bold"}).text[:-10]

    def scrap_plataformas_notas(soup):
        # plataformas & notas_p_plataforma
        plataformas = soup.find("div", {"class" : "c-product-details__section c-product-details__section--grouped"}).find_all("li", {"class" : "c-product-details__section__list-item"})
        notas_plataformas =  soup.find_all("div", {"class" : "c-siteReviewScore_background c-siteReviewScore_background-critic_xlarge product-score-card__score"})
        plataforma_nota = ""
        for plataforma in range(len(plataformas)):
            plataforma_nota += plataformas[plataforma].text + ':' + notas_plataformas[plataforma].find("span").text + ", "

        return plataforma_nota[:-2]

    def scrap_desenvolvedora(soup):
        info_developer = soup.find("p", {"class" : "m-0 text-sm leading-7"})
        caracteristicas_developer = info_developer.find_all("span")
        if len(caracteristicas_developer) > 1:
            return caracteristicas_developer[1].text
        else:
            return info_developer.find('a').text

    def scrap_publisher(soup):
        info_publisher = soup.find_all("div", {"class" : "c-product-details__section-group c-product-details__section-group--game"})[1]
        if info_publisher.find("a", {"class" : "c-product-detail-link"}) != None:
            return info_publisher.find("a", {"class" : "c-product-detail-link"}).text
        else:
            return info_publisher.find("span", {"class" : "c-product-details__section__value"}).text

    def scrap_genero(soup):
        return soup.find("span", {"class" : "global-link-button__label"}).text

    html = requests.get(url, headers=config.headers).text
    soup = BeautifulSoup(html, "html.parser")

    metascore = scrap_metascore(soup)
    userscore = scrap_userscore(soup)

    # Se não tiver Metascore ou Userscore, evita de tentar acessar uma posição inválida da lista de p:m:n
    if metascore == userscore:
        if '.' in metascore:
            metascore = "tdb"
            pmn_meta = "tdb"
            # Meta sempre é o primeiro valor. No caso, só tem 1 valor
            pmn_user = scrap_pmn_meta(soup)
        else:
            userscore = "tdb"
            pmn_meta = scrap_pmn_meta(soup)
            pmn_user = "tdb"

    else:
        pmn_meta = scrap_pmn_meta(soup)
        pmn_user = scrap_pmn_user(soup)

    return {"nome" : scrap_nome(soup),
            "url" : url,
            "lançamento" : scrap_data_lancamento(soup),
            "metascore" : metascore,
            "qnt_meta" : scrap_qnt_meta(soup),
            "p:m:n-meta" : pmn_meta,
            "userscore" : userscore,
            "qnt_user" : scrap_qnt_user(soup),
            "p:m:n-user" : pmn_user,
            "plataforma:nota" : scrap_plataformas_notas(soup),
            "desenvolvedora" : scrap_desenvolvedora(soup),
            "publisher" : scrap_publisher(soup),
            "gênero" : scrap_genero(soup)
            }

# Sobrescreve o arquivo anterior e cria o cabeçalho
def criar_csv(nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for atributo in config.cabeçalho:
            if atributo != config.cabeçalho[-1]: arquivo.write(atributo + "  ")
            else: arquivo.write(atributo + '\n')

# Adiciona os jogos ao arquivo CSV
def append_csv(nome_arquivo, dados: dict):
    with open(nome_arquivo, 'a') as arquivo:
        for atributo in config.cabeçalho:
            if atributo != config.cabeçalho[-1]: arquivo.write(dados[atributo] + "   ")
            else: arquivo.write(dados[atributo] + '\n')

# Procura na página de browse global do Metacritic
def browse_scrapping(url, ano):
    html = requests.get(url, headers=config.headers).text
    soup = BeautifulSoup(html, "html.parser")

    # Nome do CSV em que será armazenado os dados
    nome_arquivo = "dados/jogos_por_ano/jogos" + str(ano) + ".csv"

    qnt_jogos = soup.find("span", {"class" : "hidden lg:inline text-base text-gray-500"}).text[0:-8]
    qnt_paginas = int(soup.find_all("span", {"class" : "c-navigation-pagination__item-content"})[3].text)

    criar_csv(nome_arquivo)

    pagina_atual = 1
    progresso = 0

    while pagina_atual <= qnt_paginas:

        jogos = soup.find_all("div", {"data-testid" : "filter-results"})

        for jogo in jogos:
            link_jogo = "https://www.metacritic.com" + jogo.find('a')["href"]

            # Organiza os dados do jogo. A ordem do dicionário não importa
            dados = game_scraping(link_jogo)

            # Escreve no CSV os dados do jogo atual
            append_csv(nome_arquivo, dados)            

            progresso += 1
            print(str(progresso) + '/' + qnt_jogos)

        # Executa todas as operações para o próximo loop while
        pagina_atual += 1
        html = requests.get(url + f"&page={pagina_atual}", headers=config.headers).text
        soup = BeautifulSoup(html, "html.parser")