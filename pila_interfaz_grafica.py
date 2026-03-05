import tkinter as tk
from tkinter import messagebox

# ─── Colores y estilo ────────────────────────────────────────────────
BG        = "#0f0f1a"
PANEL     = "#1a1a2e"
ACCENT    = "#e94560"
GREEN     = "#00d4aa"
YELLOW    = "#f5a623"
TEXT      = "#e0e0f0"
MUTED     = "#5a5a7a"
BLOCK_CLR = ["#e94560","#f5a623","#00d4aa","#7c5cbf","#3a86ff","#ff6b6b","#06d6a0"]

# ─── Lógica de la pila ───────────────────────────────────────────────
class Pila:
    def __init__(self):
        self.elementos = []

    def push(self, val):
        self.elementos.append(val)

    def pop(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop()

    def peek(self):
        if self.esta_vacia():
            return None
        return self.elementos[-1]

    def esta_vacia(self):
        return len(self.elementos) == 0

    def tamanio(self):
        return len(self.elementos)


# ─── Aplicación gráfica ──────────────────────────────────────────────
class AppPila:
    MAX = 8          # máximo de elementos visibles

    def __init__(self, root):
        self.root = root
        self.root.title("⟨ Visualizador de Pila ⟩")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.pila = Pila()
        self.ultimo_op = tk.StringVar(value="Bienvenido  →  usa PUSH o POP")

        self._construir_ui()
        self._dibujar()

    # ── Layout ──────────────────────────────────────────────────────
    def _construir_ui(self):
        # Título
        tk.Label(self.root, text="P I L A   ( S T A C K )",
                 bg=BG, fg=ACCENT,
                 font=("Courier New", 18, "bold")).pack(pady=(20, 4))

        tk.Label(self.root, text="Estructura LIFO  —  Last In, First Out",
                 bg=BG, fg=MUTED,
                 font=("Courier New", 9)).pack(pady=(0, 12))

        # Frame principal
        main = tk.Frame(self.root, bg=BG)
        main.pack(padx=30, pady=0)

        # Canvas de la pila
        self.canvas = tk.Canvas(main, width=240, height=380,
                                bg=PANEL, highlightthickness=2,
                                highlightbackground=ACCENT)
        self.canvas.grid(row=0, column=0, padx=(0, 24))

        # Panel derecho: info + controles
        right = tk.Frame(main, bg=BG)
        right.grid(row=0, column=1, sticky="n")

        # Info
        info_frame = tk.Frame(right, bg=PANEL, bd=0, relief="flat",
                              highlightthickness=1,
                              highlightbackground=MUTED)
        info_frame.pack(fill="x", pady=(0, 16))

        tk.Label(info_frame, text="ESTADO", bg=PANEL, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", padx=12, pady=(8,0))

        self.lbl_tam   = self._stat(info_frame, "Tamaño",  "0")
        self.lbl_tope  = self._stat(info_frame, "Tope",    "—")
        self.lbl_vacia = self._stat(info_frame, "¿Vacía?", "Sí")

        # Entrada + botones
        ctrl = tk.Frame(right, bg=BG)
        ctrl.pack(fill="x")

        tk.Label(ctrl, text="Valor:", bg=BG, fg=TEXT,
                 font=("Courier New", 10)).pack(anchor="w")

        self.entrada = tk.Entry(ctrl, width=18,
                                font=("Courier New", 12, "bold"),
                                bg=PANEL, fg=GREEN,
                                insertbackground=GREEN,
                                relief="flat",
                                highlightthickness=1,
                                highlightbackground=ACCENT)
        self.entrada.pack(fill="x", ipady=6, pady=(4, 12))
        self.entrada.bind("<Return>", lambda e: self._push())

        self._btn(ctrl, "▲  PUSH", GREEN,  self._push)
        self._btn(ctrl, "▼  POP",  ACCENT, self._pop)
        self._btn(ctrl, "↺  LIMPIAR", MUTED, self._limpiar)

        # Mensaje de operación
        op_frame = tk.Frame(right, bg=PANEL, highlightthickness=1,
                            highlightbackground=MUTED)
        op_frame.pack(fill="x", pady=(16, 0))

        tk.Label(op_frame, text="ÚLTIMA OPERACIÓN", bg=PANEL, fg=MUTED,
                 font=("Courier New", 7, "bold")).pack(anchor="w", padx=12, pady=(8,0))
        tk.Label(op_frame, textvariable=self.ultimo_op,
                 bg=PANEL, fg=YELLOW,
                 font=("Courier New", 9),
                 wraplength=170, justify="left").pack(anchor="w",
                                                      padx=12, pady=(2, 10))

        # Historial
        tk.Label(right, text="HISTORIAL", bg=BG, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", pady=(14, 2))

        hist_frame = tk.Frame(right, bg=PANEL, highlightthickness=1,
                              highlightbackground=MUTED)
        hist_frame.pack(fill="x")

        self.historial = tk.Text(hist_frame, width=22, height=6,
                                 bg=PANEL, fg=MUTED,
                                 font=("Courier New", 8),
                                 relief="flat", state="disabled",
                                 insertbackground=TEXT)
        self.historial.pack(padx=8, pady=8)

    def _stat(self, parent, label, valor):
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", padx=12, pady=2)
        tk.Label(row, text=f"{label}:", bg=PANEL, fg=MUTED,
                 font=("Courier New", 9), width=8, anchor="w").pack(side="left")
        lbl = tk.Label(row, text=valor, bg=PANEL, fg=TEXT,
                       font=("Courier New", 9, "bold"), anchor="w")
        lbl.pack(side="left")
        return lbl

    def _btn(self, parent, texto, color, cmd):
        b = tk.Button(parent, text=texto, command=cmd,
                      bg=color, fg=BG,
                      font=("Courier New", 10, "bold"),
                      relief="flat", cursor="hand2",
                      activebackground=TEXT, activeforeground=BG,
                      padx=10, pady=7)
        b.pack(fill="x", pady=3)

    # ── Dibujo del canvas ────────────────────────────────────────────
    def _dibujar(self):
        self.canvas.delete("all")
        W, H = 240, 380
        BLOCK_H, BLOCK_W, MARGIN = 38, 180, 30

        # Base
        self.canvas.create_rectangle(MARGIN, H - 24, W - MARGIN, H - 18,
                                     fill=ACCENT, outline="")

        # Paredes
        self.canvas.create_rectangle(MARGIN, 20, MARGIN + 6, H - 18,
                                     fill=MUTED, outline="")
        self.canvas.create_rectangle(W - MARGIN - 6, 20, W - MARGIN, H - 18,
                                     fill=MUTED, outline="")

        elementos = self.pila.elementos
        n = len(elementos)

        # Zona vacía
        if n == 0:
            self.canvas.create_text(W // 2, H // 2,
                                    text="vacía", fill=MUTED,
                                    font=("Courier New", 13, "italic"))

        # Bloques (de abajo hacia arriba)
        for i, val in enumerate(elementos):
            if i >= self.MAX:
                break
            y2 = H - 24 - i * (BLOCK_H + 4)
            y1 = y2 - BLOCK_H
            x1, x2 = MARGIN + 6, W - MARGIN - 6
            color = BLOCK_CLR[i % len(BLOCK_CLR)]

            # Sombra
            self.canvas.create_rectangle(x1 + 3, y1 + 3, x2 + 3, y2 + 3,
                                         fill="#0a0a14", outline="")
            # Bloque
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         fill=color, outline="")

            # Índice
            self.canvas.create_text(x1 + 12, (y1 + y2) // 2,
                                    text=str(i), fill=BG,
                                    font=("Courier New", 7), anchor="w")

            # Valor
            txt = str(val)
            if len(txt) > 12:
                txt = txt[:11] + "…"
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                    text=txt, fill=BG,
                                    font=("Courier New", 11, "bold"))

            # Etiqueta TOPE
            if i == n - 1:
                self.canvas.create_text(W - MARGIN + 2, (y1 + y2) // 2,
                                        text="◀ TOPE", fill=YELLOW,
                                        font=("Courier New", 7, "bold"),
                                        anchor="w")

        # Elementos extra no mostrados
        if n > self.MAX:
            self.canvas.create_text(W // 2, 12,
                                    text=f"+{n - self.MAX} más…",
                                    fill=MUTED,
                                    font=("Courier New", 8))

        # Actualizar etiquetas de estado
        self.lbl_tam.config(text=str(n))
        tope = self.pila.peek()
        self.lbl_tope.config(text=str(tope) if tope is not None else "—")
        self.lbl_vacia.config(text="Sí" if self.pila.esta_vacia() else "No",
                               fg=GREEN if self.pila.esta_vacia() else ACCENT)

    # ── Operaciones ──────────────────────────────────────────────────
    def _push(self):
        val = self.entrada.get().strip()
        if not val:
            messagebox.showwarning("Sin valor", "Escribe un valor para hacer PUSH.")
            return
        if self.pila.tamanio() >= 20:
            messagebox.showwarning("Pila llena", "La pila ha alcanzado el límite (20).")
            return
        self.pila.push(val)
        self.ultimo_op.set(f"PUSH  →  '{val}' agregado al tope")
        self._log(f"PUSH  '{val}'")
        self.entrada.delete(0, "end")
        self._dibujar()

    def _pop(self):
        val = self.pila.pop()
        if val is None:
            messagebox.showinfo("Pila vacía", "No hay elementos para hacer POP.")
            return
        self.ultimo_op.set(f"POP   ←  '{val}' retirado del tope")
        self._log(f"POP   '{val}'")
        self._dibujar()

    def _limpiar(self):
        if messagebox.askyesno("Limpiar", "¿Vaciar toda la pila?"):
            self.pila = Pila()
            self.ultimo_op.set("Pila limpiada")
            self._log("--- LIMPIAR ---")
            self._dibujar()

    def _log(self, msg):
        self.historial.config(state="normal")
        self.historial.insert("end", msg + "\n")
        self.historial.see("end")
        self.historial.config(state="disabled")


# ─── Main ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = AppPila(root)
    root.mainloop()
