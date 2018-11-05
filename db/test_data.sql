INSERT INTO comptages.installation( permanent, name, picture, geometry, active) VALUES ( False, 'Installation 1', 'Picture 1', NULL, True);
INSERT INTO comptages.installation( permanent, name, picture, geometry, active) VALUES ( False, 'Installation 2', 'Picture 2', NULL, True);
INSERT INTO comptages.installation( permanent, name, picture, geometry, active) VALUES ( False, 'Installation 3', 'Picture 3', NULL, True);
INSERT INTO comptages.installation( permanent, name, picture, geometry, active) VALUES ( False, 'Installation 4', 'Picture 4', NULL, True);
INSERT INTO comptages.installation( permanent, name, picture, geometry, active) VALUES ( False, 'Installation 5', 'Picture 5', NULL, True);

INSERT INTO comptages.lane("number", direction, id_installation, id_section) VALUES (1, 1, 1, 64040050);
INSERT INTO comptages.lane("number", direction, id_installation, id_section) VALUES (2, 2, 1, 64040050);

INSERT INTO comptages.lane("number", direction, id_installation, id_section) VALUES (1, 1, 2, 10020290);
INSERT INTO comptages.lane("number", direction, id_installation, id_section) VALUES (2, 2, 2, 10020290);

INSERT INTO comptages.lane("number", direction, id_installation, id_section) VALUES (1, 1, 3, 64080015);
INSERT INTO comptages.lane("number", direction, id_installation, id_section) VALUES (2, 2, 3, 64080015);

INSERT INTO comptages.lane("number", direction, id_installation, id_section) VALUES (1, 1, 4, 64080019);
INSERT INTO comptages.lane("number", direction, id_installation, id_section) VALUES (2, 2, 4, 64080019);

INSERT INTO comptages.lane("number", direction, id_installation, id_section) VALUES (1, 1, 5, 64080159);
INSERT INTO comptages.lane("number", direction, id_installation, id_section) VALUES (2, 2, 5, 64080159);

INSERT INTO comptages.brand(name) VALUES ('ACME Corporation');
INSERT INTO comptages.model(name, id_brand) VALUES ('ACME Corporation - Model 1', 1);


INSERT INTO comptages.sensor_type(name, permanent) VALUES ('Boucle', False);
INSERT INTO comptages.sensor_type(name, permanent) VALUES ('Tube', False);

INSERT INTO comptages.device("number", serial, purchase_date, name, id_model) VALUES (101, 'SN1238942', '2014-04-04', 'Device 101', 1);
INSERT INTO comptages.device("number", serial, purchase_date, name, id_model) VALUES (102, 'SN1238774', '2014-04-04', 'Device 102', 1);

--INSERT INTO comptages.count(id, start_service_date, end_service_date, start_put_date, end_put_date,
--       start_process_date, end_process_date, valid, dysfunction, remarks, id_model,
--       id_device, id_sensor_type, id_class, id_installation)
--VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);

INSERT INTO comptages.count(
	start_service_date, end_service_date, 
	start_put_date, end_put_date, 
	start_process_date, end_process_date, 
	"valid", dysfunction, remarks, id_installation, id_model)
	VALUES (
		'2016-09-01', '2016-09-30',
		'2016-09-01', '2016-09-30',
		'2016-09-01', '2016-09-30',
		True,
		False,
		'Comptage 2016',
		1, 1);

INSERT INTO comptages.count(
	start_service_date, end_service_date, 
	start_put_date, end_put_date, 
	start_process_date, end_process_date, 
	"valid", dysfunction, remarks, id_installation, id_model)
	VALUES (
		'2017-09-01', '2017-09-30',
		'2017-09-01', '2017-09-30',
		'2017-09-01', '2017-09-30',
		True,
		False,
		'Comptage 2017',
		1, 1);

INSERT INTO comptages.count(
	start_service_date, end_service_date, 
	start_put_date, end_put_date, 
	start_process_date, end_process_date, 
	"valid", dysfunction, remarks, id_installation, id_model)
	VALUES (
		'2018-09-01', '2018-09-30',
		'2018-09-01', '2018-09-30',
		'2018-09-01', '2018-09-30',
		True,
		False,
		'Comptage 2018',
		1, 1);

INSERT INTO comptages.count(
	start_service_date, end_service_date, 
	start_put_date, end_put_date, 
	start_process_date, end_process_date, 
	"valid", dysfunction, remarks, id_installation, id_model)
	VALUES (
		'2018-09-01', '2018-12-31',
		'2018-09-01', '2018-12-31',
		'2018-09-01', '2018-12-31',
		True,
		False,
		'Test',
		2, 1);

INSERT INTO comptages.count(
	start_service_date, end_service_date, 
	start_put_date, end_put_date, 
	start_process_date, end_process_date, 
	"valid", dysfunction, remarks, id_installation, id_model)
	VALUES (
		'2018-09-01', '2018-12-31',
		'2018-09-01', '2018-12-31',
		'2018-09-01', '2018-12-31',
		True,
		False,
		'Test',
		3, 1);

INSERT INTO comptages.count(
	start_service_date, end_service_date, 
	start_put_date, end_put_date, 
	start_process_date, end_process_date, 
	"valid", dysfunction, remarks, id_installation, id_model)
	VALUES (
		'2018-09-01', '2018-12-31',
		'2018-09-01', '2018-12-31',
		'2018-09-01', '2018-12-31',
		True,
		False,
		'Test',
		4, 1);

INSERT INTO comptages.count(
	start_service_date, end_service_date, 
	start_put_date, end_put_date, 
	start_process_date, end_process_date, 
	"valid", dysfunction, remarks, id_installation, id_model)
	VALUES (
		'2018-09-01', '2018-12-31',
		'2018-09-01', '2018-12-31',
		'2018-09-01', '2018-12-31',
		True,
		False,
		'Test',
		5, 1);
