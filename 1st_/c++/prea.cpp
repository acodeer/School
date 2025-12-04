#include<iostream>
using namespace std;
template<typename t1 , typename t2>
void print(t1 a , t2 b){
    cout<<a<<" "<<b<<endl;
}
int main(){
    print(double(5.5) , double(5));

}