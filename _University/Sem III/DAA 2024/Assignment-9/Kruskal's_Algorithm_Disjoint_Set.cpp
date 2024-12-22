#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Edge {
    int src, dest, weight;
};

// Disjoint Set Data Structure
struct DisjointSet {
    vector<int> parent, rank;

    DisjointSet(int n) : parent(n), rank(n, 0) {
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int u) {
        if (u != parent[u]) parent[u] = find(parent[u]);  // Path compression
        return parent[u];
    }

    void unionSets(int u, int v) {
        int rootU = find(u), rootV = find(v);
        if (rootU != rootV) {
            if (rank[rootU] > rank[rootV]) parent[rootV] = rootU;
            else if (rank[rootU] < rank[rootV]) parent[rootU] = rootV;
            else {
                parent[rootV] = rootU;
                rank[rootU]++;
            }
        }
    }
};

// Kruskal's Algorithm to find MST
vector<Edge> kruskalMST(int V, vector<Edge> &edges) {
    sort(edges.begin(), edges.end(), [](Edge a, Edge b) { return a.weight < b.weight; });

    DisjointSet ds(V);
    vector<Edge> mst;

    for (const auto &edge : edges) {
        if (ds.find(edge.src) != ds.find(edge.dest)) {
            mst.push_back(edge);
            ds.unionSets(edge.src, edge.dest);
        }
        if (mst.size() == V - 1) break;  // Stop when MST has V-1 edges
    }

    return mst;
}

int main() {
    vector<Edge> edges = {
        {0, 1, 10}, {0, 2, 6}, {0, 3, 5}, {1, 3, 15}, {2, 3, 4}
    };

    vector<Edge> mst = kruskalMST(4, edges);

    cout << "Edges in the Minimum Spanning Tree:" << endl;
    for (const auto &edge : mst) {
        cout << edge.src << " -- " << edge.dest << " == " << edge.weight << endl;
    }

    return 0;
}
