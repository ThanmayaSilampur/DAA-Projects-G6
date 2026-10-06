import java.util.*;

class Job {
    char id;
    int deadline;
    int profit;

    Job(char id, int deadline, int profit) {
        this.id = id;
        this.deadline = deadline;
        this.profit = profit;
    }
}

public class Project4_JobSequencing {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of jobs: ");
        int n = sc.nextInt();

        Job[] jobs = new Job[n];

        int maxDeadline = 0;

        // Input jobs
        for (int i = 0; i < n; i++) {

            System.out.println("\nEnter details for Job " + (i + 1));

            System.out.print("Job ID: ");
            char id = sc.next().charAt(0);

            System.out.print("Deadline: ");
            int deadline = sc.nextInt();

            System.out.print("Profit: ");
            int profit = sc.nextInt();

            jobs[i] = new Job(id, deadline, profit);

            if (deadline > maxDeadline) {
                maxDeadline = deadline;
            }
        }

        // Sort jobs by decreasing profit
        Arrays.sort(jobs, (a, b) -> b.profit - a.profit);

        // Create time slots
        Job[] slots = new Job[maxDeadline + 1];

        int totalProfit = 0;

        // Schedule jobs
        for (Job job : jobs) {

            for (int j = job.deadline; j >= 1; j--) {

                if (slots[j] == null) {

                    slots[j] = job;
                    totalProfit += job.profit;

                    break;
                }
            }
        }

        // Display result
        System.out.println("\nJob Sequence:");

        for (int i = 1; i <= maxDeadline; i++) {

            if (slots[i] != null) {
                System.out.println(
                    "Slot " + i + " -> Job " + slots[i].id
                );
            }
        }

        System.out.println("\nMaximum Profit = " + totalProfit);

        sc.close();
    }
}