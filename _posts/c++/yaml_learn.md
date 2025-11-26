@[TOC](目录)

---
# 创建YAML文件
1. 可以手动写入
```bash
YAML语法格式:
1，大小写敏感
2，使用缩进表示层级关系
3，不支持Tab键制表符缩进，只使用空格缩进
4，缩进的空格数目不重要，只要相同层级的元素左侧对齐即可，通常开头缩进两个空格
5，字符后缩进一个空格，如冒号，逗号，短横杆（-)等
6，"---"表示YAML格式，一个文件的开始，用于分隔文件间
7，"#”表示注释
```
2. 通过代码写入

主要通过`cv::FileStorage fs_out(yaml_file,cv::FileStorage::WRITE);`

[参考传送门](https://blog.csdn.net/learning_tortosie/article/details/97815514)
```cpp
void WriteYaml(const string &yaml_file)
{
    cv::FileStorage fs_out(yaml_file,cv::FileStorage::WRITE);
    fs_out << "Student"
           << "{";
    fs_out << "name" << "james";
    fs_out << "age" << 18;
    fs_out << "score" << 99.1;
    fs_out << "}";
    fs_out.release();
}
```
写入之后样例子：

```yaml
%YAML:1.0
---
Student:
   name: james
   age: 18
   score: 9.9099999999999994e+01
```

# 读取YAML文件
1. `cv::FileStorage fs_in("xxx.yaml", cv::FileStorage::READ);`

```cpp
cv::FileStorage fs_in("/home/zqh/CODE/learning/src/functionCpp/config/yaml_learn.yaml", cv::FileStorage::READ);
fs_in["Student"]["age"] >> age;
```
2. 用YAML::Node 读取，==需要注意类型要对应上==

```csharp
YAML::Node config = YAML::LoadFile(yaml_path);
float score = config["score"].as<float>();
```
3. 创建类指针，读取Student下所有的参数
<font color='purple'>头文件：</font>

```cpp
#ifndef YAML_LEARN_H
#define YAML_LEARN_H

/*
创建yaml文件
读取yaml文件
读取的方式可以一个一个读
也可以创建个类的智能指针去获取yaml的内容
假设这个yaml的内容是学生的信息，包括学生姓名、年龄、成绩
*/
#include <iostream>
#include <opencv2/opencv.hpp>
// #include <opencv4/opencv2/core/core.hpp>
// #include <opencv4/opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <yaml-cpp/yaml.h>

using namespace std;

class YamlLearn
{
private:
    string m_name;
    int m_age;
    float m_score;
    
public:
    YamlLearn(const YAML::Node& config);
    ~YamlLearn();
    void print();
};
#endif
```
<font color='purple'>源文件：

```cpp
#include <yaml_learn.h>

YamlLearn::YamlLearn(const YAML::Node& config)
{
    m_name = config["name"].as<string>();
    m_age = config["age"].as<int>();
    m_score = config["score"].as<float>();

}
YamlLearn::~YamlLearn(){}

void YamlLearn::print()
{
    cout << m_name  << ","
         << m_age   << ", "
         << m_score << ", "
         << endl;
}

```
<font color='purple'>main函数：

```cpp
#include <yaml_learn.h>
#include <yaml-cpp/yaml.h>
#include <memory>

int main()
{
    string yaml_path = "/home/zqh/CODE/learning/src/functionCpp/config/yaml_learn.yaml";
    YAML::Node config = YAML::LoadFile(yaml_path);
    auto stu = make_shared<YamlLearn>(config["Student"]); //用make_shared的方式初始化shared_ptr指针
    stu->print();
    cout << stu.use_count() << endl;
}
```
==如果用类指针去读yaml文件参数，则需要在构造函数中将里面具体参数进行初始化==
