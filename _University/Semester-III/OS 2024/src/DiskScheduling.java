import java.util.*;

public class DiskScheduling {
    public static void main(String[] args) {
        int head = 50;
        int[] requests = {98, 183, 37, 122, 14, 124, 65, 67};
        int diskSize = 200;

        System.out.println("FIFO Total Movement: " + fifo(head, requests));
        System.out.println("SSTF Total Movement: " + sstf(head, requests));
        System.out.println("SCAN Total Movement: " + scan(head, requests, diskSize));
        System.out.println("LOOK Total Movement: " + look(head, requests));
    }

    static int fifo(int head, int[] requests) {
        int totalMovement = 0;
        for (int req : requests) {
            totalMovement += Math.abs(req - head);
            head = req;
        }
        return totalMovement;
    }

    static int sstf(int head, int[] requests) {
        int totalMovement = 0;
        List<Integer> queue = new ArrayList<>();
        for (int req : requests) queue.add(req);

        while (!queue.isEmpty()) {
            int finalHead = head;
            int closest = Collections.min(queue, Comparator.comparingInt(req -> Math.abs(req - finalHead)));
            totalMovement += Math.abs(closest - head);
            head = closest;
            queue.remove(Integer.valueOf(closest));
        }
        return totalMovement;
    }

    static int scan(int head, int[] requests, int diskSize) {
        List<Integer> queue = new ArrayList<>();
        for (int req : requests) queue.add(req);
        queue.add(0); // Add starting boundary
        queue.add(diskSize - 1); // Add ending boundary
        queue.add(head); // Include the head position in the queue
        Collections.sort(queue);

        int totalMovement = 0;
        int index = queue.indexOf(head);

        // Move to the right
        for (int i = index; i < queue.size(); i++) {
            totalMovement += Math.abs(queue.get(i) - head);
            head = queue.get(i);
        }

        // Move to the left
        for (int i = index - 1; i >= 0; i--) {
            totalMovement += Math.abs(queue.get(i) - head);
            head = queue.get(i);
        }

        return totalMovement;
    }

    static int look(int head, int[] requests) {
        List<Integer> queue = new ArrayList<>();
        for (int req : requests) queue.add(req);
        Collections.sort(queue);

        int totalMovement = 0, index = 0;
        for (int i = 0; i < queue.size(); i++) {
            if (queue.get(i) >= head) { index = i; break; }
        }

        for (int i = index; i < queue.size(); i++) {
            totalMovement += Math.abs(queue.get(i) - head);
            head = queue.get(i);
        }
        for (int i = index - 1; i >= 0; i--) {
            totalMovement += Math.abs(queue.get(i) - head);
            head = queue.get(i);
        }
        return totalMovement;
    }
}
