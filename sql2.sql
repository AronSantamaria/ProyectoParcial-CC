select * from cuentas;
drop table preferences;

select * from preferences;

CREATE TABLE preferences (
    id INT REFERENCES cuentas(id_cuentas),
    color_hex varchar(10) DEFAULT '#ffffff'::text,
    favorites JSONB
);





INSERT INTO preferences (id, color_hex, favorites) VALUES (1, '#690c0c'::text, '["100001", "100002", "100003","100004", "100005", "100006","100007", "100008"]');
INSERT INTO preferences (id, color_hex, favorites) VALUES (2, '#5639bf'::text, '["100001", "100002", "100003","100004"]');
