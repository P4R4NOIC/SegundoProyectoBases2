use wordsPages;
select PalabrasXPaginas.link_pagina,PalabrasXPaginas.porcentaje,PalabrasXPaginas.veces,id_tag,tagxpalabra.porcentaje as procentajetag from PalabrasXPaginas inner join tagxpalabra on tagxpalabra.id_palabra=PalabrasXPaginas.id_palabra  where PalabrasXPaginas.id_palabra=54158;

