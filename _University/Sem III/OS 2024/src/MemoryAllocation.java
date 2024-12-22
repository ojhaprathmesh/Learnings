public class MemoryAllocation {
    public static void main(String[] args) {
        int[] memory = new int[128];
        for (int i = 20; i < 30; i++) memory[i] = 1; // Simulated occupied blocks
        for (int i = 50; i < 60; i++) memory[i] = 1;
        for (int i = 80; i < 90; i++) memory[i] = 1;

        int processSize = 15;
        System.out.println("First Fit: " + allocate(memory.clone(), processSize, "first"));
        System.out.println("Best Fit: " + allocate(memory.clone(), processSize, "best"));
        System.out.println("Next Fit: " + allocate(memory.clone(), processSize, "next"));
    }

    static String allocate(int[] memory, int size, String method) {
        int lastIndex = 0, bestIndex = -1, bestSize = Integer.MAX_VALUE;
        for (int i = 0; i <= memory.length - size; i++) {
            if (isFree(memory, i, size)) {
                if (method.equals("first")) {
                    allocateBlock(memory, i, size);
                    return "Start index: " + i;
                } else if (method.equals("best")) {
                    int blockSize = getFreeBlockSize(memory, i);
                    if (blockSize < bestSize) {
                        bestSize = blockSize;
                        bestIndex = i;
                    }
                } else if (method.equals("next") && i >= lastIndex) {
                    allocateBlock(memory, i, size);
                    return "Start index: " + i;
                }
            }
        }
        if (method.equals("best") && bestIndex != -1) {
            allocateBlock(memory, bestIndex, size);
            return "Start index: " + bestIndex;
        }
        return "No space available.";
    }

    static boolean isFree(int[] memory, int start, int size) {
        for (int i = start; i < start + size; i++) if (memory[i] == 1) return false;
        return true;
    }

    static void allocateBlock(int[] memory, int start, int size) {
        for (int i = start; i < start + size; i++) memory[i] = 1;
    }

    static int getFreeBlockSize(int[] memory, int start) {
        int count = 0;
        while (start < memory.length && memory[start++] == 0) count++;
        return count;
    }
}
