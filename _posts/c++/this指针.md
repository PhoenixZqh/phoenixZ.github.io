

 - this是关键字，是const指针（<font color="purple">不能被修改</font>）
 - 指向当前对象（正在使用的对象），通过this指针可以访问当前对象的所有成员
 - this指针运行在类的内部，可以访问所有属性的成员
 - 只有在对象创建后this指针才有意义
 - 在类的非静态成员函数中返回类对象本身的时候，直接使用 return *this。

```cpp
#include <iostream>

using namespace std;

class Person
{
private:
    char * m_name;
    int m_age;
    float m_score;

public:
    Person(char* name, int age, float score):m_name(name),m_age(age),m_score(score){};

    void show()
    {
        cout << "姓名：" << "\t" << this->m_name << "\n"  << "年龄：" << "\t" << this->m_age << "\n"  << "得分：" << "\t" << this->m_score <<endl;
    } 

    
};

int main()
{
    Person p("詹姆斯", 38 ,  39.1);
    p.show();

    system("pause");
    return 0;
}

```
