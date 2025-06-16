select c.uf, count(*)
from cbf.jogo j
join cbf.estadio e on e.id_estadio = j.id_estadio
join cbf.cidade c on c.id_cidade = e.id_cidade
group by c.uf