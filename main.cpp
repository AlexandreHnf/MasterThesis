#include <iostream>
#include <fstream>
#include <iterator>
#include <sstream>
#include "Fibonacci_heap.cpp"
#include "GraphDijkstra.h"
#include "Dijkstra1.h"


vector<string> splitStr(string s) {
    /*
     * Splits a string into a list of string
     */
    istringstream iss(s);
    vector<string> results((istream_iterator<string>(iss)),istream_iterator<string>());
    return results;
}

void test_fibonacci_heap() {
    int n, m, l;
    FibonacciHeap fh;
    node *p;
    node *H;
    H = fh.InitializeHeap();

    p = fh.Create_node(7, 1);
    H = fh.Insert(H, p);
    p = fh.Create_node(3, 2);
    H = fh.Insert(H, p);
    p = fh.Create_node(17, 3);
    H = fh.Insert(H, p);
    p = fh.Create_node(24, 4);
    H = fh.Insert(H, p);

    int i = fh.Display(H);
    std::cout << i << std::endl;

    p = fh.Extract_Min(H);
    if (p != NULL)
        cout << "The node with minimum key: " << p->n << endl;
    else
        cout << "Heap is empty" << endl;

//    i = fh.Display(H);

    node* found = fh.Find(H, 24, 4);
    std::cout << "id of found node " << found->id << ", node : " << found->n<< std::endl;

//    found = fh.Find(H, 24, 4);
//    std::cout << "id of found node " << found->id << ", node : " << found->n<< std::endl;

    m = 24;
    l = 23;
//    fh.Decrease_key(H, m, l, 4);
//
//    m = 17;
//    fh.Delete_key(H, m, 3);

    //i = fh.Display(H);
}

GraphDijkstra parse(const string filename) {
    FibonacciHeap fh;
    node *p; // for new nodes
    node *H; // pointer to heap
    H = fh.InitializeHeap();

    GraphDijkstra G;

    string line;
    ifstream myfile (filename);
    if (myfile.is_open()) {
        while ( getline (myfile,line) ) {

            std::vector<std::string> l = splitStr(line); // split => list = Node or Edge
            // put in fibonacci heap
            // p = fh.Create_node(INT_MAXI, std::stoi(elements[1])); // INT_MAXI = distSoFar, elements[1] -> int
            // H = fh.Insert(H, p);

            // put in graph
            if (l[0] == "v") { // node
                G.createNode(std::stoi(l[1]), std::stoi(l[2]), std::stoi(l[3]));
            }
            else if (l[0] == "e") { // edge [(0) e, (1) id, (2) src, (3) tgt]
                G.getNode(std::stoi(l[2])-1)->addAdjacentNode(G.getNode(std::stoi(l[3])-1));
            }
            cout << line << '\n';
        }
        myfile.close();
        //fh.Display(H);
        G.show();
    }
    else cout << "Unable to open file";
    return G;
}

int main() {
    std::cout << "Hello, World!" << std::endl;
    // test_fibonacci_heap();

    GraphDijkstra G = parse("D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\testgraph.txt");
    Dijkstra1 D = Dijkstra1(0, 4, G);
    D.runDijkstra();

    return 0;
}
