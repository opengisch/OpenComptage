-- class
INSERT INTO comptages.class VALUES (2, 'SWISS2', 'SWISS 2');
INSERT INTO comptages.class VALUES (3, 'SWISS5', 'SWISS 5');
INSERT INTO comptages.class VALUES (4, 'SWISS6', 'SWISS 6 (SSVZ)');
INSERT INTO comptages.class VALUES (5, 'SWISS7', 'SWISS 7');
INSERT INTO comptages.class VALUES (6, 'SWISS10', 'SWISS 10');
INSERT INTO comptages.class VALUES (11, 'EUR13', 'EUR 13');
INSERT INTO comptages.class VALUES (12, 'NZ13', 'New Zealand 13');
INSERT INTO comptages.class VALUES (21, 'Bicycle', 'Vélos seul');

-- category
INSERT INTO comptages.category (id, name, code, id_category) VALUES (2, 'PF', '15', 2);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (3, 'MFZ', '16', 2);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (4, 'CAR', '1', 2);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (5, 'MR', '2', 2);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (6, 'PW', '11', 2);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (7, 'LIE', '12', 3);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (8, 'SGF', '14', 3);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (9, 'LW', '8', 8);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (10, 'LZ+SZ', '13', 8);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (11, 'LZ', '9', 10);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (12, 'SZ', '10', 10);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (13, 'PW', '3', 6);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (14, 'PW+ANH', '4', 6);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (15, 'LIE', '5', 7);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (16, 'LIE+ANH', '6', 7);
INSERT INTO comptages.category (id, name, code, id_category) VALUES (17, 'LIE+AUFL', '7', 7);

-- class_category
INSERT INTO comptages.class_category (id_class, id_category) VALUES (2, 2);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (2, 3);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 4);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 5);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 6);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 7);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 8);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 4);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 5);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 6);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 7);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 9);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 10);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 4);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 5);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 6);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 7);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 9);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 11);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 12);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 4);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 5);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 13);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 14);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 15);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 16);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 17);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 9);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 11);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 12);

-- brand
INSERT INTO comptages.brand VALUES (1, 'GoldenRiver');
INSERT INTO comptages.brand VALUES (2, 'MetroCount');

-- model
INSERT INTO comptages.model VALUES (1, 'M660_LT', 'L:\Data\Compteurs\MTL\Bin2Asc\grformat.exe', '8 Loop Card (HP) + Tube/Switch Input Card (Rev Polarity)', '', 1);
INSERT INTO comptages.model VALUES (2, 'M660_L', 'L:\Data\Compteurs\MTL\Bin2Asc\grformat.exe', '8 Loop Card (HP)', '', 1);
INSERT INTO comptages.model VALUES (3, 'M660_T', 'L:\Data\Compteurs\MTL\Bin2Asc\grformat.exe', 'Tube/Switch Input Card (Rev Polarity)', '', 1);
INSERT INTO comptages.model VALUES (4, 'M660_L2', 'L:\Data\Compteurs\MTL\Bin2Asc\grformat.exe', '2 x 8 Loop Card (HP)', '', 1);
INSERT INTO comptages.model VALUES (5, 'M660_T2', 'L:\Data\Compteurs\MTL\Bin2Asc\grformat.exe', '2 x Tube/Switch Input Card (Rev Polarity)', '', 1);
INSERT INTO comptages.model VALUES (6, 'M680_L', 'L:\Data\Compteurs\MTL\Bin2Asc\grformat.exe', '16 Loop Sensor', '', 1);
INSERT INTO comptages.model VALUES (7, 'M720_L', 'L:\Data\Compteurs\MTL\Bin2Asc\grformat.exe', 'Loop Sensor', '', 1);
INSERT INTO comptages.model VALUES (11, 'MC5900_T', NULL, 'Tube', '', 2);
INSERT INTO comptages.model VALUES (12, 'MC5720_P', NULL, 'Piezo', '', 2);

-- device
INSERT INTO comptages.device VALUES (1, '229007', NULL, '1', 1);
INSERT INTO comptages.device VALUES (2, '227105', NULL, '2', 1);
INSERT INTO comptages.device VALUES (23, '402755', NULL, '35', 1);
INSERT INTO comptages.device VALUES (24, NULL, NULL, 'NE_BAP', 3);
INSERT INTO comptages.device VALUES (25, '230330', NULL, 'NE_CLC', 2);
INSERT INTO comptages.device VALUES (33, NULL, NULL, 'NE_ESN', 5);
INSERT INTO comptages.device VALUES (32, '254515', NULL, 'NE_EGA', 4);
INSERT INTO comptages.device VALUES (62, '701626', NULL, 'A', 6);
INSERT INTO comptages.device VALUES (86, '701648', NULL, 'Y', 6);
INSERT INTO comptages.device VALUES (87, '701624', NULL, 'OFROU_799', 6);
INSERT INTO comptages.device VALUES (101, NULL, NULL, '101', 11);
INSERT INTO comptages.device VALUES (125, NULL, NULL, '125', 11);
INSERT INTO comptages.device VALUES (201, NULL, NULL, 'MD01', 12);
INSERT INTO comptages.device VALUES (208, NULL, NULL, 'MD08', 12);

-- sensor_type
INSERT INTO comptages.sensor_type VALUES (1, 'Boucle', true);
INSERT INTO comptages.sensor_type VALUES (2, 'Tube', false);
INSERT INTO comptages.sensor_type VALUES (3, 'Piezo', true);

-- sensor_type_class
INSERT INTO comptages.sensor_type_class VALUES (1, 2);
INSERT INTO comptages.sensor_type_class VALUES (1, 3);
INSERT INTO comptages.sensor_type_class VALUES (1, 4);
INSERT INTO comptages.sensor_type_class VALUES (1, 5);
INSERT INTO comptages.sensor_type_class VALUES (1, 6);
INSERT INTO comptages.sensor_type_class VALUES (1, 11);
INSERT INTO comptages.sensor_type_class VALUES (1, 12);
INSERT INTO comptages.sensor_type_class VALUES (2, 2);
INSERT INTO comptages.sensor_type_class VALUES (2, 3);
INSERT INTO comptages.sensor_type_class VALUES (2, 4);
INSERT INTO comptages.sensor_type_class VALUES (2, 5);
INSERT INTO comptages.sensor_type_class VALUES (2, 11);
INSERT INTO comptages.sensor_type_class VALUES (2, 12);
INSERT INTO comptages.sensor_type_class VALUES (3, 2);
INSERT INTO comptages.sensor_type_class VALUES (3, 3);
INSERT INTO comptages.sensor_type_class VALUES (3, 4);
INSERT INTO comptages.sensor_type_class VALUES (3, 5);
INSERT INTO comptages.sensor_type_class VALUES (3, 11);
INSERT INTO comptages.sensor_type_class VALUES (3, 12);
INSERT INTO comptages.sensor_type_class VALUES (3, 21);

-- sensor_type_model
INSERT INTO comptages.sensor_type_model VALUES (1, 1);
INSERT INTO comptages.sensor_type_model VALUES (1, 2);
INSERT INTO comptages.sensor_type_model VALUES (1, 4);
INSERT INTO comptages.sensor_type_model VALUES (1, 6);
INSERT INTO comptages.sensor_type_model VALUES (1, 7);
INSERT INTO comptages.sensor_type_model VALUES (2, 1);
INSERT INTO comptages.sensor_type_model VALUES (2, 3);
INSERT INTO comptages.sensor_type_model VALUES (2, 5);
INSERT INTO comptages.sensor_type_model VALUES (2, 11);
INSERT INTO comptages.sensor_type_model VALUES (3, 12);

--sequences
SELECT pg_catalog.setval('comptages.class_id_seq', 21, true);
SELECT pg_catalog.setval('comptages.category_id_seq', 17, true);
SELECT pg_catalog.setval('comptages.brand_id_seq', 2, true);
SELECT pg_catalog.setval('comptages.model_id_seq', 12, true);
SELECT pg_catalog.setval('comptages.device_id_seq', 208, true);
SELECT pg_catalog.setval('comptages.sensor_type_id_seq', 3, true);
