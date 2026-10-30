# P5664 CSP-S 2019 D2T1 Emiya 家今天的饭

## 题意

$n \times m$ 矩阵，$a_{i,j}$ 表示用方法 $i$、食材 $j$ 的菜数。选 $k \ge 1$ 道菜，要求每行（方法）最多选一道，每列（食材）最多选 $\lfloor k/2 \rfloor$ 道。求方案数 mod 998244353。$n \le 100$，$m \le 2000$。

**标签**：计数 DP、容斥（补集转化）　**难度**：6/10

## 解题思路

### 1. 底层逻辑

直接满足"每列不超过一半"很难，转化成：**总方案 − 不合法方案**。

- 总方案（只满足"每行最多一道、至少一道"）：每行选 $s_i = \sum_j a_{i,j}$ 道中的一道或不选，$\prod (s_i + 1) - 1$。
- 不合法方案：存在某一列超过一半。

### 2. 隐藏条件

- **最多只有一列会超过一半**（两列都 $> k/2$，加起来就 $> k$）。所以不合法方案可以按"哪一列超标"不重不漏地分类，逐列计算再相加。
- 固定超标列 $c$ 后，只关心"选了 $c$ 列的菜数"与"选了其他列的菜数"之差，不需要分别记录两个数。

### 3. 注意事项

- 如果 DP 状态记录 $(c$ 列数量, 其他数量$)$，复杂度 $O(m n^3)$，只能拿 84 分；用**差值**作状态降到 $O(mn^2)$。
- 差值可能为负，下标整体加 $n$ 偏移。
- 取模减法要加回模数。

### 4. 解决方案

对每一列 $c$，设 $f_{i,d}$ 为考虑前 $i$ 行、"$c$ 列菜数 − 其他列菜数" $= d$ 的方案数：

$$f_{i,d} = f_{i-1,d} + f_{i-1,d-1}\cdot a_{i,c} + f_{i-1,d+1}\cdot (s_i - a_{i,c})$$

分别对应第 $i$ 行不选 / 选 $c$ 列 / 选其他列。$\sum_{d > 0} f_{n,d}$ 就是 $c$ 列超标的方案数。

答案 $= \prod(s_i + 1) - 1 - \sum_c \sum_{d>0} f_{n,d}$。复杂度 $O(mn^2) = 2000 \times 100 \times 200$。

## 部分分策略 / 错误思路

- $m \le 3$：可以直接记录每列选了几个，$O(n^{m+1})$。
- 状态记两维数量：$O(mn^3)$，84 分。
- 直接对"合法方案"DP：需要同时记录所有列的数量，不可行；补集转化是关键。

## AC 代码

```cpp
#include <bits/stdc++.h>
using namespace std;

#define endl '\n'
#define pb push_back
#define F first
#define S second
#define For(i, a, b) for (int i = (a); i <= (b); i++)
#define Rep(i, a, b) for (int i = (a); i < (b); i++)
#define mset(arr, x) memset(arr, x, sizeof(arr))
#define dbg(x) cout << #x << " = " << x << endl

#define int long long
typedef long long ll;
typedef unsigned long long ull;
typedef pair<int, int> pii;
typedef pair<ll, ll> pll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fLL;
const double EPS = 1e-9;
const int MOD = 1e9 + 7;

const int N = 105, M = 2005, P = 998244353;
int n, m;
int a[N][M], s[N], f[N][2 * N];

void solve() {
    cin >> n >> m;
    For(i, 1, n) For(j, 1, m) cin >> a[i][j], s[i] = (s[i] + a[i][j]) % P;
    int ans = 1;
    For(i, 1, n) ans = ans * (s[i] + 1) % P;
    ans = (ans - 1 + P) % P;
    For(c, 1, m) {
        mset(f, 0);
        f[0][n] = 1;
        For(i, 1, n) For(d, n - i, n + i) {
            f[i][d] = f[i - 1][d];
            if (d > 0) f[i][d] = (f[i][d] + f[i - 1][d - 1] * a[i][c]) % P;
            f[i][d] = (f[i][d] + f[i - 1][d + 1] * (s[i] - a[i][c] + P)) % P;
        }
        For(d, n + 1, 2 * n) ans = (ans - f[n][d] + P) % P;
    }
    cout << ans;
}

signed main() {
    ios::sync_with_stdio(false), cin.tie(nullptr);
    // freopen("xxx.in", "r", stdin);
    // freopen("xxx.out", "w", stdout);
    int tests = 1;
    // cin >> tests;
    while (tests--) solve();
    return 0;
}
```
