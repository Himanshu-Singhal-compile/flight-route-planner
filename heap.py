class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    
    def __init__(self, comparison_function):
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        
        # Write your code here
        self.compare=comparison_function
        self.data=[]

        # for i in range(self.parent(len(init_array)-1),-1,-1):
        #     self.downheap(i)
        
    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        self.data.append(value)
        self.upheap(len(self.data)-1)
    
    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        self.swap(0,len(self.data)-1)
        top=self.data[len(self.data)-1]
        self.data.pop()
        self.downheap(0)
        return top
    
    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        
        # Write your code here
        if self.data:
            return self.data[0]
        else:
            return None
    
    # You can add more functions if you want to
    def parent(self,i):
        return (i-1)//2
    
    def left_child(self,i):
        return 2*i+1
    
    def right_child(self,i):
        return 2*i+2
    
    def has_left_child(self,i):
        return self.left_child(i)<len(self.data)

    def has_right_child(self,i):
        return self.right_child(i)<len(self.data)
    
    def swap(self,i,j):
        self.data[i],self.data[j]=self.data[j],self.data[i]

    def downheap(self,i):
        if self.has_left_child(i):
            if self.has_right_child(i):
                if self.compare(self.data[self.right_child(i)],self.data[self.left_child(i)]):
                    small_child=self.right_child(i)
                else:
                    small_child=self.left_child(i)
            else:
                small_child=self.left_child(i)
        else:
            return
        if small_child and not self.compare(self.data[i],self.data[small_child]):
            self.swap(i,small_child)
            self.downheap(small_child)

    def upheap(self,i):
        parent=self.parent(i)
        if i>0 and self.compare(self.data[i],self.data[parent]):
            self.swap(i,parent)
            self.upheap(parent)


