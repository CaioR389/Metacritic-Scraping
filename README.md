# Projeto de Análise de Dados do Metacritic

 - **2** O foco deste projeto é analisar dados de jogos lançados entre 2000 e 2026 na plataforma Metacritic e comparar avalições dos críticos e usuários ao longo dos anos, assim como a distribuição das notas.
 -
 - **3**
 -   *3.1* -A função browse_scraping percorre todos os jogos de determinado ano seguindo a página de browse do metacritic, e escrevendo os dados retirados através de game_scraping em um arquivo .csv        função scrap_metacritic percorre os anos que o usuário escolher, chamando o browse para cada ano, que então escreve no arquivo .csv
       Dados indisponíveis são determinados "tdb" (to be determinated)

 -    *3.2* -O arquivo config.py funciona como um indicador na formatação do csv (cabeçalho)
 -    
 - **4** São este o conjunto de dados e avaliações de profissionais, usuários comuns da comunidade gamer e "crítica": Nome do jogo
   Sobre o arquivo -Metacritc-Scraping:

   | Nome| url | Nota profissional | Nota users  |
   |-----|-----|-------------------|-------------|
   |jogo1|url1 |       0-10       |    0-10    |
   |jogo2|url2 |       0-10       |    0-10    |
   |jogo3|url3 |       0-10       |    0-10    |
   |jogo...|url...|       0-10       |    0-10    |
   |jogoN|urlN |       0-10       |    0-10    |
   
-   Em Metacritic-Scraping é feito a extração dos dados apartir do beutifulsoup4, e extraido do site Metacritc dados das demais avaliações de usuários e analistas profissionais;   
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
