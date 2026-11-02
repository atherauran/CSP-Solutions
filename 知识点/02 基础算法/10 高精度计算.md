# 高精度计算

**组别**：J　**关键词**：高精度、大整数、竖式运算、进位与借位、高精乘低精、高精除低精、压位、__int128

## 1. 是什么 / 解决什么问题

`long long` 最大约 $9.2 \times 10^{18}$，只有 19 位。但很多题的数字远不止这么大：$100!$ 有 158 位，$2^{1000}$ 有 302 位，斐波那契数第 500 项有 105 位。这时内置类型存不下，只能**用数组一位一位地存数字，再模拟小学竖式计算**，这就是高精度计算。

CSP 中常见的是：

- 高精度加法、减法；
- 高精度乘低精度（大数 × 普通整数），如求阶乘；
- 高精度乘高精度；
- 高精度除以低精度（大数 ÷ 普通整数，求商和余数）。

结果只是"稍微"超出 `long long`（比如两个 $10^{18}$ 相乘）时，也可以用 GCC 提供的 `__int128`，范围约 $\pm 1.7 \times 10^{38}$。

## 2. 核心原理

### 2.1 存储方式：倒序存

用 `vector` 存每一位数字，**下标 0 存个位**，下标 1 存十位……例如 $12345$ 存成：

```text
下标:  0  1  2  3  4
数字:  5  4  3  2  1
```

为什么倒着存：竖式计算从个位开始，进位往高位走。倒序存时个位对齐在下标 0，两个数相加时同一下标就是同一数位；最高位进位只需在末尾 `push_back`，不用整体移动。

读入时数字是字符串，从字符串末尾往前取即可。输出时从最高位（最后一个下标）往前输出。

### 2.2 加法

和竖式一样，从低位到高位逐位相加，满 10 进 1：

$$c_i = (a_i + b_i + t) \bmod 10,\quad t \leftarrow \left\lfloor \frac{a_i + b_i + t}{10} \right\rfloor$$

$t$ 是来自低位的进位。两个数位数不同时，短的那个在高位视为 0。最后若还有进位，再补一位。

```text
     9 8 7
  +    6 5
  ---------
   1 0 5 2      个位 7+5=12 写 2 进 1；十位 8+6+1=15 写 5 进 1；
                百位 9+0+1=10 写 0 进 1；最后进位 1
```

### 2.3 减法

先比较大小：若 $a < b$，计算 $b - a$ 并在前面输出负号。保证 $a \ge b$ 后逐位相减，不够减就向高位借 1：

$$c_i = a_i - b_i - t,\quad \text{若 } c_i < 0 \text{ 则 } c_i \mathrel{+}= 10,\ t = 1;\ \text{否则 } t = 0$$

相减后高位可能出现多个 0（如 $1000 - 999 = 0001$），要**去掉前导零**，但至少保留一位。

**比较大小**：没有前导零时，位数多的大；位数相同从最高位往低位比，第一个不同的位决定大小。

### 2.4 高精乘低精

大数 $a$ 乘普通整数 $b$：把 $b$ 当成一个整体，逐位乘上去再处理进位：

$$t \leftarrow a_i \cdot b + t,\quad c_i = t \bmod 10,\quad t \leftarrow \lfloor t / 10 \rfloor$$

$a$ 的位处理完后，$t$ 可能还很大（最多和 $b$ 同数量级），要继续一位一位拆到 $c$ 的末尾。

注意 $a_i \cdot b + t$ 不能溢出：$t < b$，所以这个值小于 $10b$，$b$ 在 $10^{17}$ 以内用 `long long` 都安全。

### 2.5 高精乘高精

竖式乘法中，$a$ 的第 $i$ 位（$10^i$）乘 $b$ 的第 $j$ 位（$10^j$），结果属于 $10^{i+j}$ 这一位。所以先不管进位，把所有乘积累加到对应位置：

$$c_{i+j} \mathrel{+}= a_i \cdot b_j$$

最后统一从低到高处理一遍进位。$a$ 有 $la$ 位、$b$ 有 $lb$ 位时，乘积不超过 $la + lb$ 位，$c$ 开这么大就够。

```text
        1 2 3        a = [3,2,1]
      ×   4 5        b = [5,4]
  未进位：c0 = 3·5 = 15
          c1 = 2·5 + 3·4 = 22
          c2 = 1·5 + 2·4 = 13
          c3 = 1·4 = 4
  进位后：15 → 5 进 1；22+1=23 → 3 进 2；13+2=15 → 5 进 1；4+1=5
  结果 5535 = 123 × 45
```

### 2.6 高精除以低精

除法是从**高位往低位**做的。维护余数 $r$，每次把 $r$ 乘 10 加上下一位，商这一位就是 $\lfloor r / b \rfloor$，新余数是 $r \bmod b$：

```text
  1234 ÷ 7:
  r = 1      商 0  r = 1
  r = 12     商 1  r = 5
  r = 53     商 7  r = 4
  r = 44     商 6  r = 2
  商 0176 → 去前导零得 176，余数 2（176 × 7 + 2 = 1234）
```

和其他运算不同，这里要从下标大的往小的扫，结果同样要去前导零。

高精除以高精在 CSP 中很少考，可以用"试商 + 高精减法"模拟：从高位开始，每一位商最多试 9 次减法。

### 2.7 压位

每个数组元素只存一位十进制数太浪费：乘法 $O(la \cdot lb)$ 里每次只处理一位。可以让每个元素存 **4 位或 8 位**（即以 $10^4$ 或 $10^8$ 为基数），所有公式里的 10 换成基数，长度缩短为原来的 $1/4$ 或 $1/8$，速度相应提升。

- 以 $10^8$ 为基数做高精乘低精时，$a_i \cdot b$ 要在 `long long` 范围内，$b$ 不能超过约 $10^{10}$。
- 以 $10^4$ 为基数做高精乘高精时，单个乘积不超过 $10^8$，累加时注意总和不溢出。
- 输出时最高的一段直接输出，**其余每段要补足前导零**（如 8 位一段的 `123` 要输出成 `00000123`）。

### 2.8 `__int128`

GCC 支持 128 位整数 `__int128`，加减乘除、比较、取模都能直接用，范围约 $\pm 1.7 \times 10^{38}$。但它**不能直接用 `cin` / `cout`**，需要自己写输入输出。适合中间结果偶尔超出 `long long` 的场合（两个 $10^{18}$ 级的数相乘、比较大小），答案超过 38 位就还得用高精度。

## 3. 代码模板

### 3.1 高精度基本运算

`vector<int>` 倒序存，所有函数都保证返回值没有前导零。两个同名的 `mul` 分别是高精乘低精和高精乘高精（参数类型不同，C++ 会自动选择）。

```cpp
vector<int> read(string s) {
    vector<int> a;
    for (int i = (int)s.size() - 1; i >= 0; i--) a.pb(s[i] - '0');
    return a;
}

void print(vector<int> a) {
    for (int i = (int)a.size() - 1; i >= 0; i--) cout << a[i];
    cout << endl;
}

void trim(vector<int> &c) {
    while (c.size() > 1 && c.back() == 0) c.pop_back();
}

bool geq(vector<int> &a, vector<int> &b) {
    if (a.size() != b.size()) return a.size() > b.size();
    for (int i = (int)a.size() - 1; i >= 0; i--)
        if (a[i] != b[i]) return a[i] > b[i];
    return true;
}

vector<int> add(vector<int> &a, vector<int> &b) {
    vector<int> c;
    int t = 0;
    for (int i = 0; i < a.size() || i < b.size() || t; i++) {
        if (i < a.size()) t += a[i];
        if (i < b.size()) t += b[i];
        c.pb(t % 10), t /= 10;
    }
    return c;
}

vector<int> sub(vector<int> &a, vector<int> &b) {
    vector<int> c;
    int t = 0;
    Rep(i, 0, a.size()) {
        t = a[i] - t;
        if (i < b.size()) t -= b[i];
        c.pb((t + 10) % 10);
        t = t < 0;
    }
    trim(c);
    return c;
}

vector<int> mul(vector<int> &a, int b) {
    vector<int> c;
    int t = 0;
    for (int i = 0; i < a.size() || t; i++) {
        if (i < a.size()) t += a[i] * b;
        c.pb(t % 10), t /= 10;
    }
    trim(c);
    return c;
}

vector<int> mul(vector<int> &a, vector<int> &b) {
    vector<int> c(a.size() + b.size(), 0);
    Rep(i, 0, a.size()) Rep(j, 0, b.size()) c[i + j] += a[i] * b[j];
    Rep(i, 0, c.size() - 1) c[i + 1] += c[i] / 10, c[i] %= 10;
    trim(c);
    return c;
}

vector<int> divide(vector<int> &a, int b, int &r) {
    vector<int> c(a.size());
    r = 0;
    for (int i = (int)a.size() - 1; i >= 0; i--) {
        r = r * 10 + a[i];
        c[i] = r / b, r %= b;
    }
    trim(c);
    return c;
}

void solve() {
    string s1, s2;
    int k, r;
    cin >> s1 >> s2 >> k;
    vector<int> a = read(s1), b = read(s2);
    print(add(a, b));
    if (geq(a, b)) print(sub(a, b));
    else cout << '-', print(sub(b, a));
    print(mul(a, k));
    print(mul(a, b));
    vector<int> q = divide(a, k, r);
    print(q);
    cout << r << endl;
}
```

要点：

- `add` 的循环条件 `i < a.size() || i < b.size() || t`：两个数都处理完、且没有进位时才停，最高位进位自动补上。
- `sub` 中 `(t + 10) % 10` 同时处理了够减和不够减两种情况，`t = t < 0` 表示是否向高位借位。
- 高精乘低精里 $k = 0$ 时结果会是一串 0，`trim` 把它变成单个 0。
- 读入的数如果可能带前导零（如 `007`），读完后也要 `trim` 一下，否则 `geq` 按位数比较会出错。

### 3.2 压位：计算 $n!$

以 $10^8$ 为基数，每个元素存 8 位。

```cpp
const int B = 1e8;
int n;
vector<int> a;

void solve() {
    cin >> n;
    a.pb(1);
    For(k, 2, n) {
        int t = 0;
        Rep(i, 0, a.size()) {
            t += a[i] * k;
            a[i] = t % B, t /= B;
        }
        while (t) a.pb(t % B), t /= B;
    }
    cout << a.back();
    for (int i = (int)a.size() - 2; i >= 0; i--) cout << setw(8) << setfill('0') << a[i];
    cout << endl;
}
```

$a_i < 10^8$，$k \le 10^4$ 时 $a_i \cdot k + t$ 远小于 `long long` 上限。输出时除最高段外都用 `setw(8) << setfill('0')` 补足 8 位。

### 3.3 `__int128` 的输入输出

```cpp
__int128 read128() {
    string s;
    cin >> s;
    __int128 x = 0;
    int st = s[0] == '-';
    Rep(i, st, s.size()) x = x * 10 + (s[i] - '0');
    return st ? -x : x;
}

void print(__int128 x) {
    if (x < 0) cout << '-', x = -x;
    if (x > 9) print(x / 10);
    cout << (char)('0' + x % 10);
}

void solve() {
    __int128 a = read128(), b = read128();
    print(a * b);
    cout << endl;
}
```

`print` 递归先输出高位，再输出个位。只需要把 `long long` 的乘积放大时，也可以直接写 `(__int128)x * y`，不必整套读入。

## 4. 复杂度

设大数有 $L$ 位（压位后为 $L / w$ 段）：

| 运算 | 时间 |
|:-:|:-:|
| 加、减、比较 | $O(L)$ |
| 高精乘低精、高精除以低精 | $O(L)$ |
| 高精乘高精 | $O(L_a \cdot L_b)$ |
| 高精除以高精（试商） | $O(L^2 \cdot 10)$ |

例如求 $n!$：结果约 $n \log_{10} n$ 位，做 $n$ 次高精乘低精，总 $O(n^2 \log n)$；$n = 10^4$ 时结果约 3.6 万位，不压位约 $3.6 \times 10^8$ 次运算，压 8 位后快 8 倍。

## 5. 常见题型与技巧

- **大数四则运算**：模板题，注意负号、前导零、结果为 0 的情况。
- **阶乘、阶乘之和**：反复做高精乘低精、高精加法。
- **递推结果很大**：如走楼梯方案数 $f_i = f_{i-1} + f_{i-2}$，只要把加法换成高精加法；数组每个元素是一个 `vector<int>`，或者只保留最近两项滚动。
- **大的 2 的幂**：$2^p$ 可以反复乘 2，也可以快速幂配合高精乘高精；只要后若干位时，每次乘完截断即可。
- **只要结果对某数取模**：不需要高精度，直接边算边取模。高精度大数对小整数 $m$ 取模，就是 3.1 中的 `divide` 只要余数。
- **判断是否超出范围**：有时只需要知道结果是否大于某个界（如 $10^9$），边乘边判断、超过就停，不需要真的算出大数。
- **`__int128` 应急**：中间乘积超出 `long long` 但最终结果不大，或者结果在 38 位以内。

## 6. 易错点

- **存储顺序搞混**：读入的字符串是高位在前，存进数组要倒过来；输出时再倒回来。
- **最高位进位遗漏**：加法和乘法最后的进位 $t$ 还没加进去。
- **减法没有先比较大小**：$a < b$ 时直接相减会得到错误结果。
- **前导零**：减法、乘法（乘 0）、除法后都可能产生，输出前必须去掉，但结果为 0 时要保留一个 0。
- **高精乘低精溢出**：$a_i \cdot b$ 中 $b$ 太大时会溢出，$b$ 超过约 $10^{17}$ 就得改成高精乘高精。
- **压位输出没补零**：中间段 `123` 必须输出成 `00000123`。
- **`__int128` 用 `cin` / `cout`**：编译错误，要手写读写。
- **字符和数字混淆**：`s[i] - '0'` 才是数字；输出 `__int128` 的一位时要转成字符。

## 7. 练习

**本站真题**

- [CSP-S 2019 D2T2 划分](#/P5665)：答案可达 $10^{33}$ 级，用 `__int128` 累加平方和并手写输出。
- [CSP-S 2023 T4 种树](#/P9755)：生长量的等差数列求和可达 $10^{27}$ 级，用 `__int128` 计算和比较。

**洛谷经典题**

- [P1601 高精度加法](https://www.luogu.com.cn/problem/P1601)
- [P2142 高精度减法](https://www.luogu.com.cn/problem/P2142)
- [P1303 A*B Problem](https://www.luogu.com.cn/problem/P1303)
- [P1480 A/B Problem（高精度除法Ⅰ）](https://www.luogu.com.cn/problem/P1480)
- [P1009 [NOIP1998 普及组] 阶乘之和](https://www.luogu.com.cn/problem/P1009)
- [P1255 数楼梯](https://www.luogu.com.cn/problem/P1255)
- [P1045 [NOIP2003 普及组] 麦森数](https://www.luogu.com.cn/problem/P1045)
