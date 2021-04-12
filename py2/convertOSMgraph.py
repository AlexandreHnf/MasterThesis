import json

""" 
 POINT
 - obj.features[i].geometry.type
 - obj.features[i].geometry.coordinates
 - obj.features[i].id

 EDGE
 - obj.features[i].geometry.type
 - obj.features[i].src
 - obj.features[i].tgt
"""

W = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\Datasets_graphs\\"

def parseJson(filename):
    # read file
    with open(filename, 'r') as myfile:
        data = myfile.read()

    # parse file
    all_json = json.loads(data)
    features = all_json["features"]
    node_coords = {}
    adjlist = {}
    for f in features:
        # print(f["properties"]["tags"])
        if f["geometry"]["type"] == "Point":
            point = [f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][1]]
            node_coords[f["id"]] = point
            adjlist[f["id"]] = []

        elif f["geometry"]["type"] == "LineString":
            src = f["src"]
            tgt = f["tgt"]
            adjlist[src].append(tgt)
            if "oneway" in f["properties"]["tags"]:
                if f["properties"]["tags"]["oneway"] == "no":
                    if (src not in adjlist[tgt]):
                        adjlist[tgt].append(src) # reverse arc
                    else:
                        print("deja dedans le reverse ah")
    return node_coords, adjlist

def writeToJson(node_coords, adjlist, fAdj, fNodes):
    with open(fAdj, 'w') as fp:
        fp.write(json.dumps(adjlist))
    with open(fNodes, 'w') as fp:
        fp.write(json.dumps(node_coords))

def smallGraph():
    small_graph = W + "small_graph\\small_graph.json"
    small_graph_nodes = W + "small_graph\\small_graph_nodes.json"
    small_graph_adj = W + "small_graph\\small_graph_adj.json"

    node_coords, adjlist = parseJson(small_graph)
    writeToJson(node_coords, adjlist, small_graph_adj, small_graph_nodes)

def bxlSquare():
    small_graph = W + "small_graph\\test_bxl_square.json"
    small_graph_nodes = W + "small_graph\\test_bxl_square_nodes.json"
    small_graph_adj = W + "small_graph\\test_bxl_square_adj.json"

    node_coords, adjlist = parseJson(small_graph)
    writeToJson(node_coords, adjlist, small_graph_adj, small_graph_nodes)

def ulbGraph():
    pass

def bxlCtrGraph():
    pass

def bxlGraph():
    pass

def beCtrGraph():
    pass

def beGraph():
    pass

def main():
    # smallGraph()

    bxlSquare()



if __name__ == "__main__":
    main()