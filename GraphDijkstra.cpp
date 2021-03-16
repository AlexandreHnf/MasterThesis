//
// Created by Alexandre on 06-11-20.
//

#include "GraphDijkstra.h"
#include <iostream>
#include <vector>

#define G_INT_MAXI 10000000

using namespace std;

// ========================== GraphDijkstra:: =================================

// constructor defined in hpp

// getter
int GraphDijkstra::getNodesSize() const {return _nodes.size();}
Node* GraphDijkstra::getNode(int i) const {return _nodes.at(i);}

// Other
void GraphDijkstra::createNode(int id, float lat, float lon) {
    Node* new_node = new Node(id, lat, lon);
    _nodes.push_back(new_node);
}

void GraphDijkstra::show() const {
    std::cout << "Graph : " << std::endl;
    for (int i = 0; i < _nodes.size(); i++) {
        std::cout << "Node " << _nodes.at(i)->getId() << ", adj : ";
        for (int j = 0; j < _nodes.at(i)->getNbAdjacents(); j++) {
            std::cout << _nodes.at(i)->getAdjacentNode(j)->getId() << ", ";
        }
        std::cout << "marked : " << _nodes.at(i)->getMark();
        std::cout << endl;;
    }
}
