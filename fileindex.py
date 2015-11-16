import os.path
import filemeta
import json

meta_data_dict = dict()

if False:
    # os.path.isfile('.index'):
    # TODO: compare the index hash and current hash
    pass
else:
    # build index
    f = open('.index', 'w')
    file_names_list = os.listdir("./")
    for filename in file_names_list:
        if os.path.isfile(filename):
            # print(filemeta.filemeta(filename))
            meta_data_dict.setdefault(filename, filemeta.filemeta(filename))
    print(meta_data_dict)
    f.write(json.dumps(meta_data_dict))
    f.close()