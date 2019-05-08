# -*- coding: utf-8 -*-
from py2neo import Graph, Node, Relationship
import json
from docx import *
from course.util import *

# 将对象列表中对象持久化到图形数据库
def saveListOfObjectToDB(DBgraph,objectlist):
    try:
        for object in objectlist:
            # print(type(object))
            DBgraph.push(object)
    except Exception as e:
        print(e)


graph = Graph("http://localhost:7474", username="neo4j", password='431879')
# MATCH (a:`指标点`)-[r:Subitem]-(b:`指标点`) delete r


# data1 = graph.data('MATCH(p) return p')
# print("data1 = ", data1, type(data1))
# 用find_one()方法进行node查找，返回的是查找node的第一个node
#
# 执行cql获取数据
# 返回数据列表
def getdata(cql):
    try:
        data2 = graph.run(cql)
        data4 = data2.data()
        print(type(data4))

    except Exception as e:
        print('cql run error')
        print('Neo Error: ',e)
    return data4



if __name__ == '__main__':

    # courseTable = getCourseTable(doc, 0)
    # print(courseTable)
    name = '1'
    courseName = 'Java Web技术'
    cql = 'MATCH (n:TeachingObjective {name:"'+ name +'",courseName:"'+ courseName +'"})  RETURN n '
    cql = 'MATCH (n:TeachingObjective {name:"'+ name +'",courseName:"'+ courseName +'"})  delete n '
    cql = 'match (n) return n.name limit 10'
    # cql = 'MATCH p=()-[r:CONTRIBUTION]->() RETURN p'
    # cql = 'MATCH p=()-->() RETURN p LIMIT 10'
    # cql = 'MATCH (n:course) RETURN n LIMIT 25'
    # cql = 'create (n:course { tit: "javatest",coursename:"标题"}) return n '
    # cql = 'MATCH (n { tit: "javatest",coursename:"标题"}) RETURN n LIMIT 25'
    # cql = 'create (n:course '+ jsonToCQLjson(courseTable) +') return n'
    print(cql)
    data = getdata(cql)
    print(data)
    print(len(getdata(cql)))
    for i in data:
        print(type(i))
        print(i)
        print(i['p'])
        print(type(i['p']))
        i['p'].walk