import requests
import time

id_campeonatos = [12583]
quantidade_rodadas = 38

for id_campeonato in id_campeonatos:
    for rodada in range(quantidade_rodadas):
        url = f"https://www.cbf.com.br/api/proxy?path=/jogos/campeonato/{id_campeonato}/rodada/{rodada}/fase/"
        response = requests.get(url)
        if (response.status_code == 200):
            print(response.text)
        time.sleep(2)