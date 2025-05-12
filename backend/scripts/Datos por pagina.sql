use wordsPages;
#informacion por link
select can_titulos,can_palabras,can_referencias,can_imagenes,can_palabrasximagenes from pagina where link ='https://es.wikipedia.org/wiki/1808';
#Palabras por titulos
select sum(cantidad_palabras) as PalabrasDiferentes from titulos where link_pagina ='https://es.wikipedia.org/wiki/1808';
#Palabras por subtitulos
select sum(cantidad_palabras) as PalabrasDiferentes from subtitulos where link_pagina ='https://es.wikipedia.org/wiki/1808';
#Referencias con links
select count(link) as referenciasLink from referencias where link_pagina='https://es.wikipedia.org/wiki/1808' and link like 'http%';
# Datos referencias
select nombre_cita,usos,link from referencias where link_pagina='https://es.wikipedia.org/wiki/Tecnol%C3%B3gico_de_Costa_Rica';
#palabras comunes
select palabra,veces,enTitulo from PalabrasMasComunes where link_pagina='https://es.wikipedia.org/wiki/1808';

