    #include <iostream>
    using namespace std ;
    class Node{
    public:
    int data ;
    Node* next;
    };
    class Linkedlist{
    public:
    Node*head ;
    Linkedlist(){
        head = NULL;
    }
    bool isempty(){
        return (head== NULL);
    }

    void insert(int item){
        Node* newnode = new Node();
        newnode->data = item;
        if (isempty()){
            newnode->next = NULL;
            head = newnode;
        }else {
            newnode->next = head ;
            head = newnode;
        }
    }
    void display(){
        Node * temp = head ;
        while(temp != NULL){
            cout<<"|"<<temp->data<<"|"<<"->"<<" ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }
    int count(){
        int counter = 0;
        Node* temp = head ;
        while(temp!=NULL){
            counter++;
            temp = temp->next;
        }return counter;
    }
    bool isfound(int key){
        Node* temp = head;
        while(temp!=NULL){
            if(temp->data == key){
                return true;
            }
            temp = temp->next;
        }   return false;
    }

    void insertbefore(int item,int newvalue){
    if (isfound(item)){
    Node* newnode = new Node();
    newnode->data = newvalue;
    Node* temp = head;
    while(temp != NULL && temp->next->data != item){
        temp = temp->next;
    } 
        newnode->next = temp->next;
        temp->next = newnode; 
    }else {
        cout<<" not found "<<endl;
    }
    }

    void append(int newvalue){
        if(isempty()){
            insert(newvalue);
        }else{
            Node*temp = head;
            while(temp->next != NULL){
                temp = temp->next;
            }
            Node* newnode = new Node();
            newnode->data = newvalue;
            temp->next = newnode;
            newnode->next = NULL;
        }
    }

    void Delete(int key){
        if(head == NULL){
            cout<<" the list is empty ";
        }
        Node* temp = head ;
        Node* prev = NULL;
        if (temp !=NULL && temp->data == key){
            head = temp->next;
            delete temp;
            return;
        }
        while(temp != NULL && temp->data != key){
            prev = temp;
            temp = temp->next;}

        if (temp ==NULL){
            cout<<"your item  is not found ";
            }
        prev->next = temp->next;
        delete temp;
        
    }

    void reverse(){
        Node* next = NULL;
        Node* prev = NULL;
        Node* temp = head;
        while(temp != NULL){
            next = temp->next;
            temp->next = prev;
            prev = temp ;
            temp = next ; 
        }head = prev;   
    }

    };
    int main(){
        Linkedlist lst ;
        lst.insert(5);
        lst.insert(8);
        lst.insertbefore(5,3);
        lst.append(7);
        lst.Delete(8);
        lst.Delete(3);
        cout << "Count: " << lst.count() << endl;
        cout << "Is 5 found? " << (lst.isfound(5) ? "Yes" : "No") << endl;
        if(lst.isempty()){
            cout<<"your list is empty .";
        }else {
            lst.display();
        }
    }
/*    
#include <iostream>
using namespace std ;
class Node{
     public:
     int data;
     Node* next;
     Node* prev;
};
class linkedlist{
    public:
    Node* head;
    linkedlist(){
        head = NULL;
    }

    bool isempty(){
        return(head == NULL);
    }
 
    void insert(int value){
         Node* newnode = new Node();
         newnode->data = value;
         if(isempty()){
            newnode->next = newnode;
            newnode->prev = newnode;
            head = newnode;
         }else{
            Node* temp = head;
            while(temp->next!=head){
                temp = temp->next;
            }
            newnode->next = head;
            newnode->prev = temp;
            temp->next = newnode;
            head->prev = newnode;
            head = newnode;
        }
    }
    void display(){
        if(head==NULL){
            cout<<"the list is empty."<<endl;
        }
        Node* temp = head ;
        cout<<" forward ";
        do{
            cout<<"|"<<temp->data<<"|"<<" ->  ";
            temp = temp->next;
        }while(temp!=head);
        cout<<endl;

    }
    int count(){
        int counter = 0;
        Node* temp = head;
        do{
            counter++;
            temp =temp->next;
        }while(temp!=head);
    return counter;
   }
   void append(int value){
    Node* newnode = new Node();
    newnode->data = value;
    Node* last = head->prev;
    newnode->next = head;
    newnode->prev = last;
    last->next = newnode;   
    head->prev = newnode;   
  }
};
int main(){
    linkedlist lst ;
    lst.insert(5);
    lst.insert(8);
    lst.append(7);
    cout<<"count : "<<lst.count()<<endl;
    if(lst.isempty()){
        cout<<"your list is empty.";
    }else{
        lst.display();
    }
}*/