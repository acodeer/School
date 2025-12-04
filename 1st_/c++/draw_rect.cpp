#include<iostream>

using namespace std;
class Shape{
    public:
    Shape(){
        cout<<"Shape 생성자"<<endl;
    }
    ~Shape(){
        cout<<"Shape 소멸자"<<endl;
    }
    void hi(){
        cout<<"hi"<<endl;
    }
    private:
};

class Circle : private Shape{
    public:
    Circle(){
        cout<<"Circle 생성자"<<endl;
    }
    ~Circle(){
        cout<<"Circle 소멸자"<<endl;
    }
    void hi(){
        Shape::hi();
    }
    private:
};

int main(){
    Circle c;
    c.hi();
    
    return 0;
}