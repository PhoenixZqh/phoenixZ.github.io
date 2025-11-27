---
layout:     post
title:      c++ function & bind
subtitle:   
date:       2024-11-15
author:     phoenixZ
header-img: img/post-bg-keybord.jpg
catalog: true
tags:
    - cpp
---
> 不同对象的调用方式不同，function和bind的出现是为了统一可调用对象的各种操作

{% highlight xml %}
可调用对象包括：

1. 是一个函数指针
2. 仿函数
3. 类成员函数
4. 可被转换为函数指针的类对象
   {% endhighlight %}

# function

1. 是一个类模板，可以容纳类成员（函数）指针之外的所有可调用对象
2. 指定其模板参数，它可以采用统一的方式处理函数、函数对象、函数指针，并允许保存和延迟执行它们
3. 头文件 `<functional>`

{% highlight cpp %}
using namespace std;
using namespace std::placeholders;

void Test(int a)
{
    cout << __func__ << "->" << a << endl;
}

class Person {
private:
    int m_a;

public:
    Person() = default;
    Person(int a)
        : m_a(a)
    {
    }

    int operator()(int b)
    {

    return m_a + b;
    }

    static void show(int a)
    {
        cout <<__func__ << "->" << a << endl;
    }
};

int main()
{
    //访问普通函数
    function<void(int)> f1 = Test;
    f1(10);

    //访问静态成员函数
    function<void(int)> f2 = Person::show;
    f2(11);

    //访问仿函数
    Person p(12);
    function<int(int)> f3 = p;
    cout << f3(1) << endl;

    return 0;
}
{% endhighlight %}

# bind

1. 将可调用对象与其参数一起进行绑定
2. 绑定后的结果可以使用function保存， 并延迟调用到任何我们需要的地方
3. 可以将n元参数 转换为一元或者n-1元参数
4. placeholders 占位符

---

{% highlight cpp %}
void Test(int a)
{
    cout << __func__ << "->" << a << endl;
}

class Person {
private:
public:
    int m_a;
    Person() = default;
    Person(int a)
        : m_a(a)
    {
    }

    int operator()(int b)
    {

    return m_a + b;
    }

    void show(int a)
    {
        cout <<__func__ << "->" << a << endl;
    }
};

int main()
{
    Person p1;

    //绑定普通函数
    auto f1 = bind(Test, _1);  //_1代表占第一位
    f1(11);

    //绑定成员函数
    auto f2 = bind(&Person::show, &p1, 2);
    f2(2);

    //绑定成员变量（public）
    auto f3 = bind(&Person::m_a, &p1);
    f3() = 111;
    cout << p1.m_a << endl;

    return 0;
}
{% endhighlight %}

# function 与 bind结合使用

{% highlight cpp %}
#include `<functional>`
#include `<iostream>`
#include `<memory>`
#include `<string>`
#include `<vector>`

using namespace std;
using namespace std::placeholders;

int Add(int a, int b)
{
    return a + b;
}

void show(int a, int b, function<int(int, int)> f1)
{
    cout << __func__ << "->" << f1(a, b) << endl;
}

void Test(int a)
{
    cout << __func__ << "->" << a << endl;
}

int main()
{
    function<void(int)> f1 = bind(Test, _1);
    f1(2);

    auto f2 = bind(Test, 3);
    f2();

    auto f3 = bind(Add, _1, _2);

    show(1, 2, f3); // function作为参数

    return 0;

{% endhighlight %}
