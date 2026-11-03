# Projeto de API do Metacritic

 **2** O foco deste projeto é analisar dados de jogos lançados entre 2000 e 2026 na plataforma Metacritic e comparar avaliações dos críticos e usuários ao longo dos anos, assim como a distribuição das notas.

 **3**
   *3.1* - A função `browse_scraping` percorre todos os jogos de determinado ano seguindo a página de browse do Metacritic, e escrevendo os dados retirados através de `game_scraping` em um arquivo `.csv`. A função `scrap` percorre os anos que o usuário escolher, chamando o browse para cada ano, que então escreve no arquivo `.csv`.
   Dados indisponíveis são determinados "tdb" (to be determinated).

   *3.2* - O arquivo `config_scraping.py` funciona como um indicador na formatação do csv (cabeçalho).

   *3.3* - Em Metacritic-Scraping é feita a extração dos dados de avaliações presentes no site: https://www.metacritic.com, a partir da ferramenta BeautifulSoup4 (biblioteca python).  

 **4** São este o conjunto de dados e avaliações de profissionais, usuários comuns da comunidade gamer e "crítica":

| nome  | url  | lancamento | metascore | qnt_meta | pmn_meta | userscore | qnt_user | pmn_user | plataforma_nota | desenvolvedora | publisher | genero | ano  |
|-------|------|------------|-----------|----------|----------|-----------|----------|----------|-----------------|----------------|-----------|--------|------|
| jogo1 | url1 | data1      | 0-100     | qntmeta1 | p:m:n 1  | 0.0-10.0  | qntuser1 | p:m:n 1  | plat:nota 1     | dev1           | pub1      | gen1   | ano1 |
| jogo2 | url2 | data2      | 0-100     | qntmeta2 | p:m:n 2  | 0.0-10.0  | qntuser2 | p:m:n 2  | plat:nota 2     | dev2           | pub2      | gen2   | ano2 |
| jogo3 | url3 | data3      | 0-100     | qntmeta3 | p:m:n 3  | 0.0-10.0  | qntuser3 | p:m:n 3  | plat:nota 3     | dev3           | pub3      | gen3   | ano3 |
| ..... | .... | .......... | ......... | ........ | ........ | ......... | ........ | ........ | ............... | .............. | ......... | ...... | .... |
| jogoN | urlN | dataN      | 0-100     | qntmetaN | p:m:n N  | 0.0-10.0  | qntuserN | p:m:n N  | plat:nota N     | devN           | pubN      | genN   | anoN |
--------------------------------------------------------------------------------------------------------------------------------------------------------------
*representação ilustrativa da saída*

**Dicionário de Dados:**
* **nome:** Título do jogo. Ex: *The Legend of Zelda: Ocarina of Time*
* **url:** Link da página do jogo. Ex: *https://www.metacritic.com/game/...*
* **lancamento:** Data exata de lançamento. Ex: *23/11/1998*
* **metascore:** Nota da crítica especializada (0 a 100). Ex: *99*
* **qnt_meta:** Número total de análises da crítica. Ex: *22*
* **pmn_meta:** Porcentagem de avaliações críticas positivas, mistas e negativas, respectivamente. Separados por ':'. Ex: *100:0:0*
* **userscore:** Nota média atribuída pelos usuários (0.0 a 10.0). Ex: *9.1*
* **qnt_user:** Número total de avaliações do público. Ex: *7500*
* **pmn_user:** Porcentagem de avaliações de usuários positivas, mistas e negativas, respectivamente. Separados por ':'. Ex: *90:4:6*
* **plataforma_nota:** Notas divididas por plataforma. Separados por ','. Ex: *Nintendo 64:99*
* **desenvolvedora:** Estúdio responsável pela criação do jogo. Ex: *Nintendo*
* **publisher:** Empresa distribuidora. Ex: *Nintendo*
* **genero:** Categoria em que o jogo se enquadra. Ex: *Action Adventure*

## RESUMO  
# O que este projeto faz, exatamente?
- **Coleta de dados (Data Scraping)**
- **Estruturação em formato CSV**
- **Análise comparativa**

# O que exatamente analisamos e comparamos?
- **Convergência vs. Divergência**
- **Evolução histórica**
- **Classificações (Rankings)**

# Tecnologias
- **Python3**

# Observações
*Em alguns jogos, devido a má organização da distribuidora, pode ocasionar ou não em erros na extração de dados*

*Não recomendados, embora seja possível, a extração de dados dos anos 1996-1999; pois a quantidade de jogos disponíveis e a organização destes dados durante o período: 1996-1999, são terríveis* 
