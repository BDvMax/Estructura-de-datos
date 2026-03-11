"""
Sistema de Colas de Servicios - Compañía de Seguros
====================================================
Comandos:
  C <num_servicio>  → Cliente llega y solicita atención en el servicio indicado
  A <num_servicio>  → Agente atiende al próximo cliente en la cola del servicio
  L                 → Listar estado de todas las colas
  Q / SALIR         → Salir del sistema
"""

from collections import deque


# ──────────────────────────────────────────────
# Clase Cola
# ──────────────────────────────────────────────
class Cola:
    """Cola FIFO genérica con contador de tickets."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self._elementos: deque = deque()
        self._siguiente_ticket: int = 1

    # Agrega un nuevo cliente y retorna su número de atención
    def encolar(self) -> int:
        ticket = self._siguiente_ticket
        self._elementos.append(ticket)
        self._siguiente_ticket += 1
        return ticket

    # Retira y retorna el próximo número a atender (None si vacía)
    def desencolar(self) -> int | None:
        if self._elementos:
            return self._elementos.popleft()
        return None

    def esta_vacia(self) -> bool:
        return len(self._elementos) == 0

    def tamaño(self) -> int:
        return len(self._elementos)

    def proximos(self, n: int = 3) -> list[int]:
        """Retorna los próximos n tickets en espera (sin eliminarlos)."""
        return list(self._elementos)[:n]

    def __str__(self) -> str:
        return f"Cola '{self.nombre}' | En espera: {self.tamaño()}"


# ──────────────────────────────────────────────
# Configuración de servicios
# ──────────────────────────────────────────────
SERVICIOS = {
    1: "Emisión de Pólizas",
    2: "Siniestros y Reclamos",
    3: "Pagos y Facturación",
    4: "Atención al Cliente General",
    5: "Renovaciones",
}


# ──────────────────────────────────────────────
# Sistema principal
# ──────────────────────────────────────────────
class SistemaColas:
    def __init__(self):
        # Crear una Cola por cada servicio disponible
        self.colas: dict[int, Cola] = {
            num: Cola(nombre) for num, nombre in SERVICIOS.items()
        }

    # ── Comandos ──────────────────────────────

    def cliente_llega(self, num_servicio: int) -> None:
        if num_servicio not in self.colas:
            print(f"  ✗  Servicio {num_servicio} no existe.")
            return
        cola = self.colas[num_servicio]
        ticket = cola.encolar()
        print(
            f"\n  ✔  Bienvenido/a. Servicio: [{num_servicio}] {SERVICIOS[num_servicio]}"
        )
        print(f"     Su número de atención es: {ticket:03d}")
        print(f"     Clientes antes de usted : {cola.tamaño() - 1}")

    def atender_cliente(self, num_servicio: int) -> None:
        if num_servicio not in self.colas:
            print(f"  ✗  Servicio {num_servicio} no existe.")
            return
        cola = self.colas[num_servicio]
        ticket = cola.desencolar()
        if ticket is None:
            print(
                f"\n  ⚠  La cola del servicio [{num_servicio}] {SERVICIOS[num_servicio]} está vacía."
            )
        else:
            print(
                f"\n  📢  Llamando número {ticket:03d} — Servicio [{num_servicio}] {SERVICIOS[num_servicio]}"
            )
            if not cola.esta_vacia():
                proximos = cola.proximos(3)
                print(
                    f"     Próximos en espera: {', '.join(f'{t:03d}' for t in proximos)}"
                )

    def listar_colas(self) -> None:
        print("\n  ┌─────────────────────────────────────────────────┐")
        print("  │           ESTADO DE COLAS — SEGUROS S.A.        │")
        print("  ├────┬───────────────────────────────┬────────────┤")
        print("  │ N° │ Servicio                      │ En espera  │")
        print("  ├────┼───────────────────────────────┼────────────┤")
        for num, cola in self.colas.items():
            print(f"  │ {num:2d} │ {SERVICIOS[num]:<29} │ {cola.tamaño():^10} │")
        print("  └────┴───────────────────────────────┴────────────┘")

    # ── Loop principal ────────────────────────

    def ejecutar(self) -> None:
        self._bienvenida()
        while True:
            try:
                entrada = input("\n> ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                print("\n\nSistema detenido.")
                break

            if not entrada:
                continue

            partes = entrada.split()
            comando = partes[0]

            if comando in ("Q", "SALIR", "EXIT"):
                print("Sistema cerrado. ¡Hasta pronto!")
                break

            elif comando == "L":
                self.listar_colas()

            elif comando in ("C", "A") and len(partes) == 2:
                try:
                    num_servicio = int(partes[1])
                except ValueError:
                    print("  ✗  El número de servicio debe ser un entero.")
                    continue
                if comando == "C":
                    self.cliente_llega(num_servicio)
                else:
                    self.atender_cliente(num_servicio)

            else:
                print("  ✗  Comando no reconocido. Use C <n>, A <n>, L o Q.")

    # ── Helpers ───────────────────────────────

    @staticmethod
    def _bienvenida() -> None:
        print("=" * 55)
        print("    SISTEMA DE COLAS — COMPAÑÍA DE SEGUROS S.A.")
        print("=" * 55)
        print("Servicios disponibles:")
        for num, nombre in SERVICIOS.items():
            print(f"  [{num}] {nombre}")
        print("\nComandos:")
        print("  C <n>  →  Cliente llega al servicio n")
        print("  A <n>  →  Atender próximo cliente del servicio n")
        print("  L      →  Listar estado de las colas")
        print("  Q      →  Salir")
        print("-" * 55)


# ──────────────────────────────────────────────
# Punto de entrada
# ──────────────────────────────────────────────
if __name__ == "__main__":
    sistema = SistemaColas()
    sistema.ejecutar()


    
