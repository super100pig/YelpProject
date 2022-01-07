import py2neo
from django.http import HttpResponse
import json
import pymysql
import datetime
from concurrent.futures import ProcessPoolExecutor
from backend.algorithm import do_some_work
from backend import db_setting
from tensorflow import keras
from bert_serving.client import BertClient


def get_json_by_node_id_and_depth_from_neo4j(request):
    request_content = request.GET
    node_id = request_content.get("node_id")
    depth = request_content.get("depth")
    graph = py2neo.Graph(db_setting.neo4j_url, username=db_setting.neo4j_username, password=db_setting.neo4j_password)
    cypher = "match p=(n)-[*1..%s]-() where n.id=%s with extract(x in nodes(p) | x) as ns, extract(x in relationships(p) | {start: id(startnode(x)), end: id(endnode(x)), rel: type(x), id: id(x), properties: properties(x)}) as rs, n unwind ns as na unwind rs as ra return collect(DISTINCT na),collect(DISTINCT ra), n" % (depth, node_id)
    data = graph.run(cypher).data()
    nodes = []
    for node in data[0]["collect(DISTINCT na)"]:
        label = list(node.labels)[0]
        node_id = node.identity
        complete_node = {
            "labels": [label],
            "id": node_id,
            "properties": dict(node.items()),
            "showName": node["name"],
            # "x": 0,
            # "y": 0,
        }
        nodes.append(complete_node)
    relationships = []
    for rel in data[0]["collect(DISTINCT ra)"]:
        complete_rel = {
            "startNode": rel["start"],
            "endNode": rel["end"],
            "source": rel["start"],
            "target": rel["end"],
            "id": rel["id"],
            "type": rel["rel"],
            "properties": rel["properties"],
            "linknum": "1",
            "showName": "",
        }
        relationships.append(complete_rel)
    ret = {
        "center_id": data[0]["n"].identity,
        "nodes": nodes,
        "relationships": relationships
    }

    db = pymysql.connect(host=db_setting.host,
                         user=db_setting.user,
                         password=db_setting.password,
                         db=db_setting.db,
                         charset=db_setting.charset,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    for node in ret['nodes']:
        score = 0
        try:
            sql = '''select score from label_mat where node = %s ''' % node['properties']['id']
            print(sql)
            cursor.execute(sql)
            data = cursor.fetchone()
            score = data['score']
        except Exception as e:
            print(e)
        color = rgb_to_hex(int(227 - 200 * score), int(227 - 200 * score), int(227 - 200 * score))
        node['properties']['color'] = color
        node['properties']['score'] = score

    return HttpResponse(json.dumps(ret))


def run_new_algorithm(request):
    request_content = request.GET
    algorithm_name = request_content.get("algorithm_name")
    data_name = request_content.get("data_name")
    db = pymysql.connect(host=db_setting.host,
                         user=db_setting.user,
                         password=db_setting.password,
                         db=db_setting.db,
                         charset=db_setting.charset,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    sql = '''INSERT INTO algorithm(algorithm_name, data_name, status, start_time) VALUES ('%s', '%s',  1,  '%s')''' % (
        algorithm_name,
        data_name,
        datetime.datetime.now())
    cursor.execute(sql)
    db.commit()
    cursor.execute('SELECT LAST_INSERT_ID() as id')
    run_id = cursor.fetchone()['id']
    pool = ProcessPoolExecutor()
    pool.submit(do_some_work, run_id)
    return HttpResponse(json.dumps({'status': 'success'}))


def get_all_algorithm(request):
    db = pymysql.connect(host=db_setting.host,
                         user=db_setting.user,
                         password=db_setting.password,
                         db=db_setting.db,
                         charset=db_setting.charset,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    sql = '''SELECT * FROM algorithm limit 100'''
    cursor.execute(sql)
    algorithms = cursor.fetchall()
    status_map = {
        0: '未知',
        1: '正在运行',
        2: '运行成功',
        -1: '运行失败'
    }
    for algorithm in algorithms:
        algorithm['start_time'] = str(algorithm['start_time'])
        algorithm['end_time'] = str(algorithm['end_time'])
        algorithm['status'] = status_map[int(algorithm['status'])]
    db.close()
    return HttpResponse(json.dumps(algorithms))


def get_all_nodes(request):
    db = pymysql.connect(host=db_setting.host,
                         user=db_setting.user,
                         password=db_setting.password,
                         db=db_setting.db,
                         charset=db_setting.charset,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    sql = '''SELECT * FROM label_mat order by score desc  limit 100'''
    cursor.execute(sql)
    nodes = cursor.fetchall()
    db.close()
    return HttpResponse(json.dumps(nodes))


def get_all_edges(request):
    db = pymysql.connect(host=db_setting.host,
                         user=db_setting.user,
                         password=db_setting.password,
                         db=db_setting.db,
                         charset=db_setting.charset,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    sql = '''SELECT * FROM adj_mat limit 100'''
    cursor.execute(sql)
    nodes = cursor.fetchall()
    db.close()
    return HttpResponse(json.dumps(nodes))


def rgb_to_hex(r, g, b):
    color = '#'
    color += str(hex(r))[-2:].replace('x', '0').upper()
    color += str(hex(g))[-2:].replace('x', '0').upper()
    color += str(hex(b))[-2:].replace('x', '0').upper()
    return color


def get_all_devices(request):
    db = pymysql.connect(host=db_setting.host,
                         user=db_setting.user,
                         password=db_setting.password,
                         db=db_setting.db,
                         charset=db_setting.charset,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    sql = '''SELECT * FROM device order by score desc limit 100 '''
    cursor.execute(sql)
    nodes = cursor.fetchall()
    db.close()
    return HttpResponse(json.dumps(nodes))


def get_node_paths(request):
    db = pymysql.connect(host=db_setting.host,
                         user=db_setting.user,
                         password=db_setting.password,
                         db=db_setting.db,
                         charset=db_setting.charset,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    request_content = request.GET
    component_id = request_content.get("node")
    sql = '''SELECT `label`, `score`, `node_path` FROM label_mat WHERE node = %s''' % component_id
    cursor.execute(sql)
    data = cursor.fetchone()
    label = data['label']
    score = data['score']
    device_path = data['node_path']
    devices = device_path.split(',')

    graph_data = {'center_id': 1, 'nodes': [], 'relationships': []}
    graph_data['nodes'].append({
        'labels': ['Component'],
        'id': 1,
        'properties': {
            'name': 'Component ' + component_id,
            'label': label,
            'score': score,
            'color': rgb_to_hex(int(227 - 200 * score), int(227 - 200 * score), int(227 - 200 * score))
        },
        'showName': 'Component ' + component_id,
    })
    pre_node_id = 1
    edge_id = 101
    for device_id in devices:
        sql = '''SELECT `score` FROM device WHERE `device_id` = '%s' ''' % device_id
        cursor.execute(sql)
        data = cursor.fetchone()
        graph_data['nodes'].append({
            'labels': ['Station'],
            'id': pre_node_id + 1,
            'properties': {
                'name': 'Station ' + device_id,
                'score': data['score'],
                'color': rgb_to_hex(int(227 - 200 * data['score']), int(227 - 200 * data['score']), int(227 - 200 * data['score']))
            },
            'showName': 'Station ' + device_id
        })
        graph_data['relationships'].append({
          "startNode": pre_node_id,
          "endNode": pre_node_id + 1,
          "source": pre_node_id,
          "target": pre_node_id + 1,
          "id": edge_id,
          "type": "rel",
          "properties": {},
          "linknum": "1",
          "showName": ""
        })
        pre_node_id += 1
        edge_id += 1
    db.close()

    return HttpResponse(json.dumps(graph_data))


def get_score(request):
    bc = BertClient()
    request_content = request.GET
    text = request_content.get("text")
    model = keras.models.load_model('/home/panwentao/yelp2vec_model.h5')
    x_vec = bc.encode([text])
    y = model.predict(x_vec)
    res = {'score': float(y[0][0])}
    return HttpResponse(json.dumps(res))
