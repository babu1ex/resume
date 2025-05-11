class Node:
    
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
        
        def __init__(self):
            self.node_dict = {}
            self.head = Node( 'head', None)
            self.tail = Node( 'tail', None)
            self.head.next = self.tail
            self.tail.prev = self.head

        def append(self, key, value):
            end_node = self.tail.prev 
            new_node = Node(key, value)
            self.node_dict[key] = new_node
            new_node.prev = end_node
            new_node.next = self.tail
            end_node.next = new_node
            self.tail.prev = new_node

        def delete_key(self, key):
            node = self.node_dict[key]
            if node != self.head and node != self.tail:
                node_prev = node.prev
                node_next = node.next
                node_prev.next = node_next
                node_next.prev = node_prev
                self.node_dict.pop(key)

        def move_to_end(self ,node):
            if node.next != self.tail:
                node.prev.next = node.next
                node.next.prev = node.prev
                self.tail.prev.next = node
                node.prev = self.tail.prev
                node.next = self.tail
                self.tail.prev = node

        def get(self, key):
            if key in self.node_dict:
                get_node = self.node_dict[key]
                self.move_to_end(get_node)
                return get_node.value
            else:
                return None
        
        def remove_from_front(self):
            old_node = self.head.next
            self.head.next = old_node.next
            old_node.next.prev = self.head
            self.node_dict.pop(old_node.key)
            return old_node.key