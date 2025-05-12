###########################################################################################################################################
############################################################################################################################################
#Datos generales
select sum(can_titulos)+count(link)as sumadetitulos,sum(can_imagenes) as imagenesconalt from pagina;
#
select sum(cantidad_palabras) as PalabrasDiferentes from titulos;
#
select sum(cantidad_palabras) as PalabrasDiferentes from subtitulos;
#
select count(link) as referenciasLink from referencias where link like 'http%';
#
select sum(can_palabras) from pagina;
#
select count(activo) from referencias where activo=1;