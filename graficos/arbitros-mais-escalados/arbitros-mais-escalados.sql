select a.nome, count(*)
from cbf.equipe_arbitragem ea
join cbf.arbitro a on a.id_arbitro = ea.id_arbitro
where funcao = 'Arbitro'
group by a.nome
order by 2 desc