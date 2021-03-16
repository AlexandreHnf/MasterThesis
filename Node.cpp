//
// Created by Alexandre on 12-11-20.
//

#include "Node.h"

#define G_INT_MAXI 10000000

// ============================ Node ==========================

// Node class constructor
Node::Node(int id, float lat, float lon) :
        _id(id), _lat(lat), _lon(lon), _previous(nullptr),
        _distanceFromStart(G_INT_MAXI), _marked(false) {}

// Setters
void Node::setDistFromStart(float d) {_distanceFromStart = d;}
void Node::mark(bool m) {_marked = m;}
void Node::addAdjacentNode(Node* v) {_adjacents.push_back(v);}
void Node::setPrevious(Node* p) {_previous = p;}

// Getters
Node* Node::getPrevious() const {return _previous;}
const int Node::getId() const {return _id;}
const float Node::getLatitude() const {return _lat;}
const float Node::getLongitude() const {return _lon;}
float Node::getDistFromStart() const {return _distanceFromStart;}
bool Node::getMark() const {return _marked;}
Node* Node::getAdjacentNode(int i) const {return _adjacents.at(i);}
int Node::getNbAdjacents() const {return _adjacents.size();}

void Node::show() const {
    cout << "node " << _id << ", " << endl;
}