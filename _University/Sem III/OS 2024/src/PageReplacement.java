import java.util.*;

public class PageReplacement {
    public static void main(String[] args) {
        int[] refStr = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1};
        int frames = 3;
        System.out.println("FIFO: " + fifo(refStr, frames));
        System.out.println("Optimal: " + optimal(refStr, frames));
        System.out.println("LRU: " + lru(refStr, frames));
    }

    static int fifo(int[] refStr, int frames) {
        Set<Integer> pageFrames = new HashSet<>();
        Queue<Integer> queue = new LinkedList<>();
        int pageFaults = 0;
        for (int page : refStr) {
            if (!pageFrames.contains(page)) {
                pageFaults++;
                if (pageFrames.size() == frames) pageFrames.remove(queue.poll());
                pageFrames.add(page);
                queue.offer(page);
            }
        }
        return pageFaults;
    }

    static int optimal(int[] refStr, int frames) {
        List<Integer> pageFrames = new ArrayList<>();
        int pageFaults = 0;
        for (int i = 0; i < refStr.length; i++) {
            int page = refStr[i];
            if (!pageFrames.contains(page)) {
                pageFaults++;
                if (pageFrames.size() == frames) {
                    int farthestIndex = -1, farthest = -1;
                    for (int j = 0; j < pageFrames.size(); j++) {
                        int nextUse = Integer.MAX_VALUE;
                        for (int k = i + 1; k < refStr.length; k++) {
                            if (refStr[k] == pageFrames.get(j)) {
                                nextUse = k;
                                break;
                            }
                        }
                        if (nextUse > farthest) { farthest = nextUse; farthestIndex = j; }
                    }
                    pageFrames.remove(farthestIndex);
                }
                pageFrames.add(page);
            }
        }
        return pageFaults;
    }

    static int lru(int[] refStr, int frames) {
        LinkedHashMap<Integer, Integer> pageFrames = new LinkedHashMap<>(frames, 0.75f, true);
        int pageFaults = 0;
        for (int page : refStr) {
            if (!pageFrames.containsKey(page)) {
                pageFaults++;
                if (pageFrames.size() == frames) pageFrames.remove(pageFrames.keySet().iterator().next());
            }
            pageFrames.put(page, 1);
        }
        return pageFaults;
    }
}
