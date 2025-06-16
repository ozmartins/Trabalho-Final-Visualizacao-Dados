import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

url_geojson = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
estados = gpd.read_file(url_geojson)

estados['uf'] = estados['name'].map({
    'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM',
    'Bahia': 'BA', 'Ceará': 'CE', 'Distrito Federal': 'DF', 'Espírito Santo': 'ES',
    'Goiás': 'GO', 'Maranhão': 'MA', 'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS',
    'Minas Gerais': 'MG', 'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR',
    'Pernambuco': 'PE', 'Piauí': 'PI', 'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS', 'Rondônia': 'RO', 'Roraima': 'RR', 'Santa Catarina': 'SC',
    'São Paulo': 'SP', 'Sergipe': 'SE', 'Tocantins': 'TO'
})

dados_jogos = pd.DataFrame({
    'uf': ['SP', 'RJ', 'MG', 'RS', 'BA'],
    'qtd_jogos': [320, 270, 190, 150, 140]
})

estados = estados.merge(dados_jogos, on='uf', how='left')
estados['qtd_jogos'] = estados['qtd_jogos'].fillna(0)

fig, ax = plt.subplots(figsize=(12, 10))
estados.plot(
    column='qtd_jogos',
    cmap='OrRd',
    linewidth=0.8,
    edgecolor='black',
    legend=True,
    ax=ax
)

ax.set_title('Quantidade de Jogos por Estado', fontsize=16)
ax.axis('off')
plt.show()
