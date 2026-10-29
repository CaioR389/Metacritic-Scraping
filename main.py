import metacritic_scraping as metacritic

def main():

    #determina o escopo da estração dos dados
    while True: 
        try:
            ano_inicial = int(input("Ano inicial da extração: "))
            if ano_inicial < 1996 or ano_inicial > 2026:
                print(f"O ano {ano_inicial} está fora do intervalo, digite um ano entre 1996-2026")
                continue # se não existir o ano no metacritc

            ano_final = int(input("Ano final da extração: "))
            if ano_final < 1996 or ano_final > 2026:
                print(f"O ano {ano_final} está fora do intervalo, digite um ano entre 1996-2026")
                continue # se não existir os anos no metacritc

            break
        except ValueError:

            print(f"O ano deve ser um valor inteiro entre 1996 e 2026")

    if ano_final >= ano_inicial:
        ano_final += 1
    else:
        ano_final -= 1

    for ano in range(ano_inicial, ano_final):
        print(f"Ano de {ano}:")
        metacritic.browse_scrapping("https://www.metacritic.com/browse/game/all/all/" + str(ano) + "/metascore/?pageSize=50", ano)

if __name__ == "__main__":
	main()
