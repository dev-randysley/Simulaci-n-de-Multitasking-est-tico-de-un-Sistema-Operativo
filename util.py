import csv

def parse_csv(filename, select = None, types = None, has_headers = True):
    with open(filename) as f:
        rows = csv.reader(f)

        if has_headers:
            headers = next(rows) # first row is for headers

        if has_headers:
            if select:
                indices = [headers.index(column_name) for column_name in select]
                headers = select
            else:
                indices = []

        records = []
        for row in rows:
            if not row: #ignore empty rows   
                continue

            if has_headers and indices:
                row = [row[index] for index in indices]

            if types:
                row = [func(val) for func, val in zip(types, row)]

            if has_headers:
                registro = dict(zip(headers, row))
                records.append(registro)
            else:
                registro = tuple(row)
                records.append(registro)

    return records