Use wordsPages;
DROP TABLE tagxpalabra;
DROP TABLE tag;
DROP TABLE titulos;
DROP TABLE subtitulos;
DROP TABLE referencias;
DROP TABLE PalabrasXPaginas;
DROP TABLE Palabra;
DROP TABLE PalabrasMasComunes;
DROP TABLE pagina;
CREATE TABLE pagina(
	link NVARCHAR(400) NOT NULL PRIMARY KEY,
    titulo_principal NVARCHAR(400),
    can_titulos NVARCHAR(400),
    can_palabras NVARCHAR(400),
    can_referencias NVARCHAR(400),
    can_imagenes NVARCHAR(400),
    can_palabrasximagenes NVARCHAR(400)
    );
CREATE TABLE titulos(
	id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_titulo NVARCHAR(400),
    link_pagina NVARCHAR(400),
    cantidad_palabras NVARCHAR(400),
    FOREIGN KEY(link_pagina) REFERENCES pagina(link)
);
CREATE TABLE subtitulos(
	id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_subtitulo NVARCHAR(400),
    link_pagina NVARCHAR(400),
    cantidad_palabras NVARCHAR(400),
    FOREIGN KEY(link_pagina) REFERENCES pagina(link)
);
CREATE TABLE referencias(
	 id INT AUTO_INCREMENT PRIMARY KEY,
     link_pagina NVARCHAR(400),
     id_cita NVARCHAR(400),
     nombre_cita NVARCHAR(400),
     usos NVARCHAR(400),
     link NVARCHAR(400),
     activo bool,
     FOREIGN KEY(link_pagina) REFERENCES pagina(link)
);
CREATE TABLE PalabrasMasComunes(
	id INT AUTO_INCREMENT PRIMARY KEY,
    link_pagina NVARCHAR(400),
    palabra NVARCHAR(400),
    veces NVARCHAR(400),
    enTitulo bool,
    FOREIGN KEY(link_pagina) REFERENCES pagina(link)
);
Create table Palabra(
	id INT AUTO_INCREMENT PRIMARY KEY,
    palabra NVARCHAR(400)
);
CREATE TABLE tag(
	id INT AUTO_INCREMENT PRIMARY KEY,
    nombre NVARCHAR(400)
);
CREATE TABLE PalabrasXPaginas(
	id_palabra int,
    link_pagina NVARCHAR(400),
    porcentaje NVARCHAR(400),
    veces NVARCHAR(400),
    PRIMARY KEY (id_palabra, link_pagina),
    FOREIGN KEY (id_palabra) REFERENCES Palabra(id),
    FOREIGN KEY (link_pagina) REFERENCES pagina(link)
);
CREATE TABLE tagxpalabra(
	id_palabra int,
    id_tag int,
    porcentaje NVARCHAR(400),
    PRIMARY KEY (id_palabra, id_tag),
    FOREIGN KEY (id_palabra) REFERENCES Palabra(id),
    FOREIGN KEY (id_tag) REFERENCES tag(id)
);
INSERT INTO `wordsPages`.`tag` (`id`, `nombre`) VALUES ('1', 'p');
INSERT INTO `wordsPages`.`tag` (`id`, `nombre`) VALUES ('2', 'li');
INSERT INTO `wordsPages`.`tag` (`id`, `nombre`) VALUES ('3', 'td');
INSERT INTO `wordsPages`.`tag` (`id`, `nombre`) VALUES ('4', 'th');
INSERT INTO `wordsPages`.`tag` (`id`, `nombre`) VALUES ('5', 'img');
INSERT INTO `wordsPages`.`tag` (`id`, `nombre`) VALUES ('6', 'h1');
INSERT INTO `wordsPages`.`tag` (`id`, `nombre`) VALUES ('7', 'h2');
INSERT INTO `wordsPages`.`tag` (`id`, `nombre`) VALUES ('8', 'h3');