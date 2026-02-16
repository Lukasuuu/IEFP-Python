USE efa0125_08_vet_clinic;

show tables;

select * from consultas;

DESCRIBE consultas;

DESCRIBE clientes;

SELECT animais.id, animais.nome, clientes.nome AS cliente_nome
        FROM animais
        INNER JOIN clientes ON clientes.id = animais.cliente_id
        ORDER BY animais.nome;

 SELECT animais.id, animais.nome, clientes.nome AS cliente_nome
        FROM animais
        INNER JOIN clientes ON clientes.id = animais.cliente_id
        ORDER BY animais.nome;

 UPDATE animais
                SET cliente_id="%s", nome="%s", especie="%s", raca="%s", data_nascimento="%s"
                WHERE id="%s";

UPDATE users
                    SET username="%s", role="%s", cliente_id="%s", password="%s"
                    WHERE id="%s";

SELECT id, nome, especie, raca, data_nascimento
            FROM animais
            WHERE cliente_id = "%s"
            ORDER BY nome;


SELECT 
			consultas.id,
			animais.nome AS animal,
			consultas.data_hora,
			consultas.motivo,
			consultas.notas,
			consultas.created_at
		FROM consultas
		INNER JOIN animais ON consultas.animal_id = animais.id
		WHERE animais.cliente_id = "%s"
		ORDER BY consultas.data_hora DESC;
            
		