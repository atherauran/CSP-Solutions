# 最大公约数与扩展欧几里得

**组别**：J　**关键词**：最大公约数、最小公倍数、辗转相除法、更相减损术、裴蜀定理、扩展欧几里得、线性同余方程

## 1. 是什么 / 解决什么问题

- **最大公约数** $\gcd(a, b)$：同时整除 $a$ 和 $b$ 的最大正整数。$\gcd(12, 18) = 6$。约定 $\gcd(a, 0) = a$。
- **最小公倍数** $\operatorname{lcm}(a, b)$：同时是 $a$、$b$ 倍数的最小正整数。$\operatorname{lcm}(12, 18) = 36$。
- $\gcd(a, b) = 1$ 称 $a, b$ **互质**。

用途：分数约分、判断互质、周期对齐（两个周期 $a$、$b$ 的事件下一次同时发生在 $\operatorname{lcm}$ 之后）。

**扩展欧几里得算法**（exgcd）进一步求出满足 $ax + by = \gcd(a, b)$ 的整数 $x, y$，用来解**不定方程** $ax + by = c$、**线性同余方程** $ax \equiv c \pmod m$，以及求**模逆元**。

## 2. 核心原理

### 2.1 辗转相除法（欧几里得算法）

$$\gcd(a, b) = \gcd(b,\ a \bmod b)$$

**证明**：设 $a = qb + r$（$r = a \bmod b$）。

- 若 $d \mid a$ 且 $d \mid b$，则 $d \mid a - qb = r$；
- 若 $d \mid b$ 且 $d \mid r$，则 $d \mid qb + r = a$。

所以 $(a, b)$ 的公约数和 $(b, r)$ 的公约数**完全是同一批数**，最大的那个自然相等。

不断替换，直到第二个数为 0，此时 $\gcd(g, 0) = g$。手推 $\gcd(99, 78)$：

| $a$ | $b$ | $a \bmod b$ |
|---|---|---|
| 99 | 78 | 21 |
| 78 | 21 | 15 |
| 21 | 15 | 6 |
| 15 | 6 | 3 |
| 6 | 3 | 0 |
| 3 | 0 | — |

所以 $\gcd(99, 78) = 3$。如果一开始 $a < b$，第一步 $a \bmod b = a$，会自动交换，不用特判。

**为什么是 $O(\log)$**：当 $b \le a$ 时，$a \bmod b < a / 2$：

- 若 $b \le a/2$，余数 $< b \le a/2$；
- 若 $b > a/2$，余数 $= a - b < a/2$。

每两步较大的数至少减半，所以步数是 $O(\log \min(a, b))$。最坏情况是相邻的斐波那契数。

### 2.2 更相减损术

$$\gcd(a, b) = \gcd(a - b, b)\quad (a \ge b)$$

证明同上。它是辗转相除的"慢速版"（取模就是连续减很多次），$a \gg b$ 时会很慢。但它只用减法，对**高精度数**求 gcd 时有用：再配合"两个都是偶数则提出 2、一个是偶数则除掉 2"，每两步至少有一个数减半，这叫 Stein 算法（二进制 gcd）。

### 2.3 最小公倍数

把 $a, b$ 分解质因数，$a = \prod p_i^{a_i}$，$b = \prod p_i^{b_i}$，则

$$\gcd = \prod p_i^{\min(a_i, b_i)},\qquad \operatorname{lcm} = \prod p_i^{\max(a_i, b_i)}$$

因为 $\min + \max = a_i + b_i$，所以

$$\gcd(a, b) \cdot \operatorname{lcm}(a, b) = a \cdot b$$

计算时写成 `a / gcd(a, b) * b`，**先除后乘**，避免中间结果溢出。

### 2.4 常用性质

- $\gcd(ka, kb) = k\gcd(a, b)$；$\gcd(a, b) = \gcd(a, b - a)$ = $\gcd(a, b + ka)$。
- 多个数：$\gcd(a_1, a_2, \dots, a_n) = \gcd(\gcd(a_1, a_2), a_3, \dots)$，从左到右折叠即可，lcm 同理。
- 前缀 gcd 是单调不增的，而且每次变化至少减半，所以**一个序列的前缀 gcd 最多只有 $O(\log V)$ 种不同的值**。
- 若干个数模 $m$ 同余 ⇔ $m$ 整除它们两两之差 ⇔ $m \mid \gcd(a_2 - a_1, a_3 - a_1, \dots)$。
- 若 $\gcd(a, b) = g$，则 $\gcd(a/g, b/g) = 1$。

### 2.5 裴蜀定理

> 关于 $x, y$ 的方程 $ax + by = c$ 有整数解 ⇔ $\gcd(a, b) \mid c$。

- **必要性**：$g = \gcd(a,b)$ 整除 $a$ 和 $b$，就整除 $ax + by$，所以 $g \mid c$。
- **充分性**：下面的扩展欧几里得会**构造出** $ax_0 + by_0 = g$ 的一组解。若 $c = kg$，那么 $x = kx_0, y = ky_0$ 就是 $ax + by = c$ 的解。

换句话说，$ax + by$（$x, y$ 取遍所有整数）能表示的数，恰好就是 $g$ 的所有倍数。特别地，$a, b$ 互质时能表示出 1。

### 2.6 扩展欧几里得：推导

目标：求 $ax + by = \gcd(a, b)$ 的一组解。沿着辗转相除的递归来做。

- **边界** $b = 0$：$\gcd(a, 0) = a$，取 $x = 1, y = 0$ 即可：$a \cdot 1 + 0 \cdot 0 = a$。
- **递归**：假设已经求出了下一层 $(b,\ a \bmod b)$ 的解 $x', y'$：
$$b x' + (a \bmod b) y' = g$$
把 $a \bmod b = a - \lfloor a/b \rfloor \cdot b$ 代进去：
$$b x' + \left(a - \lfloor a/b\rfloor b\right) y' = g$$
$$a \cdot y' + b \cdot \left(x' - \lfloor a/b \rfloor y'\right) = g$$
对比 $ax + by = g$，得到
$$x = y',\qquad y = x' - \lfloor a/b \rfloor \cdot y'$$

手推 $99x + 78y = 3$（沿上表从下往上回代）：

| $a$ | $b$ | $\lfloor a/b\rfloor$ | $x$ | $y$ | 验证 |
|---|---|---|---|---|---|
| 3 | 0 | — | 1 | 0 | $3 = 3$ |
| 6 | 3 | 2 | 0 | $1 - 2\cdot0 = 1$ | $0 + 3 = 3$ |
| 15 | 6 | 2 | 1 | $0 - 2\cdot1 = -2$ | $15 - 12 = 3$ |
| 21 | 15 | 1 | $-2$ | $1 - 1\cdot(-2) = 3$ | $-42 + 45 = 3$ |
| 78 | 21 | 3 | 3 | $-2 - 3\cdot3 = -11$ | $234 - 231 = 3$ |
| 99 | 78 | 1 | $-11$ | $3 - 1\cdot(-11) = 14$ | $-1089 + 1092 = 3$ |

得到 $99 \times (-11) + 78 \times 14 = 3$。求出的解满足 $|x| \le b$、$|y| \le a$，不会溢出。

### 2.7 通解与最小正整数解

已知 $ax_0 + by_0 = c$ 的一组解，设 $g = \gcd(a,b)$，则所有解为

$$x = x_0 + k\cdot\frac{b}{g},\qquad y = y_0 - k\cdot\frac{a}{g}\qquad (k \in \mathbb Z)$$

**为什么**：代入可验证 $a\cdot k\frac bg - b \cdot k\frac ag = 0$，这些都是解。反过来，若 $(x, y)$ 是解，两式相减得 $a(x - x_0) = b(y_0 - y)$，两边除以 $g$：$\frac ag(x - x_0) = \frac bg(y_0 - y)$。$\frac ag$ 与 $\frac bg$ 互质，所以 $\frac bg \mid x - x_0$，即 $x$ 只能是上面的形式。

所以 $x$ 的所有解在模 $t = b/g$ 下相同，**最小正整数解**是 `(x0 % t + t) % t`，结果为 0 时取 $t$（若要求非负则取 0）。

### 2.8 线性同余方程

$ax \equiv c \pmod m$ 的意思是 $m \mid ax - c$，即存在整数 $y$ 使 $ax + my = c$。于是：

- 有解 ⇔ $\gcd(a, m) \mid c$；
- 解在模 $m / \gcd(a, m)$ 意义下唯一。

**模逆元**是特例 $c = 1$：$ax \equiv 1 \pmod m$ 有解 ⇔ $\gcd(a, m) = 1$。exgcd 求逆元**不要求 $m$ 是质数**，详见"模运算、快速幂与逆元"。

## 3. 代码模板

gcd 与 lcm：

```cpp
int gcd(int a, int b) {
    return b ? gcd(b, a % b) : a;
}

int lcm(int a, int b) {
    return a / gcd(a, b) * b;
}
```

C++ 自带 `__gcd(a, b)`，C++17 起还有 `gcd(a, b)`、`lcm(a, b)`（在 `<numeric>` 中，`bits/stdc++.h` 已包含）。自己写的版本和 C++17 的 `gcd` 同名也能正常编译调用。

扩展欧几里得：返回 $\gcd(a,b)$，并通过引用求出 $ax + by = \gcd(a, b)$ 的一组解。

```cpp
int exgcd(int a, int b, int &x, int &y) {
    if (!b) {
        x = 1, y = 0;
        return a;
    }
    int x1, y1, g = exgcd(b, a % b, x1, y1);
    x = y1, y = x1 - a / b * y1;
    return g;
}
```

解 $ax + by = c$（$a, b > 0$，$c \ge 0$），输出 $x$ 的最小正整数解及对应的 $y$，无解输出 `-1`：

```cpp
void solve() {
    int a, b, c, x, y;
    cin >> a >> b >> c;
    int g = exgcd(a, b, x, y);
    if (c % g) {
        cout << -1;
        return;
    }
    int t = b / g;
    x = (x % t + t) % t * (c / g % t) % t;
    if (x == 0) x = t;
    y = (c - a * x) / b;
    cout << x << ' ' << y;
}
```

这里先把 $x$ 模 $t$ 再乘 $c/g$，避免 $x \cdot (c/g)$ 溢出；若 $t$ 达到 $10^9$ 以上，乘法 `% t` 也可能溢出，需要改用 `__int128`。

## 4. 复杂度

- gcd、exgcd：$O(\log \min(a,b))$，递归深度也是这个量级，不会爆栈。
- $n$ 个数求 gcd：$O(n + \log V)$（gcd 越来越小，总步数有界），通常记作 $O(n\log V)$。

## 5. 常见题型与技巧

1. **约分与分数运算**：结果写成最简分数时，分子分母同除 $\gcd$；分母要保持为正。
2. **已知 gcd 和 lcm 反推两数**：设 $a = g\cdot p$，$b = g\cdot q$，$\gcd(p,q)=1$，$p q = \operatorname{lcm}/g$。枚举 $p$ 即可。
3. **相遇 / 周期问题**：两个东西一个每步走 $m$、一个每步走 $n$，环长 $L$，问何时相遇：$(m - n)k \equiv y - x \pmod L$，就是线性同余方程（注意先把 $m - n$ 调成正数）。
4. **能凑出哪些数**：用面值 $a, b$（可以取负数个）能凑出的恰好是 $\gcd(a,b)$ 的倍数。若只能用非负个数且 $\gcd(a,b) = 1$，最大凑不出的数是 $ab - a - b$（NOIP2017 小凯的疑惑）。
5. **序列的 gcd 性质**：区间 gcd 可以用 ST 表或线段树维护（gcd 满足结合律，且 $\gcd(x, x) = x$，ST 表可以重叠查询）；"以 $r$ 为右端点的所有区间 gcd"最多 $O(\log V)$ 种。
6. **差分取 gcd**：判断能否找到 $m > 1$ 使所有数模 $m$ 同余，或者对整个数组同时加某数后的 gcd，常转化成相邻差的 gcd。

## 6. 易错点

- lcm 写成 `a * b / gcd(a, b)` 可能溢出，要先除后乘。
- 负数参与 gcd：C++ 的 `%` 对负数得负余数，结果可能为负。一般先取绝对值。
- $\gcd(0, 0)$ 没有意义，代码会返回 0，后面拿它做除数会出错。
- exgcd 求出的只是**一组**解，可能为负；题目要最小正整数解时要按通解调整，而且周期是 $b / g$，不是 $b$。
- 方程 $ax + by = c$ 的解要乘上 $c / g$，别忘了先判断 $g \mid c$。
- 同余方程中系数可能是负数（如 $m - n < 0$），先把系数和右端都调成非负再求解。

## 7. 练习

**本站真题**

- [CSP-J 2023 T3 一元二次方程](#/P9750)：输出有理数和根式系数时用 gcd 约分成最简分数。

**洛谷经典题**

- [P1029 [NOIP2001 普及组] 最大公约数和最小公倍数问题](https://www.luogu.com.cn/problem/P1029)
- [P4549 【模板】裴蜀定理](https://www.luogu.com.cn/problem/P4549)
- [P1082 [NOIP2012 提高组] 同余方程](https://www.luogu.com.cn/problem/P1082)：求逆元的线性同余方程。
- [P5656 【模板】二元一次不定方程 (exgcd)](https://www.luogu.com.cn/problem/P5656)
- [P1516 [ZJOI2002] 青蛙的约会](https://www.luogu.com.cn/problem/P1516)
