def toArray():
    return list(map(int, input().split()))

m, n = toArray()
array = [toArray() for _ in range(m)]
target = int(input())

print(1 if any(target in row for row in array) else 0)

"""
Didn't work in python for all cases

Java Code:
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        // Read matrix dimensions
        int m = sc.nextInt();
        int n = sc.nextInt();
        
        // Read the matrix
        int[][] array = new int[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                array[i][j] = sc.nextInt();
            }
        }
        
        // Read target number
        int target = sc.nextInt();
        
        // Check if target exists in the matrix
        boolean found = false;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (array[i][j] == target) {
                    found = true;
                    break;
                }
            }
            if (found) break;
        }

        // Print result
        System.out.println(found ? 1 : 0);
        
        sc.close();
    }
}

"""