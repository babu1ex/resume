class Node:  # pylint: disable=too-few-public-methods

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

    def __str__(self):
        return f"Node({self.key}, {self.value})"


class DoublyLinkedList:

    def __init__(self):
        self.node_dict = {}
        self.head = Node('head', None)
        self.tail = Node('tail', None)
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

    def move_to_end(self, node):
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
        return None

    def remove_from_front(self):
        old_node = self.head.next
        self.head.next = old_node.next
        old_node.next.prev = self.head
        self.node_dict.pop(old_node.key)
        return old_node.key


class LRUCache:

    def __init__(self, limit=42):
        self.limit = limit
        self.linked_list = DoublyLinkedList()

    def set(self, key, value):
        if self.limit == 0:
            return
        if key in self.linked_list.node_dict:
            set_node = self.linked_list.node_dict[key]
            set_node.value = value
            self.linked_list.move_to_end(set_node)
        else:
            if len(self.linked_list.node_dict) >= self.limit:
                self.linked_list.remove_from_front()
            self.linked_list.append(key, value)

    def get(self, key):
        return self.linked_list.get(key)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)


cache = LRUCache(2)

cache.set("k1", "val1")
cache.set("k2", "val2")

assert cache.get("k3") is None
assert cache.get("k2") == "val2"
assert cache.get("k1") == "val1"

cache.set("k3", "val3")

assert cache.get("k3") == "val3"
assert cache.get("k2") is None
assert cache.get("k1") == "val1"
