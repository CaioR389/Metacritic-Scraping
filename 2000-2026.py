import metacritic_scraping as metacritic

def main():
    for ano in range(2000, 2026):
        metacritic.browse_scrapping("https://www.metacritic.com/browse/game/all/all/" + str(ano) + "/metascore/?pageSize=50")

if __name__ == "__main__":
	main()
