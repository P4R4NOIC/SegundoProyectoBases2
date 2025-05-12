import express from "express";
import cors from "cors";
import body_Parser from "body-parser";
import mariadb from "mariadb";
import natural from "natural";
const app = express();
const stemmer = natural.PorterStemmer;
app.use(body_Parser.json());
app.use(cors());
app.use(express.json({
    type: "*/*"
}))
app.use(
    express.urlencoded({
      extended: true
    })
)
const pool = mariadb.createPool({
    host: 'localhost', 
    user:'root', 
    password: 'gabo1',
    port:'3307',
    database: 'wordsPages',
    connectionLimit: 5
});

app.get('/paginas', async (req, res) => {
    const query = 'SELECT titulo_principal,link FROM pagina';  // Reemplaza 'tu_tabla' con el nombre de tu tabla
  
    // Obtener una conexión del pool
    try{
        const connection= await pool.getConnection();
        const rows =await connection.query(query);
        connection.release()
        res.status(200).json(rows)
        
    }catch(error){
        console.log(error)
    }


});
app.get('/palabra/:palabra', async (req, res) => {
    const pal = req.params.palabra;
    const stemm_pal = stemmer.stem(pal);
    
    const queryid = 'SELECT id FROM Palabra WHERE palabra=?';
    const query = 'SELECT PalabrasXPaginas.link_pagina, PalabrasXPaginas.porcentaje, PalabrasXPaginas.veces, id_tag, tagxpalabra.porcentaje AS porcentajeTag FROM PalabrasXPaginas INNER JOIN tagxpalabra ON tagxpalabra.id_palabra = PalabrasXPaginas.id_palabra WHERE PalabrasXPaginas.id_palabra=?;';

    // Obtener una conexión del pool
    try {
        const connection = await pool.getConnection();
        
        // Ejecutar el primer query para obtener el id
        const [idRows] = await connection.query(queryid, [stemm_pal]);
        
        // Verificar si se obtuvo un resultado
        if ([idRows].length > 0) {
            
            const id = idRows.id;

            // Ejecutar el segundo query utilizando el id obtenido
            const rows = await connection.query(query, [id]);
            var paginas=[]
            var porcentaje_total=0;
            var porcentaje_subtitulos=0;
            var porcentaje_titulos=0;
            var porcentaje_texto= 0;
            for(const r of rows ){
                paginas.push({
                    "direccion":r.link_pagina,
                    "numero":r.veces                    
                })
                
                if(r.porcentaje>0){
                    
                    porcentaje_total=  parseFloat(r.porcentaje)
                    
                }
                
                if(r.porcentajeTag >0){
                
                    if (r.id_tag === 6){

                        porcentaje_titulos=  parseFloat(r.porcentajeTag)
                        
                        

                    }else if(r.id_tag===7){
                        porcentaje_subtitulos = parseFloat(r.porcentajeTag)
                       
                    }else if(r.id_tag === 8){
                        porcentaje_subtitulos = parseFloat(r.porcentajeTag)
                    } 
                    else{
                        porcentaje_texto = parseFloat(r.porcentajeTag)
                    }
                }
            }
            const data = {
                "palabra":pal,
                "paginas":paginas,
                "porcentajeTodasPaginas":porcentaje_total,
                "porcentajeTitulos":porcentaje_titulos,
                "porcentajeSubtitulos":porcentaje_subtitulos,
                "porcentajeTexto":porcentaje_texto

            }

            
            // Enviar la respuesta
            res.status(200).json(data);
        } else {
            // Si no se encontró ningún resultado para la palabra
            res.status(404).json({ message: 'Palabra no encontrada' });
        }

        // Liberar la conexión de vuelta al pool
        connection.release();
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error en el servidor' });
    }
});


app.get('/generales', async (req, res) => {
    const query1 = `SELECT sum(can_titulos)+count(link)as sumadetitulos,sum(can_imagenes) as imagenesconalt from pagina`;
    const query2 = 'SELECT sum(cantidad_palabras) as PalabrasDiferentes from titulos;';
    const query3= 'SELECT sum(cantidad_palabras) as PalabrasDiferentes from subtitulos;';
    const query4 = `SELECT count(link) as referenciasLink from referencias where link like 'http%';`;
    const query5 = 'SELECT sum(can_palabras) as palabraspagina from pagina;';
    const query6 = 'SELECT count(activo) as refactivas from referencias where activo=1;';

    // Obtener una conexión del pool
    try {
        const connection = await pool.getConnection();
        const rows1 = await connection.query(query1);
        const rows2= await connection.query(query2);
        const rows3 = await connection.query(query3);
        const rows4 = await connection.query(query4);
        const rows5 = await connection.query(query5);
        const rows6 = await connection.query(query6);

        var cantidadTitulos = 0
        var cantidadAltImagenes = 0
        var palabrasxTitulo = 0
        var palabrasxSubtitulo = 0
        var cantitadReferencias = 0
        var cantidadPalabras = 0
        var referenciasActivas = 0

        for(const r of rows1 ){
            cantidadTitulos += parseInt(r.sumadetitulos)
            cantidadAltImagenes += parseInt(r.imagenesconalt)
        }
        for(const r of rows2 ){
            palabrasxTitulo += parseInt(r.PalabrasDiferentes)
        }

        for(const r of rows3 ){
            palabrasxSubtitulo += parseInt(r.PalabrasDiferentes)
        }
        for(const r of rows4 ){
            
            cantitadReferencias += parseInt(r.referenciasLink)
        }
        for(const r of rows5 ){
            cantidadPalabras += parseInt(r.palabraspagina)
        }
        for(const r of rows6 ){
            referenciasActivas += parseInt(r.refactivas)
        }
            
        const data = {
            "cantidadTitulos":cantidadTitulos,
            "cantidadAltImagenes":cantidadAltImagenes,
            "palabrasxTitulo":palabrasxTitulo,
            "palabrasxSubtitulo":palabrasxSubtitulo,
            "cantitadReferencias":cantitadReferencias,
            "cantidadPalabras":cantidadPalabras, 
            "referenciasActivas":referenciasActivas
        }
        
        res.status(200).json(data);
        // Liberar la conexión de vuelta al pool
        connection.release();
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error en el servidor' });
    }

});

app.get('/datosPorPagina/:link', async (req, res) => {
    const linkPage = req.params.link;
    console.log(linkPage)
    // const query1 = `SELECT sum(can_titulos)+count(link)as sumadetitulos,sum(can_imagenes) as imagenesconalt from pagina`;
    // const query2 =  `SELECT PalabrasXPaginas.link_pagina,PalabrasXPaginas.porcentaje,Palabra.palabra from PalabrasXPaginas inner join Palabra on id_palabra=Palabra.id where Palabra.palabra='' and link_pagina=?;`;
    //const query1 =  `SELEC link,titulo_principal from pagina ;`;
    const query1 =  `SELECT can_titulos,can_palabras,can_referencias,can_imagenes,can_palabrasximagenes from pagina where link =?;`;
    const query2 =  `SELECT sum(cantidad_palabras) as PalabrasDiferentes from titulos where link_pagina =?;`;
    const query3 =  `SELECT sum(cantidad_palabras) as PalabrasDiferentes from subtitulos where link_pagina =?;`;
    const query4 =  `SELECT count(link) as referenciasLink from referencias where link_pagina=? and link like 'http%';`;
    const query5 =  `SELECT nombre_cita,usos,link,activo from referencias where link_pagina=? and activo=1;`;
    const query6 =  `SELECT palabra,veces,enTitulo from PalabrasMasComunes where link_pagina=?;`;

    // Obtener una conexión del pool
    try {
        const connection = await pool.getConnection();
        const rows1 = await connection.query(query1, [linkPage]);
        const rows2 = await connection.query(query2, [linkPage]);
        const rows3 = await connection.query(query3, [linkPage]);
        const rows4 = await connection.query(query4, [linkPage]);
        const rows5 = await connection.query(query5, [linkPage]);
        const rows6 = await connection.query(query6, [linkPage]);
    
        var canTitulos = 0
        var canPalabras = 0
        var canReferencias = 0
        var canImagenes = 0
        var canPalabrasImagenes = 0
        var palabrasDifTitulos = 0
        var palabrasDifSubtitulos = 0
        var referenciasLink = 0
        var citas = []
        var palabrasComunes = []

        for(const r of rows1 ){
            canTitulos += parseInt(r.can_titulos)
            canPalabras += parseInt(r.can_palabras)
            canReferencias += parseInt(r.can_referencias)
            canImagenes += parseInt(r.can_imagenes)
            canPalabrasImagenes += parseInt(r.can_palabrasximagenes)
            
        }
        for(const r of rows2 ){
            palabrasDifTitulos = parseInt(r.PalabrasDiferentes)
        }
        for(const r of rows3 ){
            palabrasDifSubtitulos = parseInt(r.PalabrasDiferentes)
        }
        for(const r of rows4 ){
            referenciasLink += parseInt(r.referenciasLink)
        }
        for(const r of rows5 ){
            citas.push({
                "nombre":r.nombre_cita,
                "usos":parseInt(r.usos),
                "link":r.link,
                "activo":parseInt(r.activo)
            })
        }
        for(const r of rows6 ){
            palabrasComunes.push({
                "palabra":r.palabra,
                "apariciones":parseInt(r.veces), 
                "enTitulo": parseInt(r.enTitulo)
            })
        }
        
        const data = {
            "canTitulos":canTitulos,
            "canPalabras":canPalabras,
            "canReferencias":canReferencias,
            "canImagenes":canImagenes,
            "canPalabrasImagenes":canPalabrasImagenes,
            "palabrasDifTitulos":palabrasDifTitulos,
            "palabrasDifSubtitulos":palabrasDifSubtitulos,
            "referenciasLink":referenciasLink,
            "citas":citas,
            "palabrasComunes":palabrasComunes
            
        }
        
        res.status(200).json(data);
        // Liberar la conexión de vuelta al pool
        connection.release();
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error en el servidor' });
    }

});



app.listen(3000,()=>{
    console.log(3000)
})