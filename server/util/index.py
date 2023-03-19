import uuid
import os


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def fetch_dict_result(cur):
    row_headers =[x[0] for x in cur.description]
    rv = cur.fetchall()
    res = []
    for value in rv:
        dictionary = {}
        idx = 0
        for header in row_headers:
            dictionary[header] = value[idx]
            idx += 1
        res.append(dictionary)
    return res
