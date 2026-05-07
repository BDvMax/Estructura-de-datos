"""
╔══════════════════════════════════════════════════════════════════════════╗
║         MÉTODOS DE ORDENAMIENTO - ARCHIVOS EN DISCO (.txt)             ║
║  1. Intercalación   2. Mezcla Directa   3. Mezcla Equilibrada          ║
║  Todos los datos se leen y escriben en archivos .txt del disco          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import os

# ──────────────────────────── Directorio de trabajo ───────────────────────────
WORK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ordenamiento_datos")
os.makedirs(WORK_DIR, exist_ok=True)

# Archivos permanentes
FILE_INPUT    = os.path.join(WORK_DIR, "arreglo_entrada.txt")
FILE_OUTPUT   = os.path.join(WORK_DIR, "arreglo_salida.txt")
FILE_LOG      = os.path.join(WORK_DIR, "log_pasos.txt")
# Cintas para Mezcla Directa
FILE_CINTA = [os.path.join(WORK_DIR, f"cinta_{i+1}.txt") for i in range(4)]
# Cintas temporales para Mezcla Equilibrada
FILE_TEMP  = [os.path.join(WORK_DIR, f"temp_{i+1}.txt") for i in range(4)]

# ─────────────────────────────── Utilidades de disco ──────────────────────────

def escribir_arreglo(path, arr):
    """Escribe lista de enteros en archivo, uno por línea."""
    with open(path, "w") as f:
        for v in arr:
            f.write(str(v) + "\n")

def leer_arreglo(path):
    """Lee lista de enteros desde archivo."""
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        lines = f.read().splitlines()
    return [int(x) for x in lines if x.strip().lstrip("-").isdigit()]

def escribir_runs(path, runs):
    """Escribe lista de runs (lista de listas) en archivo.
    Cada run en una línea separada por comas; runs separados por '---'."""
    with open(path, "w") as f:
        for run in runs:
            f.write(",".join(str(v) for v in run) + "\n")
            f.write("---\n")

def leer_runs(path):
    """Lee runs desde archivo. Devuelve lista de listas."""
    if not os.path.exists(path):
        return []
    runs = []
    current = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line == "---":
                if current:
                    runs.append(current)
                    current = []
            elif line:
                current = [int(x) for x in line.split(",") if x.strip().lstrip("-").isdigit()]
    if current:
        runs.append(current)
    return runs

def agregar_log(path, mensaje):
    """Agrega una línea al archivo de log."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(mensaje + "\n")

def limpiar_log(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("=== LOG DE PASOS ===\n")

def limpiar_cintas():
    for p in FILE_CINTA + FILE_TEMP:
        with open(p, "w") as f:
            pass

# ─────────────────────────────── Paletas por módulo ───────────────────────────

PAL = {
    "menu": {
        "BG": "#0a0a14", "PANEL": "#12122a",
        "ACCENT": "#7b2fff", "TEXT": "#c8c8ff", "DIM": "#6666aa"
    },
    "intercalacion": {
        "BG": "#0f0f1a", "PANEL": "#1a1a2e",
        "DEF": "#2d3561", "SORTED": "#00b4d8",
        "CUR": "#f72585", "KEY": "#7b2d8b", "CMP": "#ffd60a",
        "TEXT": "#e0e0ff", "DIM": "#8888aa", "ACCENT": "#f72585"
    },
    "mezcla_directa": {
        "BG": "#0d1117", "PANEL": "#161b22",
        "DEF": "#264653", "RUN_A": "#e76f51", "RUN_B": "#2a9d8f",
        "MERGE": "#e9c46a", "DONE": "#57cc99",
        "TEXT": "#cdd9e5", "DIM": "#768390", "ACCENT": "#e76f51"
    },
    "mezcla_eq": {
        "BG": "#10002b", "PANEL": "#1a0533",
        "C1": "#9d4edd", "C2": "#3a86ff", "C3": "#fb5607", "C4": "#06d6a0",
        "MIX": "#ffbe0b", "DONE": "#80b918",
        "TEXT": "#e0aaff", "DIM": "#9477b4", "ACCENT": "#9d4edd"
    }
}

# ══════════════════════════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL — MENÚ
# ══════════════════════════════════════════════════════════════════════════════

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos de Ordenamiento — Archivos en Disco")
        self.root.configure(bg=PAL["menu"]["BG"])
        self.root.geometry("700x520")
        self.root.resizable(False, False)
        self._build()

    def _build(self):
        p = PAL["menu"]
        tk.Label(self.root,
                 text="MÉTODOS DE ORDENAMIENTO",
                 font=("Courier New", 20, "bold"),
                 bg=p["BG"], fg=p["ACCENT"]).pack(pady=(30, 4))
        tk.Label(self.root,
                 text="Todos los datos se guardan en archivos .txt del disco",
                 font=("Courier New", 11),
                 bg=p["BG"], fg=p["DIM"]).pack()

        # Directorio activo
        tk.Label(self.root,
                 text=f"📁  Directorio: {WORK_DIR}",
                 font=("Courier New", 9),
                 bg=p["BG"], fg=p["DIM"]).pack(pady=(4, 20))

        # Botones de método
        metodos = [
            ("🃏   1. Intercalación", "#f72585", self._abrir_intercalacion),
            ("🔀   2. Mezcla Directa", "#e76f51", self._abrir_mezcla_directa),
            ("🎞   3. Mezcla Equilibrada", "#9d4edd", self._abrir_mezcla_eq),
        ]
        for texto, color, cmd in metodos:
            tk.Button(self.root, text=texto,
                      font=("Courier New", 14, "bold"),
                      bg=p["PANEL"], fg=color,
                      activebackground=color, activeforeground="white",
                      relief="flat", padx=20, pady=12,
                      cursor="hand2", width=30, command=cmd
                      ).pack(pady=8)

        # Botón ver archivos
        tk.Button(self.root, text="📂  Abrir carpeta de archivos",
                  font=("Courier New", 10),
                  bg=p["PANEL"], fg=p["TEXT"],
                  relief="flat", padx=10, pady=6,
                  cursor="hand2", command=self._abrir_carpeta
                  ).pack(pady=(16, 4))

        # Info archivos
        self.info_var = tk.StringVar(value=self._status())
        tk.Label(self.root, textvariable=self.info_var,
                 font=("Courier New", 9),
                 bg=p["BG"], fg=p["DIM"]).pack(pady=4)

    def _status(self):
        arr = leer_arreglo(FILE_INPUT)
        return f"arreglo_entrada.txt → {len(arr)} elementos  |  arreglo_salida.txt  |  log_pasos.txt  |  cintas 1-4"

    def _abrir_carpeta(self):
        import subprocess, sys
        if sys.platform == "win32":
            os.startfile(WORK_DIR)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", WORK_DIR])
        else:
            subprocess.Popen(["xdg-open", WORK_DIR])

    def _abrir_intercalacion(self):
        w = tk.Toplevel(self.root)
        IntercalacionApp(w)

    def _abrir_mezcla_directa(self):
        w = tk.Toplevel(self.root)
        MezclaDirectaApp(w)

    def _abrir_mezcla_eq(self):
        w = tk.Toplevel(self.root)
        MezclaEquilibradaApp(w)


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 1: INTERCALACIÓN
# ══════════════════════════════════════════════════════════════════════════════

class IntercalacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intercalación — Insertion Sort")
        p = PAL["intercalacion"]
        self.p = p
        self.root.configure(bg=p["BG"])
        self.root.geometry("960x700")
        self.root.resizable(False, False)
        self.array = []
        self.animating = False
        self.paused = False
        self.delay = 600
        self.step_gen = None
        self._build_ui()
        self._cargar_desde_disco()

    # ── UI ──
    def _build_ui(self):
        p = self.p
        tk.Label(self.root, text="🃏  INTERCALACIÓN  (Insertion Sort)",
                 font=("Courier New", 17, "bold"), bg=p["BG"], fg=p["ACCENT"]
                 ).pack(pady=(12, 2))
        tk.Label(self.root,
                 text="Lee/escribe arreglo en  arreglo_entrada.txt  y  arreglo_salida.txt",
                 font=("Courier New", 9), bg=p["BG"], fg=p["DIM"]).pack()

        self.canvas = tk.Canvas(self.root, width=920, height=230,
                                bg=p["PANEL"], highlightthickness=0)
        self.canvas.pack(padx=20, pady=6)

        # Leyenda
        leg = tk.Frame(self.root, bg=p["BG"])
        leg.pack(pady=2)
        for col, txt in [(p["DEF"],"Sin procesar"),(p["SORTED"],"Ordenado"),
                         (p["CUR"],"Actual (i)"),(p["KEY"],"Clave key"),(p["CMP"],"Comparando")]:
            f = tk.Frame(leg, bg=p["BG"]); f.pack(side="left", padx=8)
            tk.Label(f, width=3, bg=col, relief="flat").pack(side="left")
            tk.Label(f, text=txt, font=("Courier New", 9), bg=p["BG"], fg=p["TEXT"]).pack(side="left", padx=2)

        self.info_var = tk.StringVar(value="Cargando desde disco...")
        tk.Label(self.root, textvariable=self.info_var,
                 font=("Courier New", 11, "bold"), bg=p["BG"], fg=p["TEXT"],
                 wraplength=900, justify="center").pack(pady=4)

        # Pseudocódigo
        pc = tk.Frame(self.root, bg=p["PANEL"]); pc.pack(padx=20, fill="x", pady=2)
        tk.Label(pc, text="  Pseudocódigo:", font=("Courier New", 9,"bold"),
                 bg=p["PANEL"], fg=p["ACCENT"]).pack(anchor="w")
        lineas = [
            "  para i = 1 hasta n-1:",
            "      key = arreglo[i]          # elemento a intercalar",
            "      j = i - 1",
            "      mientras j >= 0 y arreglo[j] > key:",
            "          arreglo[j+1] = arreglo[j]    # desplaza derecha",
            "          j = j - 1",
            "      arreglo[j+1] = key        # inserta en lugar correcto",
        ]
        self.code_labels = []
        for l in lineas:
            lbl = tk.Label(pc, text=l, font=("Courier New", 9),
                           bg=p["PANEL"], fg=p["DIM"], anchor="w")
            lbl.pack(fill="x"); self.code_labels.append(lbl)

        # Controles
        ctrl = tk.Frame(self.root, bg=p["BG"]); ctrl.pack(pady=8)
        bs = dict(font=("Courier New", 10,"bold"), bg=p["PANEL"], fg=p["TEXT"],
                  relief="flat", activebackground=p["ACCENT"], activeforeground="white",
                  padx=10, pady=5, cursor="hand2")
        tk.Button(ctrl, text="🔀 Generar aleatorio", command=self._generar, **bs).pack(side="left", padx=4)
        tk.Button(ctrl, text="📂 Cargar .txt", command=self._cargar_archivo, **bs).pack(side="left", padx=4)
        self.btn_start = tk.Button(ctrl, text="▶ Iniciar", command=self.start_sort, **bs)
        self.btn_start.pack(side="left", padx=4)
        self.btn_pause = tk.Button(ctrl, text="⏸ Pausar", command=self.toggle_pause,
                                   state="disabled", **bs)
        self.btn_pause.pack(side="left", padx=4)
        tk.Label(ctrl, text=" Vel:", font=("Courier New",9), bg=p["BG"], fg=p["DIM"]).pack(side="left")
        self.speed = tk.IntVar(value=50)
        ttk.Scale(ctrl, from_=1, to=100, variable=self.speed, orient="horizontal", length=100,
                  command=lambda v: self._upd_delay()).pack(side="left", padx=4)

        self.stat_var = tk.StringVar(value="Comparaciones: 0  |  Desplazamientos: 0")
        tk.Label(self.root, textvariable=self.stat_var,
                 font=("Courier New", 9), bg=p["BG"], fg=p["DIM"]).pack()

        # Log
        log_f = tk.Frame(self.root, bg=p["PANEL"]); log_f.pack(padx=20, fill="x", pady=2)
        tk.Label(log_f, text=f"  Log → {FILE_LOG}", font=("Courier New",8),
                 bg=p["PANEL"], fg=p["DIM"]).pack(anchor="w")

    # ── Disco ──
    def _cargar_desde_disco(self):
        arr = leer_arreglo(FILE_INPUT)
        if arr:
            self.array = arr
            self.info_var.set(f"✅ Cargado desde disco: {len(arr)} elementos")
        else:
            self._generar()

    def _generar(self):
        if self.animating: return
        arr = random.sample(range(5, 100), 13)
        escribir_arreglo(FILE_INPUT, arr)
        limpiar_log(FILE_LOG)
        agregar_log(FILE_LOG, f"Arreglo generado: {arr}")
        self.array = arr
        self._highlight_code(-1)
        self.info_var.set(f"✅ Generado y guardado en arreglo_entrada.txt  ({len(arr)} elementos)")
        self.stat_var.set("Comparaciones: 0  |  Desplazamientos: 0")
        self.draw()

    def _cargar_archivo(self):
        if self.animating: return
        path = filedialog.askopenfilename(
            title="Seleccionar archivo de datos",
            initialdir=WORK_DIR,
            filetypes=[("Archivos de texto", "*.txt")])
        if path:
            arr = leer_arreglo(path)
            if arr:
                self.array = arr
                escribir_arreglo(FILE_INPUT, arr)
                limpiar_log(FILE_LOG)
                agregar_log(FILE_LOG, f"Archivo cargado: {path}")
                agregar_log(FILE_LOG, f"Arreglo: {arr}")
                self.info_var.set(f"✅ Cargado: {os.path.basename(path)}  ({len(arr)} elementos)")
                self.draw()
            else:
                messagebox.showerror("Error", "No se encontraron números en el archivo.")

    def _upd_delay(self):
        self.delay = max(50, int(1200 - self.speed.get() * 11))

    def _highlight_code(self, idx):
        p = self.p
        for i, lbl in enumerate(self.code_labels):
            lbl.config(bg=p["PANEL"] if i != idx else p["ACCENT"],
                       fg=p["DIM"] if i != idx else "white")

    def draw(self, colors=None):
        p = self.p
        self.canvas.delete("all")
        arr = self.array; n = len(arr)
        if not n: return
        w, h = 920, 230
        bw = w // n - 4; mx = max(arr)
        cols = colors if colors else [p["DEF"]] * n
        for i, v in enumerate(arr):
            x0 = i*(bw+4)+8; bh = int((v/mx)*(h-45)); y0 = h-bh-8
            x1, y1 = x0+bw, h-8
            self.canvas.create_rectangle(x0+2,y0+2,x1+2,y1+2, fill="#00000033", outline="")
            self.canvas.create_rectangle(x0,y0,x1,y1, fill=cols[i], outline="")
            self.canvas.create_text(x0+bw//2, y0-10, text=str(v),
                                    font=("Courier New",8,"bold"), fill="white")

    # ── Animación ──
    def start_sort(self):
        if self.animating or not self.array: return
        limpiar_log(FILE_LOG)
        agregar_log(FILE_LOG, f"INICIO Intercalación — arreglo: {self.array}")
        self.animating = True
        self.btn_start.config(state="disabled")
        self.btn_pause.config(state="normal")
        self.paused = False
        self.comparisons = self.shifts = 0
        self.step_gen = self._gen()
        self._next()

    def toggle_pause(self):
        self.paused = not self.paused
        self.btn_pause.config(text="▶ Reanudar" if self.paused else "⏸ Pausar")
        if not self.paused: self._next()

    def _next(self):
        if self.paused or not self.animating: return
        try:
            next(self.step_gen)
            self.root.after(self.delay, self._next)
        except StopIteration:
            self._finish()

    def _finish(self):
        p = self.p
        self.animating = False
        self.draw([p["SORTED"]]*len(self.array))
        escribir_arreglo(FILE_OUTPUT, self.array)
        agregar_log(FILE_LOG, f"FIN — arreglo ordenado: {self.array}")
        agregar_log(FILE_LOG, f"Comparaciones: {self.comparisons}  Desplazamientos: {self.shifts}")
        self.btn_start.config(state="normal")
        self.btn_pause.config(state="disabled", text="⏸ Pausar")
        self._highlight_code(-1)
        self.info_var.set("✅ Ordenado. Resultado guardado en arreglo_salida.txt y log_pasos.txt")

    def _gen(self):
        p = self.p; arr = self.array; n = len(arr)
        for i in range(1, n):
            key = arr[i]; j = i-1
            cols = [p["SORTED"]]*i + [p["DEF"]]*(n-i)
            cols[i] = p["CUR"]
            self._highlight_code(0)
            self.info_var.set(f"i={i}  key={key}  (leyendo arreglo_entrada.txt pos {i})")
            agregar_log(FILE_LOG, f"[i={i}] key={key}  arreglo: {arr}")
            self.draw(cols); yield
            cols[i] = p["KEY"]; self._highlight_code(1); self.draw(cols); yield
            while j >= 0 and arr[j] > key:
                self.comparisons += 1
                self.stat_var.set(f"Comparaciones: {self.comparisons}  |  Desplazamientos: {self.shifts}")
                c2 = cols[:]
                c2[j] = p["CMP"]; c2[j+1] = p["KEY"]
                self._highlight_code(3)
                self.info_var.set(f"arr[{j}]={arr[j]} > key={key} → desplazar ▶")
                self.draw(c2); yield
                arr[j+1] = arr[j]; self.shifts += 1
                self._highlight_code(4)
                cols = [p["SORTED"]]*(i+1) + [p["DEF"]]*(n-i-1)
                cols[j+1] = p["CMP"]; self.draw(cols); yield
                j -= 1
            arr[j+1] = key
            self.comparisons += 1
            self.stat_var.set(f"Comparaciones: {self.comparisons}  |  Desplazamientos: {self.shifts}")
            cols = [p["SORTED"]]*(i+1) + [p["DEF"]]*(n-i-1)
            cols[j+1] = p["KEY"]; self._highlight_code(6)
            self.info_var.set(f"key={key} insertado en posición {j+1}")
            # Guardar estado parcial en disco
            escribir_arreglo(FILE_OUTPUT, arr)
            self.draw(cols); yield


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 2: MEZCLA DIRECTA
# ══════════════════════════════════════════════════════════════════════════════

class MezclaDirectaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mezcla Directa — Straight Merge Sort")
        p = PAL["mezcla_directa"]
        self.p = p
        self.root.configure(bg=p["BG"])
        self.root.geometry("960x710")
        self.root.resizable(False, False)
        self.array = []
        self.animating = False
        self.paused = False
        self.delay = 500
        self.step_gen = None
        self._build_ui()
        self._cargar_desde_disco()

    def _build_ui(self):
        p = self.p
        tk.Label(self.root, text="🔀  MEZCLA DIRECTA  (Straight Merge Sort)",
                 font=("Courier New", 17, "bold"), bg=p["BG"], fg=p["ACCENT"]
                 ).pack(pady=(12,2))
        tk.Label(self.root,
                 text="Lee/escribe cinta_1.txt … cinta_4.txt y arreglo_salida.txt",
                 font=("Courier New", 9), bg=p["BG"], fg=p["DIM"]).pack()

        self.canvas = tk.Canvas(self.root, width=920, height=210,
                                bg=p["PANEL"], highlightthickness=0)
        self.canvas.pack(padx=20, pady=4)

        leg = tk.Frame(self.root, bg=p["BG"]); leg.pack(pady=2)
        for col, txt in [(p["DEF"],"Sin procesar"),(p["RUN_A"],"Run A"),
                         (p["RUN_B"],"Run B"),(p["MERGE"],"Mezclando"),(p["DONE"],"Ordenado")]:
            f = tk.Frame(leg, bg=p["BG"]); f.pack(side="left", padx=7)
            tk.Label(f, width=3, bg=col, relief="flat").pack(side="left")
            tk.Label(f, text=txt, font=("Courier New",9), bg=p["BG"], fg=p["TEXT"]).pack(side="left",padx=2)

        self.info_var = tk.StringVar(value="Cargando desde disco...")
        tk.Label(self.root, textvariable=self.info_var,
                 font=("Courier New", 11, "bold"), bg=p["BG"], fg=p["TEXT"],
                 wraplength=900, justify="center").pack(pady=3)

        self.runs_var = tk.StringVar(value="")
        tk.Label(self.root, textvariable=self.runs_var,
                 font=("Courier New", 9), bg=p["BG"], fg=p["RUN_A"],
                 wraplength=900, justify="center").pack()

        pc = tk.Frame(self.root, bg=p["PANEL"]); pc.pack(padx=20, fill="x", pady=2)
        tk.Label(pc, text="  Pseudocódigo:", font=("Courier New",9,"bold"),
                 bg=p["PANEL"], fg=p["ACCENT"]).pack(anchor="w")
        lineas = [
            "  1. Detectar runs: secuencias ascendentes naturales  → escribe cinta_1.txt / cinta_2.txt",
            "  2. Si 1 solo run → ¡listo! Guardar en arreglo_salida.txt",
            "  3. Mezclar runs adyacentes (cinta_1 + cinta_2) → cinta_3 / cinta_4",
            "     mientras A y B tengan elementos: menor al resultado",
            "     copiar restos de A o B",
            "  4. Resultado (cintas más grandes) → nueva cinta_1 / cinta_2 → ir a 1",
        ]
        self.code_labels = []
        for l in lineas:
            lbl = tk.Label(pc, text=l, font=("Courier New",9),
                           bg=p["PANEL"], fg=p["DIM"], anchor="w")
            lbl.pack(fill="x"); self.code_labels.append(lbl)

        ctrl = tk.Frame(self.root, bg=p["BG"]); ctrl.pack(pady=6)
        bs = dict(font=("Courier New",10,"bold"), bg=p["PANEL"], fg=p["TEXT"],
                  relief="flat", activebackground=p["ACCENT"], activeforeground="white",
                  padx=10, pady=5, cursor="hand2")
        tk.Button(ctrl, text="🔀 Generar aleatorio", command=self._generar, **bs).pack(side="left",padx=4)
        tk.Button(ctrl, text="📂 Cargar .txt", command=self._cargar_archivo, **bs).pack(side="left",padx=4)
        self.btn_start = tk.Button(ctrl, text="▶ Iniciar", command=self.start_sort, **bs)
        self.btn_start.pack(side="left",padx=4)
        self.btn_pause = tk.Button(ctrl, text="⏸ Pausar", command=self.toggle_pause,
                                   state="disabled", **bs)
        self.btn_pause.pack(side="left",padx=4)
        tk.Label(ctrl, text=" Vel:", font=("Courier New",9), bg=p["BG"], fg=p["DIM"]).pack(side="left")
        self.speed = tk.IntVar(value=50)
        ttk.Scale(ctrl, from_=1, to=100, variable=self.speed, orient="horizontal", length=100,
                  command=lambda v: self._upd_delay()).pack(side="left",padx=4)

        self.stat_var = tk.StringVar(value="Pasadas: 0  |  Mezclas: 0  |  Comparaciones: 0")
        tk.Label(self.root, textvariable=self.stat_var,
                 font=("Courier New",9), bg=p["BG"], fg=p["DIM"]).pack()

        tk.Label(self.root, text=f"Cintas: {WORK_DIR}",
                 font=("Courier New",8), bg=p["BG"], fg=p["DIM"]).pack(pady=2)

    def _cargar_desde_disco(self):
        arr = leer_arreglo(FILE_INPUT)
        if arr:
            self.array = arr
            self.info_var.set(f"✅ Cargado: {len(arr)} elementos de arreglo_entrada.txt")
        else:
            self._generar()

    def _generar(self):
        if self.animating: return
        arr = random.sample(range(4, 99), 14)
        escribir_arreglo(FILE_INPUT, arr)
        limpiar_log(FILE_LOG)
        limpiar_cintas()
        agregar_log(FILE_LOG, f"Arreglo generado: {arr}")
        self.array = arr
        self._highlight_code(-1); self.runs_var.set("")
        self.stat_var.set("Pasadas: 0  |  Mezclas: 0  |  Comparaciones: 0")
        self.info_var.set(f"✅ Generado → arreglo_entrada.txt  ({len(arr)} elementos)")
        self.draw([self.p["DEF"]]*len(arr))

    def _cargar_archivo(self):
        if self.animating: return
        path = filedialog.askopenfilename(title="Seleccionar .txt",
                                          initialdir=WORK_DIR,
                                          filetypes=[("Texto","*.txt")])
        if path:
            arr = leer_arreglo(path)
            if arr:
                self.array = arr
                escribir_arreglo(FILE_INPUT, arr)
                limpiar_cintas(); limpiar_log(FILE_LOG)
                self.info_var.set(f"✅ Cargado: {os.path.basename(path)}  ({len(arr)} elementos)")
                self.draw([self.p["DEF"]]*len(arr))
            else:
                messagebox.showerror("Error","No se encontraron números.")

    def _upd_delay(self):
        self.delay = max(60, int(1100 - self.speed.get()*10))

    def _highlight_code(self, idx):
        p = self.p
        for i, lbl in enumerate(self.code_labels):
            lbl.config(bg=p["PANEL"] if i!=idx else p["ACCENT"],
                       fg=p["DIM"] if i!=idx else "white")

    def draw(self, colors):
        p = self.p; self.canvas.delete("all")
        arr = self.array; n = len(arr)
        if not n: return
        w,h = 920,210; bw = w//n-4; mx = max(arr)
        for i,v in enumerate(arr):
            x0=i*(bw+4)+8; bh=int((v/mx)*(h-40)); y0=h-bh-6
            x1,y1=x0+bw,h-6
            col=colors[i] if i<len(colors) else p["DEF"]
            self.canvas.create_rectangle(x0+2,y0+2,x1+2,y1+2,fill="#00000033",outline="")
            self.canvas.create_rectangle(x0,y0,x1,y1,fill=col,outline="")
            self.canvas.create_text(x0+bw//2,y0-9,text=str(v),
                                    font=("Courier New",8,"bold"),fill="white")

    def start_sort(self):
        if self.animating or not self.array: return
        limpiar_log(FILE_LOG); limpiar_cintas()
        agregar_log(FILE_LOG, f"INICIO Mezcla Directa — arreglo: {self.array}")
        self.animating = True
        self.btn_start.config(state="disabled")
        self.btn_pause.config(state="normal")
        self.paused = False
        self.passes = self.merges = self.comps = 0
        self.step_gen = self._gen()
        self._next()

    def toggle_pause(self):
        self.paused = not self.paused
        self.btn_pause.config(text="▶ Reanudar" if self.paused else "⏸ Pausar")
        if not self.paused: self._next()

    def _next(self):
        if self.paused or not self.animating: return
        try:
            next(self.step_gen)
            self.root.after(self.delay, self._next)
        except StopIteration:
            self._finish()

    def _finish(self):
        p = self.p
        self.animating = False
        self.draw([p["DONE"]]*len(self.array))
        escribir_arreglo(FILE_OUTPUT, self.array)
        agregar_log(FILE_LOG, f"FIN — resultado: {self.array}")
        self.btn_start.config(state="normal")
        self.btn_pause.config(state="disabled",text="⏸ Pausar")
        self._highlight_code(-1); self.runs_var.set("")
        self.info_var.set("✅ Ordenado. Resultado en arreglo_salida.txt y cinta_*.txt")

    def _find_runs(self, lst):
        if not lst: return []
        runs, run = [], [lst[0]]
        for v in lst[1:]:
            if v >= run[-1]: run.append(v)
            else: runs.append(run); run = [v]
        runs.append(run); return runs

    def _gen(self):
        p = self.p; arr = self.array; n = len(arr)
        while True:
            runs = self._find_runs(arr)
            self._highlight_code(0)
            # Distribuir runs en cinta_1 y cinta_2
            c1 = [runs[i] for i in range(0,len(runs),2)]
            c2 = [runs[i] for i in range(1,len(runs),2)]
            escribir_runs(FILE_CINTA[0], c1)
            escribir_runs(FILE_CINTA[1], c2)
            agregar_log(FILE_LOG, f"Runs detectados: {len(runs)}  C1:{[r for r in c1]}  C2:{[r for r in c2]}")
            # Colorear
            cols = [p["DEF"]]*n; flat_pos = 0
            for ridx, run in enumerate(runs):
                c = p["RUN_A"] if ridx%2==0 else p["RUN_B"]
                for _ in run: cols[flat_pos]=c; flat_pos+=1
            strs = ["["+",".join(str(x) for x in r)+"]" for r in runs]
            self.runs_var.set("Runs: "+"  ".join(strs))
            self.info_var.set(f"📊 {len(runs)} run(s) → escritos en cinta_1.txt / cinta_2.txt")
            self.draw(cols); yield
            if len(runs)==1: break

            self.passes += 1
            c3_runs, c4_runs = [], []
            dest = 0
            while c1 or c2:
                ra = c1.pop(0) if c1 else []
                rb = c2.pop(0) if c2 else []
                self.merges += 1
                self._highlight_code(2)
                # Colorear los dos runs
                pos = 0; cols2 = [p["DEF"]]*n
                for v in arr:
                    if v in ra: cols2[pos]=p["RUN_A"]
                    elif v in rb: cols2[pos]=p["RUN_B"]
                    pos+=1
                self.info_var.set(f"🔀 Mezclando C1:{ra} + C2:{rb}")
                self.draw(cols2); yield
                # Merge
                merged=[]; ia=ib=0
                while ia<len(ra) and ib<len(rb):
                    self.comps+=1
                    self.stat_var.set(f"Pasadas: {self.passes}  |  Mezclas: {self.merges}  |  Comparaciones: {self.comps}")
                    if ra[ia]<=rb[ib]: merged.append(ra[ia]); ia+=1
                    else: merged.append(rb[ib]); ib+=1
                    self._highlight_code(3); self.draw(cols2); yield
                merged += ra[ia:]+rb[ib:]
                if dest==0: c3_runs.append(merged)
                else: c4_runs.append(merged)
                dest ^= 1
                # Actualizar arr parcialmente
                self.info_var.set(f"✔ Mezcla → {merged}  (cinta_{'3' if dest==1 else '4'}.txt)")
                cols3=[p["DEF"]]*n
                flat2=[x for r in (c3_runs+c4_runs) for x in r]
                for i2,v2 in enumerate(flat2[:n]): cols3[i2]=p["DONE"]
                self.draw(cols3); yield

            # Escribir cintas resultado
            escribir_runs(FILE_CINTA[2], c3_runs)
            escribir_runs(FILE_CINTA[3], c4_runs)
            agregar_log(FILE_LOG, f"Pasada {self.passes}: C3={c3_runs}  C4={c4_runs}")
            # Reconstruir arreglo desde cintas c3+c4 entrelazadas para siguiente pasada
            new_runs = []
            max_len = max(len(c3_runs), len(c4_runs))
            for i2 in range(max_len):
                if i2 < len(c3_runs): new_runs.append(c3_runs[i2])
                if i2 < len(c4_runs): new_runs.append(c4_runs[i2])
            arr[:] = [x for r in new_runs for x in r]
            self.array[:] = arr
            # Siguiente iteración usa c3/c4 como nuevas c1/c2
            c1, c2 = c3_runs[:], c4_runs[:]
            escribir_runs(FILE_CINTA[0], c1)
            escribir_runs(FILE_CINTA[1], c2)
            self._highlight_code(5)
            self.info_var.set(f"🔄 Pasada {self.passes} completa → cinta_3→cinta_1, cinta_4→cinta_2")
            self.draw([p["SORTED"]]*n); yield


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 3: MEZCLA EQUILIBRADA
# ══════════════════════════════════════════════════════════════════════════════

class MezclaEquilibradaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mezcla Equilibrada — Balanced Merge Sort")
        p = PAL["mezcla_eq"]
        self.p = p
        self.root.configure(bg=p["BG"])
        self.root.geometry("980x730")
        self.root.resizable(False, False)
        self.array = []
        self.animating = False
        self.paused = False
        self.delay = 600
        self.step_gen = None
        self.TAPE_COL = [p["C1"], p["C2"], p["C3"], p["C4"]]
        self._build_ui()
        self._cargar_desde_disco()

    def _build_ui(self):
        p = self.p
        tk.Label(self.root, text="🎞  MEZCLA EQUILIBRADA  (Balanced Merge Sort)",
                 font=("Courier New",17,"bold"), bg=p["BG"], fg=p["ACCENT"]).pack(pady=(10,2))
        tk.Label(self.root,
                 text="Lee/escribe temp_1.txt … temp_4.txt (cintas auxiliares en disco)",
                 font=("Courier New",9), bg=p["BG"], fg=p["DIM"]).pack()

        tk.Label(self.root,text="Arreglo actual:",
                 font=("Courier New",9,"bold"),bg=p["BG"],fg=p["TEXT"]).pack(anchor="w",padx=28)
        self.canvas_main = tk.Canvas(self.root, width=920, height=110,
                                     bg=p["PANEL"], highlightthickness=0)
        self.canvas_main.pack(padx=20, pady=2)

        tk.Label(self.root, text="Cintas auxiliares (temp_1…temp_4):",
                 font=("Courier New",9,"bold"), bg=p["BG"], fg=p["TEXT"]).pack(anchor="w",padx=28,pady=(4,0))
        self.canvas_tapes = tk.Canvas(self.root, width=920, height=150,
                                      bg=p["PANEL"], highlightthickness=0)
        self.canvas_tapes.pack(padx=20, pady=2)

        self.info_var = tk.StringVar(value="Cargando desde disco...")
        tk.Label(self.root, textvariable=self.info_var,
                 font=("Courier New",11,"bold"), bg=p["BG"], fg=p["TEXT"],
                 wraplength=900, justify="center").pack(pady=3)

        pc = tk.Frame(self.root, bg=p["PANEL"]); pc.pack(padx=20, fill="x", pady=2)
        tk.Label(pc, text="  Pseudocódigo (4 cintas: T1 T2 → T3 T4):",
                 font=("Courier New",9,"bold"), bg=p["PANEL"], fg=p["ACCENT"]).pack(anchor="w")
        lineas = [
            "  1. Distribuir runs alternando entre T1 (temp_1.txt) y T2 (temp_2.txt)",
            "  2. Mientras haya más de 1 run en total:",
            "  3.     Mezclar 1 run T1 + 1 run T2 → colocar alternando en T3 y T4",
            "  4.     Intercambiar: (T1,T2) ← (T3,T4) ;  limpiar T3, T4",
            "  5. El resultado en T1 (o T2) es el arreglo ordenado → arreglo_salida.txt",
        ]
        self.code_labels = []
        for l in lineas:
            lbl = tk.Label(pc, text=l, font=("Courier New",9),
                           bg=p["PANEL"], fg=p["DIM"], anchor="w")
            lbl.pack(fill="x"); self.code_labels.append(lbl)

        ctrl = tk.Frame(self.root, bg=p["BG"]); ctrl.pack(pady=6)
        bs = dict(font=("Courier New",10,"bold"), bg=p["PANEL"], fg=p["TEXT"],
                  relief="flat", activebackground=p["ACCENT"], activeforeground="white",
                  padx=10, pady=5, cursor="hand2")
        tk.Button(ctrl, text="🔀 Generar aleatorio", command=self._generar, **bs).pack(side="left",padx=4)
        tk.Button(ctrl, text="📂 Cargar .txt", command=self._cargar_archivo, **bs).pack(side="left",padx=4)
        self.btn_start = tk.Button(ctrl, text="▶ Iniciar", command=self.start_sort, **bs)
        self.btn_start.pack(side="left",padx=4)
        self.btn_pause = tk.Button(ctrl, text="⏸ Pausar", command=self.toggle_pause,
                                   state="disabled", **bs)
        self.btn_pause.pack(side="left",padx=4)
        tk.Label(ctrl, text=" Vel:", font=("Courier New",9), bg=p["BG"], fg=p["DIM"]).pack(side="left")
        self.speed = tk.IntVar(value=50)
        ttk.Scale(ctrl, from_=1, to=100, variable=self.speed, orient="horizontal", length=100,
                  command=lambda v: self._upd_delay()).pack(side="left",padx=4)

        self.stat_var = tk.StringVar(value="Pasada: 0  |  Mezclas: 0  |  Comparaciones: 0")
        tk.Label(self.root, textvariable=self.stat_var,
                 font=("Courier New",9), bg=p["BG"], fg=p["DIM"]).pack()
        tk.Label(self.root, text=f"Cintas: {WORK_DIR}",
                 font=("Courier New",8), bg=p["BG"], fg=p["DIM"]).pack(pady=1)

    def _cargar_desde_disco(self):
        arr = leer_arreglo(FILE_INPUT)
        if arr:
            self.array = arr
            self.info_var.set(f"✅ Cargado: {len(arr)} elementos de arreglo_entrada.txt")
            self.draw_main(arr, [self.p["C1"]]*len(arr))
            self.draw_tapes([[],[],[],[]])
        else:
            self._generar()

    def _generar(self):
        if self.animating: return
        arr = random.sample(range(4,99), 12)
        escribir_arreglo(FILE_INPUT, arr)
        limpiar_log(FILE_LOG); limpiar_cintas()
        agregar_log(FILE_LOG, f"Arreglo generado: {arr}")
        self.array = arr
        self._highlight_code(-1)
        self.stat_var.set("Pasada: 0  |  Mezclas: 0  |  Comparaciones: 0")
        self.info_var.set(f"✅ Generado → arreglo_entrada.txt  ({len(arr)} elementos)")
        self.draw_main(arr, ["#444"]*len(arr))
        self.draw_tapes([[],[],[],[]])

    def _cargar_archivo(self):
        if self.animating: return
        path = filedialog.askopenfilename(title="Seleccionar .txt",
                                          initialdir=WORK_DIR,
                                          filetypes=[("Texto","*.txt")])
        if path:
            arr = leer_arreglo(path)
            if arr:
                self.array = arr
                escribir_arreglo(FILE_INPUT, arr)
                limpiar_cintas(); limpiar_log(FILE_LOG)
                self.info_var.set(f"✅ Cargado: {os.path.basename(path)}  ({len(arr)} elementos)")
                self.draw_main(arr, ["#444"]*len(arr))
                self.draw_tapes([[],[],[],[]])
            else:
                messagebox.showerror("Error","No se encontraron números.")

    def _upd_delay(self):
        self.delay = max(60, int(1200 - self.speed.get()*11))

    def _highlight_code(self, idx):
        p = self.p
        for i, lbl in enumerate(self.code_labels):
            lbl.config(bg=p["PANEL"] if i!=idx else p["ACCENT"],
                       fg=p["DIM"] if i!=idx else "white")

    def draw_main(self, arr, colors):
        p = self.p; self.canvas_main.delete("all")
        n = len(arr)
        if not n: return
        w,h = 920,110; bw=w//n-3; mx=max(arr)
        for i,v in enumerate(arr):
            x0=i*(bw+3)+5; bh=int((v/mx)*(h-28)); y0=h-bh-5
            x1,y1=x0+bw,h-5
            col=colors[i] if i<len(colors) else "#444"
            self.canvas_main.create_rectangle(x0+2,y0+2,x1+2,y1+2,fill="#00000044",outline="")
            self.canvas_main.create_rectangle(x0,y0,x1,y1,fill=col,outline="")
            self.canvas_main.create_text(x0+bw//2,y0-7,text=str(v),
                                         font=("Courier New",8,"bold"),fill="white")

    def draw_tapes(self, tapes):
        """tapes: lista de 4 listas (cada una puede ser lista de runs o lista plana)"""
        p = self.p; self.canvas_tapes.delete("all")
        names = ["T1","T2","T3","T4"]
        tape_y = [5, 42, 82, 120]
        for tidx,(tape,col,name,ty) in enumerate(zip(tapes,self.TAPE_COL,names,tape_y)):
            self.canvas_tapes.create_text(22,ty+14,text=name,
                                          font=("Courier New",10,"bold"),fill=col,anchor="w")
            self.canvas_tapes.create_rectangle(45,ty,915,ty+27,
                                               fill="#1a0030",outline=col,width=1)
            flat=[]; seps=[]
            if tape and isinstance(tape[0],list):
                for run in tape:
                    flat.extend(run); seps.append(len(flat))
            else:
                flat=list(tape)
            x=50
            for eidx,v in enumerate(flat):
                cw=28
                self.canvas_tapes.create_rectangle(x,ty+2,x+cw-2,ty+25,fill=col,outline="")
                self.canvas_tapes.create_text(x+cw//2-1,ty+13,text=str(v),
                                              font=("Courier New",8,"bold"),fill="white")
                x+=cw
                if (eidx+1) in seps and (eidx+1)<len(flat):
                    self.canvas_tapes.create_line(x,ty+2,x,ty+25,fill="white",width=2,dash=(4,2))

    def start_sort(self):
        if self.animating or not self.array: return
        limpiar_log(FILE_LOG); limpiar_cintas()
        agregar_log(FILE_LOG, f"INICIO Mezcla Equilibrada — arreglo: {self.array}")
        self.animating = True
        self.btn_start.config(state="disabled")
        self.btn_pause.config(state="normal")
        self.paused = False
        self.pass_num = self.merges = self.comps = 0
        self.step_gen = self._gen()
        self._next()

    def toggle_pause(self):
        self.paused = not self.paused
        self.btn_pause.config(text="▶ Reanudar" if self.paused else "⏸ Pausar")
        if not self.paused: self._next()

    def _next(self):
        if self.paused or not self.animating: return
        try:
            next(self.step_gen)
            self.root.after(self.delay, self._next)
        except StopIteration:
            self._finish()

    def _finish(self):
        p = self.p; n = len(self.array)
        self.animating = False
        self.draw_main(self.array, [p["DONE"]]*n)
        self.draw_tapes([[],[],[],[]])
        escribir_arreglo(FILE_OUTPUT, self.array)
        agregar_log(FILE_LOG, f"FIN — resultado: {self.array}")
        self.btn_start.config(state="normal")
        self.btn_pause.config(state="disabled",text="⏸ Pausar")
        self._highlight_code(-1)
        self.info_var.set("✅ Ordenado. Guardado en arreglo_salida.txt  |  temp_1…4.txt")

    def _find_runs(self, lst):
        if not lst: return []
        runs, run = [], [lst[0]]
        for v in lst[1:]:
            if v >= run[-1]: run.append(v)
            else: runs.append(run); run=[v]
        runs.append(run); return runs

    def _gen(self):
        p = self.p; arr = self.array; n = len(arr)

        # Detectar runs e inicializar t1, t2
        runs = self._find_runs(arr)
        t1 = [runs[i] for i in range(0,len(runs),2)]
        t2 = [runs[i] for i in range(1,len(runs),2)]
        escribir_runs(FILE_TEMP[0], t1)
        escribir_runs(FILE_TEMP[1], t2)
        self._highlight_code(0)
        self.info_var.set(f"📋 {len(runs)} run(s) → distribuidos en temp_1.txt / temp_2.txt")
        agregar_log(FILE_LOG, f"Distribución inicial T1:{t1}  T2:{t2}")
        self.draw_tapes([t1, t2, [], []])
        yield

        while len(t1)+len(t2) > 1:
            self.pass_num += 1
            t3, t4 = [], []
            dest = 0
            self._highlight_code(2)

            while t1 or t2:
                ra = t1.pop(0) if t1 else []
                rb = t2.pop(0) if t2 else []
                self.merges += 1
                dest_name = "T3" if dest==0 else "T4"
                self.info_var.set(
                    f"🔀 Mezclando  T1:{ra}  +  T2:{rb}  →  {dest_name}")
                agregar_log(FILE_LOG, f"  Mezcla: {ra} + {rb}")
                self.draw_tapes([t1, t2, t3, t4]); yield

                merged=[]; ia=ib=0
                while ia<len(ra) and ib<len(rb):
                    self.comps+=1
                    self.stat_var.set(
                        f"Pasada: {self.pass_num}  |  Mezclas: {self.merges}  |  Comparaciones: {self.comps}")
                    if ra[ia]<=rb[ib]: merged.append(ra[ia]); ia+=1
                    else: merged.append(rb[ib]); ib+=1
                    self.draw_tapes([t1, t2, t3, t4]); yield
                merged += ra[ia:]+rb[ib:]

                if dest==0: t3.append(merged)
                else: t4.append(merged)
                dest ^= 1

                # Actualizar cintas en disco
                escribir_runs(FILE_TEMP[2], t3)
                escribir_runs(FILE_TEMP[3], t4)
                self.draw_tapes([t1, t2, t3, t4]); yield

            # Intercambiar roles
            self._highlight_code(3)
            self.info_var.set(f"🔄 Pasada {self.pass_num} completa → T1←T3, T2←T4")
            agregar_log(FILE_LOG, f"Pasada {self.pass_num}: T3={t3}  T4={t4}")
            self.draw_tapes([t1, t2, t3, t4]); yield

            t1, t2 = t3[:], t4[:]
            escribir_runs(FILE_TEMP[0], t1)
            escribir_runs(FILE_TEMP[1], t2)
            # Limpiar t3, t4 en disco
            with open(FILE_TEMP[2],"w") as f: pass
            with open(FILE_TEMP[3],"w") as f: pass
            self.draw_tapes([t1, t2, [], []]); yield

        # Reconstruir arreglo final
        self._highlight_code(4)
        src = t1 if t1 else t2
        result = [x for run in src for x in run]
        arr[:] = result; self.array[:] = result
        self.draw_main(arr, [p["DONE"]]*n)
        self.draw_tapes([[],[],[],[]])
        self.info_var.set("✅ Reconstruido desde temp_1.txt → guardando arreglo_salida.txt")
        yield


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    MenuApp(root)
    root.mainloop()
