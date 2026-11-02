# 字符串基础

**组别**：J　**关键词**：字符与 ASCII、字符数组、string、getline、字典序、回文、字符串解析

## 1. 是什么 / 解决什么问题

字符串就是一串字符。CSP-J 几乎每年都有字符串处理的题：统计字符、判断格式、解析输入、按规则变换。这类题算法不难，难在**细节**：读入方式、下标边界、字符与数字的转换、各种特殊情况。

C++ 中有两种字符串：

- **字符数组**（C 风格）：`char s[N];`，以 `'\0'` 结尾；
- **`string`**（C++ 风格）：长度可变，支持 `+`、比较、查找等操作，更方便、更不易出错。

本仓库以 `string` 为主。

## 2. 字符与 ASCII

`char` 本质上是一个小整数，存的是字符的 **ASCII 码**。需要记住的几段：

| 字符 | ASCII | 说明 |
| --- | --- | --- |
| `'0'` ~ `'9'` | 48 ~ 57 | 连续 |
| `'A'` ~ `'Z'` | 65 ~ 90 | 连续 |
| `'a'` ~ `'z'` | 97 ~ 122 | 连续，小写 = 大写 + 32 |
| `' '` | 32 | 空格 |
| `'\n'` | 10 | 换行 |

因为字符就是整数，所以可以直接做运算和比较：

- 数字字符转数字：`c - '0'`；数字转字符：`(char)(d + '0')`。
- 字母序号（0~25）：`c - 'a'`；常用 `cnt[c - 'a']++` 统计每个字母出现次数。
- 判断类型：`c >= '0' && c <= '9'`，或用函数 `isdigit(c)`、`isalpha(c)`、`isupper(c)`、`islower(c)`。
- 大小写转换：`toupper(c)`、`tolower(c)`，或 `c - 'a' + 'A'`。注意这两个函数返回 `int`，输出前要转回 `char`。

```cpp
string s;
int cnt[26];

void solve() {
    cin >> s;
    int sum = 0;
    for (char c : s) {
        if (isdigit(c)) sum += c - '0';
        else if (isalpha(c)) cnt[tolower(c) - 'a']++;
    }
    cout << sum << endl;
    Rep(i, 0, 26) if (cnt[i]) cout << (char)('a' + i) << cnt[i] << " ";
    cout << endl;
    for (char &c : s) if (islower(c)) c = toupper(c);
    cout << s << endl;
}
```

输入 `aB3cA9b`，输出 `12`（$3 + 9$）、`a2 b2 c1`、`AB3CA9B`。`for (char &c : s)` 用引用才能修改原串。

## 3. 字符数组

```text
const int N = 1e6 + 5;
char s[N];
cin >> (s + 1);
int n = strlen(s + 1);
```

- 字符数组以 `'\0'`（ASCII 0）标记结尾，长度为 $L$ 的串需要 $L + 1$ 个位置。
- `cin >> (s + 1)` 从下标 1 开始存，得到 1-indexed 的 $s_1 \sim s_n$。
- `strlen` 从头数到 `'\0'`，是 $O(n)$ 的。**不要写在循环条件里**：`for (int i = 0; i < strlen(s); i++)` 是 $O(n^2)$。
- `strcmp(a, b)` 比较、`strcpy` 复制，不能用 `==` 比较两个字符数组（那是在比较地址）。

字符数组在 KMP、哈希等需要 1-indexed 的场合方便一些；`string` 也可以通过 `s = " " + s;` 在前面补一个字符来实现 1-indexed。

## 4. string

### 4.1 常用操作

| 操作 | 作用 | 复杂度 |
| --- | --- | --- |
| `s.size()` / `s.length()` | 长度（无符号） | $O(1)$ |
| `s[i]` | 第 $i$ 个字符（从 0 开始） | $O(1)$ |
| `s += t`、`s += c`、`s.pb(c)` | 在末尾追加 | $O(\lvert t \rvert)$ |
| `s + t` | 拼接成新串 | $O(\lvert s \rvert + \lvert t \rvert)$ |
| `s.substr(pos, len)` | 从 `pos` 开始取**长度** `len` 的子串 | $O(\text{len})$ |
| `s.find(t)` / `s.find(t, pos)` | 从头 / 从 `pos` 开始找 `t` 第一次出现的位置，找不到返回 `string::npos` | 最坏 $O(nm)$ |
| `s.insert(pos, t)` | 在 `pos` 前插入 | $O(n)$ |
| `s.erase(pos, len)` | 删除 | $O(n)$ |
| `s.replace(pos, len, t)` | 替换一段 | $O(n)$ |
| `reverse(s.begin(), s.end())` | 翻转 | $O(n)$ |
| `==`、`<` 等 | 按字典序比较 | $O(n)$ |
| `to_string(x)` | 数字转字符串 | |
| `stoi(s)` / `stoll(s)` | 字符串转 `int` / `long long` | $O(n)$ |

```cpp
void solve() {
    string s = "hello world";
    cout << s.size() << " " << s.substr(6, 3) << " " << s.find("o") << " " << s.find("o", 5) << endl;
    cout << (s.find("xyz") == string::npos) << endl;
    s.replace(0, 5, "hi");
    s.insert(2, ",");
    s.erase(s.size() - 1, 1);
    cout << s << endl;
    string t = to_string(2026) + "!";
    reverse(t.begin(), t.end());
    cout << t << " " << stoll("-123") * 2 << endl;
    cout << (string("abc") < "abd") << " " << (string("10") < "9") << " " << (string("ab") < "abc") << endl;
}
```

输出：

```text
11 wor 4 7
1
hi, worl
!6202 -246
1 1 1
```

注意 `"10" < "9"` 为真：字符串比较的是**字典序**，先比第一个字符 `'1' < '9'`，与数值大小无关。

### 4.2 字典序

两个字符串从第一个字符开始逐个比较，第一个不同的位置上字符小的串更小；如果一个是另一个的前缀，短的更小。`"ab" < "abc"`，`"abc" < "abd"`，`"b" > "abc"`。

`sort` 字符串数组默认就是按字典序。要按数值比较数字串，先比长度再比字典序（前提是没有前导 0）。

### 4.3 读入

| 方法 | 读到什么 |
| --- | --- |
| `cin >> s` | 跳过空白，读一个不含空白的"单词" |
| `getline(cin, s)` | 读一整行（含空格），不含行末换行符 |
| `cin.get(c)` | 读一个字符，包括空格和换行 |

- `cin >> n` 后紧跟 `getline`，会读到 `n` 后面的空行。先 `getline` 一次丢掉，或写 `cin >> n >> ws;`。
- Windows 下生成的数据行末可能有 `'\r'`，`getline` 会把它读进来。保险起见读完后去掉：`if (!s.empty() && s.back() == '\r') s.pop_back();`。
- 一行里有多个单词时，可以用 `stringstream` 切分：

```cpp
string line, w, best;
int cnt;

void solve() {
    getline(cin, line);
    stringstream ss(line);
    while (ss >> w) {
        cnt++;
        if (w.size() > best.size()) best = w;
    }
    cout << cnt << " " << best << endl;
}
```

输入 `  the quick  brown fox ` 输出 `4 quick`。`stringstream` 和 `cin` 一样会跳过多余的空格。

## 5. 常见操作的写法

### 5.1 回文判断

回文串正着读反着读一样。双指针从两端向中间比较，或与翻转后的串比较：

```cpp
string s;

inline bool pal(const string &t) {
    int l = 0, r = (int)t.size() - 1;
    while (l < r) if (t[l++] != t[r--]) return false;
    return true;
}

void solve() {
    cin >> s;
    string t = s;
    reverse(t.begin(), t.end());
    cout << pal(s) << " " << (s == t) << endl;
}
```

输入 `abcba` 输出 `1 1`；输入 `abca` 输出 `0 0`。参数用 `const string &`，避免复制。

### 5.2 大整数字符串取模

一个上千位的数字放不进任何整数类型，但可以按"秦九韶"的方式从高位到低位边读边取模：$x \leftarrow (10x + d) \bmod m$。

```cpp
string s;

void solve() {
    cin >> s;
    int r9 = 0, rm = 0, x = 0;
    for (char c : s) {
        r9 = (r9 * 10 + c - '0') % 9;
        rm = (rm * 10 + c - '0') % MOD;
    }
    For(i, 0, 5) x = x * 10 + s[i] - '0';
    cout << r9 << " " << rm << " " << x << endl;
}
```

输入 `123456789012345678901234567890`，输出 `0 197434842 123456`（各位数字和为 135，能被 9 整除；最后一个是前 6 位组成的数）。手动转换时要注意中间结果会不会溢出。

### 5.3 朴素匹配

在文本 $s$ 中找模式串 $t$ 的所有出现位置。最直接的做法：枚举起点 $i$，逐个字符比较。

```cpp
string s, t;

void solve() {
    cin >> s >> t;
    int n = s.size(), m = t.size(), c = 0;
    for (int i = 0; i + m <= n; i++) {
        int j = 0;
        while (j < m && s[i + j] == t[j]) j++;
        if (j == m) cout << i + 1 << " ", c++;
    }
    cout << endl << c << endl;
    for (size_t p = s.find(t); p != string::npos; p = s.find(t, p + 1)) cout << p + 1 << " ";
    cout << endl;
}
```

输入 `abababa` 和 `aba`，输出 `1 3 5`、`3`、`1 3 5`（位置从 1 开始，出现可以重叠）。

最坏复杂度 $O(nm)$，例如 $s = \texttt{aaa\dots a}$，$t = \texttt{aa\dots ab}$。$n, m$ 都到 $10^5$ 以上时需要用字符串哈希或 KMP 做到 $O(n + m)$。

### 5.4 字符串排序：拼接最大数

把若干个正整数拼成一个最大的数。直觉"按字典序从大到小"是错的：`3` 和 `30`，字典序 `30 > 3`，但 `330 > 303`。正确的比较是：$a$ 排在 $b$ 前面当且仅当 $a + b > b + a$（拼接后比较）。

```cpp
const int N = 25;
int n;
string a[N];

bool cmp(const string &x, const string &y) { return x + y > y + x; }

void solve() {
    cin >> n;
    For(i, 1, n) cin >> a[i];
    sort(a + 1, a + 1 + n, cmp);
    For(i, 1, n) cout << a[i];
    cout << endl;
}
```

输入 `3` 和 `13 312 343`，输出 `34331213`。

## 6. 复杂度

- 遍历字符串 $O(n)$；`substr`、`find`、`insert`、`erase`、`+` 都与长度成正比，不是 $O(1)$。
- `s = s + c` 每次都复制整个串，循环 $n$ 次是 $O(n^2)$；`s += c` 是均摊 $O(1)$。
- 字符串比较、作为 `map` 的键时，单次比较 $O(\text{长度})$。
- 朴素匹配最坏 $O(nm)$；哈希、KMP 为 $O(n + m)$。

## 7. 常见题型与技巧

- **字符统计**：`cnt[c - 'a']++`，判断字母异位词、找出现最多的字符。
- **格式校验与解析**：按位置逐段扫描，检查分隔符、数字段的长度、前导 0、范围（[CSP-J 2021 T3 网络连接](#/P7911)）。数字段可能很长，先判断长度再转整数，防止溢出。
- **提取信息**：从混合串中挑出数字、字母等（[CSP-J 2025 T1 拼数](#/P14357)）。
- **按位置比较**：固定格式的串直接比较对应位置的字符（[CSP-J 2026 T1 旅游](#/P17827)）。
- **回文**：两端对称位置比较；回文的修改次数 = 不匹配的对称位置对数（[CSP-J 2026 T2 回文串](#/P17828)）。
- **游程编码**：连续相同字符压缩成 (字符, 长度)，长度巨大时只能按段处理。
- **字典序贪心**：拼接最大数、字典序最小的结果，常用"交换相邻两个看哪个更优"来推导比较规则。
- **大模拟**：多种指令、复杂格式，先设计好数据结构再写，把重复的逻辑封装成函数（[CSP-S 2023 T3 结构体](#/P9754)）。

## 8. 易错点

- 字符 `'1'` 与整数 `1` 混淆；忘记 `- '0'`。
- 按整数读入数字串，丢掉了前导 0 或溢出。
- `substr(pos, len)` 第二个参数是**长度**，不是结束位置。
- `find` 找不到返回 `string::npos`（一个很大的无符号数），直接当下标用会越界。
- `s.size() - 1` 在空串时下溢；`for (int i = 0; i < s.size() - 1; i++)` 对空串会出错。
- `cin >> s` 读不到空格；`getline` 前有残留换行；行末的 `'\r'`。
- 字符数组少开了 `'\0'` 的位置；`strlen` 写在循环条件里。
- 用字典序比较数字串（`"10" < "9"`）。
- 循环中 `s = s + c` 或反复 `s.erase(0, 1)`，导致 $O(n^2)$。
- `toupper` 返回 `int`，直接 `cout << toupper(c)` 输出的是数字。

## 9. 练习

**本站真题**

- [CSP-J 2019 T1 数字游戏](#/P5660)：按字符串读入 01 串，统计 `'1'` 的个数。
- [CSP-J 2021 T3 网络连接](#/P7911)：逐段扫描校验地址格式，再用 `map<string, int>` 查找。
- [CSP-J 2025 T1 拼数](#/P14357)：从字符串中统计每个数字出现的次数，从大到小输出。
- [CSP-J 2026 T1 旅游](#/P17827)：固定格式的座位串，直接比较对应字符。
- [CSP-J 2026 T2 回文串](#/P17828)：按游程编码的段双指针配对，统计不匹配的对称位置。
- [CSP-S 2023 T3 结构体](#/P9754)：字符串处理与大模拟。

**洛谷经典题**

- [P5015 [NOIP2018 普及组] 标题统计](https://www.luogu.com.cn/problem/P5015)
- [P1055 [NOIP2008 普及组] ISBN 号码](https://www.luogu.com.cn/problem/P1055)
- [P1308 [NOIP2011 普及组] 统计单词数](https://www.luogu.com.cn/problem/P1308)
- [P1012 [NOIP1998 提高组] 拼数](https://www.luogu.com.cn/problem/P1012)
