#include <iostream>

class String{
private:
    char* str;
    int len;
    int cap;
    void initFrom(const char* p);
    void reallocAndCopy(const char* p, int len);
    void reallocAndCopy(const String& str);

public:
    String();
    String(const char* p);
    String(const String& str);
    ~String();

    String& assign(const char* p);
    String& assign(const String& str);
    String& append(const char* p);
    String& append(const String& str);
    String& operator=(const char* p);
    String& operator=(const String& str);
    String& operator+=(const char* p);
    String& operator+=(const String& str);
    String operator+(const char* p);
    String operator+(const String& str);
    friend std::ostream& operator<<(std::ostream& os, const String& str);
    friend std::istream& operator>>(std::istream& is, String& str);

    char& operator[] (int index);

    void shrink_to_fit();
    const char* Print(bool show = true) const;
    int size();
    int length();
    int capacity();
};
