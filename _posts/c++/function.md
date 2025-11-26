# 递归
1. 递归是函数自己调用自己
2. 需要加终止条件，所以一般递归调用放在if语句中
3. 递归三部曲：
	a. 终止条件
	b. 递归调用
	c. 递归返回段(回溯)
```cpp
#include <iostream>
#include <memory>
 
using namespace std;
 
void testDigui(int n)
{
    cout << "before recursion, " << n << endl;   

    if(n<=0) return;        //递归终止条件                 
    testDigui(n-1);         //递归调用

    cout << "after recusion ," << n << endl;    //回溯返回阶段
}

int testJiecheng(int n)
{
    if(n == 0 ) return 1;
    int res = n * testJiecheng(n-1);
    cout << n << ":" <<  res << endl;;
    return res;
     
}

int main()
{   
    int res = testJiecheng(3);
    cout << res << endl;
    testDigui(5);
    return 0;
}
```

# 函数指针
1. 获取函数地址 
2. 声明一个函数指针
3. 使用函数指针来调用函数

```cpp
#include <iostream>
#include <memory>
 
using namespace std;

int add(int a, int b)
{
    return a+b;
}

int test(int a, int b, int (*pf)(int,int))    //函数指针的写法，与要用的函数返回类型，参数列表一致
{   
    cout << (*pf)(a, b) << endl;
    return (*pf)(a, b);
}
 
int main()
{
    auto pf = add;             // pf 是函数指针 ， *pf 是函数 ， 函数名即是函数地址
    test(3,4,pf);
    return 0;
}
```

