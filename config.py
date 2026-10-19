# Headers para conseguir fazer requisição
headers = {"User-Agent" : "Mozilla/5.0"}
# Cabeçalho para organização. A ordem importa. Todos os atributos listados aqui devem estar contidos na variável dados passada ao append_csv
cabeçalho = ["nome", "url", "lançamento", "metascore", "qnt_meta", "p:m:n-meta", "userscore", "qnt_user", "p:m:n-user", "plataforma:nota", "desenvolvedora", "publisher", "gênero"]

# Edita os anos que serão processados no arquivo main
# Um imput do usario fora utilizado para determinar o inicio e final do scrap para não sobrecarregar o pc.

