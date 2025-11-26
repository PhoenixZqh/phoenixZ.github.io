1. [] (){}   捕获列表， 参数列表， 函数体、
   | 捕获列表 | 含义                                                                                               |
   | -------- | -------------------------------------------------------------------------------------------------- |
   | []       | 不捕获任何变量                                                                                     |
   | [=]      | 捕获外部作用阈中所有变量，按值捕获；==不会改变外部变量的值==                                       |
   | [&]      | 捕获外部作用阈中所有变量，按引用捕获； ==会改变外部变量的值==                                      |
   | [=, &a]  | 变量a按引用捕获，其他变量按值捕获                                                                  |
   | [a]      | 按值捕获变量a，其他变量按不捕获                                                                    |
   | [this]   | 让lambda表达式拥有当前类成员函数一样的访问权限；可以访问全局变量、成员变量，==但不能放为局部变量== |

---

```cpp
/*
 * @Author: Phoenix_Z
 * @Date: 2022-10-12 09:30:52
 * @Last Modified by: Phoenix_Z
 * @Last Modified time: 2022-10-12 09:30:52
 * @Description:
 */

#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace std::placeholders;

class Person {
private:
    int m_age;
    float m_score;

public:
    // int i;
    Person(int age, float score)
        : m_age(age)
        , m_score(score)
    {
    }

    void test()
    {
        auto f1 = [this]() {
            cout << "test: " << m_age << endl;
        };
        f1();
    }
};

int main()
{
    int a = 111;
    int b = -1;
    auto f1 = [=](int c) mutable {
        a += 9;
        return a + c;
    };

    auto f2 = [&]() mutable {
        b += 1;
    };

    f2();
    cout << "a的值： " << a << endl;
    cout << "b的值： " << b << endl;
    cout << f1(3) << endl;

    Person p(100, 122);
    p.test();
    return 0;
}

```

---

2. lamda表达式的底层是依赖仿函数实现的
3. lamda表达式是闭包函数；==闭包：带有状态的函数，函数是代码，状态是一组变量，将代码和一组变量捆绑（bind）， 就形成了闭包==；
4. 优点：
   a. 声明式代码风格：就地匿名定义目标函数或函数对象，不需要额外写一个命名函数或者函数对象；以更直接的方式写程序，好的可读性和维护性
   b. 简洁
   c. 在需要的时间和地点实现功能闭包，使程序更加灵活
5. lamda表达是用处：[参考](https://blog.csdn.net/PGZXB/article/details/108398304)
   a. 结合STL使用 ： `std::sort(v.begin(), v.end(), [] ( int n1, int n2 ) { return n1 > n2; });`
   b. 作为函数参数
   c. 作为函数返回值
   d. 代替bind
   e. 将函数签名相同的lambda表达式存入容器
   f. lamda表达是可以转换成函数指针

---

[参考2](https://blog.csdn.net/czyt1988/article/details/51180885)

```cpp
#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace std::placeholders;

void Func(int a, int b)
{
    cout << "a+b: " << a + b << endl;
}

int main()
{
    int a = 9, b = 10;
    auto f1 = bind(Func, _1, _2);
    f1(a, b);

    auto f2 = [&]() { Func(a, b); };
    f2();
    return 0;
}
```
