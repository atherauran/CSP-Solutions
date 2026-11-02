# 模运算、快速幂与逆元

**组别**：S　**关键词**：取模、同余、快速幂、费马小定理、乘法逆元、线性求逆元、阶乘逆元、__int128

## 1. 是什么 / 解决什么问题

计数题的答案常常大得惊人（$2^{10^5}$、$100!$），题目就会要求"答案对 $10^9+7$（或 $998244353$）取模"。于是所有运算都要在**模 $p$ 意义下**进行：

- 加、减、乘可以随时取模；
- 求幂 $a^b \bmod p$ 用**快速幂**，$O(\log b)$；
- **除法不能直接取模**，要乘上除数的**逆元**。

$10^9+7$ 和 $998244353$ 都是质数，这正是为了让逆元一定存在、可以用费马小定理求。

## 2. 核心原理

### 2.1 同余与运算规则

若 $m \mid a - b$，称 $a$ 与 $b$ 模 $m$ **同余**，记作 $a \equiv b \pmod m$，也就是它们除以 $m$ 的余数相同。

$$(a + b) \bmod m = \big((a \bmod m) + (b \bmod m)\big) \bmod m$$
$$(a - b) \bmod m = \big((a \bmod m) - (b \bmod m) + m\big) \bmod m$$
$$(a \times b) \bmod m = \big((a \bmod m) \times (b \bmod m)\big) \bmod m$$

以乘法为例证明：设 $a = q_1 m + r_1$，$b = q_2 m + r_2$，则

$$ab = (q_1 q_2 m + q_1 r_2 + q_2 r_1)\, m + r_1 r_2$$

前一部分是 $m$ 的倍数，所以 $ab \equiv r_1 r_2 \pmod m$。加减法同理。因此**一个只含加减乘的式子，可以在任何中间步骤取模，结果不变**。

**除法不行**：$\frac{6}{2} \bmod 4 = 3$，但 $\frac{6 \bmod 4}{2 \bmod 4} = \frac 22 = 1$。

### 2.2 C++ 中取模的细节

- **负数**：C++ 的 `%` 结果符号与被除数相同，`-7 % 3 == -1`。减法后要写 `(a - b + MOD) % MOD`（$a, b$ 已在 $[0, MOD)$ 内）；一般的负数写 `(x % MOD + MOD) % MOD`。
- **乘法溢出**：$a, b < 10^9+7$ 时 $ab < 1.01\times10^{18} < 9.2\times10^{18}$，`long long` 放得下；但**三个数连乘必须中间取模**：`a * b % MOD * c % MOD`。
- 模数达到 $10^{18}$ 级别时，两数相乘会超过 `long long`，要用 `__int128` 或"龟速乘"（见代码模板）。
- 模 $2^{64}$ 不需要取模：`unsigned long long` 溢出就是自动模 $2^{64}$，字符串哈希常用。

### 2.3 快速幂

求 $a^b \bmod p$。朴素地乘 $b$ 次是 $O(b)$。把 $b$ 写成二进制，例如 $13 = (1101)_2 = 8 + 4 + 1$：

$$a^{13} = a^8 \cdot a^4 \cdot a^1$$

而 $a^1, a^2, a^4, a^8, \dots$ 每个都是前一个的平方。所以从低位到高位扫 $b$ 的二进制：维护当前的 $a^{2^i}$，若第 $i$ 位是 1 就乘进答案，然后把底数平方。

| 第 $i$ 位 | $b$ 的这一位 | 底数 $a^{2^i}$ | 答案 |
|---|---|---|---|
| 0 | 1 | $a$ | $a$ |
| 1 | 0 | $a^2$ | $a$ |
| 2 | 1 | $a^4$ | $a^5$ |
| 3 | 1 | $a^8$ | $a^{13}$ |

$b$ 有 $O(\log b)$ 位，每位常数次乘法，复杂度 $O(\log b)$。

也可以用递归理解：$a^b = (a^{\lfloor b/2\rfloor})^2 \cdot a^{b \bmod 2}$。

快速幂只依赖乘法的**结合律**，所以同样适用于矩阵乘法（见"矩阵与矩阵快速幂"）、置换的复合等。

### 2.4 乘法逆元

若 $a \cdot x \equiv 1 \pmod m$，称 $x$ 是 $a$ 模 $m$ 的**逆元**，记作 $a^{-1}$。有了逆元，"除以 $a$"就变成"乘以 $a^{-1}$"：

$$\frac{b}{a} \equiv b \cdot a^{-1} \pmod m$$

**前提**是 $\frac ba$ 本身是整数（或者题目规定分数按这种方式取模）。例：$\frac 62 = 3$；模 7 下 $2^{-1} = 4$（$2\times4 = 8 \equiv 1$），$6 \times 4 = 24 \equiv 3$。对上了。

**存在条件**：$ax \equiv 1 \pmod m$ 即 $ax + my = 1$，由裴蜀定理，有解 ⇔ $\gcd(a, m) = 1$。模质数 $p$ 时，$1 \sim p-1$ 都有逆元，而 $p$ 的倍数没有。逆元在模 $m$ 意义下唯一。

求逆元有四种常用方法。

### 2.5 方法一：费马小定理

> 若 $p$ 是质数，$p \nmid a$，则 $a^{p-1} \equiv 1 \pmod p$。

**证明**：考察 $a, 2a, 3a, \dots, (p-1)a$ 这 $p-1$ 个数模 $p$ 的余数。

- 都不是 0：$p$ 是质数，$p \nmid a$ 且 $p \nmid i$，所以 $p \nmid ia$。
- 两两不同：若 $ia \equiv ja$，则 $p \mid (i - j)a$，而 $p \nmid a$，所以 $p \mid i - j$；又 $|i - j| < p$，只能 $i = j$。

所以这 $p-1$ 个余数恰好是 $1, 2, \dots, p-1$ 的一个排列。把它们全部乘起来：

$$a^{p-1}\cdot (p-1)! \equiv (p-1)! \pmod p$$

即 $p \mid (a^{p-1} - 1)\cdot(p-1)!$。$(p-1)!$ 不含因子 $p$，所以 $p \mid a^{p-1} - 1$。证毕。

于是 $a \cdot a^{p-2} = a^{p-1} \equiv 1$，**$a^{-1} \equiv a^{p-2} \pmod p$**，一次快速幂 $O(\log p)$。

只适用于**模数是质数**的情况。

### 2.6 方法二：扩展欧几里得

解 $ax + my = 1$，$x$ 就是逆元（调整到 $[0, m)$）。只要求 $\gcd(a, m) = 1$，**模数不必是质数**。$O(\log m)$。推导见"最大公约数与扩展欧几里得"。

### 2.7 方法三：线性递推求 $1 \sim n$ 的逆元

要 $1 \sim n$ 所有数的逆元（$n < p$，$p$ 为质数），每个都做快速幂是 $O(n\log p)$，可以做到 $O(n)$。

设 $p = k \cdot i + r$，其中 $k = \lfloor p / i \rfloor$，$r = p \bmod i < i$。在模 $p$ 下：

$$k \cdot i + r \equiv 0$$

两边同乘 $i^{-1} \cdot r^{-1}$（$r \ne 0$，因为 $p$ 是质数且 $i < p$）：

$$k \cdot r^{-1} + i^{-1} \equiv 0 \quad\Longrightarrow\quad i^{-1} \equiv -k \cdot r^{-1} = -\left\lfloor \frac pi \right\rfloor \cdot (p \bmod i)^{-1}$$

$p \bmod i < i$，它的逆元已经算过了。为避免负数，写成 `(p - p / i) * inv[p % i] % p`。

### 2.8 方法四：阶乘与阶乘逆元

组合数 $\binom nm = \frac{n!}{m!\,(n-m)!}$ 需要阶乘的逆元。先算出 $fac_i = i!$，然后

- 用一次快速幂求 $ifac_n = (n!)^{-1}$；
- 倒着推：$(i-1)!^{-1} = i!^{-1} \cdot i$，即 $ifac_{i-1} = ifac_i \cdot i$。

总共 $O(n + \log p)$。顺便还有 $i^{-1} = ifac_i \cdot fac_{i-1}$。

同样的思路可以**批量求任意 $n$ 个数的逆元**：先求前缀积 $s_i$，求一次 $s_n^{-1}$，再倒推 $s_{i-1}^{-1} = s_i^{-1} a_i$，而 $a_i^{-1} = s_i^{-1} s_{i-1}$。

### 2.9 欧拉定理（了解）

费马小定理的推广：若 $\gcd(a, m) = 1$，则 $a^{\varphi(m)} \equiv 1 \pmod m$，其中 $\varphi(m)$ 是 $1 \sim m$ 中与 $m$ 互质的数的个数（$m$ 为质数时 $\varphi(m) = m - 1$）。

一个直接用途是**降幂**：模质数 $p$ 且 $p \nmid a$ 时

$$a^b \equiv a^{\,b \bmod (p-1)} \pmod p$$

所以指数是一个巨大的数（比如以字符串给出）时，可以边读边对 $p - 1$ 取模。注意**指数要模 $p-1$，不是模 $p$**。

## 3. 代码模板

快速幂与费马求逆元（模数用模板里的 `MOD`，需要 998244353 时改掉即可）：

```cpp
int qpow(int a, int b) {
    int r = 1;
    a %= MOD;
    while (b) {
        if (b & 1) r = r * a % MOD;
        a = a * a % MOD, b >>= 1;
    }
    return r;
}

inline int inv(int a) {
    return qpow(a, MOD - 2);
}
```

扩展欧几里得求逆元（模数任意，不互质返回 $-1$）：

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

int inv(int a, int m) {
    int x, y;
    if (exgcd(a, m, x, y) != 1) return -1;
    return (x % m + m) % m;
}
```

线性求 $1 \sim n$ 的逆元，以及阶乘、阶乘逆元、组合数（需要上面的 `qpow`）：

```cpp
const int N = 1e6 + 5;
int iv[N], fac[N], ifac[N];

void init(int n) {
    iv[1] = 1;
    For(i, 2, n) iv[i] = (MOD - MOD / i) * iv[MOD % i] % MOD;
    fac[0] = 1;
    For(i, 1, n) fac[i] = fac[i - 1] * i % MOD;
    ifac[n] = qpow(fac[n], MOD - 2);
    for (int i = n; i >= 1; i--) ifac[i - 1] = ifac[i] * i % MOD;
}

inline int C(int n, int m) {
    if (m < 0 || m > n) return 0;
    return fac[n] * ifac[m] % MOD * ifac[n - m] % MOD;
}
```

批量求任意 $n$ 个数 $a_i$（都不是 $p$ 的倍数）的逆元：

```cpp
const int N = 1e6 + 5;
int a[N], s[N], sv[N], iv[N];

void calc(int n) {
    s[0] = 1;
    For(i, 1, n) s[i] = s[i - 1] * a[i] % MOD;
    sv[n] = qpow(s[n], MOD - 2);
    for (int i = n; i >= 1; i--) iv[i] = sv[i] * s[i - 1] % MOD, sv[i - 1] = sv[i] * a[i] % MOD;
}
```

模数是 $10^{18}$ 级别时的乘法。`__int128` 写法简单；不能用时用"龟速乘"，把乘法拆成二进制下的加法（和快速幂一个思路），$O(\log b)$：

```cpp
inline int mul(int a, int b, int m) {
    return (__int128)a * b % m;
}

int slow(int a, int b, int m) {
    int r = 0;
    a %= m;
    while (b) {
        if (b & 1) r = (r + a) % m;
        a = a * 2 % m, b >>= 1;
    }
    return r;
}
```

## 4. 复杂度

| 操作 | 复杂度 |
|---|---|
| 快速幂 | $O(\log b)$ |
| 费马 / exgcd 求单个逆元 | $O(\log p)$ |
| 线性求 $1 \sim n$ 逆元 | $O(n)$ |
| 阶乘与阶乘逆元预处理 | $O(n + \log p)$，之后每个组合数 $O(1)$ |
| 批量求 $n$ 个数逆元 | $O(n + \log p)$ |

## 5. 常见题型与技巧

1. **计数取模**：DP 转移每一步加完就取模；方案数相减（补集转化、容斥）后加 `MOD` 再取模。
2. **组合数取模**：$n \le 10^6$、模数为大质数 → 阶乘 + 阶乘逆元；$n \le 5000$ 或模数不是质数 → 杨辉三角递推；$n$ 巨大而模数是小质数 → Lucas 定理（见"排列组合与计数"）。
3. **分数取模**：答案是分数 $\frac ab$ 时输出 $a \cdot b^{-1} \bmod p$。概率、期望题几乎都这样要求。若 $a, b$ 是超长整数（字符串），可以边读边取模（$x \gets (10x + d) \bmod p$），因为取模对加法和乘法封闭。
4. **$2^n$、$k^n$ 类计数**：每个元素独立地有 $k$ 种选择，总数 $k^n$，用快速幂。例如"$n$ 个房间、$m$ 种宗教，相邻同宗教的方案数" = $m^n - m(m-1)^{n-1}$。
5. **指数特别大**：按 2.9 节用费马小定理对指数降幂（指数模 $p-1$）。
6. **模意义下的方程**：$ax \equiv b \pmod p$ 直接 $x = b \cdot a^{-1}$；模数不是质数就用 exgcd。

## 6. 易错点

- **忘记取模**：`r * a * b % MOD` 中前两个数相乘后就可能溢出，必须 `r * a % MOD * b % MOD`。
- **减法出负数**：`(a - b) % MOD` 可能为负，要 `(a - b + MOD) % MOD`。
- 快速幂开头没有 `a %= MOD`，当 $a$ 超过约 $3\times10^9$（$\sqrt{2^{63}}$）时第一次平方就溢出。
- **费马小定理只对质数模数成立**；$a$ 是 $p$ 的倍数时没有逆元（$0$ 没有逆元），这时 `qpow(a, p - 2)` 会返回 0，不会报错，要自己判断。
- 用阶乘求组合数要求 $n < p$；否则 $n!$ 含因子 $p$，等于 0，要用 Lucas。
- 不要用 `pow` 函数算模幂：它返回 `double`，精度不够，也不能取模。
- 降幂时指数应模 $p - 1$；若底数可能是 $p$ 的倍数，要单独处理（结果为 0，除非指数为 0）。
- 线性求逆元的递推中写成 `-(MOD / i) * iv[MOD % i] % MOD` 会得到负数，记得用 `MOD - MOD / i`。

## 7. 练习

**本站真题**

- [CSP-J 2025 T4 多边形](#/P14360)：补集转化，用 $2^{i-1}$（逐步乘 2 取模）减去不合法子集数，减法后加模数。
- [CSP-S 2019 D2T1 Emiya 家今天的饭](#/P5664)：总方案减去不合法方案，全程取模 $998244353$。
- [CSP-S 2025 T4 员工招聘](#/P14364)：计数 DP 对 $998244353$ 取模，组合数和下降幂用递推表预处理。

**洛谷经典题**

- [P1226 【模板】快速幂](https://www.luogu.com.cn/problem/P1226)
- [P3811 【模板】模意义下的乘法逆元](https://www.luogu.com.cn/problem/P3811)
- [P5431 【模板】模意义下的乘法逆元 2](https://www.luogu.com.cn/problem/P5431)
- [P2613 【模板】有理数取余](https://www.luogu.com.cn/problem/P2613)
- [P1082 [NOIP2012 提高组] 同余方程](https://www.luogu.com.cn/problem/P1082)
- [P3197 [HNOI2008] 越狱](https://www.luogu.com.cn/problem/P3197)：技巧 4 中的例子。
