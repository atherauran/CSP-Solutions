# KMP

**组别**：S　**关键词**：前缀函数、next 数组、border、字符串匹配、最小循环节、KMP 自动机

## 1. 是什么 / 解决什么问题

**字符串匹配**：给定文本 $s$（长 $n$）和模式串 $t$（长 $m$），找出 $t$ 在 $s$ 中所有出现的位置。

朴素做法枚举起点逐位比较，最坏 $O(nm)$（见《字符串基础》）。它慢在哪里？看一个例子：

```
s: a a b a a b a a a b
t: a a b a a a b
             ^ 第 6 位失配
```

前 5 位 $\texttt{aabaa}$ 已经比对成功，第 6 位失配。朴素做法把 $t$ 右移一位，从头再比——但前 5 位的内容我们**已经知道**了，没必要再看一遍。

KMP 算法利用"已经匹配的部分"直接算出 $t$ 下一步应该右移到哪里，并且文本指针**永不回退**，总复杂度 $O(n + m)$。它的核心是对模式串预处理出的 **next 数组**（也叫前缀函数、失配函数）。

和字符串哈希比，KMP 是确定性的，不会出错；还能求循环节、构造匹配自动机。

## 2. 核心原理

### 2.1 border 与 next 数组

字符串 $u$ 的一个 **border** 是指：既是 $u$ 的**真前缀**、又是 $u$ 的**真后缀**的串（"真"表示不等于 $u$ 本身）。例如 $\texttt{abacaba}$ 的 border 有 $\texttt{a}$、$\texttt{aba}$，以及空串。

$$nxt_i = t_1 \dots t_i \text{ 的最长 border 的长度}$$

例如 $t = \texttt{aabaaab}$：

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $t_i$ | a | a | b | a | a | a | b |
| $t_1 \dots t_i$ | a | aa | aab | aaba | aabaa | aabaaa | aabaaab |
| 最长 border | 空 | a | 空 | a | aa | aa | aab |
| $nxt_i$ | 0 | 1 | 0 | 1 | 2 | 2 | 3 |

**它为什么有用**：匹配时如果已经匹配了 $t_1 \dots t_j$，下一位失配，$t$ 应该右移多少？右移后要想继续有希望，$t$ 的某个前缀必须和"已匹配部分的后缀"对齐——也就是 $t_1 \dots t_j$ 的 border。为了不漏掉任何可能的位置，选**最长**的那个，于是 $j \gets nxt_j$，继续比较。

### 2.2 两个关键性质

**性质 1：$nxt_i \le nxt_{i-1} + 1$。** 如果 $t_1 \dots t_i$ 有长度为 $k$ 的 border，去掉最后一个字符，$t_1 \dots t_{k-1}$ 就是 $t_1 \dots t_{i-1}$ 的 border。所以 $nxt_i$ 最多比 $nxt_{i-1}$ 多 1，只有"在某个 border 后面接上 $t_i$"这一种来源。

**性质 2：$u$ 的所有 border，按长度从大到小，恰好是 $nxt_i,\ nxt_{nxt_i},\ nxt_{nxt_{nxt_i}},\ \dots$ 直到 0。** 设 $v$ 是 $u$ 的 border，$w$ 是比 $v$ 短的另一个 border，那么 $w$ 既是 $u$ 的前缀也是 $v$ 的前缀，既是 $u$ 的后缀也是 $v$ 的后缀（$v$ 是 $u$ 的后缀），所以 $w$ 是 $v$ 的 border。因此"$u$ 的第二长 border"就是"$u$ 的最长 border 的最长 border"，依次类推。

```
u:  [ v      ]...........[ v      ]
    [w]    [w]           [w]    [w]
       w 是 v 的 border，也是 u 的 border
```

### 2.3 求 next 数组

由两个性质，求 $nxt_i$ 的方法是：沿着 $t_1 \dots t_{i-1}$ 的 border 链从长到短试，找第一个能在后面接上 $t_i$ 的 border $j$（即 $t_{j+1} = t_i$），则 $nxt_i = j + 1$；全都接不上则为 0。

用变量 $j$ 表示当前的 border 长度（初始为 $nxt_{i-1}$）：

```
对 i = 2 .. m：
    当 j > 0 且 t[i] != t[j+1] 时：j = nxt[j]   （换下一个更短的 border）
    若 t[i] == t[j+1]：j++
    nxt[i] = j
```

逐步手推 $t = \texttt{aabaaab}$：

| $i$ | $t_i$ | 初始 $j$ | 尝试过程 | $nxt_i$ |
| --- | --- | --- | --- | --- |
| 1 | a | — | 规定 $nxt_1 = 0$ | 0 |
| 2 | a | 0 | $t_1 = \texttt a = t_2$，$j \to 1$ | 1 |
| 3 | b | 1 | $t_2 = \texttt a \ne \texttt b$，$j \to nxt_1 = 0$；$t_1 = \texttt a \ne \texttt b$ | 0 |
| 4 | a | 0 | $t_1 = \texttt a$，$j \to 1$ | 1 |
| 5 | a | 1 | $t_2 = \texttt a$，$j \to 2$ | 2 |
| 6 | a | 2 | $t_3 = \texttt b \ne \texttt a$，$j \to nxt_2 = 1$；$t_2 = \texttt a$，$j \to 2$ | 2 |
| 7 | b | 2 | $t_3 = \texttt b$，$j \to 3$ | 3 |

$i = 6$ 是关键的一步：$\texttt{aabaa}$ 的最长 border $\texttt{aa}$ 后面接不上 $\texttt a$（因为 $\texttt{aab} \ne \texttt{aaa}$），于是退到 $\texttt{aa}$ 的最长 border $\texttt a$，$\texttt a$ 后面接 $\texttt a$ 成功，得到 $\texttt{aa}$。

### 2.4 匹配

匹配和求 $nxt$ 是**同一个过程**：$j$ 表示"文本当前位置结尾、与 $t$ 的前缀能匹配的最大长度"。

```
j = 0
对 i = 1 .. n：
    当 j > 0 且 s[i] != t[j+1] 时：j = nxt[j]
    若 s[i] == t[j+1]：j++
    若 j == m：在 i - m + 1 处找到一次匹配，j = nxt[j]
```

找到匹配后 $j \gets nxt_m$ 而不是 0，这样能找到**重叠**的出现（例如 $\texttt{aa}$ 在 $\texttt{aaa}$ 中出现 2 次）。

用开头的例子手推，$s = \texttt{aabaabaaab}$，$t = \texttt{aabaaab}$（$nxt = 0,1,0,1,2,2,3$）：

| $i$ | $s_i$ | 过程 | $j$ |
| --- | --- | --- | --- |
| 1–5 | aabaa | 逐位匹配 | 5 |
| 6 | b | $t_6 = \texttt a \ne \texttt b$，$j \to nxt_5 = 2$；$t_3 = \texttt b$ 匹配 | 3 |
| 7 | a | $t_4 = \texttt a$ | 4 |
| 8 | a | $t_5 = \texttt a$ | 5 |
| 9 | a | $t_6 = \texttt a$ | 6 |
| 10 | b | $t_7 = \texttt b$，$j = 7 = m$，匹配位置 $10 - 7 + 1 = 4$ | 7 → 3 |

在 $i = 6$ 失配时，$j$ 从 5 直接跳到 2：相当于把 $t$ 右移了 3 位，跳过了起点 2、3（它们不可能匹配），而且已经知道新对齐位置的前 2 位是匹配的，不用重新比。

**另一种写法**：构造串 $t + \texttt{\#} + s$（$\texttt\#$ 是两串中都不出现的字符），求它的 $nxt$ 数组，值等于 $m$ 的位置就是匹配的结尾。这样只需要写一个求 $nxt$ 的函数。

### 2.5 为什么是 $O(n + m)$

看匹配过程中的 $j$：

- 每个 $i$，`j++` 至多执行一次，所以 $j$ 总共**增加不超过 $n$**；
- `while` 循环每执行一次，$j = nxt_j < j$，$j$ 至少**减少 1**；
- $j$ 始终 $\ge 0$。

$j$ 的总减少量不超过总增加量，所以 `while` 循环在整个过程中总共执行不超过 $n$ 次。虽然某一个 $i$ 可能回退很多次，但**均摊**下来每个 $i$ 是 $O(1)$。求 $nxt$ 同理是 $O(m)$。

### 2.6 最小循环节

如果 $s_i = s_{i+p}$ 对所有 $1 \le i \le n - p$ 成立，称 $p$ 是 $s$ 的一个**周期**。

**周期与 border 一一对应**：$s$ 有长度为 $k$ 的 border $\iff$ $s$ 有周期 $n - k$。因为"前 $k$ 个字符等于后 $k$ 个字符"，就是 $s_i = s_{i + (n-k)}$ 对 $i = 1 \dots k$ 成立。

```
s:      a b c a b c a b        n = 8，最长 border = abcab（长 5）
        a b c a b              前缀
              a b c a b        后缀，错开 8 - 5 = 3 位
```

所以**最短周期** $p = n - nxt_n$（最长 border 对应最短周期）。

- 若 $p \mid n$，$s$ 恰好由 $s_1 \dots s_p$ 重复 $n / p$ 次构成（如 $\texttt{abababab}$：$nxt_8 = 6$，$p = 2$，是 $\texttt{ab}$ 重复 4 次）。
- 若 $p \nmid n$，最后一段是不完整的（如 $\texttt{abcabcab}$，$p = 3$）。此时 $s$ **不能**写成任何更短的串的整数次重复（可以用"周期引理"证明：若还有一个整除 $n$ 的周期 $q$，则 $\gcd(p, q)$ 也是周期，与 $p$ 最小矛盾）。

题目问"最短的串，使 $s$ 是它重复若干次后的子串/前缀"，答案是 $p$；问"$s$ 最多是某个串的几次幂"，答案是 $p \mid n$ 时为 $n / p$，否则为 1。

### 2.7 在线匹配：只需要一个状态 $j$

匹配过程中，处理完 $s_i$ 后的全部信息就是一个整数 $j$（当前匹配了 $t$ 的多长前缀），之后的过程只依赖 $j$ 和后续字符。这带来两个应用：

**边读边删**：文本中出现 $t$ 就删掉，删完后两边拼起来可能又形成新的 $t$，反复删直到没有。用栈存当前保留的字符，同时存"每个字符处理完后的 $j$"。一旦 $j = m$，弹出最后 $m$ 个字符，此时栈顶记录的 $j$ 就是删除后的匹配状态，从那里继续——不需要从头重新匹配。每个字符入栈、出栈各一次，总复杂度 $O(n + m)$。

**KMP 自动机**：把"状态 $j$ 读入字符 $c$ 后变成什么状态"预处理成表 $tr_{j,c}$：

$$tr_{j,c} = \begin{cases} j + 1 & t_{j+1} = c \\ tr_{nxt_j,\, c} & t_{j+1} \ne c,\ j > 0 \\ 0 & t_{j+1} \ne c,\ j = 0 \end{cases}$$

（$nxt_j < j$，所以 $tr_{nxt_j}$ 已经算好。）有了 $tr$ 就能在**DP**里使用匹配状态。例如"长度为 $n$、不含 $t$ 作为子串的小写字母串有多少个"：设 $f_{i,j}$ 为前 $i$ 个字符、当前匹配状态为 $j$ 的方案数，枚举下一个字符 $c$ 转移到 $f_{i+1,\,tr_{j,c}}$，只要不到达状态 $m$ 就合法。复杂度 $O(nm\Sigma)$，$\Sigma = 26$。若 $n$ 达到 $10^9$，转移是固定的，可以用矩阵快速幂（见《矩阵与矩阵快速幂》）。

### 2.8 border 链上的计数

把每个 $i$ 向 $nxt_i$ 连边，所有前缀构成一棵以 0 为根的树（border 树），$i$ 的所有 border 就是它到根路径上的点。很多问题转化为树上问题。

例：**每个前缀在 $t$ 中出现了几次**。$t_1 \dots t_k$ 在位置 $i$ 结尾出现 $\iff$ $k$ 是 $t_1 \dots t_i$ 的 border 或 $k = i$，即 $k$ 在 $i$ 到根的路径上。所以每个 $i$ 给自己和所有祖先各加 1：先令 $cnt_i = 1$，再按 $i$ 从大到小把 $cnt_i$ 累加到 $cnt_{nxt_i}$（$nxt_i < i$，倒序保证子树先算完）。

## 3. 代码模板

### 3.1 求 next 数组与匹配

输入文本 $s$ 和模式串 $t$，输出每个匹配的起点，再输出 $t$ 的 next 数组。

```cpp
const int N = 1e6 + 5;
int n, m;
int nxt[N];
string s, t;

void solve() {
    cin >> s >> t;
    n = s.size(), m = t.size(), s = " " + s, t = " " + t;
    for (int i = 2, j = 0; i <= m; i++) {
        while (j && t[i] != t[j + 1]) j = nxt[j];
        if (t[i] == t[j + 1]) j++;
        nxt[i] = j;
    }
    for (int i = 1, j = 0; i <= n; i++) {
        while (j && s[i] != t[j + 1]) j = nxt[j];
        if (s[i] == t[j + 1]) j++;
        if (j == m) {
            cout << i - m + 1 << endl;
            j = nxt[j];
        }
    }
    For(i, 1, m) cout << nxt[i] << ' ';
}
```

求 $nxt$ 从 $i = 2$ 开始：$nxt_1 = 0$，如果从 $i = 1$ 开始会让 $t_1$ 和自己匹配，得到错误的 $nxt_1 = 1$。

### 3.2 最小循环节

输入长度 $n$ 和串 $s$，输出最短周期 $p$，以及 $s$ 最多是几次幂。

```cpp
const int N = 1e6 + 5;
int n;
int nxt[N];
string s;

void solve() {
    cin >> n >> s;
    s = " " + s;
    for (int i = 2, j = 0; i <= n; i++) {
        while (j && s[i] != s[j + 1]) j = nxt[j];
        if (s[i] == s[j + 1]) j++;
        nxt[i] = j;
    }
    int p = n - nxt[n];
    cout << p << ' ' << (n % p == 0 ? n / p : 1);
}
```

### 3.3 边匹配边删除

反复删除 $s$ 中第一次出现的 $t$，输出最终结果。$f_k$ 是栈中第 $k$ 个字符处理完后的匹配长度，$f_0 = 0$。

```cpp
const int N = 1e6 + 5;
int n, m, top;
int nxt[N], f[N];
char st[N];
string s, t;

void solve() {
    cin >> s >> t;
    n = s.size(), m = t.size(), s = " " + s, t = " " + t;
    for (int i = 2, j = 0; i <= m; i++) {
        while (j && t[i] != t[j + 1]) j = nxt[j];
        if (t[i] == t[j + 1]) j++;
        nxt[i] = j;
    }
    For(i, 1, n) {
        int j = f[top];
        while (j && s[i] != t[j + 1]) j = nxt[j];
        if (s[i] == t[j + 1]) j++;
        st[++top] = s[i], f[top] = j;
        if (j == m) top -= m;
    }
    For(i, 1, top) cout << st[i];
}
```

"每次删除第一次出现"与"从左往右扫、一出现就删"结果相同：扫描到的第一个 $j = m$ 的位置，就是当前串中最靠左的一次出现的结尾。

### 3.4 KMP 自动机 + DP：不含 $t$ 的串计数

长度为 $n$ 的小写字母串中，不含子串 $t$ 的有多少个，对 $10^9 + 7$ 取模。

```cpp
const int N = 1e3 + 5, M = 1e2 + 5;
int n, m, ans;
int nxt[M], tr[M][26], f[N][M];
string t;

void solve() {
    cin >> n >> t;
    m = t.size(), t = " " + t;
    for (int i = 2, j = 0; i <= m; i++) {
        while (j && t[i] != t[j + 1]) j = nxt[j];
        if (t[i] == t[j + 1]) j++;
        nxt[i] = j;
    }
    Rep(j, 0, m) Rep(c, 0, 26) {
        if (t[j + 1] - 'a' == c) tr[j][c] = j + 1;
        else tr[j][c] = j ? tr[nxt[j]][c] : 0;
    }
    f[0][0] = 1;
    Rep(i, 0, n) Rep(j, 0, m) Rep(c, 0, 26) {
        int k = tr[j][c];
        if (k < m) f[i + 1][k] = (f[i + 1][k] + f[i][j]) % MOD;
    }
    Rep(j, 0, m) ans = (ans + f[n][j]) % MOD;
    cout << ans;
}
```

状态 $m$ 表示已经出现了 $t$，是非法状态，所以只需要 $0 \sim m-1$ 的转移表。

### 3.5 每个前缀的出现次数

```cpp
const int N = 1e6 + 5;
int n;
int nxt[N], cnt[N];
string s;

void solve() {
    cin >> s;
    n = s.size(), s = " " + s;
    for (int i = 2, j = 0; i <= n; i++) {
        while (j && s[i] != s[j + 1]) j = nxt[j];
        if (s[i] == s[j + 1]) j++;
        nxt[i] = j;
    }
    For(i, 1, n) cnt[i] = 1;
    for (int i = n; i >= 1; i--) cnt[nxt[i]] += cnt[i];
    For(i, 1, n) cout << cnt[i] << ' ';
}
```

## 4. 复杂度

| 操作 | 时间 | 空间 |
| --- | --- | --- |
| 求 next 数组 | $O(m)$ | $O(m)$ |
| 匹配 | $O(n)$ | — |
| 最小循环节 | $O(n)$ | $O(n)$ |
| 边匹配边删除 | $O(n + m)$ | $O(n)$ |
| 构造 KMP 自动机 | $O(m\Sigma)$ | $O(m\Sigma)$ |

均摊分析的关键是 $j$ 每步最多加 1、每次回退至少减 1。注意这个均摊依赖于"$j$ 从上一步的值继续"；如果每一步都从某个任意的 $j$ 重新开始回退（例如在树上多个分支共用父亲的状态），均摊就失效了，此时应该用自动机 $tr$。

## 5. 常见题型与技巧

- **单模式串匹配**：直接套模板。多个模式串同时匹配要用 AC 自动机（超出 CSP 常规范围），模式串不多时可以对每个跑一遍 KMP。
- **循环节、周期**：$n - nxt_n$。前缀 $t_1 \dots t_i$ 的最短周期是 $i - nxt_i$，可以对所有前缀一起回答。
- **border 链**：要求"最短的非空 border"、"所有 border 中满足某条件的"时，沿 $nxt$ 链跳；多次查询时把每个位置跳到的结果记下来（记忆化），避免重复跳。
- **匹配状态放进 DP**：问题涉及"不能出现某个子串"或"恰好出现若干次"时，用 KMP 自动机的状态 $j$ 作为 DP 的一维。
- **动态的文本**：文本可以撤销末尾字符时（栈），记录每个位置的匹配状态 $j$，撤销时恢复。
- **和哈希的取舍**：KMP 适合"模式串固定、文本流式输入"的场景，结果确定；哈希适合任意子串比较、LCP、回文。见《字符串哈希》。

## 6. 易错点

- 下标混用：本文统一 1-indexed，比较的是 `t[j + 1]`。用 0-indexed 写法时要整体改成 `t[j]`，不能混着写。
- 求 $nxt$ 从 $i = 1$ 开始，得到 $nxt_1 = 1$，后面全错。
- 找到匹配后 $j$ 的处理要按题意：允许重叠时 $j \gets nxt_m$，要求**不重叠**时 $j \gets 0$。用字符数组存 $t$ 时如果忘了处理，下一步会访问越界的 `t[m + 1]`。
- 最小循环节忘记判断 $p \mid n$：$\texttt{abcabcab}$ 的最短周期是 3，但它不是 $\texttt{abc}$ 的整数次重复。
- 把 $nxt$ 理解成"最长公共前后缀"时忘了"真"：整个串不算自己的 border，否则 $nxt_i = i$，失配时会死循环。

## 7. 练习

**洛谷经典题**

- [P3375 【模板】KMP](https://www.luogu.com.cn/problem/P3375)：求 next 数组与所有匹配位置。
- [P4391 [BalticOI 2009] Radio Transmission 无线传输](https://www.luogu.com.cn/problem/P4391)：最短周期 $n - nxt_n$。
- [P4824 [USACO15FEB] Censoring S](https://www.luogu.com.cn/problem/P4824)：栈 + KMP，边匹配边删除。
- [P3435 [POI 2006] OKR-Periods of Words](https://www.luogu.com.cn/problem/P3435)：沿 border 链找最短非空 border，记忆化。
- [P2375 [NOI2014] 动物园](https://www.luogu.com.cn/problem/P2375)：border 链上的计数，要求 border 不重叠。
- [P3193 [HNOI2008] GT考试](https://www.luogu.com.cn/problem/P3193)：KMP 自动机 + 矩阵快速幂。
