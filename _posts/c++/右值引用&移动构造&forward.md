@[TOC](目录)
# 右值引用

 1. 左值表示表达式结束后依然存在的对象 
 2. 右值是在表达式结束时就不存在的临时对象
 3. 右值表示字面常量，表达式，函数非引用返回值

==区分左值右值的最便捷的方法就是看能不能取地址==

```cpp
//示例等号左边为左值，右边为右值
int a = 10;
int b = 2;
int a = a+b;
```

# 移动构造函数
1. 为什么要使用移动构造函数？
<font color = "bulef">想用其他对象初始化同类对象时，常常会调用拷贝构造函数，这就涉及到深拷贝（new & delete），会造成资源的浪费；当使用移动构造函数时，只是创建一个临时对象，并没有开辟新的内存空间，节省资源。</font>
2. 移动构造的原理？
	<font color = "bulef">使用移动语义， 利用右值来传递；</font>
3. 如何使用移动构造函数？

```cpp
/*
 * @Author: Phoenix_Z
 * @Date: 2022-09-29 10:11:06
 * @Last Modified by: Phoenix_Z
 * @Last Modified time: 2022-09-29 10:11:06
 * @Description: move constructor
 */

#include <cstring>
#include <iostream>
#include <memory>

using namespace std;

class MyString {
private:
    char* m_str;
    int m_len;

public:
    MyString(char* str) //普通构造函数
    {
        m_str = str;
        m_len = strlen(str);
        cout << "普通构造函数调用" << endl;
    }

    MyString(const MyString& obj) //拷贝构造函数
    {
        cout << "拷贝对象obj的地址： " << (void*)&obj << endl;
        m_len = obj.m_len;
        m_str = new char[m_len + 1];
        m_str = strcpy(m_str, obj.m_str);
        cout << "拷贝构造函数调用" << endl;
    }

    MyString(MyString&& t)
    {
        cout << "移动对象t的地址：" << (void*)&t << endl;
        m_str = t.m_str;
        m_len = t.m_len;

        t.m_str = nullptr;
        t.m_len = 0;
        cout << "移动构造函数调用" << endl;
    }

    MyString& operator=(const MyString& tmp)
    {
        if (&tmp == this)
            return *this;

        m_len = 0;
        m_str = nullptr;

        m_len = tmp.m_len;
        m_str = strcpy(new char[m_len + 1], tmp.m_str);
        return *this; //返回MyString对象
    }

    ~MyString()
    {
        cout << "析构函数调用";
        if (m_str != nullptr) {
            m_str = nullptr;
            delete[] m_str;
            m_len = 0;
            cout << ", delete操作完成";
        }

        cout << endl;
    }

    void show()
    {
        cout << m_str << ": " << m_len << endl;
    }
};

MyString func()
{
    MyString obj("phoenix");
    return obj;   //这里return的时候会创建一个临时对象，调用拷贝构造
}

int main()
{
    // MyString mstr = func();   //这里赋值的时候，临时对象会释放掉，调用析构函数
    MyString&& mstr1 = func();
    mstr1.show();
    return 0;
}
```
---
<font color ="red">未使用移动构造函数结果：
```bash
普通构造函数调用
拷贝对象obj的地址： 0x7ffc12609a20
拷贝构造函数调用
析构函数调用, delete操作完成
拷贝对象obj的地址： 0x7ffc12609a70
拷贝构造函数调用
析构函数调用, delete操作完成
phoenix: 7
析构函数调用, delete操作完成
```
<font color ="red">使用移动构造函数结果：

```bash
普通构造函数调用
移动对象t的地址：0x7fff1793d740
移动构造函数调用
析构函数调用
phoenix: 7
析构函数调用, delete操作完成
```
==》创建obj时，会申请一块内存；当mstr1接的时候，通过右值引用，obj的地址会直接给到mstr1 ， 因此没有重新申请一块内存，是一种浅拷贝的方式；

# Forward完美转发
