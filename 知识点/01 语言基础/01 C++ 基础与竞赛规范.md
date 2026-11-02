# C++ 基础与竞赛规范

**组别**：J　**关键词**：数据类型、整数溢出、输入输出加速、freopen、编译选项、时空估算、代码模板

## 1. 是什么 / 解决什么问题

算法想对了，程序仍可能因为"语言层面"的问题丢分：`int` 溢出、读入太慢超时、文件名写错得 0 分、本地能过评测机 RE……这些和算法无关，但在 CSP 中非常常见。

本篇集中讲比赛里必须掌握的 C++ 基础规范：

- 各种数据类型能存多大的数，什么时候会溢出；
- 输入输出怎么写才快、才不出错；
- 考场的文件输入输出（`freopen`）和目录要求；
- 编译选项与调试手段；
- 如何根据时空限制估算程序能否通过；
- 本仓库所有代码使用的**模板**，以及其中每个宏、类型别名、常量的含义。知识库其他文章的代码都只写核心部分，默认套在这个模板里。

## 2. 数据类型与范围

### 2.1 常用类型

| 类型 | 字节 | 范围（约） | 说明 |
| --- | --- | --- | --- |
| `bool` | 1 | `true` / `false` | |
| `char` | 1 | $-128 \sim 127$ | 存字符，本质是小整数（ASCII 码） |
| `int` | 4 | $\pm 2.1 \times 10^9$ | 精确值 $-2^{31} \sim 2^{31}-1 = 2147483647$ |
| `long long` | 8 | $\pm 9.2 \times 10^{18}$ | $2^{63}-1 = 9223372036854775807$ |
| `unsigned long long` | 8 | $0 \sim 1.8 \times 10^{19}$ | $2^{64}-1$，溢出时自动对 $2^{64}$ 取模 |
| `__int128` | 16 | $\pm 1.7 \times 10^{38}$ | g++ 扩展，不能直接 `cin`/`cout` |
| `double` | 8 | $\pm 1.8 \times 10^{308}$ | 只有约 15~16 位有效数字 |
| `long double` | 16（x86） | 更大 | 约 18~19 位有效数字，较慢 |

记忆方法：$2^{10} \approx 10^3$，所以 $2^{31} \approx 2 \times 10^9$，$2^{63} \approx 9 \times 10^{18}$。

**判断用什么类型**：估计中间结果的最大值。

- 两个 $10^9$ 以内的数相乘，最大 $10^{18}$，要 `long long`；
- $n = 10^5$ 个 $10^9$ 以内的数求和，最大 $10^{14}$，要 `long long`；
- 两个 $10^{18}$ 相乘，`long long` 也存不下，要 `__int128` 或先取模；
- 答案是 $2^{64}$ 量级的非负数，用 `unsigned long long`。

### 2.2 溢出

有符号整数超出范围叫**溢出**，在 C++ 中是未定义行为，实际表现通常是"绕回"到一个奇怪的值（甚至负数），程序不会报错，只会悄悄算错。

```cpp
void solve() {
    int32_t a = 1e5, b = 1e5;
    int x = a * b, y = (int)a * b;
    cout << x << " " << y << endl;
    cout << (1LL << 40) << endl;
}
```

`a * b` 先在 32 位下计算、溢出，**之后**才赋给 64 位的 `x`，所以 `x` 是错的（通常是 1410065408）；`y` 先把 `a` 转成 64 位再乘，结果正确为 $10^{10}$。结论：**类型由参与运算的操作数决定，与结果存到哪里无关**。

常见溢出场景：

- 乘法：`a[i] * a[j]`、`i * i <= n`（$i$ 接近 $10^5$ 时 $i^2$ 已超 `int`）；
- 累加：答案、前缀和；
- 移位：`1 << 40` 中的 `1` 是 32 位常量，必须写 `1LL << 40`；
- 二分：`(l + r) / 2` 在 $l, r$ 都接近上限时溢出；
- 取绝对值：`abs(INT_MIN)` 仍然溢出；
- 无符号减法：`s.size() - 1` 在空串时得到 $2^{64}-1$，作为循环上界会出大问题。

本仓库模板用 `#define int long long` 把所有 `int` 换成 64 位，能消灭大部分溢出，但**字面量 `1` 依然是 32 位**，`1 << 40` 照样出错。

### 2.3 整数除法与取模

- 整数除法向 0 取整：`7 / 2 == 3`，`-7 / 2 == -3`（不是 $-4$）。
- 取模结果符号与被除数相同：`-7 % 3 == -1`。需要非负余数时写 `(a % m + m) % m`。
- 除以 0、对 0 取模会直接运行错误。

### 2.4 浮点数

`double` 有精度误差：`0.1 + 0.2 == 0.3` 为假。比较浮点数用误差范围：$|a - b| < \varepsilon$ 视为相等（模板中的 `EPS`）。

能用整数就不用浮点：比较分数 $\frac{a}{b} < \frac{c}{d}$ 改成 $ad < cb$（$b, d > 0$）；求 $\lfloor \sqrt{n} \rfloor$ 时 `sqrt` 可能差 1，要修正：

```cpp
inline int isqrt(int n) {
    int r = sqrt((double)n);
    while (r * r > n) r--;
    while ((r + 1) * (r + 1) <= n) r++;
    return r;
}

void solve() {
    cout << isqrt(999999999999999999LL) << " " << isqrt(16) << " " << isqrt(15) << endl;
    double a = 0.1 + 0.2;
    cout << (a == 0.3) << " " << (fabs(a - 0.3) < EPS) << endl;
}
```

同理，不要用 `pow(a, b)` 做整数乘方，它返回 `double`，大数时会有误差（[CSP-J 2022 T1 乘方](#/P8813) 就要求自己循环乘）。

## 3. 输入输出

### 3.1 cin/cout 加速

`cin`/`cout` 默认要和 C 语言的 `scanf`/`printf` 保持同步，速度较慢。模板 `main` 第一行

```text
ios::sync_with_stdio(false), cin.tie(nullptr);
```

关闭同步、解除 `cin` 与 `cout` 的绑定，此后 `cin`/`cout` 速度和 `scanf`/`printf` 相当，读入 $10^6$ 个数毫无压力。代价是**不能再混用** `scanf`/`printf`/`getchar`/`puts`（输出顺序会乱）。

另一个慢的来源是 `endl`：它除了换行还会刷新缓冲区，输出 $10^5$ 行时明显变慢。模板把 `endl` 宏定义成 `'\n'`，可以放心使用。

### 3.2 读入的几种方式

- `cin >> x`：跳过空白（空格、换行、制表符）读一个数或一个"单词"。
- `while (cin >> x)`：一直读到文件结束（EOF），适合"不告诉你有几个数"的题。
- `getline(cin, s)`：读一整行（含空格），换行符被丢弃。
- `cin >> n` 之后紧接 `getline`，会读到 `n` 后面剩下的那个空行。中间要先 `getline` 一次把它吃掉，或改用 `cin >> ws` 跳过空白。

```cpp
void solve() {
    int n, x, sum = 0;
    string line;
    cin >> n >> ws;
    getline(cin, line);
    while (cin >> x) sum += x;
    cout << n << " [" << line << "] " << sum << endl;
}
```

输入 `3\nhello world\n1 2 3` 输出 `3 [hello world] 6`。

### 3.3 输出格式

- 保留小数：`cout << fixed << setprecision(2) << x;`，四舍五入到 2 位。只写 `setprecision(2)` 不加 `fixed` 表示 2 位**有效数字**。
- 行末多余空格、文末多一个换行一般没关系（NOI 系列默认忽略行末空白），但缺空格、少换行会错。
- 调试输出一定要在提交前删掉。

### 3.4 更快的读入

输入量达到 $10^7$ 级（少见）时，可以用 `getchar` 手写读入：

```cpp
inline int read() {
    int x = 0, f = 1;
    char c = getchar();
    while (c < '0' || c > '9') {
        if (c == '-') f = -1;
        c = getchar();
    }
    while (c >= '0' && c <= '9') x = x * 10 + c - '0', c = getchar();
    return x * f;
}
```

用了 `read` 就**所有输入**都用它，不要再和 `cin` 混用。输出仍可以用 `cout`。

## 4. 文件输入输出与考场规范

CSP 第二轮要求程序从文件读入、向文件输出。例如题目英文名为 `apple`，就要读 `apple.in`、写 `apple.out`。模板中预留了两行：

```text
// freopen("xxx.in", "r", stdin);
// freopen("xxx.out", "w", stdout);
```

考场上把 `xxx` 改成题目英文名并**去掉注释**。之后 `cin`/`cout` 就自动变成读写文件，其余代码不用改。

最容易犯的错误（每年都有人因此爆零）：

- 忘记去掉注释，或调试时注释掉后忘记恢复；
- 文件名拼错、大小写错（Linux 区分大小写），`.in` 写成 `.txt`；
- `"r"` 和 `"w"` 写反，或 `stdin` 和 `stdout` 写反（会把输入文件清空）；
- 源文件名、子文件夹名不符合要求。目录结构以当年考生须知为准，常见要求是"选手目录/题目英文名/题目英文名.cpp"。

建议：每题写完立刻改好 `freopen`，交卷前逐题检查一遍文件名。

## 5. 编译选项与调试

NOI 系列评测一般使用 Linux 下的 g++，开启 `-O2` 优化，C++ 标准近年为 C++14（以当年公告为准）。所以不要使用 C++17 才有的语法（如结构化绑定 `auto [a, b] = p;`）。

本地编译建议：

```bash
g++ a.cpp -o a -O2 -std=c++14 -Wall -Wextra
```

- `-Wall -Wextra` 打开警告。下面几种警告几乎一定是 bug：变量未初始化、**有返回值的函数没有 `return`**（开 `-O2` 后可能直接死循环或 RE）、`if (x = 1)` 误把比较写成赋值、有符号与无符号比较。
- `-fsanitize=address,undefined`（Linux/macOS）在运行时检查数组越界和整数溢出，查 RE 非常有效，但会变慢，只在本地用。
- 本地递归很深时可能栈溢出，而评测机一般把栈空间设为与内存限制相同。Linux 下可以先执行 `ulimit -s unlimited` 再运行程序。

调试手段：模板中的 `dbg(x)` 输出 `x = 值`；对拍（暴力程序 + 随机数据 + 比较输出）是检查正确性最可靠的办法。

## 6. 时空限制估算

**时间**：评测机每秒能执行大约 $10^8 \sim 10^9$ 次简单运算，保守按 $10^8$ 估计。把数据范围代入复杂度：$n = 10^5$ 时 $O(n^2) = 10^{10}$ 必然超时，$O(n \log n) \approx 1.7 \times 10^6$ 轻松通过。完整的对照表见本分类《时间与空间复杂度》。

**空间**：$1\text{MB} = 2^{20}$ 字节 $\approx 10^6$ 字节。

- `int` 数组 $10^7$ 个：$4 \times 10^7$ 字节 $\approx 40$MB；
- `long long` 数组 $10^7$ 个：约 80MB；
- `int` 二维数组 $5000 \times 5000$：约 100MB。

由于模板中 `int` 是 64 位，数组占用是普通 `int` 的两倍。内存紧张时，大数组可以改用 `int32_t`（真正的 32 位整数）声明。

## 7. 本仓库模板

### 7.1 完整模板

```cpp
#include <bits/stdc++.h>
using namespace std;

#define endl '\n'
#define pb push_back
#define F first
#define S second
#define For(i, a, b) for (int i = (a); i <= (b); i++)
#define Rep(i, a, b) for (int i = (a); i < (b); i++)
#define mset(arr, x) memset(arr, x, sizeof(arr))
#define dbg(x) cout << #x << " = " << x << endl

#define int long long
typedef long long ll;
typedef unsigned long long ull;
typedef pair<int, int> pii;
typedef pair<ll, ll> pll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fLL;
const double EPS = 1e-9;
const int MOD = 1e9 + 7;

// globals here

void solve() {
    // ...
}

signed main() {
    ios::sync_with_stdio(false), cin.tie(nullptr);
    // freopen("xxx.in", "r", stdin);
    // freopen("xxx.out", "w", stdout);
    int tests = 1;
    // cin >> tests;
    while (tests--) solve();
    return 0;
}
```

代码组织顺序固定为：模板头 → 常量与全局变量 → 辅助函数 → `solve()` → `main`。数据放在全局数组里（自动初始化为 0，且不占栈空间），所有逻辑写在 `solve()` 中。知识库其他文章只给出"常量与全局变量 → 辅助函数 → `solve()`"这部分。

### 7.2 逐行说明

**头文件与命名空间**

- `#include <bits/stdc++.h>`：g++ 的"万能头文件"，包含全部标准库。
- `using namespace std;`：省去 `std::` 前缀。副作用是不能用标准库里的名字当变量名，例如全局变量 `count`、`next`、`y1`（`<cmath>` 中的函数）会编译错误或产生歧义，换个名字即可。

**宏**

| 宏 | 展开 | 说明 |
| --- | --- | --- |
| `endl` | `'\n'` | 只换行不刷新缓冲区，避免大量输出时变慢 |
| `pb` | `push_back` | `v.pb(x)` 即 `v.push_back(x)` |
| `F` / `S` | `first` / `second` | `p.F`、`p.S` 访问 `pair` 的两个分量 |
| `For(i, a, b)` | `for (int i = (a); i <= (b); i++)` | 闭区间 $[a, b]$，配合 1-indexed 数组：`For(i, 1, n)` |
| `Rep(i, a, b)` | `for (int i = (a); i < (b); i++)` | 半开区间 $[a, b)$：`Rep(i, 0, n)`、`Rep(j, 1, i)` |
| `mset(arr, x)` | `memset(arr, x, sizeof(arr))` | 把整个数组按**字节**填成 `x` |
| `dbg(x)` | ``cout << #x << " = " << x << endl`` | `#x` 把参数变成字符串，`dbg(ans)` 输出 `ans = 5` |

使用宏的注意事项：

- 宏是纯文本替换。`F`、`S` 被定义后，**任何名为 `F` 或 `S` 的标识符都会被替换**，所以不能把变量命名为 `S`、`F`。
- `For` 的上界每轮都会重新计算，循环体中修改上界变量会影响循环次数。倒序循环没有宏，直接写 `for (int i = n; i >= 1; i--)`。
- `mset` 依赖 `sizeof(arr)`，`arr` 必须是真正的数组。数组作为函数参数传入后会退化为指针，此时 `sizeof` 只有 8，`mset` 只清掉开头几个字节。
- `memset` 按字节填充，只有每个字节都相同的值才有意义：`0`（全 0）、`-1`（全 1 位，即 $-1$）、`0x3f`（见下文 `INF`）。`mset(a, 1)` **不会**把元素变成 1。要填任意值用 `fill(a + 1, a + 1 + n, x)`。
- `dbg` 输出到 `cout`，提交前必须删除。

**`#define int long long`**

把代码里所有 `int` 替换为 `long long`，从根源上减少溢出。随之而来的规则：

- `main` 必须返回 `int`，而 `int` 已被替换，所以写成 `signed main()`（`signed` 就是 `int`）。
- 函数体里一律写 `int`，不再写 `long long`。
- 字面量不受影响：`1`、`0` 仍是 32 位，所以移位要写 `1LL << k`。
- `max`、`min` 要求两个参数类型相同：`max(x, 0)` 中 `x` 是 `long long`、`0` 是 `int`，**编译错误**。写成 `max(x, 0LL)`，或 `max(x, (int)0)`（此处 `(int)` 已是 `long long`）。`max(x, (int)s.size())` 同理。
- `INT_MAX` 仍是 32 位的最大值，需要"无穷大"请用下面的 `INF` / `LINF`。
- 内存翻倍，常数略增。内存或时间特别紧时，个别大数组用 `int32_t` 声明（`int32_t` 不受宏影响）。

**类型别名**

| 别名 | 实际类型 | 用途 |
| --- | --- | --- |
| `ll` | `long long` | 与 `int` 相同，常量声明里用来强调 64 位 |
| `ull` | `unsigned long long` | 需要 $2^{64}$ 范围，或利用自然溢出（字符串哈希） |
| `pii` | `pair<int, int>` | 宏展开后其实是两个 `long long` |
| `pll` | `pair<ll, ll>` | 同上 |

**常量**

- `INF = 0x3f3f3f3f`：约 $1.06 \times 10^9$，作为"无穷大"。选它的原因：比常见数据（$\le 10^9$）大；`INF + INF` 约 $2.1 \times 10^9$ 在 32 位内不溢出，做 `dist[u] + w` 之类的加法很安全；每个字节都是 `0x3f`，可以用 `memset` 填充。
- `LINF = 0x3f3f3f3f3f3f3f3f`：约 $4.56 \times 10^{18}$，64 位的"无穷大"，`LINF + LINF` 约 $9.1 \times 10^{18}$ 仍不溢出。**注意**：由于 `int` 是 64 位，`mset(d, 0x3f)` 得到的每个元素是 `LINF` 而不是 `INF`。用 `mset` 初始化后判断"不可达"要与 `LINF` 比较。
- `EPS = 1e-9`：浮点比较的误差限。
- `MOD = 1e9 + 7`：最常见的模数（质数）。题目给的是 998244353 等其他模数时改掉它。

**`solve` 与 `main`**

- `main` 只做三件事：加速输入输出、（考场上）打开文件、调用 `solve()`。
- 多组数据的题：去掉 `// cin >> tests;` 的注释，`solve()` 每次处理一组。此时**全局变量和数组要在 `solve()` 开头清空**，且只清用到的部分（如 `For(i, 1, n) cnt[i] = 0;`），每组都 `mset` 一个大数组可能超时。
- 需要提前结束时在 `solve()` 中 `cout << -1; return;`。

## 8. 易错点

- 中间结果溢出：`a * b` 在赋值之前就已经溢出了；`1 << k` 中 $k \ge 31$。
- `max(x, 0)`、`min(ans, 1)` 这类 64 位与 32 位字面量混用，编译不通过。
- `mset(a, 1)` 不是全 1；`mset` 后与 `INF` 比较（应为 `LINF`）。
- 命名冲突：变量叫 `S`、`F`（被宏替换）、`count`、`y1`、`next`（与标准库冲突）。
- 关闭同步后混用 `cin` 与 `scanf`/`getchar`。
- `cin >> n` 后直接 `getline` 读到空行。
- 有返回值的函数漏写 `return`。
- 局部大数组（如在 `solve()` 里开 `int a[1000000]`）导致栈溢出；局部变量未初始化是随机值。
- `freopen` 文件名、注释状态错误。
- 浮点数直接用 `==` 比较；用 `pow` 算整数次方。

## 9. 练习

**本站真题**

- [CSP-J 2019 T1 数字游戏](#/P5660)：01 串要按字符串读入，按整数读会丢掉前导 0。
- [CSP-J 2022 T1 乘方](#/P8813)：累乘时及时判断是否超过 $10^9$，并特判 $a = 1$，考查溢出与循环次数估算。
- [CSP-S 2020 T2 动物园](#/P7076)：答案可能恰为 $2^{64}$，要用 `ull` 并特判，是数据范围的经典陷阱。
- [CSP-S 2019 D1T1 格雷码](#/P5657)：$k$ 可达 $2^{64}-1$，必须用 `unsigned long long`。

**洛谷经典题**

- [P1001 A+B Problem](https://www.luogu.com.cn/problem/P1001)
- [P1000 超级玛丽游戏](https://www.luogu.com.cn/problem/P1000)
