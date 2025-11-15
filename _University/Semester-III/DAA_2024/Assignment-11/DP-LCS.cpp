#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <algorithm>  // Include this for the reverse function

using namespace std;

void backtrackLCS(const vector<vector<int>> &dp, const string &str1, const string &str2, int i, int j, string currentLCS, set<string> &lcsSet) {
    if (i == 0 || j == 0) {
        reverse(currentLCS.begin(), currentLCS.end());  // Reverse the current LCS before adding
        lcsSet.insert(currentLCS);
        return;
    }
    if (str1[i - 1] == str2[j - 1]) {
        backtrackLCS(dp, str1, str2, i - 1, j - 1, currentLCS + str1[i - 1], lcsSet);
    } else {
        if (dp[i - 1][j] == dp[i][j]) backtrackLCS(dp, str1, str2, i - 1, j, currentLCS, lcsSet);
        if (dp[i][j - 1] == dp[i][j]) backtrackLCS(dp, str1, str2, i, j - 1, currentLCS, lcsSet);
    }
}

pair<int, vector<string>> findLCS(const string &str1, const string &str2) {
    int m = str1.size(), n = str2.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

    // Fill DP table
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            dp[i][j] = (str1[i - 1] == str2[j - 1]) ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);
        }
    }

    // Collect all LCS sequences
    set<string> lcsSet;
    backtrackLCS(dp, str1, str2, m, n, "", lcsSet);

    return {dp[m][n], vector<string>(lcsSet.begin(), lcsSet.end())};
}

int main() {
    string str1 = "AOJjhfiaunAOSIM", str2 = "asfdadiuhnASiniHsdiIOJsaubs";
    auto result = findLCS(str1, str2);

    cout << "Length of LCS: " << result.first << endl;
    cout << "All LCS sequences:\n";
    for (const auto &seq : result.second) {
        cout << seq << endl;
    }

    return 0;
}
