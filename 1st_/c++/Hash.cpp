#include<iostream>
#include<time.h>
#include<stdlib.h>
#include <vector>
#include <algorithm>
#include <iomanip>


using namespace std;
void InsertSort(int* data, int size) {
    for (int i = 1; i < size; ++i) {
        int key = data[i];       // 현재 비교할 값
        int j = i - 1;

        // key보다 큰 값을 오른쪽으로 한 칸씩 이동
        while (j >= 0 && data[j] > key) {
            data[j + 1] = data[j];
            j--;
        }

        // 빈 자리에 key 삽입
        data[j + 1] = key;
    }
}

void Swap(int* a , int* b){
    int temp = *a;
    *a = *b;
    *b = temp;
}

void MedianOfThree(int* data, int left, int right) {
    int mid = (left + right) / 2;
    // 세 원소를 정렬하여 중앙값을 data[mid]에 둡니다.
    if (data[left] > data[mid]) Swap(&data[left], &data[mid]);
    if (data[left] > data[right]) Swap(&data[left], &data[right]);
    if (data[mid] > data[right]) Swap(&data[mid], &data[right]);
    // 이제 data[mid]에 중앙값이 있으므로, 이를 피벗 위치(left)로 옮깁니다.
    Swap(&data[left], &data[mid]);
    // 반환값 없음 (void)
}

int Quick_Partition(int* data , int left , int right){
    int low = left +1;
    int high = right;
    int mid = (left+right)/2;
    int pivot;
    //pivot = data[left];
    //pivot = data[mid];
    //pivot = data[right];
    MedianOfThree(data , left , right);
    pivot = data[left];

    //Swap(&data[left] , &data[mid]);
    //Swap(&data[left] , &data[right]);
    
    while(low <= high){
        while(low <= right && data[low] <= pivot){
            low++;
        }
        while(high >= left && data[high] > pivot){
            high--;
        }
        if (low <= high){
            Swap(&data[low] , &data[high]);
            low++;
            high--;
        }
    }
    Swap(&data[left] , &data[high]);
    return high;
}

void QuickSort(int* data, int left, int right) {
    // 일정 크기 이하의 부분 배열은 삽입정렬로 처리
    if (right - left <= 10) {
        InsertSort(data + left, right - left + 1);
        return;
    }

    if (left < right) {
        int pivot = Quick_Partition(data, left, right);
        QuickSort(data, left, pivot - 1);
        QuickSort(data, pivot + 1, right);
    }
}

/*void QuickSort(int* data , int left , int right){
    if(left < right){
        int pivot = Quick_Partition(data , left , right); // 여기서 pivot은 high
        QuickSort(data , left , pivot-1); // OK
        QuickSort(data , pivot+1 , right); // OK
    }
}*/


int main() {
    const int SIZE = 50000000;
    vector<int> arr(SIZE);
    for (int i = 0; i < SIZE; ++i) arr[i] = i + 1;

    //srand(time(NULL));
    random_shuffle(arr.begin(), arr.end()); 
    clock_t start = clock();

    /*for(int i = 0 ; i < SIZE ; i++){
        cout<<arr[i]<<" ";
    }
    cout<<endl;*/

    QuickSort(arr.data(), 0, SIZE - 1);
    
    //InsertSort(arr.data(), SIZE);
    /*for(int i = 0 ; i < SIZE ; i++){
        cout<<arr[i]<<" ";
    }*/
    cout<<endl;
    clock_t end = clock();
    double elapsed = static_cast<double>(end - start) / CLOCKS_PER_SEC;
    cout << fixed << setprecision(10);
    cout << "소요 시간: " << elapsed << "초" << endl;
    return 0;
}
