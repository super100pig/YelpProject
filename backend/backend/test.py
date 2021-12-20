import py2neo
from datetime import datetime

def code():
    graph = py2neo.Graph('http://10.176.38.226:7474', username='neo4j', password='abc123')
    cypher = "match p=(n)-[*1..1]-() where id(n)=%s with extract(x in nodes(p) | x) as ns, extract(x in relationships(p) | {start: id(startnode(x)), end: id(endnode(x)), rel: type(x), id: id(x), properties: properties(x)}) as rs, n unwind ns as na unwind rs as ra return collect(DISTINCT na),collect(DISTINCT ra), n" % (1165702)
    # print(cypher)
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
            "linknum": "1"
        }
        relationships.append(complete_rel)
    ret = {
        "center_id": data[0]["n"].identity,
        "nodes": nodes,
        "relationships": relationships
    }
    print(ret)


if __name__ == '__main__':
    print(datetime.now())
