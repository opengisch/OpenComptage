#!/usr/bin/env python

import psycopg2
import sys


class TransferBaseTjmOk(object):

    def __init__(self, pg_service):
        self.connection = psycopg2.connect(f'service={pg_service}')
        self.special_case_sections = [
            '47226035',
            '47216025',
            '47246045',
            '47236040',
            '47346070',
            '47336065',
            '53116845',
            '53126850',
            '53136855',
            '53146860',
            '00056200',
            '00056200',
            '00056202',
            '00056202',
            '53316875',
            '53326880',
            '53336885',
            '53346890',
            '00056230',
            '00056230',
            '10020355',
            '10020355',
            '53410005',
            '53420005',
            '53430005',
            '53440005',
            '53515786',
            '53545796',
            '53536901',
            '53526896',
            '55110005',
            '55120050',
            '64010085',
            '64010085',
            '00056360',
            '00056360',
            '00056355',
            '00056355',
            '58327205',
            '58347235',
            '58417240',
            '58427245',
            '58437250',
            '58447255',
            '00056380',
            '56146965'
        ]

        self.sensor_type_id = {'BOUCLE': 1, 'TUBE': 2}

    def read_from_base_tjm_ok(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = ("select "
                         "ogc_fid,"  # 0
                         "fsection,"  # 1
                         "fonctionel,"  # 2
                         "f_prop,"  # 3
                         "f_axe,"  # 4
                         "f_sens,"  # 5
                         "f_pr_d,"  # 6
                         "f_dist_d,"  # 7
                         "ecartd,"  # 8
                         "f_pr_f,"  # 9
                         "f_dist_f,"  # 10
                         "ecartf,"  # 11
                         "usaneg,"  # 12
                         "poste,"  # 13
                         "troncon,"  # 14
                         "lieu_rue,"  # 15
                         "type_tra,"  # 16
                         "sensor,"  # 17
                         "classif,"  # 18
                         "lpseps,"  # 19
                         "permanent,"  # 20
                         "c_ehbdo,"  # 21
                         "boucon,"  # 22
                         "ccd,"  # 23
                         "ccf,"  # 24
                         "f_long,"  # 25
                         "f_surf,"  # 26
                         "nom_rue,"  # 27
                         "dir1,"  # 28
                         "dir2,"  # 29
                         "wkb_geometry "  # 30
                         "from transfer.base_tjm_ok;")
                cursor.execute(query)
                records = cursor.fetchall()
                print('Import sections, installations, lanes, etc.')
                for i, record in enumerate(records):
                    if i % 100 == 0:
                        print(i)
                    section_id = self.write_section(record)
                    if record[1] not in self.special_case_sections:
                        installation_id = self.write_installation(
                            record[20], record[1])
                        self.write_sensor_type_installation(
                            record[17], installation_id)
                        self.write_lanes(
                            record, installation_id, section_id, record[28],
                            record[29])

    def write_section(self, record):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = (
                    "INSERT INTO comptages.section("
                    "id, name, owner, road, way, start_pr, end_pr,"
                    "start_dist, end_dist, place_name, geometry)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                    "RETURNING id;"
                )
                cursor.execute(
                    query,
                    (f"{record[1]}",
                     f"{record[27]}",
                     f"{record[3]}",
                     f"{record[4]}",
                     f"{record[5]}",
                     f"{record[6]}",
                     f"{record[9]}",
                     f"{float(record[7])}",
                     f"{float(record[10])}",
                     f"{record[15]}",
                     f"{record[30]}"))

                return cursor.fetchone()[0]

    def write_installation(self, permanent, name):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = (
                    "INSERT INTO comptages.installation("
                    "permanent, name, active)"
                    "VALUES (%s, %s, %s) "
                    "RETURNING id;"
                )
                cursor.execute(
                    query,
                    (f"{(True if permanent == 'Oui' or permanent == True else False)}",
                     f"{name}",
                     f"True"))

                return cursor.fetchone()[0]

    def write_lanes(self, record, installation_id, section_id, dir1, dir2):
        if record[17] == 'Boucles':
            for i, _ in enumerate(record[22]):  # Boucon
                self.write_lane(
                    i+1, (1 if _ == 'A' else 2), installation_id, section_id,
                    (dir1 if _ == 'A' else dir2))
        else:  # Tuyaux
            if record[5] == '=':
                self.write_lane(1, 1, installation_id, section_id, dir1)
                self.write_lane(2, 2, installation_id, section_id, dir2)
            elif record[5] == '+':
                self.write_lane(1, 1, installation_id, section_id, dir1)
            elif record[5] == '-':
                self.write_lane(1, 2, installation_id, section_id, dir2)

    def write_lane(
            self, number, direction, installation_id, section_id,
            direction_desc):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = (
                    "INSERT INTO comptages.lane("
                    "number, direction, id_installation, id_section, "
                    "direction_desc) "
                    "VALUES (%s, %s, %s, %s, %s) "
                    "RETURNING id;"
                )
                cursor.execute(
                    query,
                    (f"{number}",
                     f"{direction}",
                     f"{installation_id}",
                     f"{section_id}",
                     f"{direction_desc}"))

    def write_special_cases(self):
        installation_id = self.write_installation(True, '4720_1_2')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '47226035', '')
        self.write_lane(2, 1, installation_id, '47216025', '')
        installation_id = self.write_installation(True, '4720_3_4')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '47246045', '')
        self.write_lane(2, 1, installation_id, '47236040', '')
        installation_id = self.write_installation(True, '4730_3_4')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '47346070', '')
        self.write_lane(2, 1, installation_id, '47336065', '')
        installation_id = self.write_installation(True, '53109999')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '53116845', '')
        self.write_lane(2, 1, installation_id, '53126850', '')
        self.write_lane(3, 1, installation_id, '53136855', '')
        self.write_lane(4, 1, installation_id, '53146860', '')
        installation_id = self.write_installation(True, '53309999')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '00056200', '')
        self.write_lane(2, 2, installation_id, '00056200', '')
        self.write_lane(3, 1, installation_id, '00056202', '')
        self.write_lane(4, 2, installation_id, '00056202', '')
        self.write_lane(5, 1, installation_id, '53316875', '')
        self.write_lane(6, 1, installation_id, '53326880', '')
        self.write_lane(7, 1, installation_id, '53336885', '')
        self.write_lane(8, 1, installation_id, '53346890', '')
        installation_id = self.write_installation(True, '53401002')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '00056230', '')
        self.write_lane(2, 2, installation_id, '00056230', '')
        self.write_lane(3, 1, installation_id, '10020355', '')
        self.write_lane(4, 2, installation_id, '10020355', '')
        installation_id = self.write_installation(True, '53409999')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '53410005', '')
        self.write_lane(2, 1, installation_id, '53420005', '')
        self.write_lane(3, 1, installation_id, '53430005', '')
        self.write_lane(4, 1, installation_id, '53440005', '')
        installation_id = self.write_installation(True, '5350_1_4')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '53515786', '')
        self.write_lane(2, 1, installation_id, '53545796', '')
        installation_id = self.write_installation(True, '5350_3_2')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '53536901', '')
        self.write_lane(2, 1, installation_id, '53526896', '')
        installation_id = self.write_installation(True, '5510_124')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '55110005', '')
        self.write_lane(2, 1, installation_id, '55120050', '')
        self.write_lane(3, 1, installation_id, '64010085', '')
        self.write_lane(4, 2, installation_id, '64010085', '')
        installation_id = self.write_installation(True, '5510_3_5')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '00056360', '')
        self.write_lane(2, 2, installation_id, '00056360', '')
        self.write_lane(3, 1, installation_id, '00056355', '')
        self.write_lane(4, 2, installation_id, '00056355', '')
        installation_id = self.write_installation(True, '5830_2_4')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '58327205', '')
        self.write_lane(2, 1, installation_id, '58347235', '')
        installation_id = self.write_installation(True, '5840_1_2')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '58417240', '')
        self.write_lane(2, 1, installation_id, '58427245', '')
        installation_id = self.write_installation(True, '5840_3_4')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '58437250', '')
        self.write_lane(2, 1, installation_id, '58447255', '')
        installation_id = self.write_installation(True, '5610_1_1')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '00056380', '')
        self.write_lane(2, 2, installation_id, '56146965', '')
        installation_id = self.write_installation(True, '5610_2_1')
        self.write_sensor_type_installation(None, installation_id)
        self.write_lane(1, 1, installation_id, '00056380', '')
        self.write_lane(2, 2, installation_id, '56126945', '')

    def write_sensor_type_installation(self, sensor_type, id_installation):
        if sensor_type == 'Tuyaux':
            id_sensor_type = self.sensor_type_id['TUBE']
        else:
            id_sensor_type = self.sensor_type_id['BOUCLE']

        with self.connection:
            with self.connection.cursor() as cursor:
                query = (
                    "INSERT INTO comptages.sensor_type_installation("
                    "id_sensor_type, id_installation)"
                    "VALUES (%s, %s);"
                )
                cursor.execute(
                    query,
                    (f"{id_sensor_type}",
                     f"{id_installation}",))


# if __name__ == '__main__':

pg_service = str(sys.argv[1]) if len(sys.argv) > 1 else 'comptages_dev'
transfer_base_tjm_ok = TransferBaseTjmOk(pg_service)
transfer_base_tjm_ok.read_from_base_tjm_ok()
transfer_base_tjm_ok.write_special_cases()
