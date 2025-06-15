select a.nome, count(*) quantidade_escalacoes
from cbf.escalacao e 
join cbf.atleta a on a.id_atleta = e.id_atleta
where entrou_jogando = true
group by a.nome