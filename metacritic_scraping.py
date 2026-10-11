from bs4 import BeautifulSoup
import requests

def notas(url):
	headers = {"User-Agent" : "Mozilla/5.0"}

	html = requests.get(url, headers=headers).text
	soup = BeautifulSoup(html, "html.parser")

	notas = soup.find_all("span", {"data-testid": "global-score-value"})

	return {"metascore":int(notas[0].text), "userscore":float(notas[1].text)}
