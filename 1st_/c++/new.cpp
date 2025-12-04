#include <iostream>
#include <thread>
#include <numeric>
#include <mutex>

// 스레드 안전한 출력을 위한 뮤텍스
std::mutex cout_mutex;

// 스레드에서 실행될 함수
void add_numbers(int start, int end) {
    long long sum = 0;
    for (int i = start; i <= end; ++i) {
        sum += i;
        // 중간 과정을 100000 단위로 출력
        if (i % 100000 == 0) {
            std::lock_guard<std::mutex> lock(cout_mutex);
            std::cout << "Thread " << std::this_thread::get_id() << " is at " << i << std::endl;
        }
    }
    std::lock_guard<std::mutex> lock(cout_mutex);
    std::cout << "Thread " << std::this_thread::get_id() << " has finished with sum: " << sum << std::endl;
}

int main() {
    int limit = 1000000;
    
    // 스레드 생성
    std::thread t1(add_numbers, 1, limit / 2);
    std::thread t2(add_numbers, limit / 2 + 1, limit);
    
    // 스레드가 작업을 완료할 때까지 기다림
    t1.join();
    t2.join();
    
    std::cout << "All threads finished." << std::endl;
    
    return 0;
}