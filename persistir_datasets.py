import json
import psycopg2
from pathlib import Path

conn = psycopg2.connect(
     dbname='postgres',
     user='postgres',
     password='admin',
     host='localhost',
     port='5432')
            
cur = conn.cursor()

cur.execute(f"DELETE FROM cbf.penalidade")
cur.execute(f"DELETE FROM cbf.evento")
cur.execute(f"DELETE FROM cbf.equipe_arbitragem")
cur.execute(f"DELETE FROM cbf.arbitro")
cur.execute(f"DELETE FROM cbf.alteracao")
cur.execute(f"DELETE FROM cbf.documento")
cur.execute(f"DELETE FROM cbf.escalacao")
cur.execute(f"DELETE FROM cbf.clube")
cur.execute(f"DELETE FROM cbf.atleta")
cur.execute(f"DELETE FROM cbf.jogo")
cur.execute(f"DELETE FROM cbf.estadio")
cur.execute(f"DELETE FROM cbf.cidade")
cur.execute(f"DELETE FROM cbf.campeonato")

rodadas = 38
anos = [2023, 2024]

for ano in anos:    
    for rodada in range(rodadas):
        print(f'Iniciando processamento da rodada {rodada+1} de {ano}...')
        if Path(f'./datasets/tratados/{ano}.{rodada+1}.json').exists():
            with open(f'./datasets/tratados/{ano}.{rodada+1}.json', 'r', encoding='utf-8') as file:
                dataset = json.load(file)
                
                jogos = dataset['jogos'][0]['jogo']

                for jogo in jogos:
                    cur.execute(f"""
                                INSERT INTO cbf.campeonato(id_campeonato, nome) 
                                VALUES (1, '{jogos[0]['campeonato']}')
                                ON CONFLICT (nome) DO NOTHING
                                """)    

                    cur.execute(f"""
                                INSERT INTO cbf.cidade(nome, uf) VALUES ('{jogo['cidade']}', '{jogo['uf']}')
                                ON CONFLICT (nome) DO NOTHING
                                """)
                    
                    cur.execute(f"""
                                INSERT INTO cbf.estadio(nome, id_cidade) 
                                VALUES ('{jogo['estadio']}', (select id_cidade from cbf.cidade where nome = '{jogo['cidade']}'))
                                ON CONFLICT (nome) DO NOTHING
                                """)            
                    
                    data_jogo = jogo['data'].strip().replace('/','')
                    data_jogo = data_jogo[4:8]+'-'+data_jogo[2:4]+'-'+data_jogo[0:2]
                    hora_jogo = '0001-01-01 '+jogo['hora']
                    
                    cur.execute(f"""
                                INSERT INTO cbf.jogo(id_jogo, num_jogo, rodada, grupo, data, hora, qtd_alteracoes_jogo, id_campeonato, id_estadio)
                                VALUES 
                                (
                                    {jogo['id_jogo']},
                                    {jogo['num_jogo']},
                                    {jogo['rodada']},
                                    '{jogo['grupo']}', 
                                    '{data_jogo}',
                                    '{hora_jogo}', 
                                    {jogo['qtd_alteracoes_jogo']},
                                    1,
                                    (select id_estadio from cbf.estadio where nome = '{jogo['estadio']}')
                                )                            
                                """)
                    
                    for arbitro in jogo['arbitros']:
                        cur.execute(f"""
                                    INSERT INTO cbf.arbitro(id_arbitro, nome, uf, categoria)
                                    VALUES
                                    (
                                    {arbitro['id']},
                                    '{arbitro['nome']}',
                                    '{"" if arbitro['uf'] == None else arbitro['uf']}',
                                    '{arbitro['categoria']}'
                                    )
                                    ON CONFLICT (id_arbitro) DO NOTHING
                                    """)
                        
                        cur.execute(f"""
                                    INSERT INTO cbf.equipe_arbitragem(id_arbitro, id_jogo, funcao)
                                    VALUES 
                                    (
                                    {arbitro['id']},
                                    {jogo['id_jogo']},
                                    '{arbitro['funcao']}'
                                    )
                                    ON CONFLICT (id_arbitro, id_jogo) DO NOTHING
                                    """)        
                    
                    cur.execute(f"""
                                INSERT INTO cbf.clube(
                                id_clube, nome, url_escudo)
                                VALUES 
                                (
                                    {jogo['mandante']['id']},
                                    '{jogo['mandante']['nome']}',
                                    '{jogo['mandante']['url_escudo']}'                            
                                )
                                ON CONFLICT (id_clube) DO NOTHING
                                """)
                                        
                    cur.execute(f"""
                                INSERT INTO cbf.clube(
                                id_clube, nome, url_escudo)
                                VALUES 
                                (
                                    {jogo['visitante']['id']},
                                    '{jogo['visitante']['nome']}',
                                    '{jogo['visitante']['url_escudo']}'                            
                                )
                                ON CONFLICT (id_clube) DO NOTHING
                                """)
                    
                    cur.execute(f"""    
                                INSERT INTO cbf.evento(gols, penaltis, id_jogo, id_clube)
                                VALUES 
                                (
                                    {jogo['mandante']['gols']},
                                    {jogo['mandante']['panaltis']},
                                    {jogo['id_jogo']},
                                    {jogo['mandante']['id']}
                                )
                                """)
                    
                    cur.execute(f"""    
                                INSERT INTO cbf.evento(gols, penaltis, id_jogo, id_clube)
                                VALUES 
                                (
                                    {jogo['visitante']['gols']},
                                    {jogo['visitante']['panaltis']},
                                    {jogo['id_jogo']},
                                    {jogo['visitante']['id']}
                                )
                                """)
                            
                    for atleta in jogo['mandante']['atletas']:
                        cur.execute(f"""
                                    INSERT INTO cbf.atleta(id_atleta, nome, apelido, foto)
                                    VALUES 
                                    (
                                        {atleta['id']},
                                        '{atleta['nome']}',
                                        '{atleta['apelido']}',
                                        '{atleta['foto']}'
                                    )
                                    ON CONFLICT (id_atleta) DO NOTHING
                                    """)
                        
                        cur.execute(f"""
                                    INSERT INTO cbf.escalacao
                                    (
                                        numero_camisa, 
                                        reserva, 
                                        goleiro, 
                                        entrou_jogando, 
                                        id_atleta, 
                                        id_clube, 
                                        id_jogo
                                    )
                                    VALUES 
                                    (
                                        {atleta['numero_camisa']},
                                        {atleta['reserva']},
                                        {atleta['goleiro']},
                                        {atleta['entrou_jogando']},
                                        {atleta['id']},
                                        {jogo['mandante']['id']},
                                        {jogo['id_jogo']}
                                    )
                                    """)
                                
                    for atleta in jogo['visitante']['atletas']:
                        cur.execute(f"""
                                    INSERT INTO cbf.atleta(id_atleta, nome, apelido, foto)
                                    VALUES 
                                    (
                                        {atleta['id']},
                                        '{atleta['nome']}',
                                        '{atleta['apelido']}',
                                        '{atleta['foto']}'
                                    )
                                    ON CONFLICT (id_atleta) DO NOTHING
                                    """)
                        
                        cur.execute(f"""
                                    INSERT INTO cbf.escalacao
                                    (
                                        numero_camisa, 
                                        reserva, 
                                        goleiro, 
                                        entrou_jogando, 
                                        id_atleta, 
                                        id_clube, 
                                        id_jogo
                                    )
                                    VALUES 
                                    (
                                        {atleta['numero_camisa']},
                                        {atleta['reserva']},
                                        {atleta['goleiro']},
                                        {atleta['entrou_jogando']},
                                        {atleta['id']},
                                        {jogo['visitante']['id']},
                                        {jogo['id_jogo']}
                                    )
                                    """)            
                                    
                    for alteracao in jogo['mandante']['alteracoes']:
                        cur.execute(f"""
                                    INSERT INTO cbf.alteracao
                                    (
                                        codigo_jogador_saiu, 
                                        codigo_jogador_entrou, 
                                        tempo_jogo, 
                                        tempo_subs, 
                                        tempo_acrescimo, 
                                        id_jogo, 
                                        id_clube
                                    )
                                    VALUES 
                                    (
                                        {alteracao['codigo_jogador_saiu']}, 
                                        {alteracao['codigo_jogador_entrou']}, 
                                        '0001-01-01 00:{"00:00" if alteracao['tempo_jogo'] == None else alteracao['tempo_jogo']}', 
                                        '{alteracao['tempo_subs']}', 
                                        '0001-01-01 00:{"00:00" if alteracao['tempo_acrescimo'] == None else alteracao['tempo_acrescimo']}', 
                                        {jogo['id_jogo']},
                                        {jogo['visitante']['id']}
                                    );
                                    """)
                                
                    for alteracao in jogo['visitante']['alteracoes']:
                        cur.execute(f"""
                                    INSERT INTO cbf.alteracao
                                    (
                                        codigo_jogador_saiu, 
                                        codigo_jogador_entrou, 
                                        tempo_jogo, 
                                        tempo_subs, 
                                        tempo_acrescimo, 
                                        id_jogo, 
                                        id_clube
                                    )
                                    VALUES 
                                    (
                                        {alteracao['codigo_jogador_saiu']}, 
                                        {alteracao['codigo_jogador_entrou']}, 
                                        '0001-01-01 00:{"00:00" if alteracao['tempo_jogo'] == None else alteracao['tempo_jogo']}', 
                                        '{alteracao['tempo_subs']}', 
                                        '0001-01-01 00:{"00:00" if alteracao['tempo_acrescimo'] == None else alteracao['tempo_acrescimo']}', 
                                        {jogo['id_jogo']},
                                        {jogo['visitante']['id']}
                                    );
                                    """)        
                        
                    for documento in jogo['documentos']:
                        cur.execute(f"""
                                    INSERT INTO cbf.documento(url, title, id_jogo)
                                    VALUES 
                                    (                        
                                    '{documento['url']}', 
                                    '{documento['title']}', 
                                    {jogo['id_jogo']}
                                    )
                                    """)
                        
                    for penalidade in jogo['penalidades']:
                        cur.execute(f"""
                                    INSERT INTO cbf.penalidade
                                    (
                                        id_penalidade, 
                                        tipo, 
                                        resultado, 
                                        tempo_jogo, 
                                        minutos                                    
                                    )
                                    VALUES 
                                    (
                                        {penalidade['id']}, 
                                        '{penalidade['tipo']}',
                                        '{penalidade['resultado']}',
                                        '{penalidade['tempo_jogo']}', 
                                        '0001-01-01 00:{penalidade['minutos'][0:4]}'
                                    )
                                    """)
                    
                conn.commit()                    