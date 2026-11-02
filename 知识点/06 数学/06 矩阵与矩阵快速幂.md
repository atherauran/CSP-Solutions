# 矩阵与矩阵快速幂

**组别**：S　**关键词**：矩阵乘法、单位矩阵、矩阵快速幂、线性递推、斐波那契、路径计数、广义矩阵乘法

## 1. 是什么 / 解决什么问题

求斐波那契数列第 $10^{18}$ 项（模 $10^9+7$）。按递推一项项算要 $10^{18}$ 步，不可能。但每一步都是"把当前几项做同一个**线性变换**得到下一组"，这个变换可以写成一个**矩阵**，走 $n$ 步就是乘上这个矩阵的 $n$ 次方，而矩阵的 $n$ 次方可以用**快速幂**在 $O(\log n)$ 次矩阵乘法内求出。

适用场景：

- **线性递推**（项数极大、状态很少）：斐波那契、$a_n = a_{n-1} + a_{n-3}$、带常数项、带前缀和的递推；
- **图上路径计数**：恰好走 $k$ 步从 $i$ 到 $j$ 的方案数；
- **广义矩阵乘法**：把"乘、加"换成"加、取 min"，求恰好 $k$ 条边的最短路，以及动态 DP。

## 2. 核心原理

### 2.1 矩阵与矩阵乘法

$p$ 行 $q$ 列的数表叫 $p \times q$ 矩阵。$A$ 是 $p\times q$，$B$ 是 $q \times r$ 时（**$A$ 的列数 = $B$ 的行数**），乘积 $C = AB$ 是 $p \times r$ 矩阵：

$$C_{ij} = \sum_{k=1}^{q} A_{ik} B_{kj}$$

即"$A$ 的第 $i$ 行"与"$B$ 的第 $j$ 列"对应相乘再相加。

$$\begin{pmatrix}1 & 2\\3 & 4\end{pmatrix}\begin{pmatrix}5 & 6\\7 & 8\end{pmatrix} = \begin{pmatrix}1\cdot5+2\cdot7 & 1\cdot6+2\cdot8\\3\cdot5+4\cdot7 & 3\cdot6+4\cdot8\end{pmatrix} = \begin{pmatrix}19 & 22\\43 & 50\end{pmatrix}$$

性质：

- **不满足交换律**：一般 $AB \ne BA$（上例反过来乘得 $\begin{pmatrix}23&34\\31&46\end{pmatrix}$）。
- **满足结合律**：$(AB)C = A(BC)$。两边第 $(i,l)$ 项都等于 $\sum_j\sum_k A_{ik}B_{kj}C_{jl}$，只是求和顺序不同。
- **单位矩阵** $I$：主对角线为 1、其余为 0。$AI = IA = A$，相当于数字里的 1。

结合律是快速幂成立的唯一前提：$A^{13} = A^8 A^4 A^1$ 不管怎么加括号结果都一样。所以数的快速幂代码几乎原样搬过来，把 `r = 1` 换成 `r = I`、乘法换成矩阵乘法即可。

### 2.2 用矩阵表示线性递推：斐波那契

$F_1 = F_2 = 1$，$F_n = F_{n-1} + F_{n-2}$。把相邻两项放进一个列向量：

$$\begin{pmatrix}F_{n}\\F_{n-1}\end{pmatrix} = \begin{pmatrix}1 & 1\\1 & 0\end{pmatrix}\begin{pmatrix}F_{n-1}\\F_{n-2}\end{pmatrix}$$

（第一行：$F_n = 1\cdot F_{n-1} + 1\cdot F_{n-2}$；第二行：$F_{n-1} = 1 \cdot F_{n-1} + 0\cdot F_{n-2}$，只是把旧值搬下来。）记中间的矩阵为 $M$，反复代入：

$$\begin{pmatrix}F_{n}\\F_{n-1}\end{pmatrix} = M^{n-1}\begin{pmatrix}F_{1}\\F_{0}\end{pmatrix} = M^{n-1}\begin{pmatrix}1\\0\end{pmatrix}$$

所以 $F_n$ 就是 $M^{n-1}$ 左上角的元素。$n = 10^{18}$ 时只需约 60 次平方 + 至多 60 次乘法，每次乘法是 $2\times2$ 矩阵，瞬间完成。

### 2.3 构造转移矩阵的一般方法

**第一步：确定状态向量**——递推下一项需要用到哪些量，就把哪些量放进向量。**第二步：逐行写出新向量的每一项是旧向量各项的什么线性组合**，系数就是矩阵的一行。

**例 1**：$a_n = a_{n-1} + a_{n-3}$。需要最近三项：

$$\begin{pmatrix}a_n\\a_{n-1}\\a_{n-2}\end{pmatrix} = \begin{pmatrix}1&0&1\\1&0&0\\0&1&0\end{pmatrix}\begin{pmatrix}a_{n-1}\\a_{n-2}\\a_{n-3}\end{pmatrix}$$

**例 2（带常数项）**：$f_n = 2f_{n-1} + 3f_{n-2} + 5$。常数也放进向量，它自己保持为 1：

$$\begin{pmatrix}f_n\\f_{n-1}\\1\end{pmatrix} = \begin{pmatrix}2&3&5\\1&0&0\\0&0&1\end{pmatrix}\begin{pmatrix}f_{n-1}\\f_{n-2}\\1\end{pmatrix}$$

**例 3（求前缀和）**：求 $S_n = F_1 + \cdots + F_n$。在向量中加入 $S$：$S_n = S_{n-1} + F_n = S_{n-1} + F_{n-1} + F_{n-2}$。

$$\begin{pmatrix}F_n\\F_{n-1}\\S_n\end{pmatrix} = \begin{pmatrix}1&1&0\\1&0&0\\1&1&1\end{pmatrix}\begin{pmatrix}F_{n-1}\\F_{n-2}\\S_{n-1}\end{pmatrix}$$

**例 4（带 $n$ 的多项式项）**：$f_n = f_{n-1} + n$。把 $n$ 和 1 都放进向量：$n = (n-1) + 1$。

$$\begin{pmatrix}f_n\\n\\1\end{pmatrix} = \begin{pmatrix}1&1&1\\0&1&1\\0&0&1\end{pmatrix}\begin{pmatrix}f_{n-1}\\n-1\\1\end{pmatrix}$$

（第一行：$f_n = f_{n-1} + (n-1) + 1$。）

能这样做的前提：转移是**线性**的（只有加法和乘常数），且系数**不随 $n$ 变化**。像 $f_n = f_{n-1}^2$ 或 $f_n = n \cdot f_{n-1}$ 就不行。

### 2.4 图上路径计数

设 $A$ 是图的邻接矩阵（$A_{ij}$ = 从 $i$ 到 $j$ 的边数）。则 $(A^k)_{ij}$ = 从 $i$ 出发**恰好走 $k$ 条边**到达 $j$ 的路径数。

**证明（归纳）**：$k = 1$ 显然。设对 $k-1$ 成立。走 $k$ 步到 $j$ 的路径，按倒数第二个点 $t$ 分类：先用 $k-1$ 步从 $i$ 到 $t$（$(A^{k-1})_{it}$ 种），再走一条 $t \to j$ 的边（$A_{tj}$ 种）。乘法原理加加法原理：

$$\sum_t (A^{k-1})_{it}\,A_{tj} = (A^{k-1}A)_{ij} = (A^k)_{ij}$$

这其实就是 DP $f_{k,j} = \sum_t f_{k-1,t}\,A_{tj}$ 的矩阵写法。**任何"状态数少、转移固定、步数巨大"的计数 DP 都可以这样加速**。

### 2.5 广义矩阵乘法（min, +）

把矩阵乘法中的"乘"换成"加"、"加"换成"取 min"：

$$C_{ij} = \min_k \left(A_{ik} + B_{kj}\right)$$

若 $A$ 是边权矩阵（无边为 $+\infty$），则 $A^k$ 的 $(i, j)$ 项就是**恰好经过 $k$ 条边**的最短路，证明与 2.4 完全相同（按倒数第二个点分类，取最小）。

为什么快速幂依然可用？只要新运算满足结合律。验证结合律时用到的性质是：取 min 满足交换、结合律，且加法对 min **有分配律**：$a + \min(b, c) = \min(a + b, a + c)$。这和普通乘法对加法的分配律地位相同，所以 $(AB)C = A(BC)$ 仍然成立。这种运算下的单位矩阵是"对角线 0、其余 $+\infty$"。

同理还有 (max, +)、(或, 与)（判断 $k$ 步可达性）等。动态 DP 就是把 DP 转移写成 (min, +) 或 (max, +) 矩阵，再用倍增或线段树维护矩阵乘积。

## 3. 代码模板

矩阵用结构体包一个二维数组，`m` 是当前矩阵的阶数。下标从 1 开始：

```cpp
const int N = 105;
int m;
struct mat { int a[N][N]; };

mat mul(const mat &x, const mat &y) {
    mat z;
    mset(z.a, 0);
    For(i, 1, m) For(k, 1, m) For(j, 1, m) z.a[i][j] = (z.a[i][j] + x.a[i][k] * y.a[k][j]) % MOD;
    return z;
}

mat qpow(mat x, int b) {
    mat r;
    mset(r.a, 0);
    For(i, 1, m) r.a[i][i] = 1;
    while (b) {
        if (b & 1) r = mul(r, x);
        x = mul(x, x), b >>= 1;
    }
    return r;
}
```

矩阵快速幂模板题：读入 $m \times m$ 矩阵 $A$ 和 $k$，输出 $A^k$：

```cpp
void solve() {
    int k;
    mat x;
    cin >> m >> k;
    For(i, 1, m) For(j, 1, m) cin >> x.a[i][j];
    mat r = qpow(x, k);
    For(i, 1, m) {
        For(j, 1, m) cout << r.a[i][j] << ' ';
        cout << endl;
    }
}
```

斐波那契第 $n$ 项（$n \ge 1$）：

```cpp
void solve() {
    int n;
    cin >> n;
    m = 2;
    mat x;
    mset(x.a, 0);
    x.a[1][1] = x.a[1][2] = x.a[2][1] = 1;
    cout << qpow(x, n - 1).a[1][1];
}
```

(min, +) 矩阵乘法。`LINF` 约 $4.6 \times 10^{18}$，两个相加约 $9.1\times10^{18}$，仍在 `long long` 范围内；结果初值为 `LINF`，所以每个元素都不超过 `LINF`，反复相乘也不会溢出：

```cpp
mat mulmin(const mat &x, const mat &y) {
    mat z;
    For(i, 1, m) For(j, 1, m) z.a[i][j] = LINF;
    For(i, 1, m) For(k, 1, m) For(j, 1, m) z.a[i][j] = min(z.a[i][j], x.a[i][k] + y.a[k][j]);
    return z;
}
```

求恰好 $k$ 条边的最短路时，把 `qpow` 里的 `mul` 换成 `mulmin`，单位矩阵换成"对角线 0、其余 `LINF`"。

## 4. 复杂度

一次 $m \times m$ 矩阵乘法 $O(m^3)$，快速幂共 $O(\log k)$ 次乘法，总计

$$O(m^3 \log k)$$

$m = 100$、$k = 10^{18}$ 时约 $10^6 \times 60 \times 2 \approx 1.2\times10^8$ 次运算，可以接受；$m$ 到几百就要小心了。

结构体里的数组按值返回，每次会复制 $m^2$ 个数；$N$ 很大时（如 $N = 300$，约 720 KB）注意栈空间，或者改成全局数组、传引用。

## 5. 常见题型与技巧

1. **识别**：$n$ 达到 $10^{9}$ 以上，状态数很少（几十以内），每一步的转移方式相同 → 矩阵快速幂。
2. **构造矩阵**：先写出普通的 DP / 递推，确定"下一步需要哪些量"作为状态向量，常数、$n$ 的多项式、前缀和都可以作为额外的状态塞进向量。
3. **路径计数**：邻接矩阵的 $k$ 次幂。边有权（边权较小，如 $\le 9$）时，把一条权为 $w$ 的边拆成 $w$ 条单位边（加虚点）。
4. **恰好 $k$ 条边的最短路**：(min, +) 矩阵快速幂。点数多但边数少时先离散化点。
5. **周期性变化的转移**：若转移按周期 $T$ 循环（$M_1, M_2, \dots, M_T$），先算一个周期的乘积 $P = M_T\cdots M_1$，再求 $P^{\lfloor n/T\rfloor}$，余下几步单独乘。
6. **动态 DP / 树上路径**：把一段转移写成矩阵，用倍增或线段树合并。注意矩阵**不交换**，合并顺序要与转移顺序一致。

## 6. 易错点

- **乘法顺序**：用列向量时是 $v_n = M v_{n-1}$，矩阵在左；先发生的转移在右边。写成行向量时就反过来，两种写法不要混用。
- **幂次差一**：$F_n$ 是 $M^{n-1}$ 作用在 $(F_1, F_0)$ 上，不是 $M^n$。可以用 $n = 1, 2, 3$ 手算验证。$n = 0$ 时 `qpow` 返回单位矩阵，要确认结果符合定义。
- 局部变量 `mat z;` 不会自动清零，必须 `mset` 或手动赋值。
- 乘法中 `x.a[i][k] * y.a[k][j]` 两个都已取模，乘积不溢出，但要每次取模，不能先累加再取模（$m$ 个 $10^{18}$ 相加会溢出）。
- (min, +) 中的"无穷大"相加不能溢出：用 `LINF` 可以，用 `LLONG_MAX` 不行。
- 转移不是线性的、或者系数随 $n$ 变化，就不能直接用矩阵快速幂。

## 7. 练习

**本站真题**

- [CSP-S 2022 T4 数据传输](#/P8820)：把路径上的 DP 写成 (min, +) 矩阵，用树上倍增预处理"向上跳 $2^i$ 步"的转移矩阵乘积，合并时注意矩阵乘法的顺序。

**洛谷经典题**

- [P3390 【模板】矩阵快速幂](https://www.luogu.com.cn/problem/P3390)
- [P1962 斐波那契数列](https://www.luogu.com.cn/problem/P1962)
- [P1349 广义斐波那契数列](https://www.luogu.com.cn/problem/P1349)
- [P4159 [SCOI2009] 迷路](https://www.luogu.com.cn/problem/P4159)：拆点后路径计数。
- [P2886 [USACO07NOV] Cow Relays G](https://www.luogu.com.cn/problem/P2886)：恰好 $k$ 条边的最短路，(min, +) 矩阵快速幂。
