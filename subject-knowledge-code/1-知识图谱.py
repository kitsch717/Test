__author__ = '...'
# !_*_coding:utf-8_*_
import re, json, os
from collections import OrderedDict
import json, csv
import difflib
import xlrd
from xlrd import xldate_as_tuple

class QueryNo4j:
    def __init__(self):
        self.patenId = 0#当前id号
        # 【实体构建】
        self.h_nodes = OrderedDict() # 【实体节点】  节点
        #【关系构建】
        self.h_rela = OrderedDict() # 【关系】关系
        # 【实体和关系文件】
        self.arr = [
            # 【实体对应实体文件名称】
            [self.h_nodes, "entity_node"],
            # 【关系对应关系文件名称】
            [self.h_rela, "rela_node"],
        ]

    # 参数：实体节点hash，节点名称，实体标签，节点相关属性，上级标签
    def entity_node(self, h_node,name,label_name,suxing,start_name):
        node_key = "%s_%s_%s" % (start_name, label_name, name)
        hash = OrderedDict()

        hash[':ID'] = "d_%s_%s" % (label_name, self.patenId)
        hash['name'] = name
        hash[':LABEL'] = label_name
        if suxing != {}:
            for key1,val1 in suxing.items():
                hash[key1] = val1

        # ***  如果节点存在：
        if node_key in h_node:
            if "text" in suxing: # 如果text属性存在，则更新
                h_node[node_key]["text"] = suxing["text"]  # 如果节点存在，则更新text内容  *********
            return h_node[node_key]
        else:
            self.patenId += 1
            h_node[node_key] = hash
            return hash

    # 创建关系：关系hash，开始节点，结束节点，关系名称_name,关系名称_label,属性信息hash
    def node2node(self,h_rale_name, start_id, end_id,ralename,ralename_en,suxing):
        index = "%s<#>%s" % (start_id, end_id)
        h_rale = {}
        h_rale[':START_ID'] = start_id
        h_rale['name'] = ralename
        h_rale[':END_ID'] = end_id
        h_rale[':TYPE'] = ralename_en

        if suxing != {}:
            for key1,val1 in suxing.items():
                h_rale[key1] = val1
        h_rale_name[index] = h_rale

 # 【主体】创建实体和关系
    def creat_entity(self,filename_txt):
        with xlrd.open_workbook(filename_txt) as workbook:
            name_sheets = workbook.sheet_names()  # 获取Excel的sheet表列表，存储是sheet表名
            for index in name_sheets:  # for 循环读取每一个sheet表的内容
                if index != "Sheet1": continue
                sheet_info = workbook.sheet_by_name(index)  # 根据表名获取表中的所有内容，sheet_info也是列表，列表中的值是每个单元格里值
                first_line = sheet_info.row_values(0)  # 获取首行，我这里的首行是表头，我打算用表头作为字典的key，每一行数据对应表头的value，每一行组成一个字典
                values_merge_cell = sheet_info
                for i in range(1, sheet_info.nrows):  # 开始为组成字典准备数据
                    other_line = sheet_info.row_values(i)

                    # dic = OrderedDict(map(lambda x, y: [x, y], first_line, other_line))
                    text = other_line[0]
                    subject = other_line[1]
                    rela = other_line[2]
                    object = other_line[3]

                    from_node_id = self.entity_node(self.h_nodes, subject, "Nodes", {}, "")[":ID"]
                    to_node_id = self.entity_node(self.h_nodes, object, "Nodes", {}, "")[":ID"]

                    self.node2node(self.h_rela, from_node_id, to_node_id, rela, "predicate", {})

        # 【生成实体和关系文件】 首先清理原始数据
        if os.path.exists("%s/%s.txt" % (dirname, "entity_node")):
            os.remove("%s/%s.txt" % (dirname, "entity_node"))
        if os.path.exists("%s/%s.txt" % (dirname, "rela_node")):
            os.remove("%s/%s.txt" % (dirname, "rela_node"))
        if os.path.exists(dirname) == False: os.makedirs(dirname)
        for item in self.arr:
                fw = open("%s/%s.txt" % (dirname, item[1]), "w", encoding="utf-8") # 追加方式
                for key, value in item[0].items():
                        value_s = json.dumps(value, ensure_ascii=False)
                        value_s = re.sub(r'\\n|\\r', '<n>', value_s)
                        fw.write(value_s + "\n")

if __name__ == '__main__':
    _qN = QueryNo4j()
    dirname = "./subject"
    filename_txt = "三元组实例.xls"
    _qN.creat_entity(filename_txt)
    exit()




