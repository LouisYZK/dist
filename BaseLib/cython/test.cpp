#include <iostream>
#include <string>
#include <stdlib.h>
#include "stack.h"
using namespace std ;

double square(double x){
	return x*x;
}
void pring_square(double x){
	cout << square(x) <<endl;
}

void print_string(string s){
	string ss = s;
	string s3 = "C++";
	string s4 = s + s3;
	cout << "ss:"<<ss<<endl;
	cout << "s3:"<<s3<<endl;
	cout << "s4:"<<s4<<endl;
	cout << "pick:"<<ss[1]<<endl;
}

void test_struct(){
	struct Books{
		string title;
		string author;
		int id;
	};
	Books b;
	b.title = "Java";
	b.author = "John Snow";
}

class Box{
	public:
		double length;
		double height;
		double width;
		// double getVolume()
		void setLength(double length);
		void setHeight(double height);
		void setWidth(double width);
		double getVolume(void);
		Box(double l = 1.0, double h = 2.0, double w = 3.0){
			this->length = l;
			this->height = h;
			this->width = w;
		}
		~Box(void){
			cout << "The Box object is eliminated!" <<endl;
		}
};
void Box::setLength(double length){
	this->length = length;
}
void Box::setWidth(double width){
	width = width;
}
void Box::setHeight(double height){
	height = height;
}
double Box::getVolume(){
	return this->length * this->height * this->width;
}
int main()
{	
	double x =  0.01;
	pring_square(x);
	string s = "Hello";
	print_string(s);
	printf("%s\n", "Hello C++!"); // C is also okay!
	// test_struct();
	Box box;
	// box.setHeight(1.0);
	// box.setLength(2.0);
	// box.setWidth(3.0);
	cout << "The Box's getVolume is: " << box.getVolume() <<endl;
	stack<int> S;
	S.push(1);
	S.push(100);
	S.push(77);
	while(!S.isempty()){
		cout << S.pop() <<" in the stack!"<<endl;
	}
    return 0;
}