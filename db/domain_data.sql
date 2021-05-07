-- class
INSERT INTO comptages.class VALUES (2, 'SWISS2', 'SWISS 2');
INSERT INTO comptages.class VALUES (3, 'SWISS5', 'SWISS 5');
INSERT INTO comptages.class VALUES (4, 'SWISS6', 'SWISS 6 (SSVZ)');
INSERT INTO comptages.class VALUES (5, 'SWISS7', 'SWISS 7');
INSERT INTO comptages.class VALUES (6, 'SWISS10', 'SWISS 10');
INSERT INTO comptages.class VALUES (11, 'EUR13', 'EUR 13');
INSERT INTO comptages.class VALUES (12, 'NZ13', 'New Zealand 13');
INSERT INTO comptages.class VALUES (21, 'Bicycle', 'Vélos seul');
INSERT INTO comptages.class VALUES (22, 'ARX Cycle', 'Vélos seul');
INSERT INTO comptages.class VALUES (13, 'FHWA13', 'Federal HighWay Administration 13 category');
INSERT INTO comptages.class VALUES (14, 'SWISS7-MM', 'SWISS 7 modified for Marksmann devices');
INSERT INTO comptages.class VALUES (15, 'SPCH-13', 'SPCH-13');
INSERT INTO comptages.class VALUES (16, 'SPCH-MD 5C', 'SPCH-MD 5C');

-- category
  -- SWISS 2
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (902, 'TRASH', 0, 902, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (2, 'PF', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (3, 'MFZ', 2, 2, FALSE);

  -- SWISS 5
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (904, 'TRASH', 0, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (4, 'CAR', 1, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (5, 'MR', 2, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (6, 'PW', 3, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (7, 'LIE', 4, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (8, 'SGF', 5, 2, FALSE);

  -- SWISS 6
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (909, 'TRASH', 0, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (9, 'CAR', 1, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (10, 'MR', 2, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (11, 'PW', 3, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (12, 'LIE', 4, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (13, 'LW', 5, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (14, 'LZ+SZ', 6, 2, FALSE);

  -- SWISS 7
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (915, 'TRASH', 0, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (15, 'CAR', 1, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (16, 'MR', 2, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (17, 'PW', 3, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (18, 'LIE', 4, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (19, 'LW', 5, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (20, 'LZ', 6, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (21, 'SZ', 7, 2, FALSE);

  -- SWISS 10
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (922, 'TRASH', 0, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (22, 'CAR', 1, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (23, 'MR', 2, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (24, 'PW', 3, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (25, 'PW+ANH', 4, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (26, 'LIE', 5, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (27, 'LIE+ANH', 6, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (28, 'LIE+AUFL', 7, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (29, 'LW', 8, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (30, 'LZ', 9, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (31, 'SZ', 10, 2, FALSE);

  -- ARX Cycle
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (32, 'ANY', 0, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (33, 'CYCLE', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (34, 'MC', 2, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (35, 'SV', 3, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (36, 'SVT', 4, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (37, 'TB2', 5, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (38, 'TB3', 6, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (39, 'T4', 7, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (40, 'ART3', 8, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (41, 'ART4', 9, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (42, 'ART5', 10, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (43, 'ART6', 11, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (44, 'BD', 12, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (45, 'DRT', 13, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (46, 'ELSE', 14, 2, FALSE);

  -- NZ13
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (47, 'TRASH', 0, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (48, 'NZTA 1', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (49, 'NZTA 2', 2, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (50, 'NZTA 3', 3, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (51, 'NZTA 4', 4, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (52, 'NZTA 5', 5, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (53, 'NZTA 6', 6, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (54, 'NZTA 7', 7, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (55, 'NZTA 8', 8, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (56, 'NZTA 9', 9, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (57, 'NZTA 10', 10, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (58, 'NZTA 11', 11, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (59, 'NZTA 12', 12, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (60, 'NZTA 13', 13, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (61, 'ANY', 14, 2, FALSE);

  -- FHWA13
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (62, 'TRASH', 0, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (63, 'FHW01', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (64, 'FHW02', 2, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (65, 'FHW03', 3, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (66, 'FHW04', 4, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (67, 'FHW05', 5, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (68, 'FHW06', 6, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (69, 'FHW07', 7, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (70, 'FHW08', 8, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (71, 'FHW09', 9, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (72, 'FHW10', 10, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (73, 'FHW11', 11, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (74, 'FHW12', 12, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (75, 'FHW13', 13, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (76, 'ELSE', 14, 2, FALSE);

  -- Bicycle
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (77, 'TRASH', 0, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (78, 'Bicycle', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (79, 'ELSE', 2, 2, FALSE);

  -- SWISS 7 Marksmann
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (80, 'PW', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (81, 'CAR', 2, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (82, 'LIE', 3, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (83, 'LW', 4, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (84, 'LZ', 5, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (85, 'SZ', 6, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (86, 'MR', 7, 2, TRUE);

  -- SPCH-13
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (87, 'TRASH', 0, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (88, 'CAR', 1, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (89, 'MR', 2, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (90, 'PW', 3, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (91, 'LIE', 4, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (92, 'LW', 5, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (93, 'LZ', 6, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (94, 'SZ', 7, 2, FALSE);

  -- SPCH-MD 5C
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (95, 'TRASH', 0, 2, FALSE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (96, 'VELO', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (97, 'MONO', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (98, 'SHORT', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (99, 'SPECIAL', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (100, 'MULTI', 1, 2, TRUE);
INSERT INTO comptages.category (id, name, code, id_category, light) VALUES (101, 'ELSE', 2, 2, FALSE);


-- class_category
  -- SWISS 2
INSERT INTO comptages.class_category (id_class, id_category) VALUES (2, 902);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (2, 2);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (2, 3);

  -- SWISS 5
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 904);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 4);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 5);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 6);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 7);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (3, 8);

  -- SWISS 6
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 909);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 9);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 10);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 11);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 12);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 13);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (4, 14);

  -- SWISS 7
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 915);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 15);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 16);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 17);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 18);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 19);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 20);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (5, 21);

  -- SWISS 10
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 922);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 22);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 23);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 24);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 25);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 26);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 27);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 28);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 29);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 30);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (6, 31);

  -- ARX Cycle
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 32);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 33);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 34);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 35);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 36);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 37);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 38);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 39);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 40);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 41);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 42);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 43);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 44);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 45);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (22, 46);

  -- NZ 13
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 47);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 48);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 49);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 50);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 51);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 52);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 53);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 54);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 55);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 56);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 57);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 58);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 59);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 60);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (12, 61);

  -- FHWA 13
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 62);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 63);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 64);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 65);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 66);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 67);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 68);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 69);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 70);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 71);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 72);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 73);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 74);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 75);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (13, 76);

  -- Bicycle
INSERT INTO comptages.class_category (id_class, id_category) VALUES (21, 77);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (21, 78);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (21, 79);

  -- SWISS 7 Marksmann
INSERT INTO comptages.class_category (id_class, id_category) VALUES (14, 80);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (14, 81);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (14, 82);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (14, 83);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (14, 84);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (14, 85);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (14, 86);

  -- SPCH-13
INSERT INTO comptages.class_category (id_class, id_category) VALUES (15, 87);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (15, 88);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (15, 89);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (15, 90);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (15, 91);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (15, 92);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (15, 93);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (15, 94);

  -- SPCH-MD 5C
INSERT INTO comptages.class_category (id_class, id_category) VALUES (16, 95);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (16, 96);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (16, 97);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (16, 98);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (16, 99);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (16, 100);
INSERT INTO comptages.class_category (id_class, id_category) VALUES (16, 101);

-- brand
INSERT INTO comptages.brand VALUES (1, 'GoldenRiver', 'L:\Data\Compteurs\MTL\Bin2Asc\grformat.exe');
INSERT INTO comptages.brand VALUES (2, 'MetroCount', NULL);

-- model
INSERT INTO comptages.model VALUES (1, 'M660_LT', '8 Loop Card (HP) + Tube/Switch Input Card (Rev Polarity)', '', 1);
INSERT INTO comptages.model VALUES (2, 'M660_L', '8 Loop Card (HP)', '', 1);
INSERT INTO comptages.model VALUES (3, 'M660_T', 'Tube/Switch Input Card (Rev Polarity)', '', 1);
INSERT INTO comptages.model VALUES (4, 'M660_L2', '2 x 8 Loop Card (HP)', '', 1);
INSERT INTO comptages.model VALUES (5, 'M660_T2', '2 x Tube/Switch Input Card (Rev Polarity)', '', 1);
INSERT INTO comptages.model VALUES (6, 'M680_L', '16 Loop Sensor', '', 1);
INSERT INTO comptages.model VALUES (7, 'M720_L', 'Loop Sensor', '', 1);
INSERT INTO comptages.model VALUES (11, 'MC5900_T', 'Tube', '', 2);
INSERT INTO comptages.model VALUES (12, 'MC5720_P', 'Piezo', '', 2);

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
SELECT pg_catalog.setval('comptages.class_id_seq', 22, true);
SELECT pg_catalog.setval('comptages.category_id_seq', 61, true);
SELECT pg_catalog.setval('comptages.brand_id_seq', 2, true);
SELECT pg_catalog.setval('comptages.model_id_seq', 12, true);
SELECT pg_catalog.setval('comptages.device_id_seq', 208, true);
SELECT pg_catalog.setval('comptages.sensor_type_id_seq', 3, true);


-- indexes
CREATE index ON comptages.count_aggregate_value_cls(id_count_aggregate);
CREATE index ON comptages.count_aggregate_value_cnt(id_count_aggregate);
CREATE index ON comptages.count_aggregate_value_drn(id_count_aggregate);
CREATE index ON comptages.count_aggregate_value_len(id_count_aggregate);
CREATE index ON comptages.count_aggregate_value_spd(id_count_aggregate);
CREATE index ON comptages.count_aggregate_value_sds(id_count_aggregate);
