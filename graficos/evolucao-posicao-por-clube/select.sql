select
    ano,
    rodada,
    clube,
    row_number() over (
        partition by ano, rodada 
        order by pontos_acumulados desc, gols_acumulados desc, clube asc
    ) as posicao
from (
    select
        to_char(data, 'yyyy') as ano,
        rodada,
        nome as clube,
        sum(pontos) over (
            partition by nome, to_char(data, 'yyyy')
            order by rodada
            rows between unbounded preceding and current row
        ) as pontos_acumulados,
        sum(gols) over (
            partition by nome, to_char(data, 'yyyy')
            order by rodada
            rows between unbounded preceding and current row
        ) as gols_acumulados
    from (
                    select
                j.data,
                j.rodada,
                cm.nome,
                em.gols,
                case 
                when em.gols > ev.gols then 3
                when em.gols < ev.gols then 0
                else 1
            end as pontos
            from cbf.jogo j
                join cbf.evento em on em.id_jogo = j.id_jogo and em.id_clube = j.id_clube_mandante
                join cbf.evento ev on ev.id_jogo = j.id_jogo and ev.id_clube = j.id_clube_visitante
                join cbf.clube cm on cm.id_clube = j.id_clube_mandante

        union all

            select
                j.data,
                j.rodada,
                cv.nome,
                ev.gols,
                case 
                when ev.gols > em.gols then 3
                when ev.gols < em.gols then 0
                else 1
            end as pontos
            from cbf.jogo j
                join cbf.evento em on em.id_jogo = j.id_jogo and em.id_clube = j.id_clube_mandante
                join cbf.evento ev on ev.id_jogo = j.id_jogo and ev.id_clube = j.id_clube_visitante
                join cbf.clube cv on cv.id_clube = j.id_clube_visitante        
    ) as partidas
) as acumulado
where ano in ('2018', '2022', '2023', '2024')
order by ano, rodada, posicao;
