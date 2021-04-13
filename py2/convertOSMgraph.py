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
    with open(filename, 'r', encoding='utf-8') as myfile:
        data = myfile.read()

    # parse file
    all_json = json.loads(data)
    features = all_json["features"]
    node_coords = {}
    adjlist = {}
    for f in features:
        # print(f["properties"]["tags"])
        if f["geometry"]["type"] == "Point":
            # (lat, lon)
            point = [f["geometry"]["coordinates"][1], f["geometry"]["coordinates"][0]]
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
    bxl_square_graph = W + "small_graph\\test_bxl_square.json"
    bxl_square_graph_nodes = W + "small_graph\\test_bxl_square_nodes.json"
    bxl_square_graph_adj = W + "small_graph\\test_bxl_square_adj.json"

    node_coords, adjlist = parseJson(bxl_square_graph)
    writeToJson(node_coords, adjlist, bxl_square_graph_adj, bxl_square_graph_nodes)

def ulbGraph():
    pass

def bxlCtrGraph():
    bxl_ctr_graph = W + "big graphs\\graphes victor\\graph_2_bxl_ctr.json"
    bxl_ctr_graph_nodes = W + "big graphs\\graphes victor\\graph_2_bxl_ctr_nodes.json"
    bxl_ctr_graph_adj = W + "big graphs\\graphes victor\\graph_2_bxl_ctr_adj.json"

    node_coords, adjlist = parseJson(bxl_ctr_graph)
    writeToJson(node_coords, adjlist, bxl_ctr_graph_adj, bxl_ctr_graph_nodes)

def bxlGraph():
    bxl_graph = W + "big graphs\\graphes victor\\graph_3_bxl.json"
    bxl_graph_nodes = W + "big graphs\\graphes victor\\graph_3_bxl_nodes.json"
    bxl_graph_adj = W + "big graphs\\graphes victor\\graph_3_bxl_adj.json"

    node_coords, adjlist = parseJson(bxl_graph)
    writeToJson(node_coords, adjlist, bxl_graph_adj, bxl_graph_nodes)

def beCtrGraph():
    be_ctr_graph = W + "big graphs\\graphes victor\\graph_4_be_ctr.json"
    be_ctr_graph_nodes = W + "big graphs\\graphes victor\\graph_4_be_ctr_nodes.json"
    be_ctr_graph_adj = W + "big graphs\\graphes victor\\graph_4_be_ctr_adj.json"

    node_coords, adjlist = parseJson(be_ctr_graph)
    writeToJson(node_coords, adjlist, be_ctr_graph_adj, be_ctr_graph_nodes)

def beGraph():
    be_graph = W + "big graphs\\graphes victor\\graph_5_be.json"
    be_graph_nodes = W + "big graphs\\graphes victor\\graph_5_be_nodes.json"
    be_graph_adj = W + "big graphs\\graphes victor\\graph_5_be_adj.json"

    node_coords, adjlist = parseJson(be_graph)
    writeToJson(node_coords, adjlist, be_graph_adj, be_graph_nodes)

def main():
    pass
    # smallGraph()

    bxlSquare()
    bxlCtrGraph()
    bxlGraph()
    beCtrGraph()
    beGraph()



if __name__ == "__main__":
    main()