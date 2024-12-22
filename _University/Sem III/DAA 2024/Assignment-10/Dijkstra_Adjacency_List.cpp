#include <iostream>
#include <vector>
#include <queue>
#include <limits>

using namespace std;

typedef pair<int, int> DistanceVertexPair;  // (distance, vertex)

// Dijkstra's algorithm
void dijkstra(int numVertices, const vector<vector<DistanceVertexPair>> &adjacencyList, int source) {
    vector<int> distances(numVertices, numeric_limits<int>::max());
    distances[source] = 0;

    priority_queue<DistanceVertexPair, vector<DistanceVertexPair>, greater<DistanceVertexPair>> minHeap;
    minHeap.push({0, source});

    while (!minHeap.empty()) {
        int currentVertex = minHeap.top().second;
        minHeap.pop();

        for (auto &neighbor : adjacencyList[currentVertex]) {
            int weight = neighbor.first, adjacentVertex = neighbor.second;
            if (distances[currentVertex] + weight < distances[adjacentVertex]) {
                distances[adjacentVertex] = distances[currentVertex] + weight;
                minHeap.push({distances[adjacentVertex], adjacentVertex});
            }
        }
    }

    cout << "\nVertex \t Distance from Source " << source << endl;
    for (int i = 0; i < numVertices; i++) {
        cout << i << " \t\t " << distances[i] << endl;
    }
}

// Main function
int main() {
    int numVertices = 5;
    vector<vector<DistanceVertexPair>> adjacencyList(numVertices);

    adjacencyList[0] = {{10, 1}, {5, 3}};
    adjacencyList[1] = {{1, 2}, {2, 3}};
    adjacencyList[2] = {{4, 4}};
    adjacencyList[3] = {{9, 2}, {2, 4}};
    adjacencyList[4] = {{4, 2}};

    // Run Dijkstra's algorithm starting from vertex 0
    dijkstra(numVertices, adjacencyList, 0);

    return 0;
}
