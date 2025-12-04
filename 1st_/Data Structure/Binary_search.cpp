#include<iostream>

struct Node{
    int data;
    Node* left;
    Node* right;
    Node(int val){
        data = val;
        left = nullptr;
        right = nullptr;
    }
};

class binaryTree{
public:
    binaryTree(){
        root = NULL;
    }
    void Insert(int val){
        root = Insert(root, val);
    }

    Node* Search(int val){
        Node* temp = root;
        while(temp != NULL){
            if(temp -> data == val){
                std::cout << "Found" << temp->data << std::endl;
                return temp;
            }
            else if(val < temp ->data){
                std::cout << temp->data<< "->";
                temp = temp -> left;
                
            }
            else{
                std::cout << temp->data<< "->";
                temp = temp -> right;
                
            }
        }
        std::cout << "Not Found" << std::endl;
        return NULL;
    }

    void Delete(int val){
        Node* curr;
        Node* parent;
        curr = root;
        parent = nullptr;
        while(curr != NULL && curr ){
            parent = curr;
            if(val < curr -> data){
                curr = curr -> left;
            }
            else{
                curr = curr -> right;
            }
        }
        if(curr -> left == NULL && curr -> right == NULL){
            if(parent -> left == curr){
                parent -> left = NULL;
            }
            else{
                parent-> right = NULL;
            }
            delete curr;
        }
        else if(curr -> left == NULL){
            if(parent -> left == curr){
                parent -> left = curr -> right;
            }
            else{
                parent -> right = curr -> right;
            }
            delete curr;
        }
        else if(curr -> right == NULL){
            if(parent -> left == curr){
                parent -> left = curr -> right;
            }
            else{
                parent -> right = curr -> right;
            }
            delete curr;
        }
        else{
            Node * Child;
            Node * Successor;
            Child = curr -> right;
            while(Child -> left != NULL){
                Child = Child -> left;
            }
            curr->data = Child->data;
            delete Child;
        }

    }


private:
    Node* root;
    Node* Insert(Node* root, int val){
        if(root == NULL){
            return new Node(val);
        }
        if(val < root -> data){
            root -> left = Insert(root -> left, val);
        }
        else{
            root -> right = Insert(root -> right, val); 
        }
        return root;
    }
    Node* Delete(Node* root, int val){
        if(root == NULL){ return root; }
        if(val < root->data){Delete(root->left, val);}
        else if(val > root->data){Delete(root->right, val);}
        else{
            if(root -> left == NULL && root -> right == NULL){
                delete root;
                return NULL;
            }
            else if(root -> left == NULL){
                
            }
        }
        return root;
    }
};

int main(){
    binaryTree bt;
    bt.Insert(5);
    bt.Insert(1);
    bt.Insert(3);

    bt.Search(3);
    bt.Delete(3);
    bt.Search(3);


    return 0;
    
}
