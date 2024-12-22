import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

public class RRScheduling {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Number of processes: ");
        int n = sc.nextInt();
        System.out.print("Time quantum: ");
        int timeQuantum = sc.nextInt();

        int[] arrivalTime = new int[n], burstTime = new int[n], remainingTime = new int[n], waitingTime = new int[n], turnAroundTime = new int[n];
        boolean[] isCompleted = new boolean[n];
        for (int i = 0; i < n; i++) {
            arrivalTime[i] = sc.nextInt();
            burstTime[i] = sc.nextInt();
            remainingTime[i] = burstTime[i];
        }

        int currentTime = 0;
        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < n; i++) if (arrivalTime[i] <= currentTime) queue.add(i);

        while (!queue.isEmpty()) {
            int process = queue.poll(), executedTime = Math.min(timeQuantum, remainingTime[process]);
            remainingTime[process] -= executedTime;
            currentTime += executedTime;
            if (remainingTime[process] == 0) {
                isCompleted[process] = true;
                turnAroundTime[process] = currentTime - arrivalTime[process];
                waitingTime[process] = turnAroundTime[process] - burstTime[process];
            } else queue.add(process);

            for (int i = 0; i < n; i++)
                if (arrivalTime[i] <= currentTime && !isCompleted[i] && !queue.contains(i))
                    queue.add(i);
        }

        float avgWaitingTime = 0, avgTurnAroundTime = 0;
        for (int i = 0; i < n; i++) {
            avgWaitingTime += waitingTime[i];
            avgTurnAroundTime += turnAroundTime[i];
        }

        System.out.println("Avg Waiting Time: " + (avgWaitingTime / n));
        System.out.println("Avg Turn-around Time: " + (avgTurnAroundTime / n));
    }
}
