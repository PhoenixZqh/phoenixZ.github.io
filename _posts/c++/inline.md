# 为什么会有内联函数？
1. 普通函数的调用， 会跳到相应的地址执行指令，而这种来回的跳跃意味着一定的时间花销
2. 如果调用函数时，有一种形式直接使用代码块而不是跳转地址，可以节省耗时

# 内联函数的前世今生
1. 内联函数的前世是宏定义， 但其比宏定义好用
2. 内联函数是==以空间换取时间==的方式优化代码耗时的

# 什么时候不能用内联函数？

1. 如果函数体内的代码比较长，使得内联将导致内存消耗代价比较高。
2. 如果函数体内出现循环，那么执行函数体内代码的时间要比函数调用的开销大。

# 虚函数可以是内敛函数吗？
1. 虚函数可以是内联函数，内联是可以修饰虚函数的，但是当虚函数表现多态性的时候不能内联。
2. 内联是在编译器建议编译器内联，而虚函数的多态性在运行期，编译器无法知道运行期调用哪个代码，因此虚函数表现为多态性时（运行期）不可以内联。
3. inline virtual 唯一可以内联的时候是：编译器知道所调用的对象是哪个类（如 Base::who()），这只有在编译器具有实际对象而不是对象的指针或引用时才会发生。

```cpp

#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace std::placeholders;

inline int show(int a, int b, int c) { return a * b * c; }

int main()
{

    clock_t start, end;

    int a = 3, b = 4;
    start = clock();

    cout << show(a, b, 9) << endl;
    end = clock();
    cout << "Run time: " << (double)(end - start) / CLOCKS_PER_SEC << "S" << endl;

    return 0;
}
```