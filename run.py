import csv
import logging
import time


class Compare:
    csv_rows = [['id', 'Parent Path', 'complete Name', 'name', 'plankton_id',
                 'Plankton Breadcrumbs', 'Level Match?', 'Plankton Level',
                 'parent_id', 'query']]

    def read_csv_file(self, filename):
        logging.info("Reading CSV file")
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            self.write_csv_file(self.csv_rows)
            for row in reader:
                if row[2] == 'name':
                    continue
                # row[2] is name
                # row[0] is ID plankton
                self.find_in_csv(row)
                # sys.stdout.flush()
                time.sleep(0.1)

    @staticmethod
    def compare_level(path, level):
        split_path = path.split('/')
        split_path = list(filter(None, split_path))  # remove empty string
        if len(split_path) == int(level):
            return "Match"
        return "Not Match"

    def find_in_csv(self, rows):
        fico_id = rows[0]
        parent_path = rows[1]
        data = rows[2]
        complete_name = rows[3]
        with open('product_category_prod.csv', 'r') as pc:
            reader = csv.reader(pc)
            print(f'Fico category: {data}')
            query, breadcrumbs, plankton_id = "", "", ""
            level_match, current_level, parent_id = "-", "-", ""
            for row in reader:
                # row[5] is name 3428068
                if row[5].strip().lower() == data.lower():
                    plankton_id = row[0]
                    breadcrumbs = row[1]
                    current_level = row[2]
                    parent_id = row[7]
                    query = (f"update product_category set plankton_id='"
                             f"{plankton_id}' where id={fico_id};")
                    level_match = self.compare_level(parent_path, current_level)

            self.write_csv_file(
                [
                    [
                        fico_id,
                        parent_path,
                        complete_name,
                        data,
                        plankton_id,
                        breadcrumbs,
                        level_match,
                        current_level,
                        parent_id,
                        query
                    ]
                ]
            )

        return True

    @staticmethod
    def write_csv_file(data):
        out = csv.writer(open("myfile.csv", "a+"), delimiter=',')
        out.writerows(data)


Compare().read_csv_file('product_category_prod_fico.csv')

# rows = [
#     ['id', 'name', 'plankton_id'],
#     ['4451', 'Rental Software', '10658083253'],
#     ['4447', 'Rental Peralatan Masak dan Dapur', '10658083193']
# ]

# Compare().write_csv_file(rows)
