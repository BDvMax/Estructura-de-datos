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
BLUE      = "#3a86ff"
PURPLE    = "#9b5de5"
BLOCK_CLR = ["#e94560","#f5a623","#00d4aa","#7c5cbf","#3a86ff","#ff6b6b","#06d6a0","#f15bb5"]

# ─── Lógica de la pila ───────────────────────────────────────────────
class Pila:
    def __init__(self, capacidad=8):
        self.elementos = []
        self.capacidad = capacidad

    def push(self, val):
        if self.esta_llena():
            return False, "OVERFLOW: La pila esta llena (Desbordamiento)."
        self.elementos.append(val)
        return True, val

    def pop(self):
        if self.esta_vacia():
            return False, "UNDERFLOW: La pila esta vacia (Subdesbordamiento)."
        val = self.elementos.pop()
        return True, val

    def peek(self):
        if self.esta_vacia():
            return None
        return self.elementos[-1]

    def esta_vacia(self):
        return len(self.elementos) == 0

    def esta_llena(self):
        return len(self.elementos) >= self.capacidad

    def tamanio(self):
        return len(self.elementos)


# ─── Secuencia ORIGINAL del problema (con error intencional) ─────────
#
#  a. PUSH X  → TOPE=1
#  b. PUSH Y  → TOPE=2
#  c. POP → Z="Y"   TOPE=1
#  d. POP → T="X"   TOPE=0
#  e. POP → ⚠ UNDERFLOW  (pila vacia)
#  f. PUSH V  → TOPE=1
#  g. PUSH W  → TOPE=2
#  h. POP → p="W"   TOPE=1
#  i. PUSH R  → TOPE=2
#
#  Resultado: PILA=["V","R"]  TOPE=2  Errores=1 (Underflow en e)
#
SECUENCIA_ORIGINAL = [
    ("PUSH", "X", 'a. Insertar(PILA, X)\nPUSH "X" se agrega X al tope.'),
    ("PUSH", "Y", 'b. Insertar(PILA, Y)\nPUSH "Y" se agrega Y al tope.'),
    ("POP",  "Z", 'c. Eliminar(PILA, Z)\nPOP -> Z recibe el valor del tope.'),
    ("POP",  "T", 'd. Eliminar(PILA, T)\nPOP -> T recibe el valor del tope.'),
    ("POP",  "U", 'e. Eliminar(PILA, U)\n⚠ POP con pila vacia -> UNDERFLOW.\nError: no hay elementos para extraer.'),
    ("PUSH", "V", 'f. Insertar(PILA, V)\nPUSH "V" se agrega V al tope.'),
    ("PUSH", "W", 'g. Insertar(PILA, W)\nPUSH "W" se agrega W al tope.'),
    ("POP",  "p", 'h. Eliminar(PILA, p)\nPOP -> p recibe el valor del tope.'),
    ("PUSH", "R", 'i. Insertar(PILA, R)\nPUSH "R" se agrega R al tope.'),
]

# ─── Secuencia CORREGIDA (sin ningun error) ───────────────────────────
#
#  Problema: en el paso e la pila estaba vacia (despues de sacar X e Y).
#  Solucion: insertar U antes de eliminarlo, y tambien insertar Z y T
#            antes de los pasos c y d para hacer la secuencia mas clara
#            y completamente autocontenida.
#
#  Pasos extra marcados con ★:
#    ★ PUSH "Z"  antes del paso c  (asegura que Z tenga un valor propio)
#    ★ PUSH "T"  antes del paso d  (asegura que T tenga un valor propio)
#    ★ PUSH "U"  antes del paso e  (evita el UNDERFLOW)
#
#  De esta forma cada variable que se quiere "guardar" via POP ya existe
#  en la pila cuando se ejecuta el Eliminar correspondiente.
#
#  Secuencia corregida completa:
#  a.  PUSH X  → TOPE=1
#  b.  PUSH Y  → TOPE=2
#  ★   PUSH Z  → TOPE=3   (extra: mete Z para que el POP-c lo obtenga)
#  c.  POP → Z="Z"   TOPE=2
#  ★   PUSH T  → TOPE=3   (extra: mete T para que el POP-d lo obtenga)
#  d.  POP → T="T"   TOPE=2
#  ★   PUSH U  → TOPE=3   (extra: evita Underflow en paso e)
#  e.  POP → U="U"   TOPE=2   ← ahora sin error
#  f.  PUSH V  → TOPE=3
#  g.  PUSH W  → TOPE=4
#  h.  POP → p="W"   TOPE=3
#  i.  PUSH R  → TOPE=4
#
#  Resultado: PILA=["X","Y","V","R"]  TOPE=4  Errores=0
#
SECUENCIA_CORREGIDA = [
    ("PUSH", "X",
     'a. Insertar(PILA, X)\nPUSH "X" se agrega X al tope.\n[igual al original]'),

    ("PUSH", "Y",
     'b. Insertar(PILA, Y)\nPUSH "Y" se agrega Y al tope.\n[igual al original]'),

    # ── Paso extra ★ ──────────────────────────────────────────────
    ("PUSH", "Z",
     u'\u2605 PASO EXTRA \u2014 Insertar(PILA, Z)\n'
     'PUSH "Z" se inserta Z en la pila ANTES\n'
     'de ejecutar el Eliminar(PILA,Z).\n'
     'Asi el POP del paso c tiene algo que extraer\n'
     'y Z recibe su propio valor.'),

    ("POP",  "Z",
     'c. Eliminar(PILA, Z)  \u2190 CORREGIDO\n'
     'POP -> Z = "Z"\n'
     u'\u2714 Sin error gracias al PUSH extra anterior.'),

    # ── Paso extra ★ ──────────────────────────────────────────────
    ("PUSH", "T",
     u'\u2605 PASO EXTRA \u2014 Insertar(PILA, T)\n'
     'PUSH "T" se inserta T en la pila ANTES\n'
     'de ejecutar el Eliminar(PILA,T).\n'
     'Asi el POP del paso d tiene algo que extraer.'),

    ("POP",  "T",
     'd. Eliminar(PILA, T)  \u2190 CORREGIDO\n'
     'POP -> T = "T"\n'
     u'\u2714 Sin error gracias al PUSH extra anterior.'),

    # ── Paso extra ★ ──────────────────────────────────────────────
    ("PUSH", "U",
     u'\u2605 PASO EXTRA \u2014 Insertar(PILA, U)\n'
     'PUSH "U" se inserta U en la pila ANTES\n'
     'de ejecutar el Eliminar(PILA,U).\n'
     'En el original la pila estaba VACIA aqui\n'
     'y se producia UNDERFLOW. Este PUSH lo evita.'),

    ("POP",  "U",
     'e. Eliminar(PILA, U)  \u2190 CORREGIDO\n'
     'POP -> U = "U"\n'
     u'\u2714 Sin error gracias al PUSH extra anterior.'),

    ("PUSH", "V",
     'f. Insertar(PILA, V)\nPUSH "V" se agrega V al tope.\n[igual al original]'),

    ("PUSH", "W",
     'g. Insertar(PILA, W)\nPUSH "W" se agrega W al tope.\n[igual al original]'),

    ("POP",  "p",
     'h. Eliminar(PILA, p)\nPOP -> p recibe el valor del tope.\n[igual al original]'),

    ("PUSH", "R",
     'i. Insertar(PILA, R)\nPUSH "R" se agrega R al tope.\n[igual al original]'),
]


# ─── Aplicacion grafica ──────────────────────────────────────────────
class AppPila:
    MAX = 8

    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Pila - Problema Academico")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.pila        = Pila(capacidad=8)
        self.ultimo_op   = tk.StringVar(value="Bienvenido -> usa PUSH / POP o ejecuta una Secuencia")
        self.paso_actual = 0
        self.errores     = []
        self.modo_seq    = "original"   # "original" | "corregida"

        self._construir_ui()
        self._dibujar()

    # ── Helpers ─────────────────────────────────────────────────────
    def _seq_activa(self):
        return SECUENCIA_ORIGINAL if self.modo_seq == "original" else SECUENCIA_CORREGIDA

    def _desc_paso(self):
        seq = self._seq_activa()
        if self.paso_actual >= len(seq):
            return "Secuencia completada.\nUsa 'Reiniciar' para volver a empezar."
        _, _, desc = seq[self.paso_actual]
        return f"Paso {self.paso_actual + 1}/{len(seq)}:\n{desc}"

    def _label_paso(self, idx):
        """Devuelve la etiqueta del paso (a, b, c... o estrella para extras)."""
        seq = self._seq_activa()
        _, var, desc = seq[idx]
        if desc.startswith('\u2605'):
            return u'\u2605'
        # mapeo para secuencia original
        if self.modo_seq == "original":
            return chr(ord('a') + idx)
        # mapeo para secuencia corregida: saltar indices de pasos extra
        extra_indices = {2, 4, 6}   # posiciones de los PUSH extra
        letra_map = {0:'a', 1:'b', 3:'c', 5:'d', 7:'e', 8:'f', 9:'g', 10:'h', 11:'i'}
        return letra_map.get(idx, '?')

    # ── Layout ──────────────────────────────────────────────────────
    def _construir_ui(self):
        tk.Label(self.root, text="P I L A   ( S T A C K )",
                 bg=BG, fg=ACCENT,
                 font=("Courier New", 18, "bold")).pack(pady=(18, 2))
        tk.Label(self.root,
                 text="Estructura LIFO - Last In, First Out  |  Cap. max.: 8 elementos",
                 bg=BG, fg=MUTED,
                 font=("Courier New", 8)).pack(pady=(0, 10))

        main = tk.Frame(self.root, bg=BG)
        main.pack(padx=24, pady=0)

        # Canvas de la pila
        self.canvas = tk.Canvas(main, width=240, height=380,
                                bg=PANEL, highlightthickness=2,
                                highlightbackground=ACCENT)
        self.canvas.grid(row=0, column=0, padx=(0, 16), sticky="n")

        # Panel derecho
        right = tk.Frame(main, bg=BG)
        right.grid(row=0, column=1, sticky="n")

        # Estado
        info_frame = tk.Frame(right, bg=PANEL, highlightthickness=1,
                              highlightbackground=MUTED)
        info_frame.pack(fill="x", pady=(0, 10))
        tk.Label(info_frame, text="ESTADO", bg=PANEL, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", padx=12, pady=(8, 0))
        self.lbl_tam   = self._stat(info_frame, "Tamano",  "0")
        self.lbl_tope  = self._stat(info_frame, "TOPE",    "-")
        self.lbl_vacia = self._stat(info_frame, "Vacia?",  "Si")
        tk.Frame(info_frame, height=6, bg=PANEL).pack()

        # Operacion manual
        ctrl = tk.Frame(right, bg=BG)
        ctrl.pack(fill="x")
        tk.Label(ctrl, text="-- Operacion manual --",
                 bg=BG, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", pady=(0, 4))
        tk.Label(ctrl, text="Valor:", bg=BG, fg=TEXT,
                 font=("Courier New", 10)).pack(anchor="w")
        self.entrada = tk.Entry(ctrl, width=18,
                                font=("Courier New", 12, "bold"),
                                bg=PANEL, fg=GREEN, insertbackground=GREEN,
                                relief="flat", highlightthickness=1,
                                highlightbackground=ACCENT)
        self.entrada.pack(fill="x", ipady=6, pady=(4, 8))
        self.entrada.bind("<Return>", lambda e: self._push())
        self._btn(ctrl, "PUSH  (Insertar)", GREEN,  self._push)
        self._btn(ctrl, "POP   (Eliminar)", ACCENT, self._pop)
        self._btn(ctrl, "LIMPIAR PILA",     MUTED,  self._limpiar)

        tk.Frame(right, bg=MUTED, height=1).pack(fill="x", pady=10)

        # ── Selector de secuencia ──────────────────────────────────
        tk.Label(right, text="-- Seleccionar Secuencia --",
                 bg=BG, fg=YELLOW,
                 font=("Courier New", 8, "bold")).pack(anchor="w", pady=(0, 6))

        sel_row = tk.Frame(right, bg=BG)
        sel_row.pack(fill="x", pady=(0, 6))

        self.btn_orig = tk.Button(sel_row,
                                  text="Original\n(con error)",
                                  command=self._activar_original,
                                  bg=YELLOW, fg=BG,
                                  font=("Courier New", 8, "bold"),
                                  relief="sunken", cursor="hand2",
                                  activebackground=TEXT, activeforeground=BG,
                                  padx=4, pady=6, width=11)
        self.btn_orig.pack(side="left", padx=(0, 4))

        self.btn_corr = tk.Button(sel_row,
                                  text="Corregida\n(sin errores)",
                                  command=self._activar_corregida,
                                  bg=PANEL, fg=PURPLE,
                                  font=("Courier New", 8, "bold"),
                                  relief="flat", cursor="hand2",
                                  activebackground=TEXT, activeforeground=BG,
                                  padx=4, pady=6, width=11,
                                  highlightthickness=1,
                                  highlightbackground=PURPLE)
        self.btn_corr.pack(side="left")

        # Badge de modo
        self.lbl_modo = tk.Label(right,
                                 text="MODO: ORIGINAL  (error esperado en paso e)",
                                 bg=PANEL, fg=YELLOW,
                                 font=("Courier New", 7, "bold"),
                                 padx=8, pady=4, wraplength=210)
        self.lbl_modo.pack(fill="x", pady=(0, 6))

        # Descripcion del paso
        self.lbl_paso = tk.Label(right,
                                 text=self._desc_paso(),
                                 bg=PANEL, fg=TEXT,
                                 font=("Courier New", 8),
                                 justify="left", anchor="nw",
                                 wraplength=205, padx=10, pady=8,
                                 height=5)
        self.lbl_paso.pack(fill="x", pady=(0, 6))

        seq_ctrl = tk.Frame(right, bg=BG)
        seq_ctrl.pack(fill="x")
        self._btn(seq_ctrl, "Siguiente paso",     BLUE,   self._siguiente_paso)
        self._btn(seq_ctrl, "Ejecutar todo",       YELLOW, self._ejecutar_todo)
        self._btn(seq_ctrl, "Reiniciar secuencia", MUTED,  self._reiniciar_secuencia)

        # Ultima operacion
        op_frame = tk.Frame(right, bg=PANEL, highlightthickness=1,
                            highlightbackground=MUTED)
        op_frame.pack(fill="x", pady=(10, 0))
        tk.Label(op_frame, text="ULTIMA OPERACION", bg=PANEL, fg=MUTED,
                 font=("Courier New", 7, "bold")).pack(anchor="w", padx=12, pady=(8, 0))
        tk.Label(op_frame, textvariable=self.ultimo_op,
                 bg=PANEL, fg=YELLOW,
                 font=("Courier New", 8), wraplength=200,
                 justify="left").pack(anchor="w", padx=12, pady=(2, 10))

        # ── Fila inferior ──────────────────────────────────────────
        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(padx=24, pady=(10, 16), fill="x")

        # Historial
        hist_col = tk.Frame(bottom, bg=BG)
        hist_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(hist_col, text="HISTORIAL", bg=BG, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", pady=(0, 4))
        hist_frame = tk.Frame(hist_col, bg=PANEL, highlightthickness=1,
                              highlightbackground=MUTED)
        hist_frame.pack(fill="both", expand=True)
        self.historial = tk.Text(hist_frame, width=30, height=8,
                                 bg=PANEL, fg=MUTED,
                                 font=("Courier New", 8),
                                 relief="flat", state="disabled")
        scroll_h = tk.Scrollbar(hist_frame, command=self.historial.yview)
        self.historial.configure(yscrollcommand=scroll_h.set)
        self.historial.pack(side="left", padx=6, pady=6)
        scroll_h.pack(side="right", fill="y")

        # Tabla comparativa
        cmp_col = tk.Frame(bottom, bg=BG)
        cmp_col.pack(side="left", fill="both", expand=True)
        tk.Label(cmp_col, text="COMPARATIVA", bg=BG, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", pady=(0, 4))
        cmp_frame = tk.Frame(cmp_col, bg=PANEL, highlightthickness=1,
                             highlightbackground=MUTED)
        cmp_frame.pack(fill="both", expand=True)
        comparativa = (
            " ORIGINAL          | CORREGIDA\n"
            "--------------------+--------------------\n"
            " a. PUSH X  TOPE=1 | a. PUSH X  TOPE=1\n"
            " b. PUSH Y  TOPE=2 | b. PUSH Y  TOPE=2\n"
            "                   | * PUSH Z   TOPE=3\n"
            " c. POP->Z  TOPE=1 | c. POP->Z  TOPE=2\n"
            "                   | * PUSH T   TOPE=3\n"
            " d. POP->T  TOPE=0 | d. POP->T  TOPE=2\n"
            " e. UNDERFLOW!     | * PUSH U   TOPE=3\n"
            "    (pila vacia)   | e. POP->U  TOPE=2\n"
            " f. PUSH V  TOPE=1 | f. PUSH V  TOPE=3\n"
            " g. PUSH W  TOPE=2 | g. PUSH W  TOPE=4\n"
            " h. POP->p  TOPE=1 | h. POP->p  TOPE=3\n"
            " i. PUSH R  TOPE=2 | i. PUSH R  TOPE=4\n"
            "--------------------+--------------------\n"
            " [V,R] Errores: 1  | [X,Y,V,R] Err: 0\n"
        )
        txt_cmp = tk.Text(cmp_frame, width=44, height=8,
                          bg=PANEL, fg=GREEN,
                          font=("Courier New", 7),
                          relief="flat")
        txt_cmp.insert("1.0", comparativa)
        txt_cmp.config(state="disabled")
        txt_cmp.pack(padx=8, pady=6)

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
        fg = BG if color not in (PANEL,) else TEXT
        b = tk.Button(parent, text=texto, command=cmd,
                      bg=color, fg=fg,
                      font=("Courier New", 9, "bold"),
                      relief="flat", cursor="hand2",
                      activebackground=TEXT, activeforeground=BG,
                      padx=8, pady=6)
        b.pack(fill="x", pady=2)

    # ── Selector de modo ─────────────────────────────────────────────
    def _activar_original(self):
        self.modo_seq = "original"
        self._reiniciar_secuencia(silencioso=True)
        self.lbl_modo.config(
            text="MODO: ORIGINAL  (error esperado en paso e)",
            fg=YELLOW)
        self.btn_orig.config(relief="sunken", bg=YELLOW, fg=BG)
        self.btn_corr.config(relief="flat",   bg=PANEL,  fg=PURPLE)
        self.canvas.config(highlightbackground=ACCENT)
        self._log("=== MODO: SECUENCIA ORIGINAL ===")

    def _activar_corregida(self):
        self.modo_seq = "corregida"
        self._reiniciar_secuencia(silencioso=True)
        self.lbl_modo.config(
            text="MODO: CORREGIDA  (* pasos extra, sin errores)",
            fg=GREEN)
        self.btn_corr.config(relief="sunken", bg=PURPLE, fg=TEXT)
        self.btn_orig.config(relief="flat",   bg=YELLOW, fg=BG)
        self.canvas.config(highlightbackground=PURPLE)
        self._log("=== MODO: SECUENCIA CORREGIDA * ===")

    # ── Dibujo ───────────────────────────────────────────────────────
    def _dibujar(self):
        self.canvas.delete("all")
        W, H = 240, 380
        BLOCK_H, MARGIN = 38, 30

        borde = PURPLE if self.modo_seq == "corregida" else ACCENT

        # Base y paredes
        self.canvas.create_rectangle(MARGIN, H - 24, W - MARGIN, H - 18,
                                     fill=borde, outline="")
        self.canvas.create_rectangle(MARGIN, 20, MARGIN + 6, H - 18,
                                     fill=MUTED, outline="")
        self.canvas.create_rectangle(W - MARGIN - 6, 20, W - MARGIN, H - 18,
                                     fill=MUTED, outline="")

        elementos = self.pila.elementos
        n = len(elementos)

        if n == 0:
            self.canvas.create_text(W // 2, H // 2,
                                    text="[ vacia ]", fill=MUTED,
                                    font=("Courier New", 13, "italic"))

        for i, val in enumerate(elementos):
            if i >= self.MAX:
                break
            y2 = H - 24 - i * (BLOCK_H + 4)
            y1 = y2 - BLOCK_H
            x1, x2 = MARGIN + 6, W - MARGIN - 6
            color = BLOCK_CLR[i % len(BLOCK_CLR)]

            self.canvas.create_rectangle(x1 + 3, y1 + 3, x2 + 3, y2 + 3,
                                         fill="#0a0a14", outline="")
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         fill=color, outline="")
            self.canvas.create_text(x1 + 14, (y1 + y2) // 2,
                                    text=f"[{i}]", fill=BG,
                                    font=("Courier New", 7), anchor="w")
            txt = str(val)
            if len(txt) > 12:
                txt = txt[:11] + "~"
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                    text=txt, fill=BG,
                                    font=("Courier New", 11, "bold"))
            if i == n - 1:
                self.canvas.create_text(W - MARGIN + 2, (y1 + y2) // 2,
                                        text="< TOPE", fill=YELLOW,
                                        font=("Courier New", 7, "bold"),
                                        anchor="w")

        self.lbl_tam.config(text=str(n))
        tope = self.pila.peek()
        self.lbl_tope.config(text=str(tope) if tope is not None else "-")
        self.lbl_vacia.config(text="Si" if self.pila.esta_vacia() else "No",
                               fg=GREEN if self.pila.esta_vacia() else ACCENT)

    # ── Operaciones manuales ─────────────────────────────────────────
    def _push(self):
        val = self.entrada.get().strip()
        if not val:
            messagebox.showwarning("Sin valor", "Escribe un valor para hacer PUSH.")
            return
        ok, msg = self.pila.push(val)
        if not ok:
            messagebox.showwarning("OVERFLOW", msg)
            self._log(f"[ERROR] OVERFLOW -> PUSH '{val}'")
            return
        self.ultimo_op.set(f"PUSH  ->  '{val}' agregado al tope")
        self._log(f"PUSH  '{val}'  | TOPE={self.pila.tamanio()}")
        self.entrada.delete(0, "end")
        self._dibujar()

    def _pop(self):
        ok, val = self.pila.pop()
        if not ok:
            messagebox.showinfo("UNDERFLOW", val)
            self._log("[ERROR] UNDERFLOW - pila vacia")
            return
        self.ultimo_op.set(f"POP   <-  '{val}' retirado del tope")
        self._log(f"POP   '{val}'  | TOPE={self.pila.tamanio()}")
        self._dibujar()

    def _limpiar(self):
        if messagebox.askyesno("Limpiar", "Vaciar toda la pila?"):
            self.pila = Pila(capacidad=8)
            self.ultimo_op.set("Pila limpiada")
            self._log("--- LIMPIAR ---")
            self._dibujar()

    # ── Ejecucion de secuencia ───────────────────────────────────────
    def _ejecutar_paso(self, silencioso=False):
        seq = self._seq_activa()
        if self.paso_actual >= len(seq):
            return False

        op, var, desc = seq[self.paso_actual]
        letra = self._label_paso(self.paso_actual)
        es_extra = (letra == u'\u2605')

        if op == "PUSH":
            ok, resultado = self.pila.push(var)
            if not ok:
                if not silencioso:
                    messagebox.showwarning("OVERFLOW",
                                           f"OVERFLOW en paso {letra}.\n{resultado}")
                self._log(f"[{letra}] OVERFLOW: PUSH '{var}' - pila llena")
                self.errores.append(f"Paso {letra}: OVERFLOW")
                self.ultimo_op.set(f"[{letra}] OVERFLOW al insertar '{var}'")
            else:
                prefijo = "* " if es_extra else ""
                self._log(f"[{letra}] {prefijo}PUSH '{var}'  TOPE={self.pila.tamanio()}")
                self.ultimo_op.set(f"[{letra}] {prefijo}PUSH '{var}' -> TOPE={self.pila.tamanio()}")

        elif op == "POP":
            ok, resultado = self.pila.pop()
            if not ok:
                if not silencioso:
                    messagebox.showwarning("UNDERFLOW",
                                           f"UNDERFLOW en paso {letra}.\n"
                                           f"Variable '{var}' no recibe nada.\n"
                                           f"La pila esta vacia.")
                self._log(f"[{letra}] UNDERFLOW: POP para '{var}' - pila vacia")
                self.errores.append(f"Paso {letra}: UNDERFLOW")
                self.ultimo_op.set(f"[{letra}] UNDERFLOW - '{var}' sin valor")
            else:
                self._log(f"[{letra}] POP -> {var}='{resultado}'  TOPE={self.pila.tamanio()}")
                self.ultimo_op.set(f"[{letra}] POP -> {var}='{resultado}'  TOPE={self.pila.tamanio()}")

        self.paso_actual += 1
        return True

    def _siguiente_paso(self):
        seq = self._seq_activa()
        if self.paso_actual >= len(seq):
            messagebox.showinfo("Secuencia completa",
                                f"Todos los pasos ya fueron ejecutados.\n\n"
                                f"Elementos: {self.pila.tamanio()}\n"
                                f"Tope: {self.pila.peek()}\n"
                                f"Errores: {len(self.errores)}")
            return
        self._ejecutar_paso(silencioso=False)
        self.lbl_paso.config(text=self._desc_paso())
        self._dibujar()
        if self.paso_actual == len(seq):
            self._mostrar_resumen_final()

    def _ejecutar_todo(self):
        seq = self._seq_activa()
        while self.paso_actual < len(seq):
            self._ejecutar_paso(silencioso=True)
        self._dibujar()
        self.lbl_paso.config(text=self._desc_paso())
        self._mostrar_resumen_final()

    def _reiniciar_secuencia(self, silencioso=False):
        self.pila        = Pila(capacidad=8)
        self.paso_actual = 0
        self.errores     = []
        self.ultimo_op.set("Secuencia reiniciada - lista para comenzar")
        self.lbl_paso.config(text=self._desc_paso())
        if not silencioso:
            self._log("--- REINICIO ---")
        self._dibujar()

    def _mostrar_resumen_final(self):
        contenido   = self.pila.elementos[:]
        n           = self.pila.tamanio()
        errores_str = "\n".join(self.errores) if self.errores else "Ninguno"
        modo_label  = ("ORIGINAL (con error)" if self.modo_seq == "original"
                       else "CORREGIDA * (sin errores)")
        messagebox.showinfo(
            "Secuencia completada",
            f"Modo: {modo_label}\n\n"
            f"Elementos en la pila : {n}\n"
            f"Contenido (base->tope): {contenido}\n"
            f"Tope actual          : {self.pila.peek()}\n\n"
            f"Errores detectados:\n{errores_str}"
        )

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
