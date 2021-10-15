# -*- coding: utf-8 -*-
import json
import xml.dom.minidom as xmldom
import os

"""
-- xml 转 json 
-- minidom解析xml文件
-- 数据处理
"""
def getDSSchema(xmlfile):
    xmlfilepath = os.path.abspath(xmlfile)
    # 得到文档对象
    domobj = xmldom.parse(xmlfilepath)
    # 得到元素对象
    elementobj = domobj.documentElement
    # 获得子标签  Record
    subElementObj = elementobj.getElementsByTagName("Record")

    jobDefnEle = ''
    for i in range(len(subElementObj)):
        if subElementObj[i].getAttribute('Type') == 'JobDefn':
            jobDefnEle = subElementObj[i]

    proEles = jobDefnEle.getElementsByTagName('Property')

    dSSchema = ''
    for i in range(len(proEles)):
        if proEles[i].getAttribute('Name') == 'OrchestrateCode':
            dSSchema = proEles[i].firstChild.data
    dSSchema = dSSchema.replace('\\', '')
    dSSchema = dSSchema.replace('\'', ' ')
    # print(dSSchema)

    # print('-------------------------------')
    dSSchema_tmp = dSSchema.split('DSSchema')[1].split('(')[1].split(')')[0]
    # 两个DSSchema 不取:nullable
    if len(dSSchema_tmp.split(':nullable')) > 1:
        dSSchema = dSSchema.split('DSSchema')[1]
        dSSchema_tmp = dSSchema.split('DSSchema')[1].split('(')[1].split(')')[0]
    dSSchema = dSSchema_tmp.replace('\n', '').replace(' ', '')
    dSSchema = dSSchema.split(';')

    print('字段信息：' + '|'.join(dSSchema))
    return dSSchema


def getReaderColumnList(dSSchema, tablename):
    colList = list()
    for i in range(len(dSSchema)):
        if dSSchema[i].split(':')[0] != '':
            colList.append(dSSchema[i].split(':')[0])
    # print(','.join(colList))
    colList.append('\'$ppn_tmstamp\'')
    colList.append('\'' + tablename + '\'')
    colList.append('\'0\'')
    colList.append('\'$modify_datetime\'')
    colList.append('\'$busi_date\'')
    return colList


def getWriterColumnList(dSSchema, tablename):
    colList = list()
    for i in range(len(dSSchema)):
        if dSSchema[i].split(':')[0] != '':
            tdict = {}
            tdict['name'] = dSSchema[i].split(':')[0]
            tdict['type'] = dSSchema[i].split(':')[1]
            if tdict['type'] == 'int32' or tdict['type'].startswith('decimal'):
                tdict['type'] = 'decimal'
            else:
                tdict['type'] = 'string'
            colList.append(tdict)
    # print(','.join(colList))

    colList.append({'name': 'ppn_tmstamp', 'type': 'timestamp'})
    colList.append({'name': 'etl_fl_nm', 'type': 'string'})
    colList.append({'name': 'operation_type', 'type': 'string'})
    colList.append({'name': 'modify_datetime', 'type': 'timestamp'})
    colList.append({'name': 'busi_date', 'type': 'string'})
    return colList


def replacejson(jsonfile, dSSchema, tablename):
    """
        替换json 文件
    :param jsonfile:
    :param dSSchema:
    :return:
    """
    with open(jsonfile, 'r') as f:
        config = json.load(f)
        reader = config['job']['content'][0]['reader']
        reader['parameter']['column'] = getReaderColumnList(dSSchema, tablename)

        writer = config['job']['content'][0]['writer']
        writer['parameter']['column'] = getWriterColumnList(dSSchema, tablename)
        print(config)
        return config


def witejson(jsonfile, jsonModel):
    """
    写入json 文件
    :param jsonfile:
    :param jsonModel:
    :return:
    """
    with open(jsonfile, 'w', encoding='utf-8') as json_file:
        json.dump(jsonModel, json_file, ensure_ascii=False)


if __name__ == "__main__":
    """
    主函数
    """
    dSSchema = getDSSchema("./data/123.xml")
    tablename = 'i_ld_ods_t53_applylist_1'
    jsonfile_templ = './data/templ.json'  # json模板
    jsonmodel = replacejson(jsonfile_templ, dSSchema, tablename)
    witejson('./data/test.json', jsonmodel)
