//
// Created by Alexandre Heneffe on 12-11-20.
//

#include "Dijkstra1.h"
#include <iostream>
#include <cmath>

#define earthRadiusKm 6371.0

using namespace std;

Dijkstra1::Dijkstra1(int s, int t, GraphDijkstra G):
            _start(s), _dest(t), _graph(G) {}

// Methods

// This function converts decimal degrees to radians
double Dijkstra1::deg2rad(double deg) {
    return (deg * M_PI / 180);
}

//  This function converts radians to decimal degrees
double Dijkstra1::rad2deg(double rad) {
    return (rad * 180 / M_PI);
}

double Dijkstra1::distanceEarth(double lat1d, double lon1d, double lat2d, double lon2d) {
    /*
     * Computes the distance between two geographic coordinates on earth
     */
    double lat1r, lon1r, lat2r, lon2r, u, v;
    lat1r = deg2rad(lat1d);
    lon1r = deg2rad(lon1d);
    lat2r = deg2rad(lat2d);
    lon2r = deg2rad(lon2d);
    u = sin((lat2r - lat1r)/2);
    v = sin((lon2r - lon1r)/2);
    return 2.0 * earthRadiusKm * asin(sqrt(u * u + cos(lat1r) * cos(lat2r) * v * v));
}


vector<Node*>* Dijkstra1::AdjacentRemainingNodes(Node* node){
    vector<Node*>* remaining_adjacents = new vector<Node*>();
    for (int i = 0; i < node->getNbAdjacents(); i++) {
        if (!node->getAdjacentNode(i)->getMark()) {
            // maybe more efficient to delete the node from adjacents
            remaining_adjacents->push_back(node->getAdjacentNode(i));
        }
    }
    return remaining_adjacents;
}


Node* Dijkstra1::ExtractMinimum() {
    int size = _graph.getNodesSize();
    if (size == 0) return nullptr;
    int smallestPosition = 0;
    Node* smallest = _graph.getNode(0);
    for (int i = 1; i < size; i++) {
        if (!_graph.getNode(i)->getMark()) { // if not marked (visited)
            Node *current = _graph.getNode(i);
            if (current->getDistFromStart() < smallest->getDistFromStart()) {
                smallest = current;
                smallestPosition = i;
            }
        }
    }
    _graph.getNode(smallestPosition)->mark(true);
    return smallest;
}


float Dijkstra1::Distance(Node* node1, Node* node2){
    float res = 0;
    for (int i = 0; i < node1->getNbAdjacents(); i++) {
        if (node2->getId() == node1->getAdjacentNode(i)->getId() ) {
            res= distanceEarth(node1->getLatitude(), node1->getLongitude(), node2->getLatitude(), node2->getLongitude());
        }
    }
    return res;
}

void Dijkstra1::runDijkstra(){
    Node* current = _graph.getNode(_start);
    while (current->getId() != _dest+1) { // while not destination node
        current->show();
        cout << "ici ?" << endl;
        vector<Node*>* adjacentNodes = AdjacentRemainingNodes(current);
        cout << "nb adjacents " << adjacentNodes->size() << endl;

        for (int i = 0; i < adjacentNodes->size(); i++){
            Node* adjacent = adjacentNodes->at(i);
            float distance = Distance(current, adjacent) + current->getDistFromStart();

            if (distance < adjacent->getDistFromStart()) {
                adjacent->setDistFromStart(distance);
                adjacent->setPrevious(current);
            }
        }
        current = ExtractMinimum();
        delete adjacentNodes;
    }
    PrintShortestRouteTo();
}


void Dijkstra1::PrintShortestRouteTo(){
    Node* previous = _graph.getNode(_dest);
    cout << "Distance from start: " << previous->getDistFromStart() << endl;
    while (previous) {
        cout << previous->getId() << " ";
        previous = previous->getPrevious();
    }
    cout << endl;
}

