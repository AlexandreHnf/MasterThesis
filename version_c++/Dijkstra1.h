//
// Created by Alexandre on 12-11-20.
//

#ifndef CODES_DIJKSTRA1_H
#define CODES_DIJKSTRA1_H

#define INT_MAXIM 10000000

#include <iostream>
#include <vector>
#include "GraphDijkstra.h"
#include "Node.h"

using namespace std;

class Dijkstra1 {
    private:
        GraphDijkstra _graph;
        const int _start;
        const int _dest;

    public:
        Dijkstra1(int, int, GraphDijkstra);

        // methods
        double deg2rad(double);
        double rad2deg(double);
        double distanceEarth(double, double, double, double);
        vector<Node*>* AdjacentRemainingNodes(Node* node);
        Node* ExtractMinimum();
        float Distance(Node* node1, Node* node2);
        void PrintShortestRouteTo();
        void runDijkstra();
};


#endif //CODES_DIJKSTRA1_H
