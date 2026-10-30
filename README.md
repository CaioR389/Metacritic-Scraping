# Projeto de Análise de Dados do Metacritic

 - **2** O foco deste projeto é analisar dados de jogos lançados entre 2000 e 2026 na plataforma Metacritic e comparar avalições dos críticos e usuários ao longo dos anos, assim como a distribuição das notas.
 -
 - **3**
 -   *3.1* -A função browse_scraping percorre todos os jogos de determinado ano seguindo a página de browse do metacritic, e escrevendo os dados retirados através de game_scraping em um arquivo .csv        função scrap_metacritic percorre os anos que o usuário escolher, chamando o browse para cada ano, que então escreve no arquivo .csv
       Dados indisponíveis são determinados "tdb" (to be determinated).

 -    *3.2* -O arquivo config.py funciona como um indicador na formatação do csv (cabeçalho)
 -    *3.3* -Em Metacritic-Scraping é feito a extração dos dados de avaliações presentes no site: https://www.metracritc.com, apartir da ferramenta beutifulsoup4 (biblioteca python).  

 -    
 - **4** São este o conjunto de dados e avaliações de profissionais, usuários comuns da comunidade gamer e "crítica": Nome do jogo
   Sobre o arquivo -Metacritc-Scraping:

   -*representação ilustrativa da saída*
   
   | Nome| url | metascore | userscore  | qnt_meta |  qnt_user |desenvolvedora |publisher | gênero | ANO |
   |-----|-----|-----------|-------------|----------|----------|---------------|----------|--------|-----| 
   |jogo1|url1 |    0-5    |     0-10    | qntmeta1 | qntuser1 |desenvolvedora1|publisher1|gênero1 |ANOx |
   |jogo2|url2 |    0-5    |     0-10    | qntmeta2 | qntuser2 |desenvolvedora2|publisher2|gênero2 |ANOy |
   |jogo3|url3 |    0-5    |     0-10    | qntmeta3 | qntuser3 |desenvolvedora3|publisher3|gênero3 |ANOz |
   |.....|.....|    0-5    |     0-10    |..........|..........|...............|..........|........|.....|
   |jogoN|urlN |    0-5    |     0-10    | qntmetaN | qntuserN |desenvolvedoraN|publishern|gêneroN |ANON |
   -------------------------------------------------------------------------------------------------------
   
## O que este projeto faz, exatamente?
- **Coleta de dados (Data Scraping)**

- **Estruturação em formato CSV**

- **Análise comparativa**

## O que exatamente analisamos e comparamos?
- **Convergência vs. Divergência**

- **Evolução histórica**

- **Classificações (Rankings)**

## Tecnologias
- **Python 3**

## Observações
