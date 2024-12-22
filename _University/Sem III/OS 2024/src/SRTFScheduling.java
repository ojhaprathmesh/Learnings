import java.util.Scanner;

public class SRTFScheduling {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Number of processes: ");
        int n = sc.nextInt();

        int[] arrivalTime = new int[n];
        int[] burstTime = new int[n];
        int[] remainingTime = new int[n];
        int[] waitingTime = new int[n];
        int[] turnAroundTime = new int[n];

        for (int i = 0; i < n; i++) {
            System.out.print("Process " + (i + 1) + " Arrival Time: ");
            arrivalTime[i] = sc.nextInt();
            System.out.print("Process " + (i + 1) + " Burst Time: ");
            burstTime[i] = sc.nextInt();
            remainingTime[i] = burstTime[i];
        }

        int currentTime = 0, completedProcesses = 0;
        int minRemainingTime = Integer.MAX_VALUE;
        int shortest = 0, finishTime;
        boolean check = false;

        while (completedProcesses != n) {
            for (int i = 0; i < n; i++) {
                if ((arrivalTime[i] <= currentTime) && (remainingTime[i] < minRemainingTime) && remainingTime[i] > 0) {
                    minRemainingTime = remainingTime[i];
                    shortest = i;
                    check = true;
                }
            }

            if (!check) {
                currentTime++;
                continue;
            }

            remainingTime[shortest]--;
            minRemainingTime = remainingTime[shortest];
            if (minRemainingTime == 0) {
                minRemainingTime = Integer.MAX_VALUE;
            }

            if (remainingTime[shortest] == 0) {
                completedProcesses++;
                finishTime = currentTime + 1;
                waitingTime[shortest] = finishTime - burstTime[shortest] - arrivalTime[shortest];

                if (waitingTime[shortest] < 0) {
                    waitingTime[shortest] = 0;
                }
            }
            currentTime++;
        }

        for (int i = 0; i < n; i++) {
            turnAroundTime[i] = burstTime[i] + waitingTime[i];
        }

        float avgWaitingTime = 0, avgTurnAroundTime = 0;
        for (int i = 0; i < n; i++) {
            avgWaitingTime += (float) waitingTime[i] / n;
            avgTurnAroundTime += (float) turnAroundTime[i] / n;
        }

        System.out.println("Avg Waiting Time: " + avgWaitingTime);
        System.out.println("Avg Turn-around Time: " + avgTurnAroundTime);
    }
}
