import json
from pathlib import Path

years = [2024]#, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006]

rounds_per_year = 38

for year in years:
    for round in range(rounds_per_year):
        original_file_name = f'./originais/{year}.{round+1}.json'
        treated_file_name = f'./tratados/{year}.{round+1}.json'
        if Path(original_file_name).exists():
            with open(original_file_name, 'r', encoding='utf-8') as file_for_reading:
                data = json.load(file_for_reading)            
                for game in data['jogos'][0]['jogo']:
                    #remove o número da camisa do nome e do apelido dos atletas do time mandante
                    for athlet in game['mandante']['atletas']:                    
                        name = athlet['nome']
                        nick = athlet['apelido']
                        if '-' in name:
                            name = name.split('-')[1].strip()
                        if '-' in nick:
                            nick = nick.split('-')[1].strip()                    
                        athlet['nome'] = name
                        athlet['apelido'] = nick
                    
                    #remove o número da camisa do nome e do apelido dos atletas do time visitante
                    for athlet in game['visitante']['atletas']:                    
                        name = athlet['nome']
                        nick = athlet['apelido']
                        if '-' in name:
                            name = name.split('-')[1].strip()
                        if '-' in nick:
                            nick = nick.split('-')[1].strip()                    
                        athlet['nome'] = name
                        athlet['apelido'] = nick

                    #desmembra o local da partida em estádio, cidade e UF
                    place = game['local']
                    if ('-' in place):
                        if ('Beira-Rio' in place):
                            place = place.replace('Beira-Rio', 'Beira Rio')
                        
                        stadium = place.split('-')[0].strip()
                        city = place.split('-')[1].strip()
                        state = place.split('-')[2].strip()                    

                        game.pop('local')
                        game['estadio'] = stadium
                        game['cidade'] = city
                        game['uf'] = state 

                    #remove o arbrito "Radar" que consta em todas as partidas
                    referees_to_remove = []
                    for i in range(len(game['arbitros'])):
                        if game['arbitros'][i]['nome'].lower().strip() == 'radar':
                            referees_to_remove.append(i)
                    for i in referees_to_remove[::-1]:
                        del game['arbitros'][i]

                    #remove o arbrito "Radar" que consta em todas as partidas                
                    for event in game['penalidades']:
                        team = event['clube']
                        if '-' in team:
                            team_name = team.split('-')[0].strip().replace('Saf', '').replace('S.a.f.', '')
                            team_state = team.split('-')[1].strip()
                        event.pop('clube')
                        event['clube_nome'] = team_name
                        event['clube_uf'] = team_state
                        
                        if event['tempo_jogo'] in ['1', '2']:
                            event['tempo_jogo'] = 'TN' + event['tempo_jogo'].strip()                        

                
                #salva o arquivo tratado em outra pasta
                with open(treated_file_name, 'w', encoding='utf-8') as file_for_writing:
                    json.dump(data, file_for_writing, ensure_ascii=False, indent=4)