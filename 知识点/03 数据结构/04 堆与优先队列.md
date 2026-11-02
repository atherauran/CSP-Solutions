# 堆与优先队列

**组别**：S　**关键词**：二叉堆、优先队列、priority_queue、懒删除、对顶堆、多路归并、反悔贪心

## 1. 是什么 / 解决什么问题

很多题需要反复做三件事：**加入一个数**、**查询当前最小（大）值**、**删除当前最小（大）值**。

- 用有序数组：查询删除 $O(1)$，插入要挪动 $O(n)$；
- 用无序数组：插入 $O(1)$，查询要扫一遍 $O(n)$；
- 用**堆**：三种操作分别是 $O(\log n)$、$O(1)$、$O(\log n)$。

支持这组操作的抽象结构叫**优先队列**——像排队，但每次出队的是"优先级最高"的那个，而不是最先来的那个。堆是优先队列最常用的实现。合并果子、Dijkstra、贪心里"每次取最优"的操作基本都靠它。

## 2. 核心原理

### 2.1 二叉堆的结构

二叉堆是一棵**完全二叉树**，并且满足**堆性质**：每个结点的值都不大于它的孩子（小根堆）。于是根就是最小值。

完全二叉树可以直接用数组存：结点 $x$ 的孩子是 $2x$、$2x+1$，父亲是 $\lfloor x/2 \rfloor$（见"树与二叉树"）。

```text
小根堆              数组下标： 1  2  3  4  5  6
        1           值：       1  3  2  7  4  5
      /   \
     3     2
    / \   /
   7   4 5
```

注意堆只保证"父亲 ≤ 孩子"，**兄弟之间、不同子树之间没有大小关系**，所以堆不是有序的，不能直接按顺序遍历出有序序列。

### 2.2 上浮与下沉

- **插入**：把新元素放到数组末尾（保持完全二叉树），然后**上浮**——只要比父亲小，就和父亲交换。
- **删除堆顶**：用末尾元素覆盖堆顶，大小减 1，然后**下沉**——和两个孩子中**较小的那个**比较，若比它大就交换，继续往下。

为什么下沉要和较小的孩子换：换上来的元素要同时不大于两个孩子，只有较小的孩子满足。

手推：在上图的堆中删除堆顶 1。

```text
末尾 5 移到堆顶      5 与较小孩子 2 交换      结束
        5                  2
      /   \              /   \
     3     2            3     5
    / \                / \
   7   4              7   4
```

树高为 $\lfloor \log_2 n \rfloor$，所以上浮和下沉都是 $O(\log n)$。

```cpp
const int N = 1e6 + 5;
int n, sz;
int hp[N];

void up(int x) {
    while (x > 1 && hp[x] < hp[x / 2]) swap(hp[x], hp[x / 2]), x /= 2;
}

void down(int x) {
    while (x * 2 <= sz) {
        int y = x * 2;
        if (y < sz && hp[y + 1] < hp[y]) y++;
        if (hp[x] <= hp[y]) break;
        swap(hp[x], hp[y]), x = y;
    }
}

void solve() {
    cin >> n;
    while (n--) {
        int op, x;
        cin >> op;
        if (op == 1) cin >> x, hp[++sz] = x, up(sz);
        else if (op == 2) cout << hp[1] << endl;
        else hp[1] = hp[sz--], down(1);
    }
}
```

### 2.3 $O(n)$ 建堆

把 $n$ 个数一次性建成堆，可以逐个插入（$O(n \log n)$），也可以先把数直接放进数组，再**从 $\lfloor n/2 \rfloor$ 到 1 依次下沉**：`for (int i = n / 2; i >= 1; i--) down(i);`。

后者是 $O(n)$：高度为 $h$ 的结点约有 $n / 2^{h+1}$ 个，每个下沉最多 $h$ 步，总和 $\sum_h \frac{n}{2^{h+1}} \cdot h = O(n)$。大部分结点在底层，下沉距离很短。初赛可能考这个结论。

**堆排序**：建好大根堆后，反复把堆顶和末尾交换、堆大小减 1、下沉，就得到升序序列，$O(n \log n)$，不稳定。

## 3. STL priority_queue

实际比赛几乎都用 STL：

| 写法 | 含义 |
| --- | --- |
| `priority_queue<int> q;` | **大根堆**（默认） |
| `priority_queue<int, vector<int>, greater<int>> q;` | 小根堆 |
| `priority_queue<pii> q;` | 按 `first` 再按 `second` 比较的大根堆 |
| `q.push(x)` / `q.pop()` / `q.top()` / `q.size()` / `q.empty()` | 插入 / 删除堆顶 / 取堆顶 / 大小 / 判空 |

小技巧：只想要小根堆又懒得写 `greater`，可以存相反数 `q.push(-x)`，取出时再取反。

**自定义结构体**：重载 `operator<`。priority_queue 认为"小于"的元素优先级低，堆顶是"最大"的那个。所以想让 `s` 小的在堆顶，要写 `return s > o.s;`——**方向和直觉相反**，这是最常见的错误。

### 3.1 例：多路归并

两个长度为 $n$ 的有序数组 $a, b$，求所有 $a_i + b_j$ 中最小的 $n$ 个。

把和看成 $n$ 个有序表：第 $i$ 个表是 $a_i + b_1 \le a_i + b_2 \le \dots$。先把每个表的第一个放进小根堆，每次取出最小的 $a_i + b_j$ 后，把同一个表的下一个 $a_i + b_{j+1}$ 放进去。堆里始终是每个表的"当前候选"，所以堆顶一定是全局最小。

```cpp
const int N = 1e5 + 5;
int n;
int a[N], b[N];
struct node {
    int s, i, j;
    bool operator<(const node &o) const { return s > o.s; }
};
priority_queue<node> q;

void solve() {
    cin >> n;
    For(i, 1, n) cin >> a[i];
    For(i, 1, n) cin >> b[i];
    For(i, 1, n) q.push({a[i] + b[1], i, 1});
    For(k, 1, n) {
        node u = q.top();
        q.pop();
        cout << u.s << ' ';
        if (u.j < n) q.push({a[u.i] + b[u.j + 1], u.i, u.j + 1});
    }
}
```

同样的思路可以合并 $k$ 个有序链表、求 $k$ 个函数值中最小的 $m$ 个。

## 4. 进阶技巧

### 4.1 懒删除

priority_queue 只能删堆顶。要删除任意一个值 $x$ 时，再开一个"待删除堆" $d$，把 $x$ 放进去。查询时，如果两个堆的堆顶相同，说明这个堆顶已被删除，两边一起弹出，直到不同为止。

```cpp
int n;
priority_queue<int> q, d;

void solve() {
    cin >> n;
    while (n--) {
        int op, x;
        cin >> op;
        if (op == 1) cin >> x, q.push(x);
        else if (op == 2) cin >> x, d.push(x);
        else {
            while (!d.empty() && q.top() == d.top()) q.pop(), d.pop();
            cout << q.top() << endl;
        }
    }
}
```

前提：被删除的值确实在堆里。另一种常见形式是在 Dijkstra 中：堆里存 $(dis, u)$，取出时若 $dis \ne dist_u$ 说明已经过时，直接跳过。

### 4.2 对顶堆：动态中位数

用一个**大根堆**存较小的一半，一个**小根堆**存较大的一半，并保持大根堆的大小等于小根堆或多 1。那么中位数就是大根堆的堆顶。

```text
     较小的一半（大根堆）  |  较大的一半（小根堆）
          1 3 [5]          |        [7] 8 9
                     中位数 5
```

插入时先按大小放进对应的堆，再从多的一边挪一个堆顶到另一边来平衡。

```cpp
int n;
priority_queue<int> lo;
priority_queue<int, vector<int>, greater<int>> hi;

void solve() {
    cin >> n;
    For(i, 1, n) {
        int x;
        cin >> x;
        if (lo.empty() || x <= lo.top()) lo.push(x);
        else hi.push(x);
        if (lo.size() > hi.size() + 1) hi.push(lo.top()), lo.pop();
        if (hi.size() > lo.size()) lo.push(hi.top()), hi.pop();
        if (i & 1) cout << lo.top() << endl;
    }
}
```

推广：维护"第 $k$ 小"时让大根堆的大小恒为 $k$。只求前 $k$ 大时，用一个大小为 $k$ 的**小根堆**，新元素比堆顶大就替换堆顶，堆顶就是第 $k$ 大。

### 4.3 反悔贪心

贪心时先做当前看起来最好的选择，之后如果发现更好的，就**撤销**之前选过的最差的那个。堆用来快速找到"之前选过的最差的"。

例：$n$ 项工作，每项耗时 1，第 $i$ 项要在时刻 $d_i$ 之前完成才能获得 $p_i$ 的收益，求最大收益。

按截止时间排序依次考虑，小根堆存已选工作的收益：

- 已选数量 $< d_i$：时间够，直接选；
- 否则时间已满：若堆顶（已选中收益最小的）比 $p_i$ 小，就放弃它、改选 $i$。

**为什么对**：截止时间 $\le d_i$ 的工作最多选 $d_i$ 个，这是唯一的约束。处理到 $i$ 时，堆里是前面工作在约束下的最优选择；换掉最小的一个，数量不变、约束仍满足、收益增大。

```cpp
const int N = 1e5 + 5;
int n, ans;
struct job { int d, p; } a[N];
priority_queue<int, vector<int>, greater<int>> q;

inline bool cmp(const job &x, const job &y) { return x.d < y.d; }

void solve() {
    cin >> n;
    For(i, 1, n) cin >> a[i].d >> a[i].p;
    sort(a + 1, a + 1 + n, cmp);
    For(i, 1, n) {
        if ((int)q.size() < a[i].d) q.push(a[i].p), ans += a[i].p;
        else if (q.top() < a[i].p) ans += a[i].p - q.top(), q.pop(), q.push(a[i].p);
    }
    cout << ans;
}
```

## 5. 复杂度

| 操作 | 二叉堆 |
| --- | --- |
| 插入 | $O(\log n)$ |
| 取堆顶 | $O(1)$ |
| 删除堆顶 | $O(\log n)$ |
| 建堆（下沉法） | $O(n)$ |
| 删除任意元素 | 懒删除，均摊 $O(\log n)$ |
| 查找任意元素 | 不支持（$O(n)$） |

如果还需要"删除任意元素""查询前驱后继""按顺序遍历"，用 `set` / `multiset`（也是 $O(\log n)$，常数更大）。

## 6. 常见题型与技巧

- **每次取最小/最大**：合并果子（哈夫曼）、Dijkstra、Prim、模拟"谁最先结束"的事件（存结束时间）。
- **资源分配模拟**：两个堆，一个存"忙碌的资源（按释放时间）"，一个存"空闲的资源（按编号）"，事件到来时先释放到期的，再分配最小编号。
- **前 $k$ 大 / 第 $k$ 大**：固定大小的堆；对顶堆维护动态中位数。
- **多路归并**：$k$ 个有序序列合并，每个序列只放一个候选进堆。
- **反悔贪心**：截止时间类调度、"选了某个可以撤销"的模型。
- **可以用队列代替堆的情况**：新产生的元素单调（如已排序的合并果子），两个队列就能 $O(n)$ 完成。

## 7. 易错点

- `priority_queue` 默认是**大根堆**。
- 自定义 `operator<` 的方向：`return s > o.s;` 才是 `s` 小的在堆顶。
- 对空堆调用 `top()` / `pop()` 会运行错误，懒删除、对顶堆中尤其要注意。
- 手写堆删除后要 `sz--`，下沉时判断右孩子是否存在（`y < sz`）。
- 堆不是有序数组，`hp[2]` 不一定是第二小。
- 结构体里存了下标、时间等信息时，确认比较的是正确的字段，相等时是否需要第二关键字。

## 8. 练习

**本站真题**

- [CSP-S 2021 T1 廊桥分配](#/P7913)：两个小根堆分别维护"忙碌廊桥（按离开时间）"和"空闲廊桥（按编号）"。
- [CSP-J 2023 T4 旅游巴士](#/P9751)：分层图上的 Dijkstra，堆存 $(时间, 状态)$。
- [CSP-S 2020 T4 贪吃蛇](#/P7078)：用堆模拟可拿约 70 分，正解利用单调性改成双队列。

**洛谷经典题**

- [P3378 【模板】堆](https://www.luogu.com.cn/problem/P3378)
- [P1090 [NOIP 2004 提高组] 合并果子](https://www.luogu.com.cn/problem/P1090)
- [P1168 中位数](https://www.luogu.com.cn/problem/P1168)
- [P1801 黑匣子](https://www.luogu.com.cn/problem/P1801)
- [P1631 序列合并](https://www.luogu.com.cn/problem/P1631)
- [P2085 最小函数值](https://www.luogu.com.cn/problem/P2085)
- [P2949 [USACO09OPEN] Work Scheduling G](https://www.luogu.com.cn/problem/P2949)
- [P4053 [JSOI2007] 建筑抢修](https://www.luogu.com.cn/problem/P4053)
