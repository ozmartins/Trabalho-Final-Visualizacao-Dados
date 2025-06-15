import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import pandas as pd
import numpy as np
import psycopg2

conn = psycopg2.connect(
     dbname='postgres',
     user='postgres',
     password='admin',
     host='localhost',
     port='5432'
)

query = """
    select a.nome, count(*) quantidade_escalacoes
    from cbf.escalacao e 
    join cbf.atleta a on a.id_atleta = e.id_atleta
    where entrou_jogando = true
    group by a.nome
"""

df = pd.read_sql(query, conn)
conn.close()

dados = df['quantidade_escalacoes'].values

kde = gaussian_kde(dados)
x = np.linspace(min(dados), max(dados), 1000)
y = kde(x)

plt.plot(x, y, label="Densidade")
plt.fill_between(x, y, alpha=0.3)
plt.title("Densidade de escalações como titular")
plt.xlabel("Quantidade de escalações")
plt.ylabel("Densidade")
plt.grid(True)
plt.legend()
plt.show()
