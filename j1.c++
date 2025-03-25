#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;
};

class Linkedlist {
public:
    Node* head;

    Linkedlist() {
        head = NULL;
    }

    ~Linkedlist() {  
        Node* temp;
        while (head != NULL) {
            temp = head;
            head = head->next;
            delete temp;
        }
    }

    bool isempty() {
        return (head == NULL);
    }

    void insert(int item) {
        Node* newnode = new Node();
        newnode->data = item;
        newnode->next = head;
        head = newnode;
    }

    void display() {
        Node* temp = head;
        while (temp != NULL) {
            cout << temp->data << " ";
            temp = temp->next;
        }
        cout << endl;
    }

    int count() {
        int counter = 0;
        Node* temp = head;
        while (temp != NULL) {
            counter++;
            temp = temp->next;
        }
        return counter;
    }

    bool isfound(int key) {
        Node* temp = head;
        while (temp != NULL) {
            if (temp->data == key) {
                return true;
            }
            temp = temp->next;
        }
        return false;
    }

    void insertbefore(int item, int newvalue) {
        if (head == NULL) {
            cout << "List is empty." << endl;
            return;
        }
        
        if (head->data == item) { 
            insert(newvalue);
            return;
        }

        Node* temp = head;
        while (temp->next != NULL && temp->next->data != item) {
            temp = temp->next;
        }

        if (temp->next == NULL) {
            cout << "Not found" << endl;
            return;
        }

        Node* newnode = new Node();
        newnode->data = newvalue;
        newnode->next = temp->next;
        temp->next = newnode;
    }

    void append(int newvalue) {
        Node* newnode = new Node();
        newnode->data = newvalue;
        newnode->next = NULL;

        if (isempty()) {
            head = newnode;
            return;
        }

        Node* temp = head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = newnode;
    }

    void Delete(int key) {
        if (head == NULL) {
            cout << "The list is empty" << endl;
            return;
        }

        if (head->data == key) { 
            Node* temp = head;
            head = head->next;
            delete temp;
            return;
        }

        Node* temp = head;
        Node* prev = NULL;
        while (temp != NULL && temp->data != key) {
            prev = temp;
            temp = temp->next;
        }

        if (temp == NULL) {
            cout << "Key not found" << endl;
            return;
        }

        prev->next = temp->next;
        delete temp;
    }
};

int main() { 
    Linkedlist list;

    if (list.isempty()) {
        cout << "The list is empty" << endl;
    } else {
        cout << "The list is not empty" << endl;
    }

    list.insert(5);
    list.insert(8);
    list.insertbefore(5, 3);
    list.append(7);
    list.Delete(8);
    list.Delete(3);

    if (list.isfound(5)) {
        cout << "5 is found in the list." << endl;
    } else {
        cout << "5 is not found in the list." << endl;
    }

    list.display();
    cout << "Total count: " << list.count() << endl;

    return 0;
}
