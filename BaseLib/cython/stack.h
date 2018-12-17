template <class T> class stack{
	public:
		stack();
		~stack();
		T pop();
		bool isempty();
		void push(T t);
	protected:
		int maxsize;
		int size;
		T* s;
};
template <class T> stack<T>::stack(){
	maxsize = 100;
	size = 0;
	s = new T[maxsize];
}
template <class T> stack<T>::~stack(){
	delete [] s;
}
template <class T> void stack<T>::push(T t){
	size ++;
	s[size -1] = t;
}
template <class T> T stack<T>::pop(){
	size--;
	return s[size];
}
template <class T> bool stack<T>::isempty(){
	return size ==0;
}