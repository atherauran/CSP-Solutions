# 线段树

**组别**：S　**关键词**：线段树、懒标记、区间修改、区间乘加、最大子段和、线段树上二分、动态开点、权值线段树

## 1. 是什么 / 解决什么问题

给一个序列，要反复做两类操作：修改（改一个点，或者给一段区间统一加/乘/赋值），查询（一段区间的和、最大值、最大子段和……）。

- 前缀和：查询 $O(1)$，但不支持修改。
- 《ST 表》：区间最值 $O(1)$，同样不支持修改。
- 《树状数组》：单点修改 + 前缀查询 $O(\log n)$，代码短；但只能维护"可减"的信息，区间最值、区间乘这类就做不了。

**线段树**把序列递归地对半分，每个结点存一段区间的汇总信息。只要信息满足**结合律**（左半段的答案和右半段的答案能拼出整段的答案），就能做到修改、查询都是 $O(\log n)$；配合**懒标记**，区间修改也是 $O(\log n)$。

它是 CSP-S 中适用面最广的数据结构：代码比树状数组长，但几乎所有"区间修改 + 区间查询"的问题都能套上去。

## 2. 核心原理

### 2.1 结构

根结点管整个区间 $[1, n]$。结点管 $[l, r]$ 时，令 $mid = \lfloor (l + r) / 2 \rfloor$，左儿子管 $[l, mid]$，右儿子管 $[mid + 1, r]$，直到 $l = r$（叶子，对应一个元素）。

用数组存这棵树：根编号为 1，结点 $p$ 的左儿子是 $2p$，右儿子是 $2p + 1$（和堆一样）。$n = 6$ 时：

```text
                  1:[1,6]
             /              \
        2:[1,3]            3:[4,6]
        /     \            /     \
    4:[1,2]  5:[3,3]   6:[4,5]  7:[6,6]
    /    \             /    \
8:[1,1] 9:[2,2]   12:[4,4] 13:[5,5]
```

编号 10、11 没有用到——$n$ 不是 2 的幂时编号会有空洞。树高是 $\lceil \log_2 n \rceil + 1$，最大编号小于 $2^{\lceil \log_2 n \rceil + 1} < 4n$，所以**数组开 $4n$**。

每个结点的信息由两个儿子合并而来，这一步通常叫 `pushup`。以区间和为例：$t_p = t_{2p} + t_{2p+1}$。建树就是递归到叶子赋初值，回溯时 `pushup`，共 $2n - 1$ 个结点，$O(n)$。

### 2.2 区间查询

查询 $[ql, qr]$ 时从根往下递归：

- 当前结点区间被 $[ql, qr]$ **完全包含**：直接返回它存的信息，不再往下走。
- 否则把查询分给和它有交集的儿子，再合并结果。

在上图中查询 $[2, 5]$：

```text
[1,6] 部分相交 → 左 [1,3]、右 [4,6]
  [1,3] 部分相交 → 左 [1,2]、右 [3,3]
    [1,2] 部分相交 → 只走右儿子 [2,2]  ✓ 完全包含
    [3,3] ✓ 完全包含
  [4,6] 部分相交 → 只走左儿子 [4,5]  ✓ 完全包含
答案 = t[9] + t[5] + t[6]
```

**为什么是 $O(\log n)$**：同一层的结点区间互不相交、依次排列。在某一层"部分相交"（需要继续往下走）的结点，一定包含 $ql$ 或 $qr$ 这两个边界之一——夹在中间的结点会被完全包含而直接返回。所以每层最多 2 个结点往下走，每层访问的结点不超过 4 个，总共 $O(\log n)$ 个。

### 2.3 单点修改

修改 $a_x$ 只影响从根到叶子 $[x, x]$ 这条路径上的结点：递归走到叶子改掉，回溯时逐个 `pushup`。路径长度就是树高，$O(\log n)$。

### 2.4 懒标记

区间修改如果把每个受影响的叶子都改一遍，一次就是 $O(n)$。思路和查询一样：修改 $[ql, qr]$ 时，遇到被完全包含的结点就**只改这个结点自己**，并在它身上打一个标记，记下"我的整个子树还欠着这次修改没往下传"。只有以后真的要访问它的儿子时，才把标记**下传**（`pushdown`）给两个儿子。

约定：**标记已经作用在本结点的信息上，只是还没作用到儿子**。这样"完全包含就直接返回"时，返回的值总是正确的。

例：$a = [1, 2, 3, 4, 5, 6]$，给 $[1, 3]$ 加 3。

```text
[1,6] 部分相交，下去
  [1,3] 完全包含：t[2] = 6 + 3×3 = 15，tag[2] = 3，返回
回溯：t[1] = 15 + 15 = 30
```

结点 4、5、8、9 都还是旧值。之后查询 $[2, 2]$ 要经过结点 2，在进入儿子之前先 `pushdown(2)`：$t_4 \mathrel{+}= 3 \times 2$，$t_5 \mathrel{+}= 3 \times 1$，两个儿子的 tag 都加 3，结点 2 的 tag 清零。再往下到结点 4 时同理下传给 8、9。

每次修改/查询仍然只访问 $O(\log n)$ 个结点，下传也只在这些结点上发生，所以区间修改是 $O(\log n)$。

### 2.5 能维护什么

两个条件：

1. **信息可合并**：知道左右两段的信息，能 $O(1)$ 算出整段的信息（和、最值、最大子段和、颜色段数……）。
2. **标记可作用、可叠加**（只在区间修改时需要）：知道一段的信息和一个标记，能 $O(1)$ 算出修改后的信息（区间加对区间和：加上 $v \times$ 长度）；两个标记先后作用能合成一个标记（加 3 再加 5 等于加 8）。

不满足 2 的例子：区间开根号、区间取模——标记无法 $O(1)$ 作用到"区间和"上，只能用其他技巧（如"每个数开几次根就变成 1，暴力改到叶子，全是 1 的区间跳过"）。

## 3. 代码模板

下面的函数参数统一为 `(p, l, r, ...)`：`p` 是结点编号，`[l, r]` 是它管的区间。区间不存在结点里，而是递归时算出来，省空间。

### 3.1 单点修改，区间查询

操作 `1 x k`：$a_x \mathrel{+}= k$；操作 `2 x y`：求 $\sum_{i=x}^{y} a_i$。

```cpp
const int N = 5e5 + 5;
int n, m;
int a[N], t[N << 2];

void pushup(int p) { t[p] = t[p << 1] + t[p << 1 | 1]; }

void build(int p, int l, int r) {
    if (l == r) {
        t[p] = a[l];
        return;
    }
    int mid = (l + r) >> 1;
    build(p << 1, l, mid), build(p << 1 | 1, mid + 1, r);
    pushup(p);
}

void update(int p, int l, int r, int x, int v) {
    if (l == r) {
        t[p] += v;
        return;
    }
    int mid = (l + r) >> 1;
    if (x <= mid) update(p << 1, l, mid, x, v);
    else update(p << 1 | 1, mid + 1, r, x, v);
    pushup(p);
}

int query(int p, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return t[p];
    int mid = (l + r) >> 1, s = 0;
    if (ql <= mid) s += query(p << 1, l, mid, ql, qr);
    if (qr > mid) s += query(p << 1 | 1, mid + 1, r, ql, qr);
    return s;
}

void solve() {
    cin >> n >> m;
    For(i, 1, n) cin >> a[i];
    build(1, 1, n);
    while (m--) {
        int op, x, y;
        cin >> op >> x >> y;
        if (op == 1) update(1, 1, n, x, y);
        else cout << query(1, 1, n, x, y) << endl;
    }
}
```

`p << 1 | 1` 就是 $2p + 1$（$2p$ 最低位是 0，或上 1 等于加 1）。`ql <= mid` 表示查询区间和左儿子 $[l, mid]$ 有交，`qr > mid` 表示和右儿子有交。

改成区间最大值：`pushup` 里的 `+` 换成 `max`，`query` 里 `s` 初值设成 `-LINF`、累加换成取 `max` 即可。

### 3.2 区间加，区间求和（懒标记）

操作 `1 x y k`：$[x, y]$ 每个数加 $k$；操作 `2 x y`：求区间和。

```cpp
const int N = 1e5 + 5;
int n, m;
int a[N], t[N << 2], tag[N << 2];

void pushup(int p) { t[p] = t[p << 1] + t[p << 1 | 1]; }

void apply(int p, int l, int r, int v) {
    t[p] += v * (r - l + 1);
    tag[p] += v;
}

void pushdown(int p, int l, int r) {
    if (!tag[p]) return;
    int mid = (l + r) >> 1;
    apply(p << 1, l, mid, tag[p]), apply(p << 1 | 1, mid + 1, r, tag[p]);
    tag[p] = 0;
}

void build(int p, int l, int r) {
    if (l == r) {
        t[p] = a[l];
        return;
    }
    int mid = (l + r) >> 1;
    build(p << 1, l, mid), build(p << 1 | 1, mid + 1, r);
    pushup(p);
}

void update(int p, int l, int r, int ql, int qr, int v) {
    if (ql <= l && r <= qr) {
        apply(p, l, r, v);
        return;
    }
    pushdown(p, l, r);
    int mid = (l + r) >> 1;
    if (ql <= mid) update(p << 1, l, mid, ql, qr, v);
    if (qr > mid) update(p << 1 | 1, mid + 1, r, ql, qr, v);
    pushup(p);
}

int query(int p, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return t[p];
    pushdown(p, l, r);
    int mid = (l + r) >> 1, s = 0;
    if (ql <= mid) s += query(p << 1, l, mid, ql, qr);
    if (qr > mid) s += query(p << 1 | 1, mid + 1, r, ql, qr);
    return s;
}

void solve() {
    cin >> n >> m;
    For(i, 1, n) cin >> a[i];
    build(1, 1, n);
    while (m--) {
        int op, x, y, k;
        cin >> op >> x >> y;
        if (op == 1) cin >> k, update(1, 1, n, x, y, k);
        else cout << query(1, 1, n, x, y) << endl;
    }
}
```

`apply` 把"给整个结点加 $v$"这件事一次做完：改信息、叠标记。`pushdown` 就是对两个儿子各 `apply` 一次。把这两步写成函数，换成别的修改时只需要改 `apply`。

要点：**往下走之前 `pushdown`，回来之后 `pushup`**。`update` 两者都要，`query` 只需要 `pushdown`（不改值，不用 `pushup`）。

### 3.3 区间乘、区间加（标记顺序）

操作 `1 x y k`：区间乘 $k$；`2 x y k`：区间加 $k$；`3 x y`：区间和，全部对 $mod$ 取模。

现在一个结点身上同时有乘标记 $mul$ 和加标记 $add$，要规定它们的含义和先后顺序。规定为**先乘后加**：子树中每个数 $x$ 都要变成 $x \cdot mul + add$。

再来一个新修改"乘 $k$ 加 $b$"（区间乘是 $k$ 任意、$b = 0$；区间加是 $k = 1$、$b$ 任意）：

$$(x \cdot mul + add) \cdot k + b = x \cdot (mul \cdot k) + (add \cdot k + b)$$

所以新标记是 $mul' = mul \cdot k$，$add' = add \cdot k + b$——**旧的加标记也要乘 $k$**。区间和的变化：$sum' = sum \cdot k + b \cdot len$。

如果规定成"先加后乘" $(x + add) \cdot mul$，再叠一次"加 $b$"就要 $add \mathrel{+}= b / mul$，出现除法，整数和取模下都做不了。所以统一用先乘后加。

```cpp
const int N = 1e5 + 5;
int n, m, mod;
int a[N], t[N << 2], mul[N << 2], add[N << 2];

void pushup(int p) { t[p] = (t[p << 1] + t[p << 1 | 1]) % mod; }

void apply(int p, int l, int r, int k, int b) {
    t[p] = (t[p] * k + b * (r - l + 1)) % mod;
    mul[p] = mul[p] * k % mod;
    add[p] = (add[p] * k + b) % mod;
}

void pushdown(int p, int l, int r) {
    int mid = (l + r) >> 1;
    apply(p << 1, l, mid, mul[p], add[p]), apply(p << 1 | 1, mid + 1, r, mul[p], add[p]);
    mul[p] = 1, add[p] = 0;
}

void build(int p, int l, int r) {
    mul[p] = 1;
    if (l == r) {
        t[p] = a[l] % mod;
        return;
    }
    int mid = (l + r) >> 1;
    build(p << 1, l, mid), build(p << 1 | 1, mid + 1, r);
    pushup(p);
}

void update(int p, int l, int r, int ql, int qr, int k, int b) {
    if (ql <= l && r <= qr) {
        apply(p, l, r, k, b);
        return;
    }
    pushdown(p, l, r);
    int mid = (l + r) >> 1;
    if (ql <= mid) update(p << 1, l, mid, ql, qr, k, b);
    if (qr > mid) update(p << 1 | 1, mid + 1, r, ql, qr, k, b);
    pushup(p);
}

int query(int p, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return t[p];
    pushdown(p, l, r);
    int mid = (l + r) >> 1, s = 0;
    if (ql <= mid) s += query(p << 1, l, mid, ql, qr);
    if (qr > mid) s += query(p << 1 | 1, mid + 1, r, ql, qr);
    return s % mod;
}

void solve() {
    cin >> n >> m >> mod;
    For(i, 1, n) cin >> a[i];
    build(1, 1, n);
    while (m--) {
        int op, x, y, k;
        cin >> op >> x >> y;
        if (op == 1) cin >> k, update(1, 1, n, x, y, k, 0);
        else if (op == 2) cin >> k, update(1, 1, n, x, y, 1, k);
        else cout << query(1, 1, n, x, y) << endl;
    }
}
```

乘标记的"空值"是 1 不是 0，`build` 时要把每个结点的 `mul` 置 1。

**同样的套路处理其他标记组合**：写出"一个数在标记作用下变成什么"，再推两个标记的复合。

- **区间赋值 + 区间加**：标记 $(set, add)$ 表示"先赋值为 $set$（若有），再加 $add$"。新来赋值 $v$：$set = v$，$add = 0$（之前的加全被覆盖）；新来加 $b$：$add \mathrel{+}= b$。下传时先传赋值再传加。
- **区间加 + 区间平方和**：同时维护 $s_1 = \sum x$ 和 $s_2 = \sum x^2$。加 $v$ 时 $s_2' = s_2 + 2v \cdot s_1 + v^2 \cdot len$，必须**先用旧的 $s_1$ 更新 $s_2$**，再更新 $s_1$。方差 $= s_2 / len - (s_1 / len)^2$。
- **01 序列区间取反 + 数 1 的个数**：取反后 $cnt' = len - cnt$，标记用异或叠加（取反两次等于没变）。

## 4. 合并技巧与进阶

### 4.1 区间最大子段和

单点修改，询问 $[l, r]$ 内和最大的非空连续子段（例题：小白逛公园，询问时 $l > r$ 要交换）。

只存"区间最大子段和"无法合并：整段的最优子段可能**跨过中点**，由左段的一个后缀和右段的一个前缀拼成。所以每个结点存 4 个值：

| 字段 | 含义 | 合并（左 $x$、右 $y$） |
| --- | --- | --- |
| $sum$ | 区间和 | $x.sum + y.sum$ |
| $lm$ | 最大前缀和 | $\max(x.lm,\ x.sum + y.lm)$ |
| $rm$ | 最大后缀和 | $\max(y.rm,\ y.sum + x.rm)$ |
| $mx$ | 最大子段和 | $\max(x.mx,\ y.mx,\ x.rm + y.lm)$ |

最大前缀要么完全在左段，要么包含整个左段再加上右段的一个前缀；最大子段要么在左段、要么在右段、要么跨中点。

```cpp
const int N = 5e5 + 5;
int n, m;
int a[N];
struct node { int sum, lm, rm, mx; } t[N << 2];

node merge(const node &x, const node &y) {
    node z;
    z.sum = x.sum + y.sum;
    z.lm = max(x.lm, x.sum + y.lm);
    z.rm = max(y.rm, y.sum + x.rm);
    z.mx = max(max(x.mx, y.mx), x.rm + y.lm);
    return z;
}

void build(int p, int l, int r) {
    if (l == r) {
        t[p] = {a[l], a[l], a[l], a[l]};
        return;
    }
    int mid = (l + r) >> 1;
    build(p << 1, l, mid), build(p << 1 | 1, mid + 1, r);
    t[p] = merge(t[p << 1], t[p << 1 | 1]);
}

void update(int p, int l, int r, int x, int v) {
    if (l == r) {
        t[p] = {v, v, v, v};
        return;
    }
    int mid = (l + r) >> 1;
    if (x <= mid) update(p << 1, l, mid, x, v);
    else update(p << 1 | 1, mid + 1, r, x, v);
    t[p] = merge(t[p << 1], t[p << 1 | 1]);
}

node query(int p, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return t[p];
    int mid = (l + r) >> 1;
    if (qr <= mid) return query(p << 1, l, mid, ql, qr);
    if (ql > mid) return query(p << 1 | 1, mid + 1, r, ql, qr);
    return merge(query(p << 1, l, mid, ql, qr), query(p << 1 | 1, mid + 1, r, ql, qr));
}

void solve() {
    cin >> n >> m;
    For(i, 1, n) cin >> a[i];
    build(1, 1, n);
    while (m--) {
        int op, x, y;
        cin >> op >> x >> y;
        if (op == 1) {
            if (x > y) swap(x, y);
            cout << query(1, 1, n, x, y).mx << endl;
        } else update(1, 1, n, x, y);
    }
}
```

查询返回整个 `node` 而不是一个数，因为拼接时需要 $lm$、$rm$；查询区间只落在一侧时直接返回那一侧，避免和"空结点"合并。

### 4.2 其他常见的合并

思路都一样：**想清楚跨过中点的部分需要左右两段的什么信息，就额外存什么**。

- **最长连续 1（01 序列）**：存最长前缀 1、最长后缀 1、区间内最长连续 1、区间长度。左段全是 1 时，整段的最长前缀 = 左段长度 + 右段最长前缀。
- **颜色段数**：存段数、最左颜色、最右颜色。合并时段数 $= x.c + y.c - [x.rc = y.lc]$（中间两端颜色相同就粘成一段）。
- **最大值及其出现次数**：两边最大值相等时次数相加，否则取较大一边的。
- **区间 gcd + 区间加**：$\gcd(a_l, \dots, a_r) = \gcd(a_l, a_{l+1} - a_l, \dots, a_r - a_{r-1})$，于是在差分数组上维护单点修改 + 区间 gcd，区间加只改差分的两个点，$a_l$ 用另一棵树（或树状数组）求。
- **矩阵**：每个结点存一个矩阵，合并就是矩阵乘法（注意顺序不能交换），用来做带修改的线性递推或"动态 DP"。

### 4.3 线段树上二分

问题：单点修改，询问"从位置 $x$ 开始往右，**第一个** $a_i \ge k$ 的位置"。

朴素做法：二分答案 $r$，查询 $\max(a_x..a_r)$ 是否 $\ge k$，是 $O(\log^2 n)$。更好的做法是直接在线段树上往下走，利用每个结点存的最大值做判断：

- 结点和 $[x, n]$ 无交，或者最大值 $< k$：这里不可能有答案，返回 $-1$。
- 叶子：就是答案。
- 否则先进左儿子找，找不到再进右儿子。

`mx` 是维护区间最大值的线段树（3.1 的代码把 `+` 换成 `max`），询问时调用 `find(1, 1, n, x, k)`，找不到返回 $-1$。

```cpp
int find(int p, int l, int r, int x, int k) {
    if (r < x || mx[p] < k) return -1;
    if (l == r) return l;
    int mid = (l + r) >> 1;
    int res = find(p << 1, l, mid, x, k);
    if (res == -1) res = find(p << 1 | 1, mid + 1, r, x, k);
    return res;
}
```

**为什么是 $O(\log n)$**：$[x, n]$ 在线段树上被拆成 $O(\log n)$ 个完全包含的结点，`find` 从左到右依次试它们，最大值 $< k$ 的立即返回。第一个最大值 $\ge k$ 的结点里一定有答案，从它往下走时，每层最多先试一次左儿子（失败就立即返回）再进右儿子，只走一条路径。

没有起点限制时更简单：从根开始，左儿子满足条件就进左儿子，否则进右儿子，一路走到叶子。下面权值线段树求第 $k$ 小就是这种形式。

### 4.4 动态开点与权值线段树

**权值线段树**以"值"为下标，结点存"值落在这个范围内的数有几个"，能做插入、删除、查第 $k$ 小、查排名（和权值树状数组相同的用途，但更灵活）。

值域到 $10^9$ 时开不了 $4 \times 10^9$ 的数组。离线时可以先《离散化》；如果必须在线，就用**动态开点**：结点不再按 $2p$、$2p + 1$ 编号，而是**用到时才新建**，记录左右儿子的编号 `ls[p]`、`rs[p]`（0 表示还没建，相当于空树）。

一次插入只经过根到叶子的一条路径，最多新建 $\lceil \log_2 V \rceil + 1$ 个结点。$q$ 次操作、值域 $V = 10^9$ 时，结点数不超过约 $31q$。

操作：`1 x` 插入 $x$，`2 x` 删除一个 $x$，`3 k` 查第 $k$ 小（$1 \le x \le 10^9$）。

```cpp
const int N = 1e5 + 5, M = N * 32, V = 1e9;
int q, tot, rt;
int ls[M], rs[M], cnt[M];

void update(int &p, int l, int r, int x, int v) {
    if (!p) p = ++tot;
    cnt[p] += v;
    if (l == r) return;
    int mid = (l + r) >> 1;
    if (x <= mid) update(ls[p], l, mid, x, v);
    else update(rs[p], mid + 1, r, x, v);
}

int kth(int p, int l, int r, int k) {
    if (l == r) return l;
    int mid = (l + r) >> 1;
    if (cnt[ls[p]] >= k) return kth(ls[p], l, mid, k);
    return kth(rs[p], mid + 1, r, k - cnt[ls[p]]);
}

void solve() {
    cin >> q;
    while (q--) {
        int op, x;
        cin >> op >> x;
        if (op == 1) update(rt, 1, V, x, 1);
        else if (op == 2) update(rt, 1, V, x, -1);
        else cout << kth(rt, 1, V, x) << endl;
    }
}
```

`p` 按引用传：新建结点时直接把编号写回父亲的 `ls`/`rs`（或根 `rt`）。空结点编号 0 的 `cnt[0]` 永远是 0，所以访问不存在的儿子也不会出错。

动态开点也是**线段树合并**、**可持久化线段树（主席树）**的基础，它们超出 CSP 常考范围，了解即可。

## 5. 复杂度

| 操作 | 复杂度 |
| --- | --- |
| 建树 | $O(n)$ |
| 单点修改 / 区间查询 / 区间修改（懒标记） | $O(\log n)$ |
| 线段树上二分 | $O(\log n)$ |
| 空间 | 普通 $4n$；动态开点 $O(q \log V)$ |

常数比树状数组大几倍（递归、每层访问多个结点），$n, m$ 在 $10^6$ 级别时要注意。

## 6. 常见题型与技巧

- **模板型**：区间加/乘/赋值 + 区间和/最值，关键是设计标记和推复合顺序。
- **需要特殊合并的信息**：最大子段和、最长连续段、颜色段数——列出"跨中点"需要的量。
- **"第一个满足条件的位置"**：线段树上二分，常和最值、前缀和配合（如"第一个前缀和 $\ge k$ 的位置"）。
- **权值线段树**：第 $k$ 小、排名、"比 $x$ 小的数有几个"，值域大就离散化或动态开点。
- **扫描线**：矩形面积并，把矩形的上下边按 $y$ 排序扫描，线段树维护 $x$ 方向"被覆盖的长度"。
- **DFS 序 / 树上问题**：子树对应 DFS 序上的连续区间，子树修改、子树查询直接变成区间操作。
- **DP 优化**：$f_i = \min_{j \in [i - k, i)} f_j + c_i$ 这类转移，用线段树维护 $f$ 的区间最值；转移区间不单调或带修改时比单调队列更通用。
- **离线 + 排序**：和《树状数组》的离线技巧一样，按一维排序扫描，另一维用线段树。
- **只要区间加 + 区间和**，用《树状数组》更短更快；**静态区间最值**用《ST 表》$O(1)$ 查询。

## 7. 易错点

- 数组开 `N << 2`，不是 `N << 1`。动态开点按 $q \times (\lceil \log_2 V \rceil + 1)$ 估算。
- 有懒标记时，**任何**要访问儿子的地方（修改、查询、线段树上二分）都必须先 `pushdown`；修改后必须 `pushup`。
- `apply` 里区间和要乘**区间长度** $r - l + 1$，不是乘 1。
- 乘标记初值是 1，`build` 时初始化；多组数据时标记也要重置。
- 乘加混合时，旧的 `add` 也要乘 $k$；`apply` 中先用旧值算 `t`，顺序别写反。
- 取模题中 `b * (r - l + 1)` 可能超过 $mod$ 很多倍，乘积要在 64 位范围内（本仓库模板 `int` 是 64 位，$mod \le 10^9$、长度 $\le 10^6$ 时安全）。
- 查询最值时 `s` 的初值要用 `-LINF` / `LINF`，不能用 0（数可能是负的）。
- 递归函数写成 `query(1, 1, n, ...)`：第一个参数是根编号 1，后面才是区间。
- 结构体合并时注意查询区间只在一侧的情况，不要和一个"全 0 的空结点"合并（最大子段和要求非空，空结点会算出错误的 0）。

## 8. 练习

**本站真题**

- [CSP-S 2022 T2 策略游戏](#/P8818)：需要多种静态区间最值（最大、最小、最大负数、最小非负数），题解用 ST 表；也可以每种开一棵线段树，单次 $O(\log n)$ 同样能过。

**洛谷经典题**

- [P3372 【模板】线段树 1](https://www.luogu.com.cn/problem/P3372)
- [P3373 【模板】线段树 2](https://www.luogu.com.cn/problem/P3373)
- [P1531 I Hate It](https://www.luogu.com.cn/problem/P1531)
- [P1198 [JSOI2008] 最大数](https://www.luogu.com.cn/problem/P1198)
- [P4513 小白逛公园](https://www.luogu.com.cn/problem/P4513)
- [P2574 XOR的艺术](https://www.luogu.com.cn/problem/P2574)
- [P1253 扶苏的问题](https://www.luogu.com.cn/problem/P1253)（区间赋值 + 区间加 + 区间最值）
- [P1471 方差](https://www.luogu.com.cn/problem/P1471)
- [P2572 [SCOI2010] 序列操作](https://www.luogu.com.cn/problem/P2572)
