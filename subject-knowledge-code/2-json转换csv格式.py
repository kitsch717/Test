#-*- coding:utf-8 -*-
# coding = UTF-8
import json
import os
import re
import csv
from collections import OrderedDict
def txtTocsv(dirname):
    dirname_csv = dirname + "-csv"
    if not os.path.exists(dirname_csv):
        os.mkdir(dirname_csv)
        print(dirname_csv)
    else:
        return
    for dirpath, dirpath2, dirpath3 in os.walk(dirname):
        for file in dirpath3:
            # if re.search(r'^r_pat_App\.txt$', file) == None:continue
            url = dirpath + "/" + file
            filename_csv = dirname_csv + "/" + re.sub(".txt", ".csv", file)
            filename_csv_header = dirname_csv + "/" + re.sub(".txt", ".Header.csv", file)

            fw = open(filename_csv, "w", encoding='utf-8', newline='')
            writer = csv.writer(fw)
            fw_h = open(filename_csv_header, "w", encoding='utf-8')

            fr = open(url, "r", encoding="utf-8")
            arr_head = []
            hash_new_head = OrderedDict()
            for line in fr:
                jsonData = line.strip()
                try:
                    doc = json.loads(jsonData, object_pairs_hook=OrderedDict)  # 保持json解码后顺序不变
                except:
                    pass
                for kk in  list(doc.keys()):
                    hash_new_head[kk] = 1
            print(list(hash_new_head.keys()))
            fr.close()

            fr = open(url, "r", encoding="utf-8")
            for line in fr:
                jsonData = line.strip()
                try:
                    doc = json.loads(jsonData, object_pairs_hook=OrderedDict)  # 保持json解码后顺序不变
                except:
                    pass
                hash_new_json = OrderedDict()
                for kk in list(hash_new_head.keys()):
                    vv  = doc.get(kk,"")
                    hash_new_json[kk] = vv
                doc = hash_new_json
                # csv直接写入文档。
                arr_value = doc.values()
                writer.writerow(arr_value)
                if arr_head == []: arr_head = list(doc.keys())
            fw_h.write(",".join(arr_head))

dirname = "./subject"
txtTocsv(dirname)
exit()
