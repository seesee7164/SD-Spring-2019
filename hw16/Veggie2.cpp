#include<iostream>
using namespace std;
class Veggie{
    public:
    int calories;
    Veggie(int x):calories(x){};
};
int main(){
    Veggie carrot(100);
    cout << carrot.calories;
}