from abc import ABC, abstractmethod

# 1. La clase Order (El Pedido)
class Order:
    def __init__(self, qtty: int, customer: str):
        self.customer = customer
        self.qtty = qtty

    def print_order(self):
        print(f"     Customer: {self.get_customer()}")
        print(f"     Quantity: {self.get_qtty()}")
        print("     ------------")

    def get_qtty(self):
        return self.qtty

    def get_customer(self):
        return self.customer


# 2. La clase Node (El eslabón)
class Node:
    def __init__(self, info):
        self.info = info  # El objeto que guardamos (un Order)
        self.next = None  # Apuntador al siguiente nodo


# 3. La interfaz QueueInterface
class QueueInterface(ABC):
    @abstractmethod
    def size(self) -> int: pass

    @abstractmethod
    def is_empty(self) -> bool: pass

    @abstractmethod
    def front(self): pass

    @abstractmethod
    def enqueue(self, info): pass

    @abstractmethod
    def dequeue(self): pass


# 4. La clase principal LinkedQueue
class LinkedQueue(QueueInterface):
    def __init__(self):
        self.top = None   # Cabeza de la cola (por donde salen)
        self.tail = None  # Final de la cola (por donde entran)
        self._size = 0    # Llevamos la cuenta para no tener que recorrerla

    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def front(self):
        if self.is_empty():
            return None
        return self.top.info

    def enqueue(self, info):
        new_node = Node(info)
        
        # Si la cola está vacía, el nuevo nodo es tanto el principio como el final
        if self.is_empty():
            self.top = new_node
            self.tail = new_node
        else:
            # Si ya hay elementos, lo enganchamos al final y actualizamos el 'tail'
            self.tail.next = new_node
            self.tail = new_node
            
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None
            
        # Guardamos la info del frente para devolverla
        removed_info = self.top.info
        
        # Avanzamos el top al siguiente nodo (el anterior se desconecta)
        self.top = self.top.next
        self._size -= 1
        
        # Si al sacar el elemento la cola quedó vacía, el tail también debe ser None
        if self.is_empty():
            self.tail = None
            
        return removed_info

    def print_info(self):
        print("********* QUEUE DUMP *********")
        print(f"   Size: {self.size()}")
        
        current_node = self.top
        count = 1
        
        while current_node is not None:
            print(f"   ** Element {count}")
            # Verificamos si el objeto guardado tiene el método print_order
            if hasattr(current_node.info, 'print_order'):
                current_node.info.print_order()
            else:
                print(current_node.info)
                
            current_node = current_node.next
            count += 1
            
        print("******************************")

    def get_nth(self, pos: int):
        # Validamos que la posición sea válida
        if pos < 1 or pos > self.size():
            return None
            
        current_node = self.top
        count = 1
        
        while current_node is not None:
            if count == pos:
                return current_node.info
            current_node = current_node.next
            count += 1
            
        return None


# 5. La prueba (Simulando el TestQueue main de Java)
if __name__ == "__main__":
    queue = LinkedQueue()
    
    # Creamos 4 pedidos
    order1 = Order(20, "cust1")
    order2 = Order(30, "cust2")
    order3 = Order(40, "cust3")
    order4 = Order(50, "cust4")
    
    # Encolamos los primeros 3
    print("\n--- Encolando pedidos 1, 2 y 3 ---")
    queue.enqueue(order1)
    queue.enqueue(order2)
    queue.enqueue(order3)
    queue.print_info()
    
    # Probamos front
    print(f"\n--- Probando front() ---")
    print(f"El elemento al frente es del cliente: {queue.front().get_customer()}")
    
    # Desencolamos uno
    print("\n--- Desencolando (dequeue) el primer elemento ---")
    despachado = queue.dequeue()
    print(f"Se atendió a: {despachado.get_customer()}")
    queue.print_info()
    
    # Encolamos un cuarto elemento
    print("\n--- Encolando pedido 4 ---")
    queue.enqueue(order4)
    queue.print_info()
    
    # Probamos obtener el n-ésimo (vamos a pedir el 3ro en la fila actual)
    print("\n--- Obteniendo el 3er elemento de la cola actual ---")
    tercero = queue.get_nth(3)
    if tercero:
        tercero.print_order()
    else:
        print("Posición no válida")
