import csv
import logging
import time

import odoorpc


class CategoryOdoo:

    def __init__(self):
        self.parent_plankton_id = []

    def __init__(self):
        odoo_conn = odoorpc.ODOO('dev-erp.bhinnekalocal.com', port=443,
                                 protocol='jsonrpc+ssl')
        odoo_conn.login('development-bmd22', 'bmdbot', 'bmdjayaselalu')
        self.odoo = odoo_conn

    def find_id_level_2(self, parent_plankton_id):
        with open('myfile.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[4] == parent_plankton_id:
                    return row[0]

    def find_id_csv_file(self, plankton_id):
        _file = 'myfile.csv'
        logging.info(f"Find plankton id {plankton_id} in {_file}")
        category_id = ""
        with open(_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[4] == plankton_id and row[7] == "2":
                    category_id = self.find_id_level_2(row[8])
                    break
        return category_id

    def update_plankton_id(self):
        logging.info("Reading CSV file")
        id_unknown = []
        with open('myfile_example.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == "id" or row[4] is None:
                    continue

                print(f'Cari dan Update category {row[2]}')
                try:
                    category = self.odoo.env['product.category'].browse(
                        int(row[0]))
                except ValueError:
                    id_unknown.append(row[0])
                    continue

                if category.plankton_id is False:
                    category.write({'plankton_id': row[4]})
                    print(category)

                time.sleep(0.5)
        print(id_unknown)

    def update_parent_category_fico(self):
        # update category yang mempunyai level tidak sesuai dengan plankton
        logging.info("Reading CSV file")
        with (open('myfile_example.csv', 'r') as f):
            reader = csv.reader(f)
            for row in reader:
                if row[0] == "id" or row[4] is None:
                    continue

                plankton_id = row[4]
                level_fico = row[1].count("/")
                plankton_level = row[7]
                if level_fico == 1 and plankton_level == "2" \
                        and row[6] == 'Not Match':
                    print(f'Update parent category {row[2]}')
                    parent_category_id = self.find_id_level_2(plankton_id)
                    category = self.odoo.env['product.category'].browse(
                        int(row[0]))
                    if parent_category_id:
                        category.write({'parent_id': int(parent_category_id)})
                        print(category)

                    time.sleep(0.5)

    def update_parent_category_fico2(self):
        logging.info("Reading CSV file")
        start = time.time()
        with (open('myfile.csv', 'r') as f):
            reader = csv.reader(f)
            for row in reader:
                if row[0] == "id" or row[4] is None:
                    continue

                # plankton_id = row[4]
                plankton_level = row[7]
                parent_plankton_id = row[8]
                if row[6] == 'Not Match':
                    print(f'Check category {row[3]}')
                    parent_category_id = self.find_id_level_2(
                        parent_plankton_id)
                    category = self.odoo.env['product.category'].browse(
                        int(row[0]))
                    level_fico = category.parent_path.count("/")

                    # if int(level_fico) != int(
                    #         plankton_level) and parent_category_id:
                    if parent_category_id:
                        print(f'Level fico {level_fico}, Level plankton '
                              f'{plankton_level}, parent category {parent_category_id}')
                        category.write({'parent_id': int(parent_category_id)})
                        print(category)

                    time.sleep(0.5)
        end = time.time()
        print(end - start)

    def check_level_category_fico(self):
        with (open('myfile.csv', 'r') as f):
            reader = csv.reader(f)
            unknown_category = []
            for row in reader:
                if row[0] == "id" or row[4] is None:
                    continue

                if row[6] == "Not Match":
                    plankton_level = row[7]
                    id_fico = row[0]
                    category = self.odoo.env['product.category'].browse(
                        int(id_fico))
                    level_fico = category.parent_path.count("/")
                    if int(level_fico) != int(plankton_level):
                        print(f'category: {row[3]}')
                        unknown_category.append(id_fico)
                time.sleep(0.5)
            print(unknown_category)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    odoo = CategoryOdoo()
    # odoo.update_plankton_id()
    odoo.update_parent_category_fico2()
    # odoo.check_level_category_fico()
