import metacritic_scraping as metacritic

def main():
	notas_jogo = metacritic.notas("https://www.metacritic.com/game/elden-ring/")

	print(notas_jogo)

if __name__ == "__main__":
	main()
