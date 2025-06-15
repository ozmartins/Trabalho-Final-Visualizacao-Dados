select to_char(j.data, 'yyyy'), j.rodada, sum(e.gols)
from cbf.evento e
join cbf.jogo j on (j.id_jogo = e.id_jogo)
group by to_char(j.data, 'yyyy'), j.rodada
order by 1,2