drop table cuentas CASCADE;
DROP TABLE preferences cascade;
select * from movies;
select * from portada;
select * from cuentas;
select * from preferences;

create table portada(
	id INT NOT NULL,
	tittle VARCHAR ( 80 ) UNIQUE NOT NULL,
	poster VARCHAR ( 150 ) UNIQUE NOT NULL,
	description TEXT DEFAULT 'Pending',
	
	likes_ INT NOT NULL DEFAULT 0,
	rating FLOAT NOT NULL DEFAULT 0,
	PRIMARY KEY (id)
);
CREATE TABLE movies (
	id INT NOT NULL,
	video VARCHAR ( 150 ) UNIQUE NOT NULL,
	added_on TIMESTAMP NOT NULL DEFAULT now(),
	views_ INT NOT NULL DEFAULT 0,
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES portada(id) ON UPDATE CASCADE
);


create table cuentas(
	id_cuentas SERIAL,
	email varchar(40) NOT NULL,
	username varchar(30) NOT NULL,
	password varchar(500) NOT NULL,
	PRIMARY KEY (id_cuentas)
);
CREATE TABLE preferences (
    id INT REFERENCES cuentas(id_cuentas),
    color_hex varchar(10) DEFAULT '#ffffff'::text,
    favorites JSONB
);



INSERT INTO preferences (id, color_hex, favorites) VALUES (1, '#690c0c'::text, '["100001", "100002", "100003","100004", "100005", "100006","100007", "100008"]');
INSERT INTO preferences (id, color_hex, favorites) VALUES (2, '#5639bf'::text, '["100001", "100002", "100003","100004"]');

INSERT INTO portada VALUES (100001, 'Django', 'https://akroos.s3.amazonaws.com/imagenes/django-poster.jpg', 'Un antiguo esclavo une sus fuerzas con un cazador de recompensas alemán que lo libera y ayuda a cazar a los criminales más buscados del Sur, todo ello con la esperanza de encontrar a su esposa perdida hace mucho tiempo.');
INSERT INTO portada VALUES (100002, 'Darknight', 'https://akroos.s3.amazonaws.com/imagenes/dark-night-poster.jpg','Con la ayuda del teniente Jim Gordon y del Fiscal del Distrito Harvey Dent, Batman mantiene a raya el crimen organizado en Gotham. Todo cambia cuando aparece el Joker, un nuevo criminal que desencadena el caos y tiene aterrados a los ciudadanos.');
INSERT INTO portada VALUES (100003, 'Gaton con Botas', 'https://akroos.s3.amazonaws.com/imagenes/el-gato-con-botas-poster.jpg', 'Mucho antes de conocer a Shrek, el Gato con botas, recién nombrado héroe por salvar a una mujer de la embestida de un toro, tiene que huir de la ciudad cuando comienzan a sospechar que ha robado un banco, aunque el verdadero villano es su amigo Humpty Dumpty');
INSERT INTO portada VALUES (100004, 'Bastardos sin gloria', 'https://akroos.s3.amazonaws.com/imagenes/bastardos-sin-gloria-poster.jpg', 'II Guerra Mundial, Francia, Shosanna presencia la ejecución de su familia por orden del coronel nazi Hans Landa. Huye a Paris y adopta una nueva identidad como propietaria de un cine. Mientras el teniente Aldo Raine adiestra a un grupo de soldados judíos. Los hombres de Raine y una actriz alemana que agente doble, deben llevar a cabo una misión que hará caer a los jefes del Tercer Reich.');
INSERT INTO portada VALUES (100005, 'Spiderman', 'https://akroos.s3.amazonaws.com/imagenes/spiderman-1-poster.jpg', 'Luego de sufrir la picadura de una araña genéticamente modificada, un estudiante de secundaria tímido y torpe adquiere increíbles capacidades como arácnido. Pronto comprenderá que su misión es utilizarlas para luchar contra el mal y defender a sus vecinos.');
INSERT INTO portada VALUES (100006, 'Almas en pena de Inisherin', 'https://akroos.s3.amazonaws.com/imagenes/almas_en_pena_de_inisherin-poster.jpg' , 'En una remota isla irlandesa, Pádraic queda devastado cuando su amigo, Colm, de repente pone fin a su amistad de toda la vida. Con la ayuda de su hermana y un isleño con problemas, Pádraic se propone reparar la relación dañada por todos los medios.');
INSERT INTO portada VALUES (100007, '300', 'https://akroos.s3.amazonaws.com/imagenes/300-poster.jpg', 'En el año 480 antes de Cristo, existe un estado de guerra entre Persia, dirigidos por el Rey Xerxes (Rodrigo Santoro), y Grecia. En la Batalla de Thermopylae, Leonidas (Gerard Butler), rey de la ciudad griega de Esparta, encabeza a sus autonombrados guerreros en contra del numeroso ejército persa.');
INSERT INTO portada VALUES (100008, 'Terminator 2', 'https://akroos.s3.amazonaws.com/imagenes/terminator-2-poster.jpg', 'Algunos años antes, un viajero del tiempo le reveló a la madre de John que su hijo sería el salvador de la humanidad. Cuando un nuevo androide mejorado llega del futuro para asesinar a John, un viejo modelo será enviado para protegerle.');

INSERT INTO movies VALUES (100001, 'https://akroos.s3.amazonaws.com/videos/django.mp4');
INSERT INTO movies VALUES (100002, 'https://akroos.s3.amazonaws.com/videos/darkknight.mp4');
INSERT INTO movies VALUES (100003, 'https://akroos.s3.amazonaws.com/videos/gatos-con-botas-ultimo-deseo.mp4');
INSERT INTO movies VALUES (100004, 'https://akroos.s3.amazonaws.com/videos/malditos-basstardos.mp4');
INSERT INTO movies VALUES (100005, 'https://akroos.s3.amazonaws.com/videos/spiderman-1.mp4');
INSERT INTO movies VALUES (100006, 'https://akroos.s3.amazonaws.com/videos/almas-en-pena-de-inisherin.mp4');
INSERT INTO movies VALUES (100007, 'https://akroos.s3.amazonaws.com/videos/300.mp4');
INSERT INTO movies VALUES (100008, 'https://akroos.s3.amazonaws.com/videos/terminator-2.mp4');

