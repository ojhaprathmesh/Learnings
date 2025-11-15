import java.util.Scanner;

public class SJFScheduling {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Number of processes: ");
        int n = sc.nextInt();

        int[] arrivalTime = new int[n];
        int[] burstTime = new int[n];
        int[] waitingTime = new int[n];
        int[] turnAroundTime = new int[n];
        int[] process = new int[n];

        for (int i = 0; i < n; i++) {
            process[i] = i + 1;
            System.out.print("Process " + (i + 1) + " Arrival Time: ");
            arrivalTime[i] = sc.nextInt();
            System.out.print("Process " + (i + 1) + " Burst Time: ");
            burstTime[i] = sc.nextInt();
        }

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (burstTime[i] > burstTime[j]) {
                    int temp = burstTime[i];
                    burstTime[i] = burstTime[j];
                    burstTime[j] = temp;

                    temp = process[i];
                    process[i] = process[j];
                    process[j] = temp;
                }
            }
        }

        waitingTime[0] = 0;
        for (int i = 1; i < n; i++) {
            waitingTime[i] = burstTime[i - 1] + waitingTime[i - 1] - arrivalTime[i];
            if (waitingTime[i] < 0) {
                waitingTime[i] = 0;
            }
        }

        for (int i = 0; i < n; i++) {
            turnAroundTime[i] = waitingTime[i] + burstTime[i];
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
