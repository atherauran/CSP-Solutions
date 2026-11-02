# STL 常用容器与算法

**组别**：J　**关键词**：vector、stack、queue、priority_queue、set、map、sort、lower_bound

## 1. 是什么 / 解决什么问题

STL（标准模板库）是 C++ 自带的一组现成的数据结构（**容器**）和**算法**。动态数组、栈、队列、堆、平衡树、哈希表、排序、二分查找……这些都不用自己写，直接用就行，而且经过充分优化、不易出错。

比赛中用 STL 的关键是三件事：

1. 知道每种容器能做什么；
2. 知道每个操作的**复杂度**，避免在循环里调用 $O(n)$ 的操作；
3. 知道常见的坑（`map` 的 `[]` 会插入、`size()` 是无符号数等）。

本文代码默认套在本仓库模板中，`int` 即 `long long`，`pb` 即 `push_back`，`F`/`S` 即 `first`/`second`。

## 2. 基础概念

- **迭代器**：指向容器中某个元素的"位置"，用 `*it` 取值、`it++` 前进。`v.begin()` 指向第一个元素，`v.end()` 指向**最后一个元素的下一个位置**（不能解引用）。
- **左闭右开**：STL 的区间一律是 $[\text{first}, \text{last})$。所以对 1-indexed 数组 $a_1 \sim a_n$ 排序写 `sort(a + 1, a + 1 + n)`，数组名加偏移就是指针，指针可以当迭代器用。
- `auto`：让编译器推断类型，如 `auto it = s.begin();`。
- 范围 for：`for (int x : v)` 依次取出每个元素的拷贝；`for (int &x : v)` 取引用，可以修改。
- `size()` 返回**无符号**整数。空容器的 `v.size() - 1` 是 $2^{64} - 1$，不是 $-1$。需要做减法时先转成 `int`：`(int)v.size() - 1`。

## 3. 容器

### 3.1 vector：动态数组

长度可变的数组，支持下标访问。最常见的用途是**邻接表**（`vector<int> g[N]`，每个点一个 `vector` 存它的邻居）和长度不确定的数组。

| 操作 | 作用 | 复杂度 |
| --- | --- | --- |
| `v.pb(x)` / `v.pop_back()` | 尾部插入 / 删除 | 均摊 $O(1)$ |
| `v[i]`、`v.front()`、`v.back()` | 访问 | $O(1)$ |
| `v.size()`、`v.empty()` | 大小 / 是否为空 | $O(1)$ |
| `v.clear()` | 清空 | $O(n)$ |
| `v.resize(n)`、`vector<int> v(n, x)` | 改大小 / 建 $n$ 个 $x$ | $O(n)$ |
| `v.insert(it, x)`、`v.erase(it)` | 中间插入 / 删除 | $O(n)$ |

```cpp
void solve() {
    vector<int> v;
    For(i, 1, 5) v.pb(i * i);
    v.pop_back();
    v.insert(v.begin() + 1, 7);
    v.erase(v.begin());
    cout << v.size() << " " << v.front() << " " << v.back() << endl;
    for (int x : v) cout << x << " ";
    cout << endl;
    vector<vector<int>> f(3, vector<int>(4, -1));
    cout << f[2][3] << endl;
}
```

依次得到 `1 4 9 16 25` → `1 4 9 16` → `1 7 4 9 16` → `7 4 9 16`，输出 `4 7 16`、`7 4 9 16`、`-1`。

`pb` 均摊 $O(1)$ 的原因：容量不够时 `vector` 申请两倍大的空间并整体搬过去，$n$ 次插入总共搬运 $1 + 2 + 4 + \dots < 2n$ 次。

### 3.2 string

字符串类，可以看作 `vector<char>` 加上字符串专用操作（`+`、`substr`、`find` 等）。详见《字符串基础》。

### 3.3 stack：栈

后进先出（LIFO），只能操作栈顶：`push(x)`、`pop()`、`top()`、`empty()`、`size()`，全部 $O(1)$。

用途：括号匹配、表达式求值、单调栈、手写递归。例：判断括号串是否合法。

```cpp
string s;
stack<char> st;

void solve() {
    cin >> s;
    for (char c : s) {
        if (c == '(' || c == '[') {
            st.push(c);
            continue;
        }
        char need = c == ')' ? '(' : '[';
        if (st.empty() || st.top() != need) {
            cout << "No" << endl;
            return;
        }
        st.pop();
    }
    cout << (st.empty() ? "Yes" : "No") << endl;
}
```

`([]())` 输出 `Yes`，`([)]` 输出 `No`。遇到右括号时必须先判断栈**非空**再取 `top()`，空栈 `top()`/`pop()` 会直接 RE。

### 3.4 queue：队列

先进先出（FIFO）：`push(x)` 从队尾进，`pop()` 从队头出，`front()` 取队头，`back()` 取队尾，全部 $O(1)$。

用途：BFS、按顺序处理的模拟。例：约瑟夫问题，$n$ 人围成一圈，从 1 开始报数，报到 $m$ 的出圈，输出出圈顺序。把圈看成队列：报数没到 $m$ 的人从队头移到队尾。

```cpp
int n, m;
queue<int> q;

void solve() {
    cin >> n >> m;
    For(i, 1, n) q.push(i);
    while (!q.empty()) {
        For(i, 1, m - 1) q.push(q.front()), q.pop();
        cout << q.front() << " ";
        q.pop();
    }
    cout << endl;
}
```

$n = 10, m = 3$ 输出 `3 6 9 2 7 1 8 5 10 4`。复杂度 $O(nm)$。

`queue` 没有 `clear()`，多组数据清空写 `while (!q.empty()) q.pop();` 或 `q = queue<int>();`。

### 3.5 deque：双端队列

两端都能 $O(1)$ 插入删除：`push_front`、`push_back`、`pop_front`、`pop_back`、`front`、`back`，还支持下标访问。

最典型的用途是**单调队列**（详见数据结构部分）和 0-1 BFS。例：长度为 $n$ 的序列，求每个长度为 $k$ 的窗口的最大值。队列里存下标，保持对应的值从队头到队尾递减：

```cpp
const int N = 1e6 + 5;
int n, k;
int a[N];
deque<int> q;

void solve() {
    cin >> n >> k;
    For(i, 1, n) cin >> a[i];
    For(i, 1, n) {
        while (!q.empty() && a[q.back()] <= a[i]) q.pop_back();
        q.pb(i);
        if (q.front() <= i - k) q.pop_front();
        if (i >= k) cout << a[q.front()] << " ";
    }
    cout << endl;
}
```

输入 `8 3` 和 `1 3 -1 -3 5 3 6 7`，输出 `3 3 5 5 6 7`。每个下标进出队各一次，$O(n)$。

`deque` 常数比 `vector` 大，只需要尾部操作时用 `vector`。

### 3.6 priority_queue：优先队列（堆）

每次取出"最大"的元素：`push(x)` $O(\log n)$，`top()` $O(1)$，`pop()` $O(\log n)$。

- 默认是**大根堆**，`top()` 是最大值。
- 小根堆：`priority_queue<int, vector<int>, greater<int>> q;`，或者把数取负放进大根堆。
- 存 `pair` 时先比 `F` 再比 `S`，Dijkstra 中用 `priority_queue<pii, vector<pii>, greater<pii>>` 存 `{距离, 点}`。
- 存结构体需要重载 `<`。堆顶是按 `<` 意义下"最大"的，想让 `d` 小的在堆顶，就把 `<` 定义成 `d > o.d`。

例：合并果子，每次合并最小的两堆，代价为两堆之和，求最小总代价（贪心，哈夫曼思想）。

```cpp
int n, ans;
priority_queue<int, vector<int>, greater<int>> q;
struct node {
    int d, u;
    bool operator<(const node &o) const { return d > o.d; }
};
priority_queue<node> h;

void solve() {
    cin >> n;
    For(i, 1, n) {
        int x;
        cin >> x;
        q.push(x);
    }
    while (q.size() > 1) {
        int a = q.top();
        q.pop();
        int b = q.top();
        q.pop();
        ans += a + b, q.push(a + b);
    }
    cout << ans << endl;
    h.push({5, 1}), h.push({2, 2}), h.push({7, 3});
    cout << h.top().u << endl;
}
```

输入 `3` 和 `1 2 9`，输出 `15`（先合并 1、2 代价 3，再合并 3、9 代价 12）。后面的结构体堆演示了反向重载，输出 `2`（$d$ 最小的是 2 号）。

### 3.7 set / multiset：有序集合

内部是平衡二叉搜索树，元素**自动从小到大排序**。`set` 自动去重，`multiset` 允许重复。

| 操作 | 作用 | 复杂度 |
| --- | --- | --- |
| `s.insert(x)` | 插入 | $O(\log n)$ |
| `s.erase(x)` | 删除**所有**等于 $x$ 的元素 | $O(\log n + \text{个数})$ |
| `s.erase(it)` | 删除迭代器指向的那一个 | 均摊 $O(1)$ |
| `s.count(x)`、`s.find(x)` | 个数 / 查找（找不到返回 `s.end()`） | $O(\log n)$ |
| `s.lower_bound(x)` | 第一个 $\ge x$ 的元素 | $O(\log n)$ |
| `s.upper_bound(x)` | 第一个 $> x$ 的元素 | $O(\log n)$ |
| `*s.begin()`、`*s.rbegin()` | 最小值 / 最大值 | $O(1)$ |

例：维护一个可重集合，支持插入、删除一个、查询 $x$ 的前驱（$< x$ 的最大值）和后继（$\ge x$ 的最小值）。

```cpp
int q;
multiset<int> s;

void solve() {
    cin >> q;
    while (q--) {
        int op, x;
        cin >> op >> x;
        if (op == 1) s.insert(x);
        else if (op == 2) s.erase(s.find(x));
        else {
            auto it = s.lower_bound(x);
            if (it == s.begin()) cout << "none ";
            else cout << *prev(it) << " ";
            if (it == s.end()) cout << "none" << endl;
            else cout << *it << endl;
        }
    }
}
```

输入

```text
7
1 5
1 5
1 9
3 6
2 5
3 5
3 10
```

输出 `5 9`、`none 5`、`9 none`（删掉一个 5 后集合里剩下 5 和 9）。

要点：

- `multiset` 删一个要写 `s.erase(s.find(x))`（先确认存在）；`s.erase(x)` 会把所有 $x$ 都删掉。
- `prev(it)`、`next(it)` 得到前一个、后一个迭代器。对 `s.begin()` 取 `prev` 或对 `s.end()` 解引用都是错误的，先判断。
- 必须用成员函数 `s.lower_bound(x)`。写成 `lower_bound(s.begin(), s.end(), x)` 虽然结果正确，但 `set` 迭代器不能随机跳转，复杂度退化为 $O(n)$。
- `set` 不能用下标访问第 $k$ 个元素。

### 3.8 map：有序映射

存"键 → 值"对，按键从小到大排序，内部也是平衡树，单次操作 $O(\log n)$。键可以是 `int`、`string`、`pair` 等任何能比较大小的类型。

- `mp[k]`：访问键 $k$ 的值。**若 $k$ 不存在，会先插入 `{k, 0}`**。
- `mp.count(k)`：判断是否存在（结果为 0 或 1），不会插入。
- `mp.find(k)`：找不到返回 `mp.end()`。
- 遍历：`for (auto p : mp)` 按键升序得到每个 `pair`，`p.F` 是键，`p.S` 是值。
- `mp.erase(k)` 删除。

```cpp
int n;
map<string, int> mp;

void solve() {
    cin >> n;
    For(i, 1, n) {
        string s;
        cin >> s;
        mp[s]++;
    }
    for (auto p : mp) cout << p.F << " " << p.S << endl;
    cout << mp.count("dog") << " " << mp.size() << endl;
    if (mp["dog"] == 0) cout << mp.size() << endl;
}
```

输入 `5` 和 `bob amy bob cat amy`，输出 `amy 2`、`bob 2`、`cat 1`，然后 `0 3`，最后一行是 `4`：`mp["dog"]` 把 `dog` 插了进去。

所以判断存在一律用 `count` / `find`，不要用 `mp[k]`。值域很大（如 $10^9$）但出现的值不多时，`map` 可以当作"稀疏数组"使用。

### 3.9 unordered_map / unordered_set：哈希表

用法和 `map` / `set` 几乎一样，但内部是哈希表：**不排序**，单次操作**平均** $O(1)$。

- 只需要"查找是否存在 / 计数"、不关心顺序时，可以用它代替 `map` 提速。
- 常数比数组大得多；键是 `pair` 时没有默认哈希函数，不能直接用。
- 特定数据可以让大量键冲突，退化成 $O(n)$。CSP 数据一般不会刻意构造，但如果 `unordered_map` 反而变慢，就换回 `map` 或排序 + 二分。
- 值域不大（$\le 10^7$）时，直接开数组最快。

例：给定 $n$ 个数和 $c$，求满足 $a_i - a_j = c$ 的有序对 $(i, j)$ 个数。对每个 $a_i$，找有多少个 $a_j = a_i - c$：

```cpp
const int N = 2e5 + 5;
int n, c, ans;
int a[N];
unordered_map<int, int> cnt;

void solve() {
    cin >> n >> c;
    For(i, 1, n) cin >> a[i], cnt[a[i]]++;
    For(i, 1, n) if (cnt.count(a[i] - c)) ans += cnt[a[i] - c];
    cout << ans << endl;
}
```

输入 `4 1` 和 `1 1 2 3`，输出 `3`。$O(n)$ 平均。

### 3.10 pair

`pair<A, B>` 把两个值打包，`p.F`、`p.S` 访问，`{x, y}` 或 `make_pair(x, y)` 构造。比较规则是**字典序**：先比 `F`，相等再比 `S`。所以 `pair` 数组直接 `sort` 就是"第一关键字升序、第二关键字升序"。

```cpp
const int N = 105;
int n;
pii p[N];

void solve() {
    cin >> n;
    For(i, 1, n) cin >> p[i].F >> p[i].S;
    sort(p + 1, p + 1 + n);
    For(i, 1, n) cout << "(" << p[i].F << "," << p[i].S << ") ";
    cout << endl;
    pii a = {3, 1}, b = {2, 9};
    cout << (a < b) << " " << max(a, b).S << endl;
}
```

输入 `3` 和 `2 5 1 7 2 3`，输出 `(1,7) (2,3) (2,5)`，然后 `0 1`。

## 4. 常用算法

以下函数都在 `<algorithm>` 中（`accumulate` 在 `<numeric>`），参数都是左闭右开区间。

### 4.1 sort 与相关

- `sort(a + 1, a + 1 + n)`：升序，$O(n \log n)$。
- 降序：`sort(a + 1, a + 1 + n, greater<int>())`，或自定义 `cmp`。
- `stable_sort`：相等元素保持原来的相对顺序。
- `reverse(a + 1, a + 1 + n)`：翻转，$O(n)$。
- `nth_element(a + 1, a + k, a + 1 + n)`：把第 $k$ 小放到位置 $k$，左边都不大于它、右边都不小于它，平均 $O(n)$。

### 4.2 二分查找：lower_bound / upper_bound

在**已排序**区间上二分，$O(\log n)$：

- `lower_bound(a + 1, a + 1 + n, x)`：第一个 $\ge x$ 的位置；
- `upper_bound(a + 1, a + 1 + n, x)`：第一个 $> x$ 的位置；
- `binary_search(...)`：是否存在 $x$。

返回的是指针（迭代器），减去 `a` 就得到下标；找不到时返回 `a + 1 + n`（即下标 $n+1$）。由此：

- 等于 $x$ 的个数 = `upper_bound - lower_bound`；
- $< x$ 的个数 = `lower_bound(...) - (a + 1)`；
- $\le x$ 的最后一个元素位置 = `upper_bound(...) - a - 1`。

### 4.3 unique 与离散化

`unique` 把**相邻**的重复元素移到后面，返回去重后的末尾位置。所以先排序再 `unique` 才能完全去重。

**离散化**：把值域很大的数映射为它在所有不同值中的排名（$1 \sim m$），之后就能用数组下标处理。

```cpp
const int N = 1e5 + 5;
int n, m;
int a[N], b[N];

void solve() {
    cin >> n;
    For(i, 1, n) cin >> a[i], b[i] = a[i];
    sort(b + 1, b + 1 + n);
    m = unique(b + 1, b + 1 + n) - b - 1;
    For(i, 1, n) cout << lower_bound(b + 1, b + 1 + m, a[i]) - b << " ";
    cout << endl;
    cout << m << " " << upper_bound(b + 1, b + 1 + m, 100) - b - 1 << endl;
    cout << binary_search(b + 1, b + 1 + m, 7) << endl;
}
```

输入 `6` 和 `1000000000 7 -5 7 300 1000000000`，`b` 去重后为 `-5 7 300 1000000000`，$m = 4$。输出 `4 2 1 2 3 4`、`4 2`（$\le 100$ 的有 2 个）、`1`。

`vector` 的写法：`sort(v.begin(), v.end()); v.erase(unique(v.begin(), v.end()), v.end());`。

### 4.4 next_permutation

把区间变成字典序的**下一个**排列，已经是最后一个排列时返回 `false`（并变回第一个）。从升序开始配合 `do-while` 可以枚举全部排列，可重元素也只枚举不同的排列：

```cpp
int a[5] = {0, 1, 2, 2};

void solve() {
    do {
        For(i, 1, 3) cout << a[i];
        cout << " ";
    } while (next_permutation(a + 1, a + 4));
    cout << endl;
}
```

输出 `122 212 221`。`prev_permutation` 方向相反。枚举全部 $n!$ 个排列只适合 $n \le 10$ 左右。

### 4.5 其他常用函数

```cpp
const int N = 15;
int n;
int a[N];

void solve() {
    cin >> n;
    For(i, 1, n) cin >> a[i];
    int mx = *max_element(a + 1, a + 1 + n);
    int pos = min_element(a + 1, a + 1 + n) - a;
    int sum = accumulate(a + 1, a + 1 + n, 0LL);
    cout << mx << " " << pos << " " << sum << " " << count(a + 1, a + 1 + n, 3) << endl;
    reverse(a + 1, a + 1 + n);
    fill(a + 1, a + 3, 0);
    For(i, 1, n) cout << a[i] << " ";
    cout << endl;
}
```

输入 `5` 和 `3 1 4 1 5`，输出 `5 2 14 1`（最小值第一次出现在下标 2，3 出现 1 次）和 `0 0 4 1 3`。

- `max_element` / `min_element` 返回位置，`*` 取值，减 `a` 得下标，$O(n)$。
- `accumulate` 的返回类型由**初值**决定：写 `0` 就按 32 位累加会溢出，要写 `0LL`。
- `count(l, r, x)` 计数，$O(n)$；`fill(l, r, x)` 填充，$O(n)$。
- `swap(a, b)` 交换任意两个同类型变量（包括两个容器，$O(1)$）。

## 5. 复杂度总表

| 容器 / 函数 | 主要操作 | 复杂度 |
| --- | --- | --- |
| `vector` | 尾部增删、下标访问 | $O(1)$（均摊） |
| `vector` | 中间插入删除 | $O(n)$ |
| `stack` / `queue` / `deque` | 两端操作 | $O(1)$ |
| `priority_queue` | `push` / `pop` / `top` | $O(\log n)$ / $O(\log n)$ / $O(1)$ |
| `set` / `map` 及 `multi` 版本 | 增删查、`lower_bound` | $O(\log n)$ |
| `unordered_set` / `unordered_map` | 增删查 | 平均 $O(1)$ |
| `sort` / `stable_sort` | 排序 | $O(n \log n)$ |
| `lower_bound` / `upper_bound` | 有序数组二分 | $O(\log n)$ |
| `unique` / `reverse` / `fill` / `count` / `max_element` | 扫描 | $O(n)$ |
| `next_permutation` | 下一个排列 | 均摊 $O(1)$，最坏 $O(n)$ |

`set`、`map` 虽然是 $O(\log n)$，但常数较大，$10^6$ 次操作大约需要几百毫秒；能用排序 + 数组解决时优先用数组。

## 6. 常见题型与技巧

- **选容器**：要按顺序处理用 `queue`；后来的先处理用 `stack`；反复取最值用 `priority_queue`；要有序 + 动态插删 + 找前驱后继用 `set`；"键 → 值"统计用 `map`（键少或值域小时用数组）。
- **去重计数**：放进 `set` 后看 `size()`（[CSP-J 2024 T1 扑克牌](#/P11227)）；或排序 + `unique`。
- **离散化**：排序 + `unique` + `lower_bound`，把大值域映射到 $1 \sim m$。
- **贪心取最值**：每次取最小的两个合并（合并果子）、维护"当前可用的资源"（[CSP-S 2021 T1 廊桥分配](#/P7913)）。
- **字符串作键**：`map<string, int>` 给字符串编号或计数（[CSP-J 2021 T3 网络连接](#/P7911)）。
- **两端操作的模拟**：`deque`（[CSP-S 2020 T4 贪吃蛇](#/P7078)）。
- **多关键字**：用 `pair` 或 `pair<int, pii>` 代替结构体，直接比较、排序、放进 `set`。

## 7. 易错点

- 对空容器调用 `top()`、`front()`、`pop()`、`*s.begin()`：RE。
- `mp[k]` 判断存在时意外插入，导致 `size()` 变大、遍历多出元素。
- `multiset` 用 `s.erase(x)` 想删一个，结果全删了。
- 对 `set` 使用全局的 `lower_bound(s.begin(), s.end(), x)`，复杂度 $O(n)$。
- `unique` 前没排序；忘记 `unique` 返回的是新的末尾，后面仍然用 $n$。
- `lower_bound` 用在无序数组上；返回值减错基址（1-indexed 时应减 `a`）。
- `v.size() - 1` 无符号下溢；`accumulate` 初值写 `0` 溢出。
- 遍历 `set`/`map` 时直接 `erase(it)` 后再 `it++`：迭代器已失效，应写 `it = s.erase(it);`。
- 在循环中 `v.insert(v.begin(), x)`、`v.erase(v.begin())`，每次 $O(n)$，整体 $O(n^2)$。
- 多组数据忘记清空全局容器（`clear()`；`queue`、`stack`、`priority_queue` 没有 `clear`，重新赋值为空）。
- 大量小 `vector`（如 $10^6$ 个）本身也占不少内存，每个空 `vector` 约 24 字节。

## 8. 练习

**本站真题**

- [CSP-J 2024 T1 扑克牌](#/P11227)：用 `set<string>` 去重，答案为 52 减去集合大小。
- [CSP-J 2021 T3 网络连接](#/P7911)：`map<string, int>` 记录"地址 → 服务机编号"。
- [CSP-J 2019 T2 公交换乘](#/P5661)：优惠券按时间先后进出，用队列思想维护。
- [CSP-S 2021 T1 廊桥分配](#/P7913)：两个优先队列模拟"空闲廊桥"和"占用中的廊桥"。
- [CSP-S 2020 T4 贪吃蛇](#/P7078)：每次取最大最小值，用双端队列维护有序序列。
- [CSP-S 2025 T3 谐音替换](#/P14363)：以字符串为键的哈希表给二元组分组。

**洛谷经典题**

- [P1059 [NOIP2006 普及组] 明明的随机数](https://www.luogu.com.cn/problem/P1059)
- [P1996 约瑟夫问题](https://www.luogu.com.cn/problem/P1996)
- [P1540 [NOIP2010 提高组] 机器翻译](https://www.luogu.com.cn/problem/P1540)
- [P3378 【模板】堆](https://www.luogu.com.cn/problem/P3378)
- [P1088 [NOIP2004 普及组] 火星人](https://www.luogu.com.cn/problem/P1088)
- [P1102 A-B 数对](https://www.luogu.com.cn/problem/P1102)
