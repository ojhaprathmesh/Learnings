public class BankersAlgorithm {
    public static void main(String[] args) {
        // Hardcoded values for the number of processes and resources
        int n = 5; // Number of processes
        int m = 3; // Number of resources

        // Hardcoded Max matrix
        int[][] Max = {
                {7, 5, 3},  // P0
                {3, 2, 2},  // P1
                {9, 0, 2},  // P2
                {2, 2, 2},  // P3
                {4, 3, 3}   // P4
        };

        // Hardcoded Allocation matrix
        int[][] Allocation = {
                {0, 1, 0},  // P0
                {2, 0, 0},  // P1
                {3, 0, 2},  // P2
                {2, 1, 1},  // P3
                {0, 0, 2}   // P4
        };

        // Hardcoded Available array
        int[] Available = {3, 3, 2};

        // Hardcoded sequence to check
        int[] sequence = {4, 2, 1, 3, 0};

        // Need matrix calculation
        int[][] Need = new int[n][m];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                Need[i][j] = Max[i][j] - Allocation[i][j];
            }
        }

        // Check if the sequence is safe
        System.out.println(isSafeSequence(n, m, Need, Allocation, Available, sequence)
                ? "The sequence <P4, P2, P1, P3, P0> is a safe state."
                : "The sequence <P4, P2, P1, P3, P0> is NOT a safe state.");
    }

    public static boolean isSafeSequence(int n, int m, int[][] Need, int[][] Allocation, int[] Available, int[] sequence) {
        int[] Work = Available.clone();
        boolean[] Finish = new boolean[n];

        for (int process : sequence) {
            boolean canAllocate = true;
            for (int j = 0; j < m; j++) if (Need[process][j] > Work[j]) { canAllocate = false; break; }
            if (!canAllocate) return false;

            for (int j = 0; j < m; j++) Work[j] += Allocation[process][j];
            Finish[process] = true;
        }

        for (boolean f : Finish) if (!f) return false;
        return true;
    }
}
