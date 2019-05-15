# -*- coding: utf-8 -*-
from py2neo import Graph, Node, Relationship
import json
from docx import *
from course.util import *
# 全局变量
# neo4j中的标签
lables = ['Course', 'TeachingObjective', 'IndexPoint']
graph = Graph("http://localhost:7474", username="neo4j", password='431879')


# 将对象列表中对象持久化到图形数据库
def saveListOfObjectToDB(DBgraph,objectlist):
    try:
        for object in objectlist:
            # print(type(object))
            DBgraph.push(object)
    except Exception as e:
        print(e)

# 执行cql获取数据
# 返回数据列表
def getData(cql):
    try:
        # 执行查询并转换为列表
        data = graph.run(cql).data()
    except Exception as e:
        print('cql run error')
        print('Neo Error: ',e)
    return data

#获取所有同标签节点name
def getNodenameByLabel(label):
    cql = 'MATCH (n:'+ label +') RETURN n.name'
    try:
        data = getData(cql)
    except Exception as e:
        print('input lable not found')
        print(e)
    return data

# 标签，对应前端，图例
def getCategories():
    categories = []
    for lable in lables:
        categories.append({'name':lable})
    return categories

# 从数据库中获取所有节点
def getNodes():
    # name：节点名称 取neo4j中的节点名称
    # category:对应图例的索引，必须为整数值。
    # 名称和值都可以展示
    # symbolSize设置节点大小
    nodes = []
    for lable in lables:
        dataList = getNodenameByLabel(lable)
        for data in dataList:
            node = {'name': '','category': '','symbolSize':'20'}
            node['name'] = data['n.name']
            node['category'] = lables.index(lable)
            nodes.append(node)
    return nodes

# 从数据库中获取所有边
def getLinks():
    # source:源节点 的名称
    # target：目标节点 的名称
    # value：可有可无， 取neo4j中的边的值
    # 方向可以展示，单向，可覆盖方向。 例：2》3和3》2 ，最终展示结果是后面方向覆盖前面方向
    links = []
    cql = 'MATCH p=()-->() RETURN p'
    dataList = getData(cql)
    for data in dataList:
        recoad = data['p']
        for relation in recoad.relationships:
            link = {'source': '', 'target': '', 'value': ''}
            link['source'] = relation.start_node['name']
            link['target'] = relation.end_node['name']
            links.append(link)
    return links


if __name__ == '__main__':

    name = '1'
    courseName = 'Java Web技术'
    cql = 'MATCH (n:TeachingObjective {name:"'+ name +'",courseName:"'+ courseName +'"})  RETURN n '
    cql = 'MATCH (n:TeachingObjective {name:"'+ name +'",courseName:"'+ courseName +'"})  delete n '
    cql = 'match (n) return n.name limit 10'
    cql = 'MATCH p=()-[r:REACH]->() RETURN p'
    # cql = 'MATCH p=()-->() RETURN p LIMIT 10'
    # cql = 'MATCH (n:course) RETURN n LIMIT 25'
    # cql = 'create (n:course { tit: "javatest",coursename:"标题"}) return n '
    # cql = 'MATCH (n { tit: "javatest",coursename:"标题"}) RETURN n LIMIT 25'
    # cql = 'create (n:course '+ jsonToCQLjson(courseTable) +') return n'



    print(getNodes())
    print(getLinks())
