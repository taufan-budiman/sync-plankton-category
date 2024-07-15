import csv
import time
from functools import wraps

import odoorpc


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # first item in the args, ie `args[0]` is `self`
        print(f'Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


class OdooCategory:

    def __init__(self):
        odoo_conn = odoorpc.ODOO('dev-erp.bhinnekalocal.com', port=443,
                                 protocol='jsonrpc+ssl')
        odoo_conn.login('development-bmd22', 'bmdbot', 'bmdjayaselalu')
        self.odoo = odoo_conn

    @timeit
    def upsert_plankton_id(self):
        # 2,5 jam atau Took 8777.2533 seconds
        with open('product_category_prod.csv', 'r') as pc:
            reader = csv.reader(pc)
            for row in reader:
                if row[0] == 'id' or row[8] == 'deleted':
                    continue

                name = row[5]
                category = self.odoo.env['product.category']
                print(f"find category {name} in fico")
                search_category = category.search(
                    [
                        ('name', '=', name)
                    ]
                )
                if search_category:
                    print(f"Update Category {name}")
                    category_object = category.browse(search_category[0])
                    category_object.write(
                        {'plankton_id': row[0]}
                    )
                else:
                    print(f"Create Category {name}")
                    category.create(
                        {
                            'name': name,
                            'plankton_id': row[0]
                        }
                    )

                time.sleep(0.5)
            print(f'total data: {reader.line_num}')

    @timeit
    def update_parent_fico(self):
        """
        Category found: Stop Kontak in Bow, 400, plankton_id: 3425794
        Category found: Kamera Mobil dan Aksesori, 1904, plankton_id: 3423952
        cCategory found: Aksesori Kamera Mobil, 3340, plankton_id: 3423984
        ['3425794', '3423952', '3423984']
        Took 6352.2793 seconds
        :return:
        """
        # Took 8042.0997 seconds atau 2,5 jam
        with open('product_category_prod.csv', 'r') as pc:
            reader = csv.reader(pc)
            need_to_check = []
            for row in reader:
                if row[0] == 'id' or row[8] == 'deleted':
                    continue

                plankton_id = row[0]
                parent_plankton_id = row[7] if row[7] else False
                category = self.odoo.env['product.category']
                category_search = category.search([
                    ('plankton_id', '=', plankton_id)
                ])
                if category_search:
                    category_object = category.browse(category_search[0])
                    # jika ada parent plankton, cari id parentnya
                    if parent_plankton_id:

                        print(f'find parent category {category_object.name}')
                        parent_search = category.search([
                            ('plankton_id', '=', parent_plankton_id)
                        ])
                        if parent_search:
                            parent_plankton_id = parent_search[0]
                            print(f'set parent to {parent_plankton_id}')
                    try:
                        category_object.write({'parent_id': parent_plankton_id})
                    except odoorpc.error.RPCError:
                        need_to_check.append(parent_plankton_id)
                        print(f'need to check {parent_plankton_id}')

                print('Update Done')
                time.sleep(1)
            print(need_to_check)
            print(f'total data: {reader.line_num}')

    @timeit
    def check_level_fico_plankton(self):
        with open('product_category_prod.csv', 'r') as pc:
            reader = csv.reader(pc)
            known_plankton_id = []
            for row in reader:
                if row[0] == 'id' or row[8] == 'deleted':
                    continue

                plankton_id = row[0]
                plankton_level = row[2]
                category = self.odoo.env['product.category']
                category_search = category.search([
                    ('plankton_id', '=', plankton_id)
                ])
                if category_search:
                    category_object = category.browse(category_search[0])

                    fico_level = category_object.parent_path.count("/")
                    if int(plankton_level) != int(fico_level):
                        print(f'Category found: {category_object.name}, '
                              f'{str(category_object.id)}, plankton_id: '
                              f'{plankton_id}')
                        known_plankton_id.append(row[0])
                time.sleep(0.5)
            print(known_plankton_id)


if __name__ == '__main__':
    odoo = OdooCategory()
    # odoo.upsert_plankton_id()
    # odoo.update_parent_fico()
    odoo.check_level_fico_plankton()
