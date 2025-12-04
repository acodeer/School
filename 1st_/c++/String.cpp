#include <iostream>
#include <cstring>
#include "String.h"

using namespace std;

String::String() {
    initFrom("");
}

String::String(const char* p) {
    initFrom(p);
}

String::String(const String& other) {
    initFrom(other.str);
}

String::~String() {
    delete[] str;
}

void String::initFrom(const char* p) {
    if (!p || *p == '\0') {
        len = cap = 0;
        str = new char[1];
        str[0] = '\0';
        return;
    }
    len = strlen(p);
    cap = len;
    str = new char[len + 1];
    strcpy(str, p);
}

// const char* 할당
String& String::assign(const char* p) {
    if(this->str == p) return *this;
    delete[] str;           // 기존 문자열 메모리 해제
    initFrom(p);            // 새 문자열로 초기화
    return *this;
}


// String 할당
String& String::assign(const String& other) {
    if(this == &other) return *this;
    delete[] str;           
    initFrom(other.str);  
    return *this;
}

void String::reallocAndCopy(const char* p, int pLen) {
    int newLen = this->len + pLen;
    char* newStr = new char[newLen + 1];

    // 기존 문자열 복사 + 이어붙이기
    strcpy(newStr, this->str);
    strcat(newStr, p);

    delete[] this->str;
    this->str = newStr;
    this->len = newLen;
    this->cap = newLen;
}

String& String::append(const char* s) {
    if (!s) return *this;

    if (s == this->str) {
        char* temp = new char[this->len + 1];
        strcpy(temp, s);
        reallocAndCopy(temp, strlen(temp));
        delete[] temp;
    } else {
        reallocAndCopy(s, strlen(s));
    }

    return *this;
}

String& String::append(const String& other) {
    if (this == &other) {
        String temp(other); // 복사 생성자 사용
        return append(temp.str); // 문자열만 전달
    }
    return append(other.str);  // 재사용
}


String& String::operator+=(const char* s) {
    return this->append(s);
}

String& String::operator+=(const String& other) {
    return this->append(other);
}

String& String::operator=(const char* p) {
    return assign(p);
}

String& String::operator=(const String& other) {  
    return assign(other);
}

String String::operator+(const char* p) {
    String NewStr(this->str);
    NewStr.append(p);
    return NewStr;
}

String String::operator+(const String& other) {
    String NewStr(*this);  
    NewStr.append(other);  
    return NewStr;         
}

char& String::operator[](int index) {
    if (index < 0) index = 0;
    else if (index >= len) index = len - 1;

    return str[index];
}

// 출력 연산자 <<
std::ostream& operator<<(std::ostream& os, const String& str) {
    os << str.str;  
    return os;
}

// 입력 연산자 >>
std::istream& operator>>(std::istream& is, String& str) {
    char buffer[str.len + 1];  
    is >> buffer;       
    str.assign(buffer); 
    return is;
}

const char* String::Print(bool show) const {
    if(show){
        for(int i = 0; i < len; i++){
            cout << str[i];
        }
        cout << endl;
    }
    return str;
    
}

int String::size() {
    return len;
}

int String::length() {
    return len;
}

int String::capacity() {
    return len;
}

void String::shrink_to_fit() {
    if (cap == len) return;  // 이미 딱 맞으면 아무것도 하지 않음

    char* newStr = new char[len + 1];
    for (int i = 0; i < len; ++i) {
        newStr[i] = str[i];
    }
    newStr[len] = '\0';

    delete[] str;
    str = newStr;
    cap = len;
}
