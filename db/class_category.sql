-- Class Volume
INSERT INTO comptages.class(name, description)	VALUES ('Volume', 'Volume');
INSERT INTO comptages.category(name, code, id_category)	VALUES ('MFZ', '0', (select currval('comptages.category_id_seq')));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));

-- Class SWISS 2
INSERT INTO comptages.class(name, description)	VALUES ('SWISS 2', 'SWISS 2');
INSERT INTO comptages.category(name, code, id_category)	VALUES ('PF', '15', (select id from comptages.category where code = '0'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('MFZ', '16', (select id from comptages.category where code = '0'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));

-- Class SWISS 5
INSERT INTO comptages.class(name, description)	VALUES ('SWISS 5', 'SWISS 5');
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
INSERT INTO comptages.class(name, description)	VALUES ('SWISS 6', 'SWISS 6 (SSVZ)');
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='1'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='2'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='11'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select id from comptages.category where code ='12'));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('LW', '8', (select id from comptages.category where code = '14'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));
INSERT INTO comptages.category(name, code, id_category)	VALUES ('LZ+SZ', '13', (select id from comptages.category where code = '14'));
INSERT INTO comptages.class_category(id_class, id_category)	VALUES ((select currval('comptages.class_id_seq')), (select currval('comptages.category_id_seq')));

-- Class SWISS 7
INSERT INTO comptages.class(name, description)	VALUES ('SWISS 7', 'SWISS 7');
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
INSERT INTO comptages.class(name, description)	VALUES ('SWISS 10', 'SWISS 10');
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
