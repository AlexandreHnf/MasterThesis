// Dijkstra's Algorithm in C++

#include <iostream>
#include <vector>
#include "Utils.cpp"
#include "GraphDijkstra.h"
#include "Node.h"

using namespace std;

#define INT_MAXIM 10000000

class Node;

void Dijkstras();
vector<Node*>* AdjacentRemainingNodes(Node* node);
Node* ExtractMinimum(vector<Node*>& nodes);
int Distance(Node* node1, Node* node2);
void PrintShortestRouteTo(Node* destination);

vector<Node*> nodes;

class Node {
    public:
        Node(char id)
        : id(id), previous(NULL), distanceFromStart(INT_MAXIM) {
            nodes.push_back(this);
        }
    public:
        char id;
        float lat;
        float lon;
        Node* previous;
        int distanceFromStart;
        bool marked;
        std::vector<Node*> adjacents;
};

void DijkstrasTest();

///////////////////
void DijkstrasTest() {
  Node* a = new Node('a');
  Node* b = new Node('b');
  Node* c = new Node('c');
  Node* d = new Node('d');
  Node* e = new Node('e');
  Node* f = new Node('f');
  Node* g = new Node('g');

  a->distanceFromStart = 0;  // set start node
  Dijkstras();
  PrintShortestRouteTo(f);
}

///////////////////

void Dijkstras(GraphDijkstra G, int start, int dest) {
    while (nodes.size() > 0) {
        Node* mini = ExtractMinimum(nodes);
        vector<Node*>* adjacentNodes = AdjacentRemainingNodes(mini);

        for (int i = 0; i < adjacentNodes->size(); i++){
            Node* adjacent = adjacentNodes->at(i);
            int distance = Distance(mini, adjacent) + mini->distanceFromStart;

            if (distance < adjacent->distanceFromStart) {
                adjacent->distanceFromStart = distance;
                adjacent->previous = mini;
            }
        }
        delete adjacentNodes;
    }
}

// Find the node with the smallest distance,
// remove it, and return it. NO OPTIMAL PRIORITY QUEUE HERE
Node* ExtractMinimum(vector<Node*>& nodes) {
    int size = nodes.size();
    if (size == 0) return NULL;
    int smallestPosition = 0;
    Node* smallest = nodes.at(0);
    for (int i = 1; i < size; i++) {
        if (!nodes.at(i)->marked) { // if not marked (visited)
            Node *current = nodes.at(i);
            if (current->distanceFromStart < smallest->distanceFromStart) {
                smallest = current;
                smallestPosition = i;
            }
        }
    }
//    nodes.erase(nodes.begin() + smallestPosition);
    smallest->marked = true;
    return smallest;
}

// Return all nodes adjacent to 'node' which are still
// in the 'nodes' collection.
vector<Node*>* AdjacentRemainingNodes(Node* node) {
    vector<Node*>* remaining_adjacents = new vector<Node*>();
    for (int i = 0; i < node->adjacents.size(); i++) {
        if (!node->adjacents.at(i)->marked) {
            // maybe more efficient to delete the node from adjacents
            remaining_adjacents->push_back(node->adjacents.at(i));
        }
    }
    return remaining_adjacents;
}

// Return distance between two connected nodes
int Distance(Node* node1, Node* node2) {
    for (int i = 0; i < node1->adjacents.size(); i++) {
        if (node2->id == node1->adjacents.at(i)->id ) {
            return distanceEarth(node1->lat, node1->lon, node2->lat, node2->lon);
        }
    }
}

///////////////////

void PrintShortestRouteTo(Node* destination) {
  Node* previous = destination;
  cout << "Distance from start: "
     << destination->distanceFromStart << endl;
  while (previous) {
    cout << previous->id << " ";
    previous = previous->previous;
  }
  cout << endl;
}
