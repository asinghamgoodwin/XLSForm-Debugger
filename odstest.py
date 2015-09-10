import sys 
from pyexcel_ods import get_data
import pyexcel as pe
import pyexcel.ext.ods
import ast

import json
import pudb


data = get_data(sys.argv[1])
workbook = json.dumps(data)
d = ast.literal_eval(workbook)
print d.keys()
print len(d['choices'])
print d['choices'][1][:5]
#book = pe.get_book(file_name=sys.argv[1])
#sheets = book.to_dict()

#for name in sheets.keys():
#    print name
