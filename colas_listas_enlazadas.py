from abc import ABC, abstractmethod


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


class Node:
    def __init__(self, info):
        self.info = info
        self.next = None


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


class LinkedQueue(QueueInterface):
    def __init__(self):
        self.top = None
        self.tail = None
        self._size = 0

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
        if self.is_empty():
            self.top = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        removed_info = self.top.info
        self.top = self.top.next
        self._size -= 1
        if self.is_empty():
            self.tail = None
        return removed_info

    def remove_at(self, pos: int):
        if pos < 1 or pos > self._size:
            print(f"     Posición {pos} fuera de rango.")
            return None
        if pos == 1:
            return self.dequeue()
        prev_node = self.top
        for _ in range(pos - 2):
            prev_node = prev_node.next
        target_node = prev_node.next
        prev_node.next = target_node.next
        if target_node == self.tail:
            self.tail = prev_node
        self._size -= 1
        return target_node.info

    def get_nth(self, pos: int):
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

    def print_info(self):
        print("********* QUEUE DUMP *********")
        print(f"   Size: {self.size()}")
        current_node = self.top
        count = 1
        while current_node is not None:
            print(f"   ** Element {count}")
            if hasattr(current_node.info, 'print_order'):
                current_node.info.print_order()
            else:
                print(current_node.info)
            current_node = current_node.next
            count += 1
        print("******************************")


def menu():
    print("\n=============================")
    print("  GESTOR DE COLA DE PEDIDOS  ")
    print("=============================")
    print("  1. Insertar pedido (enqueue)")
    print("  2. Quitar del frente (dequeue)")
    print("  3. Eliminar por posición")
    print("  4. Ver frente (front)")
    print("  5. Obtener pedido por posición")
    print("  6. Mostrar toda la cola")
    print("  0. Salir")
    print("-----------------------------")


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("     Por favor ingresa un número válido.")


if __name__ == "__main__":
    queue = LinkedQueue()

    while True:
        menu()
        opcion = input("  Elige una opción: ").strip()

        if opcion == "1":
            customer = input("     Nombre del cliente: ").strip()
            if not customer:
                print("     El nombre no puede estar vacío.")
                continue
            qtty = input_int("     Cantidad: ")
            queue.enqueue(Order(qtty, customer))
            print(f"     Pedido de '{customer}' insertado al final de la cola.")

        elif opcion == "2":
            removed = queue.dequeue()
            if removed:
                print(f"     Pedido atendido:")
                removed.print_order()
            else:
                print("     La cola está vacía.")

        elif opcion == "3":
            if queue.is_empty():
                print("     La cola está vacía.")
                continue
            queue.print_info()
            pos = input_int("     Posición a eliminar: ")
            removed = queue.remove_at(pos)
            if removed:
                print(f"     Pedido eliminado:")
                removed.print_order()

        elif opcion == "4":
            frente = queue.front()
            if frente:
                print("     Pedido al frente:")
                frente.print_order()
            else:
                print("     La cola está vacía.")

        elif opcion == "5":
            if queue.is_empty():
                print("     La cola está vacía.")
                continue
            pos = input_int(f"     Posición (1 - {queue.size()}): ")
            pedido = queue.get_nth(pos)
            if pedido:
                print(f"     Pedido en posición {pos}:")
                pedido.print_order()
            else:
                print("     Posición fuera de rango.")

        elif opcion == "6":
            queue.print_info()

        elif opcion == "0":
            print("\n     Hasta luego.\n")
            break

        else:
            print("     Opción no válida, intenta de nuevo.")
