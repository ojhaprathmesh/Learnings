#include <iostream>
#include <stdexcept>
using namespace std;

struct MaxHeap {
    int *heap;
    int capacity;
    int size;

    MaxHeap(int cap) : capacity(cap), size(0) {
        heap = new int[capacity];
    }

    ~MaxHeap() {
        delete[] heap;
    }

    void insert(int key) {
        if (size == capacity) throw runtime_error("Heap is full");
        heap[size++] = key;
        shiftUp(size - 1);
    }

    int extractMax() {
        if (size == 0) throw runtime_error("Heap is empty");
        int max = heap[0];
        heap[0] = heap[--size];
        shiftDown(0);
        return max;
    }

    int getMax() const {
        if (size == 0) throw runtime_error("Heap is empty");
        return heap[0];
    }

    bool isEmpty() const {
        return size == 0;
    }

    void display() const {
        for (int i = 0; i < size; i++) {
            cout << heap[i] << " ";
        }
        cout << endl;
    }

private:
    void shiftUp(int index) {
        while (index > 0 && heap[index] > heap[(index - 1) / 2]) {
            swap(heap[index], heap[(index - 1) / 2]);
            index = (index - 1) / 2;
        }
    }

    void shiftDown(int index) {
        while (index < size) {
            int largest = index;
            int left = 2 * index + 1, right = 2 * index + 2;
            if (left < size && heap[left] > heap[largest]) largest = left;
            if (right < size && heap[right] > heap[largest]) largest = right;
            if (largest == index) break;
            swap(heap[index], heap[largest]);
            index = largest;
        }
    }
};

// Heap sort using Max Heap
void heapSort(int arr[], int n) {
    MaxHeap heap(n);
    for (int i = 0; i < n; i++) heap.insert(arr[i]);
    for (int i = n - 1; i >= 0; i--) arr[i] = heap.extractMax();
}

// Priority Queue using Max Heap
struct PriorityQueue {
    MaxHeap maxHeap;

    PriorityQueue(int capacity) : maxHeap(capacity) {}

    void enqueue(int priority) { maxHeap.insert(priority); }
    int dequeue() { return maxHeap.extractMax(); }
    int peek() const { return maxHeap.getMax(); }
    bool isEmpty() const { return maxHeap.isEmpty(); }
};

int main() {
    // MaxHeap usage
    MaxHeap maxheap(8);
    maxheap.insert(11);
    maxheap.insert(14);
    maxheap.insert(16);
    maxheap.insert(21);
    maxheap.insert(19);
    maxheap.insert(23);
    maxheap.insert(54);
    maxheap.insert(78);

    maxheap.display();

    int arr[] = {32, 21, 5, 23, 6};
    int n = sizeof(arr) / sizeof(arr[0]);

    heapSort(arr, n);
    cout << "Sorted array: ";
    for (int i = 0; i < n; i++) cout << arr[i] << " ";
    cout << endl;

    // Priority Queue usage
    PriorityQueue pq(10);
    pq.enqueue(10);
    pq.enqueue(20);
    pq.enqueue(5);
    pq.enqueue(30);

    cout << "Max priority element: " << pq.peek() << endl;
    cout << "Dequeue max priority element: " << pq.dequeue() << endl;
    cout << "New max priority element: " << pq.peek() << endl;

    return 0;
}
