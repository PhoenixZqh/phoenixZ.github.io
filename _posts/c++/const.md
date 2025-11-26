# const
1. 被 const 修饰的变量不可修改
2. const的作用
 
   a. 可以定义常量
   b. 类型检查
   c. 防止修改内容， 使得程序更加健壮

      ```cpp
      void func(const int x)
      {
        x++; // err, x被const所修饰，不可修改
      }
      ```
    d. 可以节省空间

    ```xml
    const 给的是对应的内存地址，cosnt定义的常量在程序运行过程中只有一份拷贝
    define 给出的是立即数，所以define定义的常量在内存中有多个拷贝
    ```    
    
3. const 与 指针
   a. 常量指针
   ==常量指针， 指针指向是常量，指向的值不可修改，地址可以修改==
   ```cpp
    int a = 0, b = 1;
    cout << "常量指针初始化的指：" << a << endl;
    const int* p1 = &a;
    // *p1 = b;  err：常量指针指向的值不可修改
    p1 = &b;
    cout << "常量指针改变地址后的值： " << *p1 << endl;
   ```
      
   b. 指针常量
   ==指针本身是常量，指针是地址， 所以地址不可以修改， 指向的值可以修改==

   ```cpp
    int* const p2 = &b;  //指针常量必须进行初始化
    *p2 = a;
    // p2 = &a;   err: 指针常量的地址不可修改
    cout << "指针常量改值后： " << *p2 << endl;
   ```

4. const 与 函数
   a. const 放在函数名前， 修饰返回值
   ```cpp
   const int func1();

   const int* func2(); //指针指向的内容不可变

   int *const func2(); //指针本身不可变， 参考指针常量（地址不可变）
   ```

   b. const 放在函数名后， 该成员函数为只读函数，不允许修改类中成员变量的值；
   ```cpp
   class Func {
   private:
        int m_a;

    public:
        void test(int b) const // const 放在函数名后仅限成员函数使用
        {
            m_a = b; //err 
        }
    };
   ```

   c. const修饰函数参数
   ```cpp
   void func(const int var); // 传递过来的参数不可变

   void func(int *const var); // 指针本身不可变

   void StringCopy(char *dst, const char *src); //src为常量不可变

   void func(const A &a) //引用传参 比 值传递 效率高， 因为不用创建临时对象，仅仅借用下别名； 引用传参可能修改参数的值， 加const修饰后就不会有变化（想想交换两个变量的值）

   ```
5. const与类
   ```xml
   1. 类中的const成员变量必须通过初始化列表进行初始化
   2. const对象只能访问const成员函数,而非const对象可以访问任意的成员函数,包括const成员函数
   3. 类中cosnt 修饰的成员变量， 要通过初始化列表来进行初始化
   4. 而如果是static const 修饰的成员变量，在类外定义
   ```

   ```cpp
   class Person {
   private:
      const int m_age;

   public:
      static const int m_score;
      Person(int age)
          : m_age(age)
      {
      }

      const void show()
      {
          cout << "m_age" << m_age << endl;
      }
   };

   const int Person::m_score = 10;

   int main()
   {
      Person p(11);
      p.show();
      cout << p.m_score << endl;
   }
   
   ```

   [bug参考](https://stackoverflow.com/questions/55329892/what-does-this-compiler-error-means-qualified-id-in-declaration-before-to)