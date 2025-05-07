#include <iostream>
using namespace std;

class Student{
private:
string name ;
int ID ;
int age ;
public:
Student(string Name, int id, int Age  ){
name = Name;
ID = id ;
age = Age ; }

string get_name(){
    return name ;
}
void set_name(string N){
    name=N;
}

void info(){
    cout<<"the name : "<<name;
    cout<<"\nthe id : "<<ID;
    cout<<"\nthe age : "<<age<<endl;
}
};
int main(){
    Student s1 = Student("mohamed",320,18);
    s1.info();
    s1.set_name("bassem");
    s1.info();
}