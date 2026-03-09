import tkinter as tk
from tkinter import messagebox

# ── Colores ──────────────────────────────────────────────────────────
BG, PANEL, ACCENT = "#0f0f1a", "#1a1a2e", "#e94560"
GREEN, YELLOW, TEXT, MUTED = "#00d4aa", "#f5a623", "#e0e0f0", "#5a5a7a"
BLUE, PURPLE = "#3a86ff", "#9b5de5"
ORANGE = "#ff9f43"
BLOQUES = ["#e94560","#f5a623","#00d4aa","#7c5cbf","#3a86ff","#ff6b6b","#06d6a0","#f15bb5"]

# ── Secuencias ───────────────────────────────────────────────────────
SEQ_ORIG = [
    ("PUSH","X","a. Insertar(PILA, X)\nPUSH 'X' al tope."),
    ("PUSH","Y","b. Insertar(PILA, Y)\nPUSH 'Y' al tope."),
    ("POP", "Z","c. Eliminar(PILA, Z)\nPOP -> Z recibe el tope."),
    ("POP", "T","d. Eliminar(PILA, T)\nPOP -> T recibe el tope."),
    ("POP", "U","e. Eliminar(PILA, U)\n⚠ Pila vacia -> UNDERFLOW."),
    ("PUSH","V","f. Insertar(PILA, V)\nPUSH 'V' al tope."),
    ("PUSH","W","g. Insertar(PILA, W)\nPUSH 'W' al tope."),
    ("POP", "p","h. Eliminar(PILA, p)\nPOP -> p recibe el tope."),
    ("PUSH","R","i. Insertar(PILA, R)\nPUSH 'R' al tope."),
]

SEQ_CORR = [
    ("PUSH","X","a. Insertar(PILA, X)\nPUSH 'X' al tope."),
    ("PUSH","Y","b. Insertar(PILA, Y)\nPUSH 'Y' al tope."),
    ("PUSH","Z","★ PASO EXTRA: Insertar(PILA, Z)\nSe inserta Z antes de eliminarlo."),
    ("POP", "Z","c. Eliminar(PILA, Z) [CORREGIDO]\nPOP -> Z recibe el tope. Sin error."),
    ("PUSH","T","★ PASO EXTRA: Insertar(PILA, T)\nSe inserta T antes de eliminarlo."),
    ("POP", "T","d. Eliminar(PILA, T) [CORREGIDO]\nPOP -> T recibe el tope. Sin error."),
    ("PUSH","U","★ PASO EXTRA: Insertar(PILA, U)\nEvita el UNDERFLOW del paso e."),
    ("POP", "U","e. Eliminar(PILA, U) [CORREGIDO]\nPOP -> U recibe el tope. Sin error."),
    ("PUSH","V","f. Insertar(PILA, V)\nPUSH 'V' al tope."),
    ("PUSH","W","g. Insertar(PILA, W)\nPUSH 'W' al tope."),
    ("PUSH","p","★ PASO EXTRA: Insertar(PILA, p)\nSe inserta p antes de eliminarlo."),
    ("POP", "p","h. Eliminar(PILA, p) [CORREGIDO]\nPOP -> p recibe el tope. Sin error."),
    ("PUSH","R","i. Insertar(PILA, R)\nPUSH 'R' al tope."),
]

COMPARATIVA = (
    " ORIGINAL          | CORREGIDA\n"
    "-------------------+--------------------\n"
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
    "                   | * PUSH p   TOPE=5\n"
    " h. POP->p  TOPE=1 | h. POP->p  TOPE=4\n"
    " i. PUSH R  TOPE=2 | i. PUSH R  TOPE=5\n"
    "-------------------+--------------------\n"
    " [V,R] Errores: 1  | [X,Y,V,p,R] Err:0\n"
)

# ── Clase Pila ───────────────────────────────────────────────────────
class Pila:
    def __init__(self):
        self.elementos = []

    def push(self, val):
        if len(self.elementos) >= 8:
            return False, "OVERFLOW: pila llena."
        self.elementos.append(val)
        return True, val

    def pop(self):
        if not self.elementos:
            return False, "UNDERFLOW: pila vacia."
        return True, self.elementos.pop()

    def peek(self):
        return self.elementos[-1] if self.elementos else None

    def tope(self):
        return len(self.elementos)


# ── App ──────────────────────────────────────────────────────────────
class App:
    def __init__(self, root):
        self.root = root
        self.pila = Pila()
        self.pila_aux = Pila()
        self.ultimo_op = tk.StringVar(value="Bienvenido -> usa PUSH / POP o una Secuencia")
        self.paso = 0
        self.errores = []
        self.modo = "original"
        self._ui()
        self._dibujar()

    def _seq(self):
        return SEQ_ORIG if self.modo == "original" else SEQ_CORR

    # ── UI ───────────────────────────────────────────────────────────
    def _ui(self):
        tk.Label(self.root, text="P I L A  ( S T A C K )", bg=BG, fg=ACCENT,
                 font=("Courier New", 18, "bold")).pack(pady=(16,2))
        tk.Label(self.root, text="LIFO — Last In, First Out  |  Cap. max: 8",
                 bg=BG, fg=MUTED, font=("Courier New", 8)).pack(pady=(0,8))

        main = tk.Frame(self.root, bg=BG)
        main.pack(padx=20)

        # Canvas PILA PRINCIPAL
        lbl_main = tk.Label(main, text="PILA PRINCIPAL", bg=BG, fg=ACCENT,
                            font=("Courier New", 9, "bold"))
        lbl_main.grid(row=0, column=0, padx=(0,16), pady=(0,2))

        self.canvas = tk.Canvas(main, width=240, height=380, bg=PANEL,
                                highlightthickness=2, highlightbackground=ACCENT)
        self.canvas.grid(row=1, column=0, padx=(0,16), sticky="n")

        # Panel derecho
        R = tk.Frame(main, bg=BG)
        R.grid(row=0, column=1, rowspan=2, sticky="n")

        # Estado
        sf = self._frame(R)
        tk.Label(sf, text="ESTADO", bg=PANEL, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", padx=10, pady=(6,0))
        self.lbl_tam   = self._stat(sf, "Tamano", "0")
        self.lbl_tope  = self._stat(sf, "TOPE",   "-")
        self.lbl_vacia = self._stat(sf, "Vacia?", "Si")
        tk.Frame(sf, height=4, bg=PANEL).pack()

        # Operacion manual
        tk.Label(R, text="-- Operacion manual --", bg=BG, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", pady=(8,2))
        self.entrada = tk.Entry(R, width=18, font=("Courier New", 12, "bold"),
                                bg=PANEL, fg=GREEN, insertbackground=GREEN,
                                relief="flat", highlightthickness=1,
                                highlightbackground=ACCENT)
        self.entrada.pack(fill="x", ipady=5, pady=(0,6))
        self.entrada.bind("<Return>", lambda e: self._push_manual())
        self._btn(R, "PUSH (Insertar)", GREEN,  self._push_manual)
        self._btn(R, "POP  (Eliminar)", ACCENT, self._pop_manual)

        # ── BOTONES PILA AUXILIAR ─────────────────────────────────
        tk.Frame(R, bg=ORANGE, height=1).pack(fill="x", pady=(8,4))
        tk.Label(R, text="-- Pila Auxiliar (Hanoi) --", bg=BG, fg=ORANGE,
                 font=("Courier New", 8, "bold")).pack(anchor="w", pady=(0,4))

        self._btn(R, "POP  -> AUX  (mueve tope a aux)", ORANGE, self._pop_a_aux)
        self._btn(R, "AUX  -> PUSH (mueve tope de aux)", PURPLE, self._aux_a_main)

        # Estado auxiliar compacto
        saf = self._frame(R)
        tk.Label(saf, text="ESTADO AUX", bg=PANEL, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", padx=10, pady=(6,0))
        self.lbl_aux_tam  = self._stat(saf, "Tamano", "0")
        self.lbl_aux_tope = self._stat(saf, "TOPE",   "-")
        tk.Frame(saf, height=4, bg=PANEL).pack()

        self._btn(R, "Limpiar pila",    MUTED,  self._limpiar)

        # Selector de secuencia
        tk.Frame(R, bg=MUTED, height=1).pack(fill="x", pady=8)
        tk.Label(R, text="-- Secuencia --", bg=BG, fg=YELLOW,
                 font=("Courier New", 8, "bold")).pack(anchor="w", pady=(0,4))

        row = tk.Frame(R, bg=BG)
        row.pack(fill="x", pady=(0,4))
        self.btn_orig = tk.Button(row, text="Original\n(con error)",
                                  command=self._modo_original,
                                  bg=YELLOW, fg=BG, font=("Courier New", 8, "bold"),
                                  relief="sunken", cursor="hand2", width=11, pady=5)
        self.btn_orig.pack(side="left", padx=(0,4))
        self.btn_corr = tk.Button(row, text="Corregida\n(sin errores)",
                                  command=self._modo_corregida,
                                  bg=PANEL, fg=PURPLE, font=("Courier New", 8, "bold"),
                                  relief="flat", cursor="hand2", width=11, pady=5,
                                  highlightthickness=1, highlightbackground=PURPLE)
        self.btn_corr.pack(side="left")

        self.lbl_modo = tk.Label(R, text="MODO: ORIGINAL (error en paso e)",
                                 bg=PANEL, fg=YELLOW,
                                 font=("Courier New", 7, "bold"), padx=6, pady=3)
        self.lbl_modo.pack(fill="x", pady=(0,4))

        self.lbl_paso = tk.Label(R, text=self._desc_paso(), bg=PANEL, fg=TEXT,
                                 font=("Courier New", 8), justify="left",
                                 anchor="nw", wraplength=200, padx=8, pady=6, height=5)
        self.lbl_paso.pack(fill="x", pady=(0,4))

        self._btn(R, "Siguiente paso",     BLUE,   self._siguiente)
        self._btn(R, "Ejecutar todo",      YELLOW, self._ejecutar_todo)
        self._btn(R, "Reiniciar",          MUTED,  self._reiniciar)

        # Ultima operacion
        of = self._frame(R, pady=(8,0))
        tk.Label(of, text="ULTIMA OPERACION", bg=PANEL, fg=MUTED,
                 font=("Courier New", 7, "bold")).pack(anchor="w", padx=10, pady=(6,0))
        tk.Label(of, textvariable=self.ultimo_op, bg=PANEL, fg=YELLOW,
                 font=("Courier New", 8), wraplength=195,
                 justify="left").pack(anchor="w", padx=10, pady=(2,8))

        # Canvas PILA AUXILIAR (debajo de pila principal)
        lbl_aux = tk.Label(main, text="PILA  AUXILIAR", bg=BG, fg=ORANGE,
                           font=("Courier New", 9, "bold"))
        lbl_aux.grid(row=2, column=0, padx=(0,16), pady=(14,2))

        self.canvas_aux = tk.Canvas(main, width=240, height=200, bg=PANEL,
                                    highlightthickness=2, highlightbackground=ORANGE)
        self.canvas_aux.grid(row=3, column=0, padx=(0,16), sticky="n")

        # Fila inferior: historial + comparativa
        bot = tk.Frame(self.root, bg=BG)
        bot.pack(padx=20, pady=(8,14), fill="x")

        # Historial
        hf = tk.Frame(bot, bg=BG)
        hf.pack(side="left", fill="both", expand=True, padx=(0,8))
        tk.Label(hf, text="HISTORIAL", bg=BG, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", pady=(0,2))
        hframe = self._frame(hf)
        self.historial = tk.Text(hframe, width=28, height=7, bg=PANEL, fg=MUTED,
                                 font=("Courier New", 8), relief="flat", state="disabled")
        sc = tk.Scrollbar(hframe, command=self.historial.yview)
        self.historial.configure(yscrollcommand=sc.set)
        self.historial.pack(side="left", padx=5, pady=5)
        sc.pack(side="right", fill="y")

        # Comparativa
        cf = tk.Frame(bot, bg=BG)
        cf.pack(side="left", fill="both", expand=True)
        tk.Label(cf, text="COMPARATIVA", bg=BG, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", pady=(0,2))
        cframe = self._frame(cf)
        txt = tk.Text(cframe, width=42, height=7, bg=PANEL, fg=GREEN,
                      font=("Courier New", 7), relief="flat")
        txt.insert("1.0", COMPARATIVA)
        txt.config(state="disabled")
        txt.pack(padx=6, pady=5)

    def _frame(self, parent, pady=(0,0)):
        f = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=MUTED)
        f.pack(fill="x", pady=pady)
        return f

    def _stat(self, parent, label, valor):
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", padx=10, pady=1)
        tk.Label(row, text=f"{label}:", bg=PANEL, fg=MUTED,
                 font=("Courier New", 9), width=8, anchor="w").pack(side="left")
        lbl = tk.Label(row, text=valor, bg=PANEL, fg=TEXT,
                       font=("Courier New", 9, "bold"), anchor="w")
        lbl.pack(side="left")
        return lbl

    def _btn(self, parent, texto, color, cmd):
        tk.Button(parent, text=texto, command=cmd, bg=color, fg=BG,
                  font=("Courier New", 9, "bold"), relief="flat", cursor="hand2",
                  activebackground=TEXT, activeforeground=BG,
                  padx=8, pady=5).pack(fill="x", pady=2)

    # ── Dibujo pila principal ─────────────────────────────────────────
    def _dibujar(self):
        self._dibujar_canvas(self.canvas, self.pila, 380,
                             PURPLE if self.modo == "corregida" else ACCENT)
        self._dibujar_canvas_aux()
        # update estado principal
        n = self.pila.tope()
        t = self.pila.peek()
        self.lbl_tam.config(text=str(n))
        self.lbl_tope.config(text=str(t) if t is not None else "-")
        self.lbl_vacia.config(text="Si" if n == 0 else "No",
                              fg=GREEN if n == 0 else ACCENT)
        # update estado auxiliar
        na = self.pila_aux.tope()
        ta = self.pila_aux.peek()
        self.lbl_aux_tam.config(text=str(na))
        self.lbl_aux_tope.config(text=str(ta) if ta is not None else "-")

    def _dibujar_canvas(self, canvas, pila, H, borde_color):
        canvas.delete("all")
        W, BH, M = 240, 38, 30
        canvas.config(highlightbackground=borde_color)
        canvas.create_rectangle(M, H-24, W-M, H-18, fill=borde_color, outline="")
        canvas.create_rectangle(M, 20, M+6, H-18, fill=MUTED, outline="")
        canvas.create_rectangle(W-M-6, 20, W-M, H-18, fill=MUTED, outline="")
        elems = pila.elementos
        n = len(elems)
        if n == 0:
            canvas.create_text(W//2, H//2, text="[ vacia ]",
                               fill=MUTED, font=("Courier New", 13, "italic"))
        for i, val in enumerate(elems[:8]):
            y2 = H - 24 - i*(BH+4)
            y1, x1, x2 = y2-BH, M+6, W-M-6
            c = BLOQUES[i % len(BLOQUES)]
            canvas.create_rectangle(x1+3, y1+3, x2+3, y2+3, fill="#0a0a14", outline="")
            canvas.create_rectangle(x1, y1, x2, y2, fill=c, outline="")
            canvas.create_text(x1+14, (y1+y2)//2, text=f"[{i}]",
                               fill=BG, font=("Courier New", 7), anchor="w")
            txt = str(val)[:12]
            canvas.create_text((x1+x2)//2, (y1+y2)//2, text=txt,
                               fill=BG, font=("Courier New", 11, "bold"))
            if i == n-1:
                canvas.create_text(W-M+2, (y1+y2)//2, text="< TOPE",
                                   fill=YELLOW, font=("Courier New", 7, "bold"), anchor="w")

    def _dibujar_canvas_aux(self):
        canvas = self.canvas_aux
        canvas.delete("all")
        W, H, BH, M = 240, 200, 34, 30
        canvas.config(highlightbackground=ORANGE)
        canvas.create_rectangle(M, H-18, W-M, H-12, fill=ORANGE, outline="")
        canvas.create_rectangle(M, 10, M+6, H-12, fill=MUTED, outline="")
        canvas.create_rectangle(W-M-6, 10, W-M, H-12, fill=MUTED, outline="")
        elems = self.pila_aux.elementos
        n = len(elems)
        if n == 0:
            canvas.create_text(W//2, H//2, text="[ aux vacia ]",
                               fill=MUTED, font=("Courier New", 11, "italic"))
        for i, val in enumerate(elems[:5]):
            y2 = H - 18 - i*(BH+3)
            y1, x1, x2 = y2-BH, M+6, W-M-6
            c = BLOQUES[(i+4) % len(BLOQUES)]
            canvas.create_rectangle(x1+3, y1+3, x2+3, y2+3, fill="#0a0a14", outline="")
            canvas.create_rectangle(x1, y1, x2, y2, fill=c, outline="")
            canvas.create_text(x1+14, (y1+y2)//2, text=f"[{i}]",
                               fill=BG, font=("Courier New", 7), anchor="w")
            txt = str(val)[:12]
            canvas.create_text((x1+x2)//2, (y1+y2)//2, text=txt,
                               fill=BG, font=("Courier New", 11, "bold"))
            if i == n-1:
                canvas.create_text(W-M+2, (y1+y2)//2, text="< TOPE",
                                   fill=ORANGE, font=("Courier New", 7, "bold"), anchor="w")

    # ── Operaciones manuales ─────────────────────────────────────────
    def _push_manual(self):
        val = self.entrada.get().strip()
        if not val:
            return messagebox.showwarning("Sin valor", "Escribe un valor para PUSH.")
        ok, msg = self.pila.push(val)
        if not ok:
            return messagebox.showwarning("OVERFLOW", msg)
        self.ultimo_op.set(f"PUSH '{val}' -> TOPE={self.pila.tope()}")
        self._log(f"PUSH '{val}' | TOPE={self.pila.tope()}")
        self.entrada.delete(0, "end")
        self._dibujar()

    def _pop_manual(self):
        ok, val = self.pila.pop()
        if not ok:
            return messagebox.showinfo("UNDERFLOW", val)
        self.ultimo_op.set(f"POP '{val}' <- TOPE={self.pila.tope()}")
        self._log(f"POP '{val}' | TOPE={self.pila.tope()}")
        self._dibujar()

    def _pop_a_aux(self):
        """POP de pila principal -> PUSH en pila auxiliar"""
        ok, val = self.pila.pop()
        if not ok:
            return messagebox.showinfo("UNDERFLOW", "Pila principal vacia.")
        ok2, msg2 = self.pila_aux.push(val)
        if not ok2:
            # revertir: devolver a principal
            self.pila.push(val)
            return messagebox.showwarning("OVERFLOW AUX", f"Pila auxiliar llena.\n{msg2}")
        self.ultimo_op.set(f"POP '{val}' MAIN -> AUX tope={self.pila_aux.tope()}")
        self._log(f"[AUX] '{val}' MAIN->AUX | MainTOPE={self.pila.tope()} AuxTOPE={self.pila_aux.tope()}")
        self._dibujar()

    def _aux_a_main(self):
        """POP de pila auxiliar -> PUSH en pila principal"""
        ok, val = self.pila_aux.pop()
        if not ok:
            return messagebox.showinfo("AUX VACIA", "Pila auxiliar vacia.")
        ok2, msg2 = self.pila.push(val)
        if not ok2:
            self.pila_aux.push(val)
            return messagebox.showwarning("OVERFLOW MAIN", f"Pila principal llena.\n{msg2}")
        self.ultimo_op.set(f"AUX '{val}' -> MAIN tope={self.pila.tope()}")
        self._log(f"[AUX] '{val}' AUX->MAIN | MainTOPE={self.pila.tope()} AuxTOPE={self.pila_aux.tope()}")
        self._dibujar()

    def _limpiar(self):
        if messagebox.askyesno("Limpiar", "Vaciar pila principal Y auxiliar?"):
            self.pila = Pila()
            self.pila_aux = Pila()
            self.ultimo_op.set("Pilas limpiadas")
            self._log("--- LIMPIAR AMBAS ---")
            self._dibujar()

    # ── Secuencia ────────────────────────────────────────────────────
    def _desc_paso(self):
        seq = self._seq()
        if self.paso >= len(seq):
            return "Secuencia completada.\nUsa 'Reiniciar' para repetir."
        return f"Paso {self.paso+1}/{len(seq)}:\n{seq[self.paso][2]}"

    def _es_extra(self, idx):
        return self._seq()[idx][2].startswith("★")

    def _letra(self, idx):
        if self._es_extra(idx):
            return "★"
        if self.modo == "original":
            return chr(ord('a') + idx)
        mapa = {0:'a',1:'b',3:'c',5:'d',7:'e',8:'f',9:'g',11:'h',12:'i'}
        return mapa.get(idx, '?')

    def _ejecutar_paso(self, silencioso=False):
        seq = self._seq()
        if self.paso >= len(seq):
            return
        op, var, _ = seq[self.paso]
        L = self._letra(self.paso)
        pre = "* " if self._es_extra(self.paso) else ""

        if op == "PUSH":
            ok, res = self.pila.push(var)
            if not ok:
                if not silencioso:
                    messagebox.showwarning("OVERFLOW", f"Paso {L}: {res}")
                self._log(f"[{L}] OVERFLOW: PUSH '{var}'")
                self.errores.append(f"Paso {L}: OVERFLOW")
                self.ultimo_op.set(f"[{L}] OVERFLOW al insertar '{var}'")
            else:
                self._log(f"[{L}] {pre}PUSH '{var}' | TOPE={self.pila.tope()}")
                self.ultimo_op.set(f"[{L}] {pre}PUSH '{var}' -> TOPE={self.pila.tope()}")
        else:
            ok, res = self.pila.pop()
            if not ok:
                if not silencioso:
                    messagebox.showwarning("UNDERFLOW",
                                           f"Paso {L}: '{var}' no recibe nada.\nPila vacia.")
                self._log(f"[{L}] UNDERFLOW: POP para '{var}'")
                self.errores.append(f"Paso {L}: UNDERFLOW")
                self.ultimo_op.set(f"[{L}] UNDERFLOW - '{var}' sin valor")
            else:
                self._log(f"[{L}] POP -> {var}='{res}' | TOPE={self.pila.tope()}")
                self.ultimo_op.set(f"[{L}] POP -> {var}='{res}' TOPE={self.pila.tope()}")
        self.paso += 1

    def _siguiente(self):
        if self.paso >= len(self._seq()):
            return messagebox.showinfo("Listo", "Secuencia ya completada.")
        self._ejecutar_paso()
        self.lbl_paso.config(text=self._desc_paso())
        self._dibujar()
        if self.paso == len(self._seq()):
            self._resumen()

    def _ejecutar_todo(self):
        while self.paso < len(self._seq()):
            self._ejecutar_paso(silencioso=True)
        self.lbl_paso.config(text=self._desc_paso())
        self._dibujar()
        self._resumen()

    def _reiniciar(self, silencioso=False):
        self.pila, self.paso, self.errores = Pila(), 0, []
        self.pila_aux = Pila()
        self.ultimo_op.set("Reiniciado - listo para comenzar")
        self.lbl_paso.config(text=self._desc_paso())
        if not silencioso:
            self._log("--- REINICIO ---")
        self._dibujar()

    def _resumen(self):
        modo = "ORIGINAL (con error)" if self.modo == "original" else "CORREGIDA (sin errores)"
        err = "\n".join(self.errores) if self.errores else "Ninguno"
        messagebox.showinfo("Secuencia completada",
                            f"Modo: {modo}\n\n"
                            f"Elementos: {self.pila.tope()}\n"
                            f"Contenido: {self.pila.elementos}\n"
                            f"Tope: {self.pila.peek()}\n\n"
                            f"Errores:\n{err}")

    def _modo_original(self):
        self.modo = "original"
        self._reiniciar(silencioso=True)
        self.lbl_modo.config(text="MODO: ORIGINAL (error en paso e)", fg=YELLOW)
        self.btn_orig.config(relief="sunken", bg=YELLOW, fg=BG)
        self.btn_corr.config(relief="flat", bg=PANEL, fg=PURPLE)
        self.canvas.config(highlightbackground=ACCENT)
        self._log("=== ORIGINAL ===")

    def _modo_corregida(self):
        self.modo = "corregida"
        self._reiniciar(silencioso=True)
        self.lbl_modo.config(text="MODO: CORREGIDA (* pasos extra, sin errores)", fg=GREEN)
        self.btn_corr.config(relief="sunken", bg=PURPLE, fg=TEXT)
        self.btn_orig.config(relief="flat", bg=YELLOW, fg=BG)
        self.canvas.config(highlightbackground=PURPLE)
        self._log("=== CORREGIDA * ===")

    def _log(self, msg):
        self.historial.config(state="normal")
        self.historial.insert("end", msg + "\n")
        self.historial.see("end")
        self.historial.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Visualizador de Pila")
    root.configure(bg=BG)

    container = tk.Frame(root, bg=BG)
    container.pack(fill="both", expand=True)

    canvas_scroll = tk.Canvas(container, bg=BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas_scroll.yview)
    canvas_scroll.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas_scroll.pack(side="left", fill="both", expand=True)

    inner = tk.Frame(canvas_scroll, bg=BG)
    win_id = canvas_scroll.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
    canvas_scroll.bind("<Configure>", lambda e: canvas_scroll.itemconfig(win_id, width=e.width))

    canvas_scroll.bind_all("<MouseWheel>", lambda e: canvas_scroll.yview_scroll(int(-1*(e.delta/120)), "units"))
    canvas_scroll.bind_all("<Button-4>", lambda e: canvas_scroll.yview_scroll(-1, "units"))
    canvas_scroll.bind_all("<Button-5>", lambda e: canvas_scroll.yview_scroll(1, "units"))

    sh = root.winfo_screenheight()
    root.geometry(f"900x{min(sh-80, 860)}")

    App(inner)
    root.mainloop()
