# 数位动态规划

**组别**：S　**关键词**：数位 DP、上界限制、前导零、记忆化搜索、区间计数、前缀差分

## 1. 是什么 / 解决什么问题

典型问题：

> 求 $[L, R]$ 中满足某种"数字特征"的整数个数，$R$ 可达 $10^{18}$。

例如：相邻数位之差至少为 2 的数有多少个？每个数字 0~9 一共出现多少次？数位和能整除自身的数有多少个？

$R$ 太大，不能一个个枚举。但这些特征都只和**每一位上的数字**有关。数位 DP 的思路是：像填表一样**从高位到低位一位一位地填数字**，把"已经填了的部分"中对后面有影响的信息作为状态。很多数前面若干位不同、后面的情况却完全一样，可以合并计算。

## 2. 核心原理

### 2.1 转化为前缀

设 $\text{calc}(x)$ = $[0, x]$ 中满足条件的数的个数，则

$$\text{ans}(L, R) = \text{calc}(R) - \text{calc}(L - 1)$$

这样只需要处理"不超过 $x$"这一个上界。

### 2.2 按位填数与上界限制

把 $x$ 拆成数位，从最高位往低位填。以 $x = 2357$ 为例：

```
位：      千 百 十 个
x：        2  3  5  7
```

- 千位可以填 $0 \sim 2$。
  - 填 0 或 1：已经比 $x$ 小了，后面三位可以**随便填** $0 \sim 9$。
  - 填 2：和 $x$ 一样，后面仍然受限制，百位只能填 $0 \sim 3$。
- 百位（千位填了 2）：填 $0 \sim 2$ 后面就自由了；填 3 继续受限……

用一个布尔量 `limit` 表示"前面每一位都和 $x$ 相同（贴着上界）"：

- `limit = true`：当前位最大只能填 $x$ 的这一位；
- `limit = false`：当前位可以填 $0 \sim 9$。

当前位填了上界数字且原来 `limit = true`，下一位仍然 `limit = true`；否则变成 `false`。

### 2.3 记忆化搜索模板

```
dfs(pos, state, limit, lead):
    if pos == 0: 根据 state 返回这个数是否合法（或贡献）
    if !limit && !lead && 记忆过: 返回 f[pos][state]
    up = limit ? d[pos] : 9
    res = 0
    for i in 0..up:
        res += dfs(pos - 1, 新 state, limit && i == up, lead && i == 0)
    if !limit && !lead: f[pos][state] = res
    return res
```

- `pos`：还剩几位没填。数位按 $d_1$ 为个位、$d_{len}$ 为最高位存放，从 `pos = len` 开始往下。
- `state`：题目需要的附加信息（上一位数字、数位和、余数……）。
- `lead`：是否还在前导零中（见下一节）。

**为什么只在 `!limit` 时记忆化？** $f_{pos,state}$ 的含义是"后面 $pos$ 位**自由填写**时的答案"，它和上界 $x$ 无关。`limit = true` 的状态在每一位上只有一个（就是一直贴着上界的那条路径），记不记都一样，而且它的答案依赖于 $x$ 的后几位，不能复用。

**一个好处**：因为 $f$ 与 $x$ 无关，计算 $\text{calc}(R)$ 和 $\text{calc}(L-1)$、甚至多组询问时，**不用清空** $f$。（前提是状态的含义不随询问变化。）

每个状态的计算量是 10（枚举一位数字），总复杂度 $O(\text{位数} \times \text{状态数} \times 10)$。

### 2.4 前导零

从最高位开始填，$x = 2357$ 时，数 $57$ 被表示成 $0057$。前面的 0 不是真正的数位。

**什么时候要管前导零？** 当前导零会影响判断时：

- "相邻两位之差至少为 2"：$0057$ 中 $0$ 和 $5$ 不算相邻；
- "数字 0 出现了几次"：$0057$ 中的 0 不能算；
- "数位和"、"是否含有数字 7"：前导零加了也不影响，不用管。

需要时加一个 `lead` 参数：`lead = true` 表示前面全是 0，此时填 0 仍然是前导零，不计入状态。

### 2.5 例 1：windy 数

不含前导零且相邻两个数字之差至少为 2 的正整数称为 windy 数，求 $[A, B]$ 中 windy 数的个数。

状态：`last` = 上一位填的数字。转移时若不在前导零中，要求 $|i - last| \ge 2$。

注意 $\text{calc}(x)$ 中，全部填 0 的"数"（即 0）也会被计入一次，但 $\text{calc}(B) - \text{calc}(A-1)$ 时两边都有，正好抵消。

### 2.6 例 2：数字计数

求 $[a, b]$ 中所有整数里，数字 $0 \sim 9$ 各出现了多少次。

对每个数字 $k$ 分别做一次。状态 `cnt` = 前面已经出现了几个 $k$，到 `pos = 0` 时返回 `cnt`。这时 `dfs` 返回的不再是"个数"，而是"所有数中 $k$ 的出现次数之和"——数位 DP 不仅能计数，也能对所有数**求和**某个量。

$k = 0$ 时前导零不能计入，所以需要 `lead`。

### 2.7 例 3：数位和之和

求 $L \sim R$ 中所有整数的数位和之和，对 $10^9+7$ 取模，多组询问。

状态 `sum` = 已填数位之和（最多 $9 \times 18 = 162$），到底时返回 `sum`。前导零不影响数位和，不需要 `lead`。多组询问共用记忆化数组。

### 2.8 常见的状态

| 条件 | 状态 |
| --- | --- |
| 相邻数位关系 | 上一位数字 |
| 数字出现次数 | 已出现次数 |
| 数位和满足某条件 | 当前数位和 |
| 能被 $m$ 整除 | 当前前缀对 $m$ 的余数（新余数 $= (r \cdot 10 + i) \bmod m$） |
| 不含某个子串（如 "62"） | 上一位（或匹配到子串的第几位） |
| 二进制下 1 的个数 | 改成二进制拆位，状态为已有的 1 的个数 |

**条件依赖最终结果时**（例如"数位和能整除这个数本身"），数位和要到最后才知道，而取余又需要知道模数。做法是**枚举最终的数位和 $s$**，对每个 $s$ 做一次数位 DP，状态为（当前数位和，当前余数 mod $s$），最后要求数位和恰为 $s$ 且余数为 0。

## 3. 代码模板

### 3.1 windy 数

```cpp
const int N = 20;
int a, b, len;
int d[N], f[N][10];

int dfs(int pos, int last, bool limit, bool lead) {
    if (pos == 0) return 1;
    if (!limit && !lead && f[pos][last] != -1) return f[pos][last];
    int up = limit ? d[pos] : 9, res = 0;
    For(i, 0, up) {
        if (!lead && abs(i - last) < 2) continue;
        res += dfs(pos - 1, i, limit && i == up, lead && i == 0);
    }
    if (!limit && !lead) f[pos][last] = res;
    return res;
}

int calc(int x) {
    len = 0;
    while (x) d[++len] = x % 10, x /= 10;
    return dfs(len, 0, true, true);
}

void solve() {
    cin >> a >> b;
    mset(f, -1);
    cout << calc(b) - calc(a - 1);
}
```

用 $-1$ 表示"没算过"，因为答案可能是 0。$x = 0$ 时 `len = 0`，直接返回 1（只有数 0）。

### 3.2 数字计数

```cpp
const int N = 20;
int a, b, len, k;
int d[N], f[N][N];

int dfs(int pos, int cnt, bool limit, bool lead) {
    if (pos == 0) return cnt;
    if (!limit && !lead && f[pos][cnt] != -1) return f[pos][cnt];
    int up = limit ? d[pos] : 9, res = 0;
    For(i, 0, up) {
        int c = cnt + (i == k && !(lead && i == 0));
        res += dfs(pos - 1, c, limit && i == up, lead && i == 0);
    }
    if (!limit && !lead) f[pos][cnt] = res;
    return res;
}

int calc(int x) {
    len = 0;
    while (x) d[++len] = x % 10, x /= 10;
    return dfs(len, 0, true, true);
}

void solve() {
    cin >> a >> b;
    for (k = 0; k <= 9; k++) {
        mset(f, -1);
        cout << calc(b) - calc(a - 1) << " ";
    }
}
```

不同的 $k$ 对应不同的 $f$ 含义，所以每换一个 $k$ 都要清空。

### 3.3 数位和之和（多组询问）

```cpp
const int N = 20;
int T, l, r, len;
int d[N], f[N][N * 9];

int dfs(int pos, int sum, bool limit) {
    if (pos == 0) return sum;
    if (!limit && f[pos][sum] != -1) return f[pos][sum];
    int up = limit ? d[pos] : 9, res = 0;
    For(i, 0, up) res = (res + dfs(pos - 1, sum + i, limit && i == up)) % MOD;
    if (!limit) f[pos][sum] = res;
    return res;
}

int calc(int x) {
    len = 0;
    while (x) d[++len] = x % 10, x /= 10;
    return dfs(len, 0, true);
}

void solve() {
    mset(f, -1);
    cin >> T;
    while (T--) {
        cin >> l >> r;
        cout << (calc(r) - calc(l - 1) + MOD) % MOD << endl;
    }
}
```

$f$ 只在开头清空一次，所有询问共用。

## 4. 复杂度

$$O(\text{位数} \times \text{状态数} \times 10)$$

- windy 数：$19 \times 10 \times 10$，极快。
- 数字计数：每个数字 $19 \times 19 \times 10$，共 10 个数字。
- 数位和：$19 \times 163 \times 10$，每组询问只有贴上界的那条路径需要重新计算，约 $19 \times 10$ 次调用。
- 枚举最终数位和的题：再乘上枚举量（如 $162$）和余数状态数，要估算清楚。

## 5. 常见题型与技巧

- **识别**：区间 $[L, R]$ 很大（$10^9 \sim 10^{18}$），条件只与数位有关，求个数或求和。
- **先写前缀** $\text{calc}(x)$，答案做差；注意 $L = 0$ 时 $L - 1 = -1$ 要单独处理。
- **其他进制**：二进制、$k$ 进制只要把拆位和 `up` 的 9 换成 $k-1$。
- **求和型**：`dfs` 返回"所有合法数的某个量之和"，在 `pos = 0` 时返回该量；如果要对"数本身"求和，可以同时返回（个数，和）一对值，转移时 $\text{和} = \sum (\text{子和} + i \cdot 10^{pos-1} \cdot \text{子个数})$。
- **求第 $k$ 小的合法数**：先用数位 DP 算出"后面自由填时的合法个数"，再从高位开始逐位确定，每一位从小到大试，个数不够 $k$ 就减掉继续试下一个数字。
- **递推写法**：也可以先预处理 $g_{pos,state}$ 表示"$pos$ 位自由填的方案数"，再沿着上界逐位累加。思路一样，记忆化搜索更不容易写错。

## 6. 易错点

- 忘记 `limit` 下的状态不能记忆化（或者把 `limit` 也放进了记忆化而又在不同上界之间复用）。
- 前导零处理错误：该管的时候没管（windy 数、数字 0 的计数），或者不该管的时候管了导致状态变多。
- 用 0 表示"没算过"，答案恰好为 0 的状态被反复计算。
- 记忆化数组的含义依赖于某个外部参数（如数字计数中的 $k$、枚举的数位和 $s$），换参数时没有清空。
- $\text{calc}(L-1)$ 在 $L = 0$ 时出错；取模减法没加 `MOD`。
- 数位存放顺序与 `pos` 的含义不一致（本文 $d_1$ 是个位，`pos` 从高位 `len` 递减到 0）。

## 7. 练习

**洛谷经典题**

- [P2657 [SCOI2009] windy 数](https://www.luogu.com.cn/problem/P2657)：上一位数字作为状态，需要处理前导零。
- [P2602 [ZJOI2010] 数字计数](https://www.luogu.com.cn/problem/P2602)：统计每个数字的出现次数。
- [P4999 烦人的数学作业](https://www.luogu.com.cn/problem/P4999)：数位和之和，多组询问共用记忆化。
- [P6218 [USACO06NOV] Round Numbers S](https://www.luogu.com.cn/problem/P6218)：二进制下的数位 DP。
- [P4127 [AHOI2009] 同类分布](https://www.luogu.com.cn/problem/P4127)：枚举最终数位和，状态记录余数。
