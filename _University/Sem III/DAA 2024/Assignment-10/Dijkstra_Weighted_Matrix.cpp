#include <iostream>
#include <vector>
#include <limits>

using namespace std;

// Function to select the vertex with the minimum distance that is not yet included in the SPT
int selectMinVertex(const vector<int>& distances, const vector<bool>& includedInSPT, int numVertices) {
    int minDistance = numeric_limits<int>::max(), minIndex;
    for (int i = 0; i < numVertices; i++) {
        if (!includedInSPT[i] && distances[i] < minDistance) {
            minDistance = distances[i];
            minIndex = i;
        }
    }
    return minIndex;
}

// Dijkstra's algorithm
void dijkstra(int numVertices, const vector<vector<int>>& graph, int source) {
    vector<int> distances(numVertices, numeric_limits<int>::max());
    vector<bool> includedInSPT(numVertices, false);
    distances[source] = 0;

    for (int i = 0; i < numVertices - 1; i++) {
        int u = selectMinVertex(distances, includedInSPT, numVertices);
        includedInSPT[u] = true;

        for (int v = 0; v < numVertices; v++) {
            if (graph[u][v] && !includedInSPT[v] && distances[u] != numeric_limits<int>::max() 
                && distances[u] + graph[u][v] < distances[v]) {
                distances[v] = distances[u] + graph[u][v];
            }
        }
    }

    // Output the shortest distances from source
    cout << "Vertex \t Distance from Source " << source << endl;
    for (int i = 0; i < numVertices; i++) {
        cout << i << " \t\t " << distances[i] << endl;
    }
}

int main() {
    int numVertices = 5;
    vector<vector<int>> graph = {
        {0, 10, 0, 5, 0},
        {10, 0, 1, 2, 0},
        {0, 1, 0, 9, 4},
        {5, 2, 9, 0, 2},
        {0, 0, 4, 2, 0}
    };

    dijkstra(numVertices, graph, 0);  // Run Dijkstra's algorithm starting from vertex 0

    return 0;
}
