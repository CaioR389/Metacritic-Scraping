import metacritic_scraping as metacritic

import config

def main():
    # Se quiser mudar o ano, edite o config.py. Se quiser apenas um ano, coloque-o como inicial e o seguinte como final (ex: 2000 e 2001)
    for ano in range(config.ano_inicial, config.ano_final + 1):
        print(f"Ano de {ano}:")
        metacritic.browse_scrapping("https://www.metacritic.com/browse/game/all/all/" + str(ano) + "/metascore/?pageSize=50", str(ano))

if __name__ == "__main__":
	main()
