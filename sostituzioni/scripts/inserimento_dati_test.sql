INSERT OR IGNORE INTO nota_standard VALUES ( 'Ora a pagamento' );

INSERT OR IGNORE INTO ora_predefinita VALUES
    ('1', '07:50', '08:40'),
    ('2', '08:40', '09:30'),
    ('3', '09:30', '10:20'),
    ('Prima Pausa', '10:20', '10:35'),
    ('4', '10:35', '11:25'),
    ('5', '11:25', '12:10'),
    ('Seconda Pausa', '12:10', '12:25'),
    ('6', '12:25', '13:15'),
    ('7', '13:15', '14:05');

INSERT OR IGNORE INTO docente VALUES
    ('Maria', 'Brambilla', 0),
    ('Giuseppina', 'Villa', 0),
    ('Laura', 'Colombo', 0),
    ('Anna', 'Sala', 0),
    ('Angela', 'Fumagalli', 0),
    ('Francesca', 'Magni', 0),
    ('Elena', 'Mauri', 0),
    ('Paola', 'Motta', 0),
    ('Silvia', 'Ronchi', 0),
    ('Chiara', 'Beretta', 0),
    ('Giuseppe', 'Passoni', 0),
    ('Marco', 'Marchesi', 0),
    ('Andrea', 'Carzaniga', 0),
    ('Francesco', 'Cantù', 0),
    ('Luigi', 'Frigerio', 0),
    ('Alessandro', 'Stucchi', 0),
    ('Roberto', 'Redaelli', 0),
    ('Luca', 'Galbussera', 0),
    ('Antonio', 'Pirola', 0),
    ('Giovanni', 'Crippa', 0);

INSERT OR IGNORE INTO aula VALUES
    ('-013', 0, 0),
    ('010', 0, 0),
    ('011', 0, 0),
    ('012', 0, 0),
    ('101', 1, 0),
    ('102', 1, 0),
    ('103', 1, 0),
    ('104', 1, 0),
    ('201', 2, 0),
    ('202', 2, 0),
    ('203', 2, 0),
    ('204', 2, 0),
    ('301', 3, 0),
    ('302', 3, 0),
    ('303', 3, 0);

INSERT OR IGNORE INTO classe VALUES
    ('1 LC', 0),
    ('1 LL', 0),
    ('1 LS', 0),
    ('1 LSU', 0),
    ('1 LSA', 0),
    ('1 ITE', 0),
    ('2 LC', 0),
    ('2 LL', 0),
    ('2 LS', 0),
    ('2 LSU', 0),
    ('2 LSA', 0),
    ('2 ITE', 0);

INSERT OR IGNORE INTO visualizzazione VALUES
    ('online'),
    ('fisica');
