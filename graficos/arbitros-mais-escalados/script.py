import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

conn = psycopg2.connect(
     dbname='postgres',
     user='postgres',
     password='admin',
     host='localhost',
     port='5432'
)


query = """
        SELECT a.nome, COUNT(*) AS qtd_partidas
        FROM cbf.equipe_arbitragem ea
        JOIN cbf.arbitro a ON a.id_arbitro = ea.id_arbitro
        WHERE funcao = 'Arbitro'
        GROUP BY a.nome
        ORDER BY qtd_partidas DESC
        """

df = pd.read_sql(query, conn)
conn.close()

df = df.head(50)

plt.figure(figsize=(12, 8))
plt.barh(df['nome'], df['qtd_partidas'], color='steelblue')
plt.xlabel("Quantidade de partidas")
plt.ylabel("Árbitro")
plt.title("Árbitros que mais atuaram")
plt.gca().invert_yaxis()  # Coloca o mais atuante no topo
plt.tight_layout()
plt.show()