def es_numero(token):
    """Función auxiliar para verificar si un token es un número (entero o decimal)."""
    try:
        float(token)
        return True
    except ValueError:
        return False

def evaluar_posfija(expresion):
    """
    Evalúa una expresión aritmética en notación posfija (ej. '3 4 + 2 *').
    Se lee de izquierda a derecha.
    """
    pila = []
    tokens = expresion.split()
    
    for token in tokens:
        if es_numero(token):
            # Si es un operando, lo apilamos (push)
            pila.append(float(token))
        else:
            # Si es un operador, desapilamos (pop) los dos últimos operandos
            # Nota: el primer elemento que sacamos es el operando DERECHO
            op2 = pila.pop()
            op1 = pila.pop()
            
            if token == '+':
                pila.append(op1 + op2)
            elif token == '-':
                pila.append(op1 - op2)
            elif token == '*':
                pila.append(op1 * op2)
            elif token == '/':
                pila.append(op1 / op2)
            else:
                raise ValueError(f"Operador no soportado: {token}")
                
    # El resultado final será el único elemento restante en la pila
    return pila.pop()


def evaluar_prefija(expresion):
    """
    Evalúa una expresión aritmética en notación prefija (ej. '* + 3 4 2').
    Se lee de derecha a izquierda.
    """
    pila = []
    tokens = expresion.split()
    
    # Invertimos la lista de tokens para evaluarla de derecha a izquierda
    for token in reversed(tokens):
        if es_numero(token):
            pila.append(float(token))
        else:
            # Si es un operador, desapilamos los dos últimos operandos
            # Nota: al leer al revés, el primer elemento que sacamos es el operando IZQUIERDO
            op1 = pila.pop()
            op2 = pila.pop()
            
            if token == '+':
                pila.append(op1 + op2)
            elif token == '-':
                pila.append(op1 - op2)
            elif token == '*':
                pila.append(op1 * op2)
            elif token == '/':
                pila.append(op1 / op2)
            else:
                raise ValueError(f"Operador no soportado: {token}")
                
    return pila.pop()

# ==========================================
# Ejemplos de uso
# ==========================================
if __name__ == "__main__":
    # Expresión infija equivalente: (3 + 4) * 2 = 14
    expr_posfija = "3 4 + 2 *"
    expr_prefija = "* + 3 4 2"
    
    # Expresión infija equivalente: 5 * (6 - 2) / 4 = 5.0
    expr_posfija_2 = "5 6 2 - * 4 /"
    expr_prefija_2 = "/ * 5 - 6 2 4"

    print("--- Evaluación Posfija ---")
    print(f"Expresión: {expr_posfija}  => Resultado: {evaluar_posfija(expr_posfija)}")
    print(f"Expresión: {expr_posfija_2} => Resultado: {evaluar_posfija(expr_posfija_2)}")
    
    print("\n--- Evaluación Prefija ---")
    print(f"Expresión: {expr_prefija}  => Resultado: {evaluar_prefija(expr_prefija)}")
    print(f"Expresión: {expr_prefija_2} => Resultado: {evaluar_prefija(expr_prefija_2)}")
    
