import metacritic_scraping as metacritic

def main():
    for ano in range(2000, 2026):
        print(f"Ano de {ano}:")
        metacritic.browse_scrapping("https://www.metacritic.com/browse/game/all/all/" + str(ano) + "/metascore/?pageSize=50", str(ano))

if __name__ == "__main__":
	main()
