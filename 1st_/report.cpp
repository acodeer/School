#include <iostream>

using namespace std;

class Point{
  int x , y;
  public:
    Point(int x , int y){
      this->x = x;
      this->y = y;
    }
    Point& operator++(){
      ++x;
      ++y;
      return (*this);
    }
    Point operator++(int){
      Point temp = *this;
      ++(*this);
      return temp;
    }
    Point operator+(const Point& p){
      x = x + p.x;
      y = y + p.y;
      return (*this);
    }
    void print()const{
      cout<<this->x<<" "<<this->y<<endl;
    }
};
int main(){
  const Point p(3 , 1);
  p.print();
  Point p2(3,5);
  p2+p;
  p2.print();
  return 0;
}