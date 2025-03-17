#include <iostream>
using namespace std ;
void bubble_sort(int arr[], int n){
    int temp;
    for(int i=0;i<n-1;i++){
        for(int j=0;j<n-i-1;j++){
          if(arr[j]>arr[j+1]){
            swap(arr[j],arr[j+1]);
          }
        }
    }
}

int main(){
    int n = 5;
    int arr[] = {5, 2, 4, 6, 7};
    for(int i = 0; i < n; i++){
        cout << arr[i] << " ";
    }
    cout << "\n===============\n";
    bubble_sort(arr, n);
    for(int i = 0; i < n; i++){
        cout << arr[i] << " ";
    }
    return 0;
}
