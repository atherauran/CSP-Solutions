# 树状数组

**组别**：S　**关键词**：树状数组、lowbit、单点修改区间查询、区间修改、逆序对、离散化、离线扫描线、倍增求第 k 小

## 1. 是什么 / 解决什么问题

前缀和能 $O(1)$ 求区间和，但只要修改一个元素，后面所有前缀和都要改，$O(n)$。直接存原数组则修改 $O(1)$、求和 $O(n)$。

**树状数组**（Binary Indexed Tree / Fenwick Tree）在两者之间取平衡：**单点修改**和**前缀和查询**都是 $O(\log n)$。代码只有几行，常数很小，是 CSP-S 最常用的数据结构之一。

凡是"修改一个点 + 求前缀的某种可减信息"的问题都可以用它；配合差分、离散化、离线排序，还能解决区间修改、逆序对、二维数点等问题。

## 2. 核心原理

### 2.1 lowbit

$\operatorname{lowbit}(x)$ 是 $x$ 二进制中最低位的 1 所代表的值：

| $x$ | 二进制 | lowbit |
| --- | --- | --- |
| 6 | 110 | 2 |
| 8 | 1000 | 8 |
| 12 | 1100 | 4 |
| 7 | 111 | 1 |

计算方法 `x & -x`：补码中 $-x$ 等于 $x$ 取反加 1，取反后最低的 1 变成 0、它下面的 0 全变成 1，加 1 后又进位回到这个位置，于是 $x$ 和 $-x$ 只有这一位同时为 1。

### 2.2 每个 c[i] 管一段

树状数组 $c_i$ 存的是区间 $(i - \operatorname{lowbit}(i),\ i]$ 的和，即**以 $i$ 结尾、长度为 $\operatorname{lowbit}(i)$** 的一段。$n = 8$ 时：

```text
i    :  1   2   3   4   5   6   7   8
c[1] :  #
c[2] :  #####
c[3] :          #
c[4] :  #############
c[5] :                  #
c[6] :                  #####
c[7] :                          #
c[8] :  #############################
```

**查询前缀和** $sum(x)$：$c_x$ 管 $(x - \operatorname{lowbit}(x), x]$，剩下的前缀是 $[1, x - \operatorname{lowbit}(x)]$，继续查。每次去掉 $x$ 的最低位 1，最多 $\log n$ 次。

$$sum(7) = c_7 + c_6 + c_4 \qquad (7 = 111_2 \to 110_2 \to 100_2 \to 0)$$

本质是把 $[1, x]$ 按 $x$ 的二进制拆成若干段：$7 = 4 + 2 + 1$，对应 $[1,4]$、$[5,6]$、$[7,7]$。

**单点修改** $a_x \mathrel{+}= v$：要更新所有包含位置 $x$ 的 $c_i$。它们恰好是 $x,\ x + \operatorname{lowbit}(x),\ \dots$，每次加上最低位 1（向上进位），最多 $\log n$ 次。

$$\text{修改 } a_3:\ c_3 \to c_4 \to c_8 \qquad (3 = 011_2 \to 100_2 \to 1000_2)$$

从图上也能看出来：包含位置 3 的只有 $c_3, c_4, c_8$。

### 2.3 能维护什么

查询拆成若干段再合并，所以信息要能**合并**；求区间 $[l, r]$ 时用 $sum(r) - sum(l-1)$，所以还要能**相减**。和、异或、计数都可以。

最大值不能相减，只能查**前缀**最大值，而且修改只能让值变大（变小时旧的最大值撤不掉）。一般的区间最值用 ST 表或线段树。

## 3. 代码模板

### 3.1 单点修改，区间查询

```cpp
const int N = 5e5 + 5;
int n, m;
int c[N];

inline int lowbit(int x) { return x & -x; }

void add(int x, int v) {
    for (; x <= n; x += lowbit(x)) c[x] += v;
}

int ask(int x) {
    int s = 0;
    for (; x; x -= lowbit(x)) s += c[x];
    return s;
}

void solve() {
    cin >> n >> m;
    For(i, 1, n) {
        int x;
        cin >> x;
        add(i, x);
    }
    while (m--) {
        int op, x, y;
        cin >> op >> x >> y;
        if (op == 1) add(x, y);
        else cout << ask(y) - ask(x - 1) << endl;
    }
}
```

初始化时逐个 `add` 是 $O(n \log n)$。也可以 $O(n)$ 建树：先 `c[i] += a[i]`，再把 `c[i]` 加到它的"父亲" `c[i + lowbit(i)]` 上（$i$ 从小到大）。

### 3.2 区间修改，单点查询

维护差分数组 $d_i = a_i - a_{i-1}$。区间 $[l, r]$ 加 $k$ 只改两个点：$d_l \mathrel{+}= k$，$d_{r+1} \mathrel{-}= k$；而 $a_x = \sum_{i \le x} d_i$ 是前缀和。

```cpp
const int N = 5e5 + 5;
int n, m;
int a[N], c[N];

inline int lowbit(int x) { return x & -x; }

void add(int x, int v) {
    for (; x <= n; x += lowbit(x)) c[x] += v;
}

int ask(int x) {
    int s = 0;
    for (; x; x -= lowbit(x)) s += c[x];
    return s;
}

void solve() {
    cin >> n >> m;
    For(i, 1, n) cin >> a[i], add(i, a[i] - a[i - 1]);
    while (m--) {
        int op, x, y, k;
        cin >> op >> x;
        if (op == 1) cin >> y >> k, add(x, k), add(y + 1, -k);
        else cout << ask(x) << endl;
    }
}
```

### 3.3 区间修改，区间查询

还是维护差分 $d$，推一下前缀和：

$$\sum_{i=1}^{p} a_i = \sum_{i=1}^{p}\sum_{j=1}^{i} d_j = \sum_{j=1}^{p} d_j \cdot (p - j + 1) = (p+1)\sum_{j=1}^{p} d_j - \sum_{j=1}^{p} j \cdot d_j$$

（第二步：$d_j$ 在 $i = j, j+1, \dots, p$ 时都被加到，共 $p - j + 1$ 次。）

所以开两个树状数组，分别维护 $d_j$ 和 $j \cdot d_j$。

```cpp
const int N = 1e5 + 5;
int n, m;
int c1[N], c2[N];

inline int lowbit(int x) { return x & -x; }

void add(int x, int v) {
    for (int i = x; i <= n; i += lowbit(i)) c1[i] += v, c2[i] += v * x;
}

int ask(int x) {
    int s = 0;
    for (int i = x; i; i -= lowbit(i)) s += (x + 1) * c1[i] - c2[i];
    return s;
}

void solve() {
    cin >> n >> m;
    For(i, 1, n) {
        int x;
        cin >> x;
        add(i, x), add(i + 1, -x);
    }
    while (m--) {
        int op, x, y, k;
        cin >> op >> x >> y;
        if (op == 1) cin >> k, add(x, k), add(y + 1, -k);
        else cout << ask(y) - ask(x - 1) << endl;
    }
}
```

这能做线段树 1 那道模板题，而且代码更短、更快。但如果还要区间乘、区间最值，就只能用线段树了。

## 4. 经典应用

### 4.1 逆序对

逆序对是 $i < j$ 且 $a_i > a_j$ 的对数。从左往右扫，把出现过的**值**当作下标放进树状数组（值 $v$ 出现一次就 `add(v, 1)`）。处理 $a_i$ 时，前面 $i - 1$ 个数中 $\le a_i$ 的有 `ask(a[i])` 个，剩下的都比它大，构成逆序对。

值域很大时先**离散化**：排序去重后用排名代替原值，大小关系不变。

```cpp
const int N = 5e5 + 5;
int n, m, ans;
int a[N], b[N], c[N];

inline int lowbit(int x) { return x & -x; }

void add(int x, int v) {
    for (; x <= n; x += lowbit(x)) c[x] += v;
}

int ask(int x) {
    int s = 0;
    for (; x; x -= lowbit(x)) s += c[x];
    return s;
}

void solve() {
    cin >> n;
    For(i, 1, n) cin >> a[i], b[i] = a[i];
    sort(b + 1, b + 1 + n);
    m = unique(b + 1, b + 1 + n) - b - 1;
    For(i, 1, n) {
        int x = lower_bound(b + 1, b + 1 + m, a[i]) - b;
        ans += i - 1 - ask(x);
        add(x, 1);
    }
    cout << ans;
}
```

这种"以值为下标"的树状数组叫**权值树状数组**，可以回答"已插入的数中有多少个 $\le x$"。

### 4.2 倍增求第 k 小

在权值树状数组上找第 $k$ 小的数，二分 + 前缀和是 $O(\log^2 n)$。利用 $c$ 的结构可以 $O(\log n)$：从高位到低位确定答案的二进制，维护当前位置 $p$（前 $p$ 个值的总数 $< k$）。尝试 $p + 2^i$ 时，$c_{p + 2^i}$ 恰好就是 $(p, p + 2^i]$ 的个数（因为 $p$ 的低 $i$ 位全是 0），不用再求前缀和。

操作：`1 x` 插入 $x$，`2 x` 删除一个 $x$，`3 k` 询问第 $k$ 小（值域 $[1, 10^5]$）。

```cpp
const int N = 1e5 + 5, LG = 17;
int q;
int c[N];

inline int lowbit(int x) { return x & -x; }

void add(int x, int v) {
    for (; x < N; x += lowbit(x)) c[x] += v;
}

int kth(int k) {
    int p = 0;
    for (int i = LG; i >= 0; i--)
        if (p + (1 << i) < N && c[p + (1 << i)] < k) p += 1 << i, k -= c[p];
    return p + 1;
}

void solve() {
    cin >> q;
    while (q--) {
        int op, x;
        cin >> op >> x;
        if (op == 1) add(x, 1);
        else if (op == 2) add(x, -1);
        else cout << kth(x) << endl;
    }
}
```

### 4.3 离线：区间不同数的个数

询问 $[l, r]$ 中有多少种不同的数。把询问按 $r$ 排序，从左往右扫。关键想法：**每种数只在它最后一次出现的位置记 1**。扫到 $i$ 时，若 $a_i$ 之前出现在 $lst$，就把 $lst$ 处的 1 撤掉，在 $i$ 处记 1。这时对所有 $r = i$ 的询问，$[l, r]$ 中 1 的个数就是答案——每种在 $[l, r]$ 出现过的数，最后一次出现位置一定在 $[l, r]$ 中且只记了一次。

```cpp
const int N = 1e6 + 5;
int n, m;
int a[N], c[N], lst[N], ans[N];
struct qry { int l, r, id; } q[N];

inline bool cmp(const qry &x, const qry &y) { return x.r < y.r; }

inline int lowbit(int x) { return x & -x; }

void add(int x, int v) {
    for (; x <= n; x += lowbit(x)) c[x] += v;
}

int ask(int x) {
    int s = 0;
    for (; x; x -= lowbit(x)) s += c[x];
    return s;
}

void solve() {
    cin >> n;
    For(i, 1, n) cin >> a[i];
    cin >> m;
    For(i, 1, m) cin >> q[i].l >> q[i].r, q[i].id = i;
    sort(q + 1, q + 1 + m, cmp);
    int j = 1;
    For(i, 1, n) {
        if (lst[a[i]]) add(lst[a[i]], -1);
        add(i, 1), lst[a[i]] = i;
        while (j <= m && q[j].r == i) ans[q[j].id] = ask(i) - ask(q[j].l - 1), j++;
    }
    For(i, 1, m) cout << ans[i] << endl;
}
```

### 4.4 二维数点（扫描线）

问题：平面上有若干点，多次询问矩形 $[x_1, x_2] \times [y_1, y_2]$ 内有多少点。

把一个矩形询问拆成 4 个前缀询问（二维前缀和的容斥）：$Q(x_2, y_2) - Q(x_1 - 1, y_2) - Q(x_2, y_1 - 1) + Q(x_1 - 1, y_1 - 1)$，其中 $Q(x, y)$ 是 $x' \le x, y' \le y$ 的点数。

把点和前缀询问**按 $x$ 排序**一起扫描：遇到点就在树状数组的 $y$ 位置加 1；遇到询问 $(x, y)$ 就查 `ask(y)`。因为按 $x$ 排序，此时树状数组里恰好是所有 $x' \le x$ 的点。$x$ 相同时先加点再询问。

反过来，"有多少个矩形包含某个点"也可以这样做：矩形在 $x_1$ 处对 $[y_1, y_2]$ 区间加 1，在 $x_2 + 1$ 处减 1，点处单点查询。逆序对其实就是一维的数点。

## 5. 复杂度

| 操作 | 复杂度 |
| --- | --- |
| 单点修改 / 前缀查询 | $O(\log n)$ |
| 建树 | $O(n)$ 或 $O(n \log n)$ |
| 倍增求第 $k$ 小 | $O(\log n)$ |
| 空间 | $O(n)$（区间修改区间查询是 $2n$） |

二维树状数组（两层循环）每次 $O(\log n \cdot \log m)$，空间 $O(nm)$，只在 $n, m$ 都不大时可用。

## 6. 常见题型与技巧

- **动态前缀和**：单点修改 + 区间和，或通过差分实现区间修改。
- **逆序对及其变形**：冒泡排序的交换次数、两个排列"对齐"所需的最少相邻交换（转化成逆序对，如火柴排队）。
- **权值树状数组**：统计"前面有多少个比我小/大的数"，第 $k$ 小，配合离散化。
- **离线 + 排序**：把询问按某一维排序，扫描另一维，消掉一维后用树状数组处理剩下的一维（区间不同数、二维数点、矩形包含点）。
- **DFS 序**：子树对应 DFS 序上的连续区间，"子树加、单点查"或"单点加、子树求和"直接变成区间问题。
- **DP 优化**：$f_i = \max_{j < i,\ a_j < a_i} f_j + 1$（LIS），以 $a_j$ 为下标维护前缀最大值（$f$ 只会变大，满足前缀最大值树状数组的条件）。

## 7. 易错点

- 下标必须从 1 开始：`lowbit(0) = 0`，`add(0, v)` 会死循环。值域含 0 或负数时先平移或离散化。
- `add` 的上界是**树状数组的大小**（值域大小或序列长度），不是别的变量；权值树状数组要用离散化后的个数或值域上界。
- 差分时 `add(r + 1, -k)`，$r + 1 > n$ 时循环自然不执行，不用特判，但数组要开够。
- 逆序对要的是**严格**大于：`i - 1 - ask(x)`，而不是 `i - 1 - ask(x - 1)`。
- 区间修改区间查询的公式里，`c2` 加的是 `v * x`（修改的位置），查询时乘的是 `x + 1`（查询的位置），不要混。
- 结果可能超过 int（逆序对最多约 $n^2/2$），本仓库模板中 `int` 已是 64 位。
- 多组数据要清空 `c`。

## 8. 练习

**本站真题**

- [CSP-S 2025 T3 谐音替换](#/P14363)：Trie 上的祖先关系变成 DFS 序区间，问题化为"数有多少个矩形包含点"，离线扫描线 + 树状数组。

**洛谷经典题**

- [P3374 【模板】树状数组 1](https://www.luogu.com.cn/problem/P3374)
- [P3368 【模板】树状数组 2](https://www.luogu.com.cn/problem/P3368)
- [P3372 【模板】线段树 1](https://www.luogu.com.cn/problem/P3372)（用区间修改区间查询的树状数组）
- [P1908 逆序对](https://www.luogu.com.cn/problem/P1908)
- [P1966 [NOIP2013 提高组] 火柴排队](https://www.luogu.com.cn/problem/P1966)
- [P1972 [SDOI2009] HH的项链](https://www.luogu.com.cn/problem/P1972)
- [P5367 【模板】康托展开](https://www.luogu.com.cn/problem/P5367)
