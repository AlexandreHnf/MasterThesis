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

def main():
    small_graph = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\big graphs\\small_graph.json"

    small_graph_nodes = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\big graphs\\small_graph_nodes.json"
    small_graph_adj = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\big graphs\\small_graph_adj.json"

    node_coords, adjlist = parseJson(small_graph)

    with open(small_graph_adj, 'w') as fp:
        fp.write(json.dumps(adjlist))
    with open(small_graph_nodes, 'w') as fp:
        fp.write(json.dumps(node_coords))




if __name__ == "__main__":
    main()