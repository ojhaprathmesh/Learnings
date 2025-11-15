import java.util.Scanner;

public class PriorityScheduling {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Number of processes: ");
        int n = sc.nextInt();
        int[] burstTime = new int[n], priority = new int[n], waitingTime = new int[n], turnAroundTime = new int[n]
                , process = new int[n];

        for (int i = 0; i < n; i++) {
            process[i] = i + 1;
            System.out.print("Process " + process[i] + " Burst Time: ");
            burstTime[i] = sc.nextInt();
            System.out.print("Process " + process[i] + " Priority: ");
            priority[i] = sc.nextInt();
        }

        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                if (priority[i] > priority[j]) {
                    swap(burstTime, i, j);
                    swap(priority, i, j);
                    swap(process, i, j);
                }

        for (int i = 1; i < n; i++)
            waitingTime[i] = burstTime[i - 1] + waitingTime[i - 1];

        float avgWaitingTime = 0, avgTurnAroundTime = 0;
        for (int i = 0; i < n; i++) {
            turnAroundTime[i] = burstTime[i] + waitingTime[i];
            avgWaitingTime += waitingTime[i];
            avgTurnAroundTime += turnAroundTime[i];
        }

        System.out.println("Avg Waiting Time: " + (avgWaitingTime / n));
        System.out.println("Avg Turn-around Time: " + (avgTurnAroundTime / n));
    }

    static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
