import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

import config

# Adquire as notas de críticos e usuários
# Notas iguais (metascore = userscore) significa que não tem dados de um deles, e substitui pelo outro
def game_scraping(url):
    def scrap_nome(soup):
        return soup.find("h1", {"class" : "text-4xl font-bold text-[#333]"}).text

    def scrap_data_lancamento(soup):
        tabela_data = {"Jan" : "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", "May" : "05", "Jun" : "06", "Jul" : "07", "Aug" : "08", "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"}

        # Tinha um jogo sem data de lançamento, por isso essa manipulação toda só para pegar a data
        try:
            data_lançamento = soup.find("div", {"class" : "inline-block uppercase"}).text
            if len(data_lançamento) == 11:
                data_lançamento = f"0{data_lançamento[4]}/{tabela_data[data_lançamento[0:3]]}/{data_lançamento[-4:]}"
            else:
                data_lançamento = f"{data_lançamento[4:6]}/{tabela_data[data_lançamento[0:3]]}/{data_lançamento[-4:]}"

        except AttributeError:
            data_lançamento = "tdb"

        return data_lançamento

    def scrap_metascore(soup):
        reviews = soup.find_all("div", {"data-testid" : "global-score-wrapper"})

        for review in reviews:
            if review.find("div", {"data-testid" : "global-score-header"}).text == "Metascore":
                return review.find("div", {"data-testid" : "global-score-value-wrapper"}).find("span").text

        return soup.find("span", {"data-testid" : "global-score-value"}).text

    def scrap_qnt_meta(soup):
        reviews = soup.find_all("div", {"data-testid" : "global-score-wrapper"})
        
        for review in reviews:
            if review.find("div", {"data-testid" : "global-score-header"}).text == "Metascore":
                try:
                    return review.find("a", {"data-testid" : "global-score-review-count-link"}).text[9:-15]
                except AttributeError:
                    return "tdb"

    def scrap_pmn_meta(soup):
        reviews = soup.find_all("div", {"class" : "flex flex-col lg:flex-row gap-5 pt-6 pb-4"})

        for review in reviews:
            try:
                if review.find("div", {"data-testid" : "global-score-header"}).text == "Metascore":
                    p_m_n = review.find("div", {"class" : "grid grid-cols-[repeat(3,1fr)] justify-evenly gap-0 px-0 py-4 text-center text-[0.75rem] leading-5 font-normal"}).find_all("div")

                    positiva = p_m_n[0].find("span").text
                    mista = p_m_n[1].find("span").text
                    negativa = p_m_n[2].find("span").text
                                
                    return positiva[:-10] + ':' + mista[:-7] + ':' + negativa[:-10]

            # Não é uma review
            except AttributeError:
                continue

        return "tdb"
            
    def scrap_userscore(soup):
        reviews = soup.find_all("div", {"data-testid" : "global-score-wrapper"})

        for review in reviews:
            if review.find("div", {"data-testid" : "global-score-header"}).text == "User score":
                return review.find("div", {"data-testid" : "global-score-value-wrapper"}).find("span").text

    def scrap_qnt_user(soup):
        reviews = soup.find_all("div", {"data-testid" : "global-score-wrapper"})
        
        for review in reviews:
            if review.find("div", {"data-testid" : "global-score-header"}).text == "User score":
                try:
                    return review.find("a", {"data-testid" : "global-score-review-count-link"}).text[9:-13]
                except AttributeError:
                    return "tdb"

    def scrap_pmn_user(soup):
        reviews = soup.find_all("div", {"class" : "flex flex-col lg:flex-row gap-5 pt-6 pb-4"})

        for review in reviews:
            try:
                 if review.find("div", {"data-testid" : "global-score-header"}).text == "User score":
                    p_m_n = review.find("div", {"class" : "grid grid-cols-[repeat(3,1fr)] justify-evenly gap-0 px-0 py-4 text-center text-[0.75rem] leading-5 font-normal"}).find_all("div")
                
                    positiva = p_m_n[0].find("span").text
                    mista = p_m_n[1].find("span").text
                    negativa = p_m_n[2].find("span").text
                                                
                    return positiva[:-10] + ':' + mista[:-7] + ':' + negativa[:-10]

            # Não é uma review
            except AttributeError:
                continue

        return "tdb"

    def scrap_plataformas_notas(soup):
        todas_plataformas = soup.find("div", {"data-testid" : "all-platforms"})

        try:
            plataforma_nota = todas_plataformas.find("div", {"data-testid" : "product-score-card"}).find("div", {"class" : "inline-block leading-0"}).find("span")["title"] + ':' + todas_plataformas.find("div", {"data-testid" : "product-score-card"}).find("div", {"class" : "c-siteReviewScore_background c-siteReviewScore_background-critic_xlarge shrink-0"}).find("span").text + ", "
        except AttributeError:
            plataforma_nota = ""

        plataformas = todas_plataformas.find_all("a", {"data-testid" : "product-score-card"})
        for plataforma in plataformas:
            try:
                nome_plataforma = plataforma.find("div", {"class" : "inline-block leading-0"}).find("span")["title"]
            except AttributeError:
                nome_plataforma = plataforma.find("div", {"class" : "game-platform-logo__text truncate font-[family-name:var(--font-family-body,'Proxima_Nova',sans-serif)] text-[1.5rem] leading-8 font-bold text-black"}).text

            nota_plataforma = plataforma.find("div", {"class" : "c-siteReviewScore_background c-siteReviewScore_background-critic_xlarge shrink-0"}).find("span").text

            try:
                plataforma_nota += nome_plataforma + ':' + nota_plataforma + ", "
            except AttributeError:
                continue

        return plataforma_nota[:-2]

    def scrap_desenvolvedora(soup):
        try: 
            info_developer = soup.find("p", {"class" : "m-0 text-sm leading-7"})
            caracteristicas_developer = info_developer.find_all("span")
            if len(caracteristicas_developer) > 1:
                return caracteristicas_developer[1].text
            else:
                return info_developer.find('a').text

        except AttributeError:
            return "tbd"

    def scrap_publisher(soup):
        try: 
            info_publisher = soup.find("div", {"data-testid" : "game-details"}).find_all("div", {"class" : "flex items-baseline gap-4 max-md:flex-row max-md:gap-2 [&_.c-genreList]:m-0 min-h-[unset] bg-transparent p-0"})[2]

            if info_publisher.find("a", {"class" : "inline text-[0.875rem] text-gray-500 underline transition-[color] duration-200 ease-[ease] [word-break:break-word] hover:text-gray-600 hover:no-underline"}) != None:
                publisher = info_publisher.find("a", {"class" : "inline text-[0.875rem] text-gray-500 underline transition-[color] duration-200 ease-[ease] [word-break:break-word] hover:text-gray-600 hover:no-underline"}).text
            elif info_publisher.find("span", {"class" : "c-product-details__section__value block text-gray-700"}) != None:
                publisher = info_publisher.find("span", {"class" : "c-product-details__section__value block text-gray-700"}).text
            else:
                publisher = None

            if publisher != None:
                return publisher
            else:
                return "tdb"

        except AttributeError:
            return "tbd"

    def scrap_genero(soup):
        try:
            return soup.find('a', {"class" : "inline-flex cursor-pointer flex-row items-center justify-center gap-2 rounded-sm border border-solid no-underline [transition:all_0.15s_ease] focus-visible:outline-2 focus-visible:outline-offset-[0.125rem] focus-visible:outline-current focus-visible:outline-solid font-[family-name:var(--font-family-body,'Proxima_Nova',sans-serif)] h-8 px-3 text-[0.875rem] leading-[1.625rem] font-normal max-md:px-1 border-(--color-bg-brand-primary-default) bg-(--color-bg-brand-primary-default) text-(--color-text-grayscale-primary-default) hover:border-(--color-bg-brand-primary-hover) hover:bg-(--color-bg-brand-primary-hover) hover:text-(--color-text-grayscale-primary-default) active:border-(--color-bg-brand-primary-pressed) active:bg-(--color-bg-brand-primary-pressed)"}).find("span", {"class" : "leading-none"}).text
        
        except AttributeError:
            return "tdb"

    html = requests.get(url, headers=config.headers).text
    soup = BeautifulSoup(html, "html.parser")

    while True:
        try:
            scrap_nome(soup)
            break
        except AttributeError:
            print("Deu pau. Esperando 10 minutos para a próxima requisição.")

            sleep(600)

            html = requests.get(url, headers=config.headers).text
            soup = BeautifulSoup(html, "html.parser")

    return {"nome" : scrap_nome(soup),
            "url" : url,
            "lançamento" : scrap_data_lancamento(soup),
            "metascore" : scrap_metascore(soup),
            "qnt_meta" : scrap_qnt_meta(soup),
            "p:m:n-meta" : scrap_pmn_meta(soup),
            "userscore" : scrap_userscore(soup),
            "qnt_user" : scrap_qnt_user(soup),
            "p:m:n-user" : scrap_pmn_user(soup),
            "plataforma:nota" : scrap_plataformas_notas(soup),
            "desenvolvedora" : scrap_desenvolvedora(soup),
            "publisher" : scrap_publisher(soup),
            "gênero" : scrap_genero(soup)
            }

# Sobrescreve o arquivo anterior e cria o cabeçalho"
def criar_csv(nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for atributo in config.cabeçalho:
            if atributo != config.cabeçalho[-1]: arquivo.write(atributo + "\t")
            else: arquivo.write(atributo + '\n')

# Adiciona os jogos ao arquivo CSV
def append_csv(nome_arquivo, dados: dict):
    with open(nome_arquivo, 'a') as arquivo:
        for atributo in config.cabeçalho:
            if atributo != config.cabeçalho[-1]: arquivo.write(dados[atributo] + "\t")
            else: arquivo.write(dados[atributo] + '\n')

# Procura na página de browse global do Metacritic
def browse_scraping(url, ano: str, sobrescrever: bool):
    html = requests.get(url, headers=config.headers).text
    soup = BeautifulSoup(html, "html.parser")

    # Nome do CSV em que será armazenado os dados
    nome_arquivo = "jogos_por_ano/jogos" + str(ano) + ".csv"

    if sobrescrever:
        criar_csv(nome_arquivo)

    else:
        try:
            links_acessados = set(pd.read_csv(nome_arquivo, sep='\t')["url"])
        except FileNotFoundError:
            criar_csv(nome_arquivo)
            links_acessados = set()

    while True:
            try:
                qnt_jogos = soup.find("span", {"class" : "hidden lg:inline text-base text-gray-500"}).text[0:-8]
                qnt_paginas = int(soup.find_all("span", {"class" : "flex items-center justify-center min-w-8 h-8 p-3 rounded-[100px] font-bold text-gray-800 group-hover/item:bg-gray-100"})[1].text)
                break
            except AttributeError:
                print("Deu pau. Esperando 10 minutos para a próxima requisição.")
    
                sleep(600)
    
                html = requests.get(url, headers=config.headers).text
                soup = BeautifulSoup(html, "html.parser")

    pagina_atual = 1
    progresso = 0

    while pagina_atual <= qnt_paginas:

        jogos = soup.find_all("div", {"data-testid" : "filter-results"})

        for jogo in jogos:
            link_jogo = "https://www.metacritic.com" + jogo.find('a')["href"]
            if sobrescrever == False:
                if link_jogo in links_acessados:
                    progresso += 1
                    continue

            # Organiza os dados do jogo. A ordem do dicionário não importa
            dados = game_scraping(link_jogo)

            # Escreve no CSV os dados do jogo atual
            append_csv(nome_arquivo, dados)            

            progresso += 1
            print(f"{ano}: {str(progresso)}/{qnt_jogos}")

        # Executa todas as operações para o próximo loop while
        pagina_atual += 1
        html = requests.get(url + f"&page={pagina_atual}", headers=config.headers).text
        soup = BeautifulSoup(html, "html.parser")
