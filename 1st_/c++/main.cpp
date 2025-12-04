#include <iostream>
#include <vector>
#include <list>

using namespace std;

int main() {
    vector<int> v(10);
    for (int i = 0; i < 10; ++i) {
        v[i] = i + 1;
    }

    list<int> l;
    for (int i = 0; i < 10; ++i) {
        l.push_back(v[i]);
    }

    vector<int>::iterator it = v.begin();
    while (it != v.end()) {
        cout << *it << " ";
        ++it;
    }
    list<int> :: iterator it2 = l.begin();
    cout<<endl;
    while (it2 != l.end()) {
        cout << *it2 << " ";
        ++it2;
    }
    cout<<endl;
    
    vector<int>::iterator iter = v.begin();
    while (iter != v.end()) {
        cout << *iter << " ";
        ++iter;
    }
}

