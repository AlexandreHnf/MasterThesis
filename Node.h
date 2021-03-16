//
// Created by Alexandre on 12-11-20.
//

#ifndef CODES_NODE_H
#define CODES_NODE_H

#include <iostream>
#include <vector>
using namespace std;

class Node {
    private:
        const int _id;
        const float _lat;
        const float _lon;
        Node* _previous;
        float _distanceFromStart;
        bool _marked;
        std::vector<Node*> _adjacents;

    public:
        // constructor
        Node(int, float, float);

        // Methods Getter
        Node* getPrevious() const;
        const int getId() const;
        const float getLatitude() const;
        const float getLongitude() const;
        float getDistFromStart() const;
        bool getMark() const;
        Node* getAdjacentNode(int) const;
        int getNbAdjacents() const;

        // Methods Setter
        void setDistFromStart(float) ;
        void mark(bool) ;
        void addAdjacentNode(Node*) ;
        void setPrevious(Node*);

        void show() const;
};


#endif //CODES_NODE_H
