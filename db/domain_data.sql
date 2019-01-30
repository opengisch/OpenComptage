-- Class Volume
INSERT INTO comptages.class(name, description)	VALUES ('Volume', 'Volume');
INSERT INTO comptages.category(name, code, id_category)	VALUES ('MFZ', '0', (select currval('comptages.category_id_seq')));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));

-- Class SWISS 2
INSERT INTO comptages.class(name, description)	VALUES ('SWISS2', 'SWISS 2');
INSERT INTO comptages.category(name, code, id_category)	VALUES ('PF', '15', (select id from comptages.category where code = '0'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('MFZ', '16', (select id from comptages.category where code = '0'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));

-- Class SWISS 5
INSERT INTO comptages.class(name, description)	VALUES ('SWISS5', 'SWISS 5');
INSERT INTO comptages.category(name, code, id_category)	VALUES ('CAR', '1', (select id from comptages.category where code = '15'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('MR', '2', (select id from comptages.category where code = '15'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('PW', '11', (select id from comptages.category where code = '15'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('LIE', '12', (select id from comptages.category where code = '16'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('SGF', '14', (select id from comptages.category where code = '16'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));

-- Class SWISS 6
INSERT INTO comptages.class(name, description)	VALUES ('SWISS6', 'SWISS 6 (SSVZ)');
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='1'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='2'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='11'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='12'));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('LW', '8', (select id from comptages.category where code = '14'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('LZ+SZ', '13', (select id from comptages.category where code = '14'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));

-- Class SWISS 7
INSERT INTO comptages.class(name, description)	VALUES ('SWISS7', 'SWISS 7');
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='1'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='2'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='11'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='12'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='8'));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('LZ', '9', (select id from comptages.category where code = '13'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('SZ', '10', (select id from comptages.category where code = '13'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));

-- Class SWISS 10
INSERT INTO comptages.class(name, description)	VALUES ('SWISS10', 'SWISS 10');
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='1'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='2'));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('PW', '3', (select id from comptages.category where code = '11'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('PW+ANH', '4', (select id from comptages.category where code = '11'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('LIE', '5', (select id from comptages.category where code = '12'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('LIE+ANH', '6', (select id from comptages.category where code = '12'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('LIE+AUFL', '7', (select id from comptages.category where code = '12'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='8'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='9'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='10'));

-- Sensor type
INSERT INTO comptages.sensor_type(name, permanent) VALUES ('Boucle', True);
INSERT INTO comptages.sensor_type(name, permanent) VALUES ('Tube', False);

-- Brand
INSERT INTO comptages.brand(name) VALUES ('GoldenRiver');

-- Model
INSERT INTO comptages.model(name, formatter_name, card_name, id_brand) VALUES ('M660', '', '8 Loop Card (HP) + Tube/Switch Input Card (Rev Polarity)', (select currval('comptages.brand_id_seq')));
  -- TODO: Add models
  
-- Device
INSERT INTO comptages.device(serial, purchase_date, name, id_model) VALUES ('229007', NULL, '1', (select currval('comptages.model_id_seq')));
  -- TODO: Add devices
