#include <iostream>
using namespace std ;
class Rectangle {
  private:
  float length;
  float width;
  public: 
  void setlen(float len, float wid){
    if (len > 0) {
      length = len;
    } else {
      cout << "error invalid number" << endl;
    }
    if (wid > 0) {
      width = wid;
    } else {
      cout << "error invalid number" << endl;
    }
  }
   float  area() {
    return width * length;
  }
};
;
int main() {
  float len;
  float wid;
  cout << "enter your length: ";
  cin >> len;
  cout << "\nenter your width: ";
  cin >> wid;
  
  Rectangle rect;
  rect.setlen(len, wid);
  cout << "The area is: " << rect.area() << endl;
  
  return 0;
}