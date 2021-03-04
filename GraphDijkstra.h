//
// Created by Alexandre on 06-11-20.
//

#ifndef CODES_GRAPHDIJKSTRA_H
#define CODES_GRAPHDIJKSTRA_H

#include <iostream>
#include <vector>
#include "Node.h"

using namespace std;


class GraphDijkstra{
    private:
        vector<Node*> _nodes;

    public:
        GraphDijkstra() {} // constructor

        void createNode(int id, float lat, float lon);

        int getNodesSize() const;
        Node* getNode(int i) const;
        void show() const;
};




#endif //CODES_GRAPHDIJKSTRA_H
