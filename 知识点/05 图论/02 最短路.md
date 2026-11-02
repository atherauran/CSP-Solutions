# 最短路

**组别**：S　**关键词**：Floyd、Dijkstra、Bellman-Ford、SPFA、负环、差分约束、分层图、最短路计数

## 1. 是什么 / 解决什么问题

给一张带权图，求从点 $s$ 到点 $t$ 的路径中，边权和最小的那条（的长度）。按问法分两类：

- **单源最短路**：从一个起点 $s$ 到所有点的最短距离，记作 $d_v$。
- **全源最短路**：任意两点之间的最短距离，记作 $d_{i,j}$。

边权都相同（无权图）时，BFS 就能求最短路，见《图的存储与遍历》。本篇处理一般的边权：

| 算法 | 类型 | 负权边 | 复杂度 | 适用 |
| --- | --- | --- | --- | --- |
| Floyd | 全源 | 可以 | $O(n^3)$ | $n \le 500$ 左右 |
| Dijkstra（堆优化） | 单源 | **不行** | $O(m \log m)$ | 非负边权，首选 |
| Dijkstra（朴素） | 单源 | 不行 | $O(n^2)$ | 稠密图 |
| Bellman-Ford | 单源 | 可以 | $O(nm)$ | 判负环、限制边数 |
| SPFA | 单源 | 可以 | 一般较快，最坏 $O(nm)$ | 有负权、判负环 |

## 2. 核心原理

### 2.1 松弛与三角形不等式

所有最短路算法都基于同一个操作——**松弛**：已知 $s$ 到 $u$ 的一条路径长 $d_u$，有边 $u \to v$ 权为 $w$，那么 $s$ 到 $v$ 就有一条长 $d_u + w$ 的路径，于是

$$d_v \gets \min(d_v, d_u + w)$$

最短路求完后，对每条边都有 $d_v \le d_u + w$，这叫**三角形不等式**。反过来，各算法的区别只在于"按什么顺序松弛、松弛多少次"。

**负环**：若图中有一个边权和为负的环，绕着它走一圈距离就变小，可以无限变小，最短路不存在。下文除了专门判负环的地方，都假设没有负环。

### 2.2 Floyd：全源最短路

设 $f_k(i, j)$ 表示从 $i$ 到 $j$、**中间只经过编号 $1 \sim k$ 的点**的最短路长度。考虑这条路径是否经过点 $k$：

- 不经过：$f_{k-1}(i, j)$；
- 经过：经过一次就够了（没有负环），路径被 $k$ 分成两段，$f_{k-1}(i, k) + f_{k-1}(k, j)$。

$$f_k(i, j) = \min\big(f_{k-1}(i, j),\ f_{k-1}(i, k) + f_{k-1}(k, j)\big)$$

初值 $f_0(i, j)$ 就是邻接矩阵（$i = j$ 为 0，没边为 $\infty$），答案是 $f_n(i, j)$。

第一维可以直接省掉、原地更新：第 $k$ 轮用到的 $f(i, k)$ 和 $f(k, j)$ 本轮不会变小（"经过 $k$ 到达 $k$"没有意义），所以新旧值一样。

**$k$ 必须放在最外层循环**。这是 DP 的阶段，内外层顺序写反就错了。

几个用法：

- **传递闭包**：只关心"能否到达"，把 $\min$ 和 $+$ 换成"或"和"与"：`r[i][j] |= r[i][k] & r[k][j]`。
- **判负环**：跑完后若某个 $d_{i,i} < 0$，就有负环。
- **最小环**（无向图）：在用 $k$ 更新之前，$d_{i,j}$ 还没经过 $k$，所以对 $i < j < k$，$d_{i,j} + a_{i,k} + a_{k,j}$ 就是"以 $k$ 为最大编号点"的环长（$a$ 是原始边权）。取最小值即可。
- **按顺序加点**：$k$ 一轮一轮加入，第 $k$ 轮结束时得到"只用前 $k$ 个点中转"的最短路。如果点是按时间逐个可用的，就按可用时间的顺序作为 $k$ 的顺序。

### 2.3 Dijkstra：非负权单源最短路

**思想**：把点分成"已确定最短距离"和"未确定"两类。每次从未确定的点中取 $d$ 最小的点 $u$，此时 $d_u$ 就是最终答案，把它标为已确定，并用它松弛所有出边。

**为什么取出的点已经是最短距离**：设 $u$ 是当前未确定点中 $d$ 最小的。任何一条到 $u$ 的更短路径，都要在某处第一次离开"已确定"集合，走到某个未确定点 $x$，此时这段路径长度已经 $\ge d_x \ge d_u$；后面的边权非负，只会更长。所以不存在更短的路径。

这个证明用到了**边权非负**。有负权边时会出错，例如：

```
1 --2--> 2
1 --3--> 3 --(-2)--> 2
```

Dijkstra 先取出 1，再取出 $d = 2$ 的点 2 并认定它确定了，但实际 $1 \to 3 \to 2$ 只要 1。

**手推一遍**：有向图，边为 $1 \to 2\,(2)$、$1 \to 3\,(5)$、$2 \to 3\,(1)$、$2 \to 4\,(6)$、$3 \to 4\,(2)$、$3 \to 5\,(7)$、$4 \to 5\,(1)$，从 1 出发：

| 取出 | 处理后 $d_1 \sim d_5$ | 说明 |
| --- | --- | --- |
| 1（距离 0） | 0, 2, 5, ∞, ∞ | |
| 2（距离 2） | 0, 2, **3**, 8, ∞ | $d_3$ 从 5 改成 3 |
| 3（距离 3） | 0, 2, 3, **5**, 10 | |
| 3（距离 5） | — | 过时的记录，跳过 |
| 4（距离 5） | 0, 2, 3, 5, **6** | |
| 5（距离 6） | — | 确定 |
| 4（距离 8）、5（距离 10） | — | 过时，跳过 |

**堆优化与懒删除**：用小根堆存 `{距离, 点}`，每次取堆顶。松弛成功就把新的 `{d_v, v}` 压入堆，旧记录不删除；取出时若记录的距离不等于当前 $d_v$，说明是过时记录，直接跳过。每条边最多压一次堆，所以堆大小是 $O(m)$，复杂度 $O(m \log m)$。

**朴素版本**：不用堆，每次 $O(n)$ 扫一遍找最小值，总共 $O(n^2 + m)$。在 $m$ 接近 $n^2$ 的稠密图上反而比堆优化的 $O(n^2 \log n)$ 快。

### 2.4 Bellman-Ford

没有负环时，最短路一定是简单路径，最多 $n - 1$ 条边。Bellman-Ford 就是：**把所有边松弛一遍，重复 $n - 1$ 轮**。

为什么够：归纳可知，第 $i$ 轮结束后，所有"边数 $\le i$ 的最短路"都已求对。最短路最多 $n - 1$ 条边，所以 $n - 1$ 轮后全部正确。

**判负环**：如果第 $n$ 轮还能松弛成功，说明存在从 $s$ 出发能到达的负环。

**限制边数的最短路**：如果题目要求"最多走 $k$ 条边"，就只做 $k$ 轮，而且每轮要用**上一轮的 $d$ 的备份**来松弛，否则一轮内可能连续走多条边。

### 2.5 SPFA

Bellman-Ford 每轮都扫所有边，但其实只有**上一轮 $d$ 变小了的点**，它的出边才可能松弛成功。SPFA 用队列存"$d$ 变小了、还没处理"的点，只处理它们的出边：

1. 起点入队；
2. 取出队首 $u$，松弛 $u$ 的出边；某个 $v$ 被松弛成功且不在队列中，就把 $v$ 入队；
3. 队列空了就结束。

随机图上 SPFA 很快，但可以构造数据让它退化到 $O(nm)$，和 Bellman-Ford 一样。所以**没有负权边时一律用 Dijkstra**，SPFA 只在有负权或要判负环时使用。

**判负环**：记录 $cnt_v$ 为当前最短路径的边数，松弛时 $cnt_v = cnt_u + 1$。如果某个 $cnt_v \ge n$，路径上有 $n$ 条边、$n + 1$ 个点，必然有重复的点，即有负环。

注意：从 $s$ 出发只能发现 **$s$ 能到达的**负环。要判断整张图有没有负环，就把所有点都作为起点（$d$ 全设为 0、全部入队），相当于加一个向所有点连 0 权边的超级源点。

### 2.6 差分约束

给出若干形如 $x_a - x_b \le c$ 的不等式，求一组满足所有条件的整数解，或判断无解。

关键观察：三角形不等式 $d_v \le d_u + w$ 移项就是 $d_v - d_u \le w$。所以：

- 每个变量 $x_i$ 对应一个点；
- 约束 $x_a - x_b \le c$ 对应一条边 $b \to a$，权为 $c$；
- 加一个超级源点 $0$，向每个点连权为 0 的边（保证所有点可达，并让 $x_i \le 0$）；
- 从 0 跑最短路（有负权，用 SPFA 或 Bellman-Ford）。**有负环则无解**，否则 $x_i = d_i$ 就是一组解。

为什么负环说明无解：沿着负环把对应的不等式全部相加，左边正负抵消为 0，右边是环的边权和，得到 $0 \le$ 负数，矛盾。

例：$x_1 - x_2 \le 3$，$x_2 - x_3 \le -2$，$x_1 - x_3 \le 2$。建边 $2 \to 1\,(3)$、$3 \to 2\,(-2)$、$3 \to 1\,(2)$，加上 $0 \to 1, 2, 3$ 的 0 权边，求得 $d = (0, -2, 0)$。验证：$0 - (-2) = 2 \le 3$，$-2 - 0 \le -2$，$0 - 0 \le 2$。

各种约束的转化：

| 约束 | 转成 | 建边 |
| --- | --- | --- |
| $x_a - x_b \le c$ | — | $b \to a$，权 $c$ |
| $x_a - x_b \ge c$ | $x_b - x_a \le -c$ | $a \to b$，权 $-c$ |
| $x_a = x_b$ | $x_a - x_b \le 0$ 且 $x_b - x_a \le 0$ | 两条 0 权边 |
| $x_a - x_b < c$（整数） | $x_a - x_b \le c - 1$ | $b \to a$，权 $c - 1$ |

求 $x_t - x_s$ 的**最大值**：从 $s$ 跑最短路，$d_t$ 就是答案（最短路给出的是每个变量"能取到的最大值"）。求**最小值**则把约束都写成 $\ge$ 的形式跑最长路，或者等价地取相反数。

### 2.7 分层图（拆点）

有些题目在普通最短路上多了一个**小范围的额外状态**，例如"可以让最多 $k$ 条边免费"。只记录"在哪个点"不够，还要记录"已经用了几次免费"。

做法是把每个点拆成 $k + 1$ 个：$(u, j)$ 表示到达 $u$、已用 $j$ 次免费。图也随之变成 $k + 1$ 层：

- 层内：原图的边 $u \to v$（权 $w$），连 $(u, j) \to (v, j)$，权 $w$；
- 层间：使用一次免费，连 $(u, j) \to (v, j + 1)$，权 0。

```
第 0 层:  1 --w-- 2 --w-- 3
            \       \
             0       0        （层间的免费边）
              \       \
第 1 层:  1 --w-- 2 --w-- 3
```

编号时让 $(u, j)$ 对应 $j \cdot n + u$。在这张 $n(k+1)$ 个点的图上跑 Dijkstra，答案是 $\min_j d_{(t, j)}$。

其他常见的"层"：时间对 $k$ 取模的值、路径长度的奇偶性、当前持有的某种物品……只要额外状态的取值不多，都可以这样拆点。

### 2.8 最短路计数

求从 $s$ 到每个点的最短路**有多少条**。在 Dijkstra 松弛时顺便维护 $cnt$：

- $d_u + w < d_v$：找到更短的路，$d_v = d_u + w$，$cnt_v = cnt_u$（之前的都作废）；
- $d_u + w = d_v$：又找到一批同样短的路，$cnt_v \mathrel{+}= cnt_u$。

正确性：所有"最短路上 $v$ 的前驱 $u$"都满足 $d_u < d_v$（边权为正），它们都在 $v$ 之前被取出并完成了对 $v$ 的贡献，所以 $v$ 被取出时 $cnt_v$ 已经是最终值，可以继续往后传。

边权全为 1 时直接在 BFS 中做同样的事。**有 0 权边时这个方法会出错**（前驱可能和 $v$ 距离相同、在 $v$ 之后才被取出），要先把 0 权边缩起来或换思路。

### 2.9 其他常用技巧

- **路径还原**：松弛成功时记录 $pre_v = u$，最后从 $t$ 沿 $pre$ 倒着走回 $s$。所有 $pre$ 边构成一棵**最短路树**。
- **多个点到同一个终点**：在**反图**上从终点跑一次单源最短路。"去一趟再回来"就正图、反图各跑一次。
- **多个起点**：建一个超级源点，向每个起点连 0 权边；或者一开始把所有起点的 $d$ 设为 0 并全部入堆。
- **判断边是否在某条最短路上**：从 $s$ 在正图跑得 $d_1$，从 $t$ 在反图跑得 $d_2$。边 $u \to v$ 在某条最短路上 $\iff d_1(u) + w + d_2(v) = d_1(t)$。
- **点权**：把点权加到"进入这个点的边"上；或者拆点，用一条内部边表示点权。
- **最短路上的"最大值最小"**：如果路径代价不是边权和而是最大边权，松弛改为 $\max(d_u, w)$，Dijkstra 仍然成立（也可以二分答案 + BFS，或用最小生成树）。

## 3. 代码模板

### 3.1 Floyd

$n$ 个点 $m$ 条无向边，输出两两最短距离，不连通输出 $-1$。

```cpp
const int N = 505;
int n, m;
int d[N][N];

void solve() {
    cin >> n >> m;
    mset(d, 0x3f);
    For(i, 1, n) d[i][i] = 0;
    For(i, 1, m) {
        int u, v, w;
        cin >> u >> v >> w;
        d[u][v] = d[v][u] = min(d[u][v], w);
    }
    For(k, 1, n) For(i, 1, n) For(j, 1, n)
        d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
    For(i, 1, n) {
        For(j, 1, n) cout << (d[i][j] == LINF ? -1 : d[i][j]) << ' ';
        cout << endl;
    }
}
```

`mset(d, 0x3f)` 让每个元素都变成 `LINF`，两个 `LINF` 相加约 $9.1 \times 10^{18}$，还没有超过 `long long` 的上限，所以不用特判。

### 3.2 Dijkstra（堆优化）

$n$ 个点 $m$ 条有向边，从 $s$ 出发，输出到每个点的最短距离。

```cpp
const int N = 1e5 + 5;
int n, m, s;
vector<pii> g[N];

vector<int> dijkstra(int s, vector<pii> g[]) {
    vector<int> dist(n + 1, LINF);
    priority_queue<pii, vector<pii>, greater<pii>> q;
    dist[s] = 0;
    q.push({0, s});
    while (!q.empty()) {
        auto cur = q.top();
        int d = cur.F, u = cur.S;
        q.pop();
        if (d != dist[u]) continue;
        for (auto e : g[u]) {
            int v = e.F, w = e.S;
            if (dist[v] > d + w) {
                dist[v] = d + w;
                q.push({dist[v], v});
            }
        }
    }
    return dist;
}

void solve() {
    cin >> n >> m >> s;
    For(i, 1, m) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].pb({v, w});
    }
    vector<int> d = dijkstra(s, g);
    For(i, 1, n) cout << d[i] << ' ';
}
```

- 堆里存 `{距离, 点}`，`pair` 先比第一维，所以按距离排序；`greater<pii>` 让它成为小根堆。
- `if (d != dist[u]) continue;` 就是懒删除。
- 图作为参数传入，方便对正图、反图分别调用：`dijkstra(s, g1)`、`dijkstra(t, g2)`。

### 3.3 Dijkstra（朴素 $O(n^2)$）

稠密图上用邻接矩阵。

```cpp
const int N = 2005;
int n, m, s;
int a[N][N], d[N];
bool vis[N];

void solve() {
    cin >> n >> m >> s;
    mset(a, 0x3f);
    For(i, 1, m) {
        int u, v, w;
        cin >> u >> v >> w;
        a[u][v] = min(a[u][v], w);
    }
    mset(d, 0x3f);
    d[s] = 0;
    For(t, 1, n) {
        int u = 0;
        For(i, 1, n)
            if (!vis[i] && (!u || d[i] < d[u])) u = i;
        vis[u] = true;
        For(v, 1, n) d[v] = min(d[v], d[u] + a[u][v]);
    }
    For(i, 1, n) cout << d[i] << ' ';
}
```

### 3.4 Bellman-Ford

边集数组存图。若第 $n$ 轮仍有松弛，说明从 $s$ 能走到负环。

```cpp
const int N = 1e4 + 5, M = 1e5 + 5;
int n, m, s;
int d[N];
struct edge { int u, v, w; } e[M];

void solve() {
    cin >> n >> m >> s;
    For(i, 1, m) cin >> e[i].u >> e[i].v >> e[i].w;
    mset(d, 0x3f);
    d[s] = 0;
    For(t, 1, n) {
        bool upd = false;
        For(i, 1, m) {
            int u = e[i].u, v = e[i].v, w = e[i].w;
            if (d[u] != LINF && d[v] > d[u] + w) d[v] = d[u] + w, upd = true;
        }
        if (!upd) break;
        if (t == n) {
            cout << "negative cycle";
            return;
        }
    }
    For(i, 1, n) {
        if (d[i] == LINF) cout << "INF ";
        else cout << d[i] << ' ';
    }
}
```

有负权边时必须判 `d[u] != LINF`：否则不可达的点也会被"$\infty$ 加负数"更新成一个比 $\infty$ 略小的值。

### 3.5 SPFA 判负环

多组数据（在 `main` 中打开 `cin >> tests;`）。每组 $n$ 个点 $m$ 条边，$w \ge 0$ 时是无向边，$w < 0$ 时是有向边 $u \to v$。判断从 1 出发能否到达负环。

```cpp
const int N = 2005;
int n, m;
int d[N], cnt[N];
bool inq[N];
vector<pii> g[N];

bool spfa(int s) {
    For(i, 1, n) d[i] = LINF, cnt[i] = 0, inq[i] = false;
    queue<int> q;
    d[s] = 0, q.push(s), inq[s] = true;
    while (!q.empty()) {
        int u = q.front();
        q.pop(), inq[u] = false;
        for (auto e : g[u]) {
            int v = e.F, w = e.S;
            if (d[v] > d[u] + w) {
                d[v] = d[u] + w, cnt[v] = cnt[u] + 1;
                if (cnt[v] >= n) return true;
                if (!inq[v]) q.push(v), inq[v] = true;
            }
        }
    }
    return false;
}

void solve() {
    cin >> n >> m;
    For(i, 1, n) g[i].clear();
    For(i, 1, m) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].pb({v, w});
        if (w >= 0) g[v].pb({u, w});
    }
    cout << (spfa(1) ? "YES" : "NO") << endl;
}
```

`inq` 标记点是否已在队列中，避免重复入队。

### 3.6 差分约束

$n$ 个变量、$m$ 个约束，每个约束 `a b c` 表示 $x_a - x_b \le c$。输出一组解，无解输出 `NO`。

```cpp
const int N = 5005;
int n, m;
int d[N], cnt[N];
bool inq[N];
vector<pii> g[N];

bool spfa() {
    mset(d, 0x3f);
    queue<int> q;
    d[0] = 0, q.push(0), inq[0] = true;
    while (!q.empty()) {
        int u = q.front();
        q.pop(), inq[u] = false;
        for (auto e : g[u]) {
            int v = e.F, w = e.S;
            if (d[v] > d[u] + w) {
                d[v] = d[u] + w, cnt[v] = cnt[u] + 1;
                if (cnt[v] > n) return false;
                if (!inq[v]) q.push(v), inq[v] = true;
            }
        }
    }
    return true;
}

void solve() {
    cin >> n >> m;
    For(i, 1, m) {
        int a, b, c;
        cin >> a >> b >> c;
        g[b].pb({a, c});
    }
    For(i, 1, n) g[0].pb({i, 0});
    if (!spfa()) {
        cout << "NO";
        return;
    }
    For(i, 1, n) cout << d[i] << ' ';
}
```

加上超级源点后共 $n + 1$ 个点，所以负环的判定条件是 $cnt_v > n$。

### 3.7 分层图

$c$ 个城市（编号 $0 \sim c-1$）、$m$ 条无向航线，最多可以免费乘坐 $k$ 次，求 $s$ 到 $t$ 的最小花费。$(u, j)$ 编号为 $j \cdot c + u$，Dijkstra 用的点数 $n$ 设为 $c(k+1)$。

```cpp
const int N = 1e4 + 5, K = 12;
int n, m, k, c, s, t;
vector<pii> g[N * K];

vector<int> dijkstra(int s, vector<pii> g[]) {
    vector<int> dist(n + 1, LINF);
    priority_queue<pii, vector<pii>, greater<pii>> q;
    dist[s] = 0;
    q.push({0, s});
    while (!q.empty()) {
        auto cur = q.top();
        int d = cur.F, u = cur.S;
        q.pop();
        if (d != dist[u]) continue;
        for (auto e : g[u]) {
            int v = e.F, w = e.S;
            if (dist[v] > d + w) {
                dist[v] = d + w;
                q.push({dist[v], v});
            }
        }
    }
    return dist;
}

void solve() {
    cin >> c >> m >> k >> s >> t;
    s++, t++;
    For(i, 1, m) {
        int u, v, w;
        cin >> u >> v >> w;
        u++, v++;
        For(j, 0, k) {
            g[j * c + u].pb({j * c + v, w}), g[j * c + v].pb({j * c + u, w});
            if (j < k) g[j * c + u].pb({(j + 1) * c + v, 0}), g[j * c + v].pb({(j + 1) * c + u, 0});
        }
    }
    n = c * (k + 1);
    vector<int> d = dijkstra(s, g);
    int ans = LINF;
    For(j, 0, k) ans = min(ans, d[j * c + t]);
    cout << ans;
}
```

答案要对所有层取最小值：免费次数不一定用完。

### 3.8 最短路计数

$n$ 个点 $m$ 条无向正权边，求 1 到每个点的最短路条数，对 $100003$ 取模。

```cpp
const int N = 1e6 + 5, P = 100003;
int n, m;
int dist[N], cnt[N];
vector<pii> g[N];

void solve() {
    cin >> n >> m;
    For(i, 1, m) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].pb({v, w}), g[v].pb({u, w});
    }
    mset(dist, 0x3f);
    priority_queue<pii, vector<pii>, greater<pii>> q;
    dist[1] = 0, cnt[1] = 1;
    q.push({0, 1});
    while (!q.empty()) {
        auto cur = q.top();
        int d = cur.F, u = cur.S;
        q.pop();
        if (d != dist[u]) continue;
        for (auto e : g[u]) {
            int v = e.F, w = e.S;
            if (dist[v] > d + w) {
                dist[v] = d + w, cnt[v] = cnt[u];
                q.push({dist[v], v});
            } else if (dist[v] == d + w) cnt[v] = (cnt[v] + cnt[u]) % P;
        }
    }
    For(i, 1, n) cout << cnt[i] << endl;
}
```

## 4. 复杂度

| 算法 | 时间 | 空间 |
| --- | --- | --- |
| BFS（无权图） | $O(n + m)$ | $O(n + m)$ |
| Floyd | $O(n^3)$ | $O(n^2)$ |
| 朴素 Dijkstra | $O(n^2 + m)$ | $O(n^2)$（邻接矩阵） |
| 堆优化 Dijkstra | $O(m \log m)$ | $O(n + m)$ |
| Bellman-Ford | $O(nm)$ | $O(m)$ |
| SPFA | 最坏 $O(nm)$ | $O(n + m)$ |
| 分层图 Dijkstra | $O(km \log(km))$ | $O(k(n + m))$ |

估算：Floyd 在 $n = 500$ 时约 $1.25 \times 10^8$ 次运算，还能接受；$n = 1000$ 就要 $10^9$，太慢。堆优化 Dijkstra 在 $n, m \le 10^6$ 时可以通过。

## 5. 常见题型与技巧

- **选算法**：看数据范围和边权。$n$ 几百且要全源 → Floyd；非负边权 → 堆优化 Dijkstra；有负权 → SPFA / Bellman-Ford；边权全相同 → BFS；边权只有 0、1 → 0-1 BFS。
- **建图是难点**：很多题的图不是直接给的，要想清楚"什么是点、什么是边"。比如把"线路"当作点、"换乘"当作边；把平面图的"面"当作点（对偶图）。
- **拆点 / 分层图**：额外状态取值不多（免费次数、时间取模、奇偶性），就把它放进点里。
- **正反图**：多个点到一个终点、往返路程、判断某边是否在最短路上。
- **全源但 $n$ 很大**：边权全为 1 时从每个点 BFS，$O(n(n+m))$；要么想办法只对少数关键点跑单源最短路。
- **最短路计数 / 最短路图**：在松弛时维护额外信息，或先求出 $d$ 再在"最短路 DAG"（满足 $d_u + w = d_v$ 的边）上做 DP。
- **差分约束**：题目给出一堆"$a$ 比 $b$ 至多大多少""至少大多少"的条件，问可行性或最值。
- **二分答案 + 最短路**：如"路径上第 $k+1$ 大的边最小"，二分阈值 $x$，大于 $x$ 的边权记为 1、其余记为 0，跑 0-1 BFS 看最短路是否 $\le k$。

## 6. 易错点

- **INF 溢出**：用 `0x3f3f3f3f`（`INF`）作 `int` 无穷大、`LINF` 作 `long long` 无穷大，两个相加都不会溢出。不要用 `INT_MAX` / `LLONG_MAX`，一加就溢出成负数。
- **Dijkstra 遇到负权边**：结果不对，或者复杂度失控。
- **Floyd 循环顺序**：$k$ 在最外层。
- **无向图只存了一条边**，或边数组没开两倍。
- **重边**：邻接矩阵要取 $\min$，邻接表天然没问题。
- **Bellman-Ford / SPFA 处理负权时没判断不可达**：$\infty$ 加负数会变成"可达"。
- **SPFA 判负环**：用"入队次数 $\ge n$"也可以，但用"最短路边数 $\ge n$"更快发现；超级源点存在时点数变成 $n + 1$。
- **只从一个点出发判负环**，漏掉它到不了的负环。
- **分层图数组开小**：点数是 $n(k+1)$，边数也要乘上 $k$ 的倍数。
- **多组数据**：清空邻接表、`cnt`、`inq`。
- **距离要开 `long long`**：$10^5$ 条边、每条 $10^9$，和就到 $10^{14}$。

## 7. 练习

**本站真题**

- [CSP-J 2019 T4 加工零件](#/P5663)：按路径长度奇偶性拆点，BFS 求最短路。
- [CSP-J 2023 T4 旅游巴士](#/P9751)：按"时刻 $\bmod k$"拆点，Dijkstra 求最早到达时刻。
- [CSP-S 2021 T4 交通规划](#/P7916)：平面图最小割转化为对偶图上的 Dijkstra。
- [CSP-S 2022 T1 假期计划](#/P8817)：从每个点 BFS 求全源最短步数。
- [CSP-S 2026 T2 地铁](#/P17832)：把线路当作点建图，Floyd 求全源最短路。
- [CSP-S 2026 T3 迁徙](#/P17833)：分析最短路的分层结构，统计恰好两条最短路的点对。

**洛谷经典题**

- [P3371 【模板】单源最短路径（弱化版）](https://www.luogu.com.cn/problem/P3371)
- [P4779 【模板】单源最短路径（标准版）](https://www.luogu.com.cn/problem/P4779)：卡 SPFA，必须用堆优化 Dijkstra。
- [P3385 【模板】负环](https://www.luogu.com.cn/problem/P3385)
- [P1119 灾后重建](https://www.luogu.com.cn/problem/P1119)：按时间顺序加点的 Floyd。
- [P6175 无向图的最小环问题](https://www.luogu.com.cn/problem/P6175)：Floyd 求最小环。
- [P1629 邮递员送信](https://www.luogu.com.cn/problem/P1629)：正图、反图各跑一次 Dijkstra。
- [P1144 最短路计数](https://www.luogu.com.cn/problem/P1144)
- [P4568 [JLOI2011] 飞行路线](https://www.luogu.com.cn/problem/P4568)：分层图。
- [P1993 小 K 的农场](https://www.luogu.com.cn/problem/P1993)：差分约束。
