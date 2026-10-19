# Headers para conseguir fazer requisição
headers = {"User-Agent" : "Mozilla/5.0"}
# Cabeçalho para organização. A ordem importa. Todos os atributos listados aqui devem estar contidos na variável dados passada ao append_csv
cabeçalho = ["nome", "url", "lançamento", "metascore", "qnt_meta", "p:m:n-meta", "userscore", "qnt_user", "p:m:n-user", "plataforma:nota", "desenvolvedora", "publisher", "gênero"]

# Edita os anos que serão processados no arquivo main
# Um imput do usario fora utilizado para determinar o inicio e final do scrap para não sobrecarregar o pc.

print("Digite as datas entre os anos 1996 e 2026 para extração de dados{n}")

#força o usuário a digitar um período válido

while True: 
    try:
        ano_inicial = int(input("Ano inicial da extração: "))
        if ano_inicial < 1996 or ano_inicial > 2026:
            print(f"O ano:{ano_inicial} está fora do intervalo, digite um ano entre 1996-2026")
            continue # se não existir o ano no metacritc

        ano_final = int(input("Ano final da extração: "))
        if ano_final < 1996 or ano_final > 2026:
            print(f"O ano:{ano_final} está fora do intervalo, digite um ano entre 1996-2026")
            continue # se não existir os anos no metacritc

        break
    except ValueError:

        print(f"O ano deve ser um valor inteiro entre 1996 e 2026")

if ano_final >= ano_inicial:
    ano_final += 1
else:
    ano_final -= 1

