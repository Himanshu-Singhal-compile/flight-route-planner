class Queue:
    class Node:
        def __init__(self,value):
            self.value=value
            self.next=None
        
        def __repr__(self):
            return str(self.value)
    
    def __init__(self):
        self.head=None
        self.tail=None
        self.size=0
    
    def enqueue(self,value):
        new_node=self.Node(value)
        if self.size==0:
            self.head=new_node
        else:
            self.tail.next=new_node
        self.tail=new_node
        self.size+=1

    def dequeue(self):
        if self.size==0:
            return None
        else:
            node=self.head
            self.head=self.head.next
            if self.size==1:
                self.tail=None
            value=node.value
            self.size-=1
            return value
        
    def isNotEmpty(self):
        return self.size!=0
    
    def __str__(self):
        a=""
        node=self.head
        while node is not None:
            a+=f' {node.value} #'
            node=node.next
        return a
        

if __name__=="__main__":
    q=Queue()
    q.enqueue(2)
    q.dequeue()
    q.enqueue(3)
    q.enqueue(4)
    q.enqueue(5)
    print(q.dequeue())
    # print(q.dequeue())
    print(q)



    
