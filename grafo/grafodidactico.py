"""
╔══════════════════════════════════════════════════════════════╗
║         TDA GRAFO - Implementación Visual e Interactiva      ║
║         Basado en el Tipo de Dato Abstracto Grafo            ║
╚══════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math
import random


# ═══════════════════════════════════════════════════════════
#  CLASE POSICION (nodo base del TDA)
# ═══════════════════════════════════════════════════════════
class Posicion:
    def __init__(self, elemento):
        self._elemento = elemento

    def elemento(self):
        return self._elemento

    def __repr__(self):
        return f"Pos({self._elemento})"


# ═══════════════════════════════════════════════════════════
#  CLASE VERTICE
# ═══════════════════════════════════════════════════════════
class Vertice(Posicion):
    def __init__(self, elemento):
        super().__init__(elemento)
        self._indice = None  # para la matriz de adyacencia

    def __repr__(self):
        return f"V({self._elemento})"

    def __hash__(self):
        return hash(id(self))


# ═══════════════════════════════════════════════════════════
#  CLASE ARISTA
# ═══════════════════════════════════════════════════════════
class Arista(Posicion):
    def __init__(self, u, v, elemento=None, dirigida=False):
        super().__init__(elemento)
        self._origen = u
        self._destino = v
        self._dirigida = dirigida

    def verticesFinales(self):
        """Devuelve un array de tamaño con los vértices finales de e"""
        return (self._origen, self._destino)

    def opuesto(self, v):
        """Devuelve los puntos extremos de la arista e diferente a v"""
        if v is self._origen:
            return self._destino
        elif v is self._destino:
            return self._origen
        raise ValueError("v no es un vértice de esta arista")

    def esDirigida(self):
        """Devuelve verdadero si la arista e es dirigida"""
        return self._dirigida

    def origen(self):
        """Devuelve el origen de la arista dirigida e"""
        return self._origen

    def destino(self):
        """Devuelve el destino de la arista dirigida e"""
        return self._destino

    def __repr__(self):
        flecha = "→" if self._dirigida else "—"
        peso = f" [{self._elemento}]" if self._elemento is not None else ""
        return f"A({self._origen._elemento}{flecha}{self._destino._elemento}{peso})"

    def __hash__(self):
        return hash((id(self._origen), id(self._destino)))


# ═══════════════════════════════════════════════════════════
#  CLASE GRAFO (TDA completo)
# ═══════════════════════════════════════════════════════════
class Grafo:
    """
    Implementación del TDA Grafo usando lista de adyacencia.
    Soporta grafos dirigidos y no dirigidos.
    """

    def __init__(self, dirigido=False):
        self._dirigido = dirigido
        self._vertices = {}   # vertice -> dict de aristas incidentes
        self._num_aristas = 0

    # ── Operaciones posicionales ──────────────────────────
    def tamano(self):
        """Devuelve el número de vértices más el número de aristas de G"""
        return self.numVertices() + self.numAristas()

    def estaVacio(self):
        """Devuelve True si el grafo está vacío"""
        return len(self._vertices) == 0

    def elementos(self):
        """Devuelve todos los elementos almacenados"""
        elems = [v.elemento() for v in self._vertices]
        elems += [a.elemento() for a in self.aristas()]
        return elems

    def posiciones(self):
        """Devuelve todas las posiciones (vértices y aristas)"""
        pos = list(self._vertices.keys())
        pos += list(self.aristas())
        return pos

    def reemplazar(self, p, r):
        """Reemplaza el elemento en posición p por r"""
        p._elemento = r

    def intercambiar(self, p, q):
        """Intercambia los elementos de las posiciones p y q"""
        p._elemento, q._elemento = q._elemento, p._elemento

    # ── Operaciones generales ─────────────────────────────
    def numVertices(self):
        """Devuelve el número de vértices de G"""
        return len(self._vertices)

    def numAristas(self):
        """Devuelve el número de aristas de G"""
        return self._num_aristas

    def vertices(self):
        """Devuelve una lista de los índices de los vértices de G"""
        return list(self._vertices.keys())

    def aristas(self):
        """Devuelve una lista de los índices de las aristas de G"""
        resultado = set()
        for aristas_dict in self._vertices.values():
            for a in aristas_dict.values():
                resultado.add(a)
        return list(resultado)

    def grado(self, v, salida=True):
        """Devuelve el grado de v"""
        adj = self._vertices[v]
        if self._dirigido and not salida:
            return sum(1 for a in adj.values() if a.destino() is v)
        return len(adj)

    def verticesAdyacentes(self, v):
        """Devuelve una lista de los vértices adyacentes a v"""
        return [a.opuesto(v) for a in self._vertices[v].values()]

    def aristasIncidentes(self, v):
        """Devuelve una lista de las aristas incidentes en v"""
        return list(self._vertices[v].values())

    def esAdyacente(self, v, w):
        """Devuelve verdadero si los vértices v y w son adyacentes"""
        return w in self._vertices[v]

    def obtenerArista(self, u, v):
        """Devuelve la arista entre u y v, o None si no existe"""
        return self._vertices[u].get(v)

    # ── Operaciones con aristas dirigidas ─────────────────
    def aristasDirigidas(self):
        """Devuelve una lista de todas las aristas dirigidas"""
        return [a for a in self.aristas() if a.esDirigida()]

    def aristasNodirigidas(self):
        """Devuelve una lista de todas las aristas no dirigidas"""
        return [a for a in self.aristas() if not a.esDirigida()]

    def gradoEnt(self, v):
        """Devuelve el grado de entrada de v"""
        if not self._dirigido:
            return self.grado(v)
        return sum(1 for a in self.aristas() if a.destino() is v)

    def gradoSalida(self, v):
        """Devuelve el grado de salida de v"""
        if not self._dirigido:
            return self.grado(v)
        return sum(1 for a in self.aristas() if a.origen() is v)

    def aristasIncidentesEnt(self, v):
        """Devuelve una lista de todas las aristas de entrada a v"""
        if not self._dirigido:
            return self.aristasIncidentes(v)
        return [a for a in self.aristas() if a.destino() is v]

    def aristasIncidentesSal(self, v):
        """Devuelve una lista de todas las aristas de salida a v"""
        if not self._dirigido:
            return self.aristasIncidentes(v)
        return [a for a in self.aristas() if a.origen() is v]

    def verticesAdyacentesEnt(self, v):
        """Devuelve una lista de todos los vértices adyacentes entrantes a v"""
        return [a.origen() for a in self.aristasIncidentesEnt(v)]

    def verticesAdyacentesSal(self, v):
        """Devuelve una lista de todos los vértices adyacentes salientes de v"""
        return [a.destino() for a in self.aristasIncidentesSal(v)]

    # ── Operaciones de actualización ──────────────────────
    def insertaVertice(self, o):
        """Inserta y devuelve un nuevo vértice almacenando el objeto o"""
        v = Vertice(o)
        self._vertices[v] = {}
        return v

    def insertaArista(self, v, w, o=None):
        """Inserta y devuelve una arista no dirigida entre v y w"""
        a = Arista(v, w, o, dirigida=False)
        self._vertices[v][w] = a
        self._vertices[w][v] = a
        self._num_aristas += 1
        return a

    def insertaAristaDirigida(self, v, w, o=None):
        """Inserta y devuelve una arista dirigida entre v y w"""
        a = Arista(v, w, o, dirigida=True)
        self._vertices[v][w] = a
        self._num_aristas += 1
        return a

    def eliminaVertice(self, v):
        """Elimina vértice v y todas las aristas incidentes"""
        for w in list(self._vertices[v].keys()):
            self._elimina_arista_interna(self._vertices[v][w])
        del self._vertices[v]

    def _elimina_arista_interna(self, a):
        u, w = a.verticesFinales()
        if w in self._vertices.get(u, {}):
            del self._vertices[u][w]
        if not a.esDirigida():
            if u in self._vertices.get(w, {}):
                del self._vertices[w][u]
        self._num_aristas -= 1

    def eliminaArista(self, a):
        """Elimina arista a"""
        self._elimina_arista_interna(a)

    def convierteNoDirigida(self, a):
        """Convierte la arista a en no dirigida"""
        u, w = a.verticesFinales()
        a._dirigida = False
        self._vertices[w][u] = a

    def invierteDir(self, a):
        """Invierte la dirección de la arista dirigida a"""
        u, w = a.verticesFinales()
        del self._vertices[u][w]
        a._origen, a._destino = a._destino, a._origen
        self._vertices[w][u] = a

    def asignaDirDesde(self, a, v):
        """Produce arista dirigida a salga del vértice v"""
        u, w = a.verticesFinales()
        if v is w:
            self.invierteDir(a)
        a._dirigida = True

    def asignaDirA(self, a, v):
        """Produce arista dirigida a entrante al vértice v"""
        u, w = a.verticesFinales()
        if v is u:
            self.invierteDir(a)
        a._dirigida = True

    def __repr__(self):
        return (f"Grafo({'Dirigido' if self._dirigido else 'No Dirigido'}) | "
                f"{self.numVertices()} vértices, {self.numAristas()} aristas")


# ═══════════════════════════════════════════════════════════
#  INTERFAZ GRÁFICA
# ═══════════════════════════════════════════════════════════

COLORES = {
    "fondo":       "#0a0e1a",
    "panel":       "#111827",
    "panel2":      "#1a2235",
    "acento":      "#00d4ff",
    "acento2":     "#ff6b35",
    "acento3":     "#7c3aed",
    "texto":       "#e2e8f0",
    "texto2":      "#94a3b8",
    "vertice":     "#1e3a5f",
    "vertice_sel": "#00d4ff",
    "arista":      "#334155",
    "arista_dir":  "#ff6b35",
    "verde":       "#10b981",
    "rojo":        "#ef4444",
    "amarillo":    "#f59e0b",
}

FUENTE_TITULO  = ("Courier New", 13, "bold")
FUENTE_NORMAL  = ("Courier New", 10)
FUENTE_PEQUENA = ("Courier New", 9)
FUENTE_MONO    = ("Courier New", 11)


class AplicacionGrafo:
    def __init__(self, root):
        self.root = root
        self.root.title("TDA Grafo — Visualizador Interactivo")
        self.root.configure(bg=COLORES["fondo"])
        self.root.geometry("1280x780")

        self.grafo = Grafo(dirigido=False)
        self.posiciones_vis = {}   # vertice -> (x, y)
        self.seleccionado = None   # vertice seleccionado para arista
        self.vertex_items = {}     # vertice -> canvas item id
        self.log_lines = []

        self._construir_ui()
        self._log("✦ TDA Grafo inicializado. ¡Empieza agregando vértices!")
        self._log("  Modo: Grafo No Dirigido")

    # ── Construcción de la UI ─────────────────────────────
    def _construir_ui(self):
        # Título
        titulo = tk.Label(self.root,
            text="◈  T D A   G R A F O  ◈",
            font=("Courier New", 16, "bold"),
            fg=COLORES["acento"], bg=COLORES["fondo"])
        titulo.pack(pady=(10, 0))

        subtitulo = tk.Label(self.root,
            text="Visualizador Interactivo del Tipo de Dato Abstracto",
            font=FUENTE_PEQUENA, fg=COLORES["texto2"], bg=COLORES["fondo"])
        subtitulo.pack(pady=(0, 8))

        # Marco principal
        main = tk.Frame(self.root, bg=COLORES["fondo"])
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        # Panel izquierdo (controles)
        self._panel_controles(main)

        # Canvas central
        self._panel_canvas(main)

        # Panel derecho (log)
        self._panel_log(main)

    def _panel_controles(self, parent):
        panel = tk.Frame(parent, bg=COLORES["panel"], width=230,
                         relief="flat", bd=0)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        panel.pack_propagate(False)

        def seccion(texto):
            tk.Label(panel, text=f"── {texto} ──",
                     font=FUENTE_TITULO, fg=COLORES["acento"],
                     bg=COLORES["panel"]).pack(pady=(14, 4))

        def boton(parent_w, texto, comando, color=None):
            c = color or COLORES["acento3"]
            b = tk.Button(parent_w, text=texto, command=comando,
                          font=FUENTE_NORMAL, fg=COLORES["texto"],
                          bg=c, activebackground=COLORES["acento"],
                          activeforeground=COLORES["fondo"],
                          relief="flat", bd=0, padx=8, pady=5,
                          cursor="hand2")
            b.pack(fill=tk.X, padx=12, pady=2)
            return b

        # ── Tipo de grafo
        seccion("TIPO")
        self.tipo_var = tk.StringVar(value="No Dirigido")
        for txt, val in [("No Dirigido", "No Dirigido"), ("Dirigido", "Dirigido")]:
            rb = tk.Radiobutton(panel, text=txt, variable=self.tipo_var,
                                value=val, command=self._cambiar_tipo,
                                font=FUENTE_NORMAL, fg=COLORES["texto"],
                                bg=COLORES["panel"], selectcolor=COLORES["panel2"],
                                activebackground=COLORES["panel"],
                                activeforeground=COLORES["acento"])
            rb.pack(anchor=tk.W, padx=16)

        # ── Vértices
        seccion("VÉRTICES")
        self.entry_v = tk.Entry(panel, font=FUENTE_MONO,
                                bg=COLORES["panel2"], fg=COLORES["acento"],
                                insertbackground=COLORES["acento"],
                                relief="flat", bd=4)
        self.entry_v.pack(fill=tk.X, padx=12, pady=2)
        self.entry_v.insert(0, "Nombre vértice")
        self.entry_v.bind("<FocusIn>",  lambda e: self._clear_entry(self.entry_v, "Nombre vértice"))
        boton(panel, "＋ insertaVertice(o)", self._insertar_vertice, COLORES["verde"])
        boton(panel, "✕ eliminaVertice(v)", self._eliminar_vertice, COLORES["rojo"])

        # ── Aristas
        seccion("ARISTAS")
        tk.Label(panel, text="(Haz clic en 2 vértices del canvas)",
                 font=FUENTE_PEQUENA, fg=COLORES["texto2"],
                 bg=COLORES["panel"], wraplength=200).pack(padx=12)

        self.entry_peso = tk.Entry(panel, font=FUENTE_MONO,
                                   bg=COLORES["panel2"], fg=COLORES["acento"],
                                   insertbackground=COLORES["acento"],
                                   relief="flat", bd=4)
        self.entry_peso.pack(fill=tk.X, padx=12, pady=2)
        self.entry_peso.insert(0, "Peso (opcional)")
        self.entry_peso.bind("<FocusIn>",  lambda e: self._clear_entry(self.entry_peso, "Peso (opcional)"))

        self.modo_arista = tk.StringVar(value="no_dirigida")
        for txt, val in [("No dirigida", "no_dirigida"), ("Dirigida →", "dirigida")]:
            rb = tk.Radiobutton(panel, text=txt, variable=self.modo_arista,
                                value=val, font=FUENTE_NORMAL,
                                fg=COLORES["texto"], bg=COLORES["panel"],
                                selectcolor=COLORES["panel2"],
                                activebackground=COLORES["panel"])
            rb.pack(anchor=tk.W, padx=16)

        boton(panel, "✕ eliminaArista(e)", self._eliminar_arista, COLORES["rojo"])
        boton(panel, "⇄ convierteNoDirigida(e)", self._convierte_no_dir, COLORES["amarillo"])
        boton(panel, "↺ invierteDir(e)", self._inviertedir, COLORES["amarillo"])

        # ── Consultas
        seccion("CONSULTAS")
        boton(panel, "ℹ  Info del grafo",       self._info_grafo)
        boton(panel, "🔍 Consultar vértice",     self._consultar_vertice)
        boton(panel, "🔗 Consultar arista",      self._consultar_arista)
        boton(panel, "↔  esAdyacente(v,w)",     self._es_adyacente)

        # ── Utilidades
        seccion("UTILIDADES")
        boton(panel, "🎲 Grafo ejemplo",         self._grafo_ejemplo, COLORES["acento2"])
        boton(panel, "🗑  Limpiar grafo",         self._limpiar_grafo, COLORES["rojo"])

    def _panel_canvas(self, parent):
        marco = tk.Frame(parent, bg=COLORES["panel"], relief="flat")
        marco.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(marco, text="CANVAS — Haz clic para seleccionar vértices",
                 font=FUENTE_PEQUENA, fg=COLORES["texto2"],
                 bg=COLORES["panel"]).pack(pady=(6, 0))

        self.canvas = tk.Canvas(marco, bg=COLORES["fondo"],
                                highlightthickness=1,
                                highlightbackground=COLORES["acento3"])
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.canvas.bind("<Button-1>", self._click_canvas)
        self.canvas.bind("<B1-Motion>", self._arrastrar_vertice)
        self.canvas.bind("<Configure>", lambda e: self._redibujar())

        # Instrucciones en el canvas
        self._instrucciones_canvas()

    def _panel_log(self, parent):
        panel = tk.Frame(parent, bg=COLORES["panel"], width=280)
        panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 0))
        panel.pack_propagate(False)

        tk.Label(panel, text="── CONSOLA ──",
                 font=FUENTE_TITULO, fg=COLORES["acento"],
                 bg=COLORES["panel"]).pack(pady=(14, 4))

        self.log_text = tk.Text(panel, font=FUENTE_PEQUENA,
                                bg=COLORES["fondo"], fg=COLORES["texto"],
                                relief="flat", bd=0, wrap=tk.WORD,
                                state=tk.DISABLED, cursor="arrow")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Colores de tag
        self.log_text.tag_config("ok",      foreground=COLORES["verde"])
        self.log_text.tag_config("error",   foreground=COLORES["rojo"])
        self.log_text.tag_config("info",    foreground=COLORES["acento"])
        self.log_text.tag_config("warn",    foreground=COLORES["amarillo"])
        self.log_text.tag_config("normal",  foreground=COLORES["texto"])
        self.log_text.tag_config("metodo",  foreground=COLORES["acento2"])

        boton_limpiar = tk.Button(panel, text="Limpiar consola",
            command=self._limpiar_log,
            font=FUENTE_PEQUENA, fg=COLORES["texto2"],
            bg=COLORES["panel2"], relief="flat", bd=0, pady=3)
        boton_limpiar.pack(fill=tk.X, padx=8, pady=(0, 8))

    # ── Helpers UI ────────────────────────────────────────
    def _clear_entry(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def _instrucciones_canvas(self):
        self.canvas.delete("instrucciones")
        self.canvas.create_text(
            400, 200,
            text="◈ Canvas vacío\n\nUsa los controles de la izquierda\npara insertar vértices\n\nLuego haz clic en dos vértices\npara crear una arista",
            font=("Courier New", 12), fill=COLORES["panel2"],
            tags="instrucciones", justify=tk.CENTER)

    def _log(self, mensaje, tipo="normal"):
        self.log_text.configure(state=tk.NORMAL)
        # Detectar tipo automáticamente
        if tipo == "normal":
            if mensaje.startswith("✓") or mensaje.startswith("✦"):
                tipo = "ok"
            elif mensaje.startswith("✗") or "Error" in mensaje:
                tipo = "error"
            elif mensaje.startswith("»"):
                tipo = "info"
            elif mensaje.startswith("⚠"):
                tipo = "warn"
            elif mensaje.startswith("  ["):
                tipo = "metodo"

        self.log_text.insert(tk.END, mensaje + "\n", tipo)
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _limpiar_log(self):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)

    # ── Dibujo del grafo ──────────────────────────────────
    def _redibujar(self):
        self.canvas.delete("all")
        if not self.grafo.vertices():
            self._instrucciones_canvas()
            return

        # Aristas
        for arista in self.grafo.aristas():
            u, v = arista.verticesFinales()
            if u not in self.posiciones_vis or v not in self.posiciones_vis:
                continue
            x1, y1 = self.posiciones_vis[u]
            x2, y2 = self.posiciones_vis[v]
            color = COLORES["arista_dir"] if arista.esDirigida() else COLORES["acento"]
            lw = 2

            self.canvas.create_line(x1, y1, x2, y2,
                fill=color, width=lw, tags="arista")

            # Flecha si es dirigida
            if arista.esDirigida():
                self._dibujar_flecha(x1, y1, x2, y2, color)

            # Peso
            if arista.elemento() is not None:
                mx, my = (x1+x2)/2, (y1+y2)/2
                self.canvas.create_oval(mx-12, my-10, mx+12, my+10,
                    fill=COLORES["panel2"], outline=color, width=1)
                self.canvas.create_text(mx, my, text=str(arista.elemento()),
                    font=FUENTE_PEQUENA, fill=color)

        # Vértices
        r = 22
        for v in self.grafo.vertices():
            if v not in self.posiciones_vis:
                continue
            x, y = self.posiciones_vis[v]
            es_sel = (v is self.seleccionado)
            color_borde = COLORES["vertice_sel"] if es_sel else COLORES["acento"]
            color_fondo = "#0a2040"             if es_sel else COLORES["vertice"]
            lw = 3 if es_sel else 1.5

            # Glow si seleccionado
            if es_sel:
                self.canvas.create_oval(x-r-5, y-r-5, x+r+5, y+r+5,
                    fill="", outline=COLORES["acento"], width=1,
                    tags=f"v_{id(v)}")

            self.canvas.create_oval(x-r, y-r, x+r, y+r,
                fill=color_fondo, outline=color_borde, width=lw,
                tags=(f"v_{id(v)}", "vertice"))
            self.canvas.create_text(x, y, text=str(v.elemento()),
                font=("Courier New", 10, "bold"),
                fill=COLORES["texto"], tags=f"v_{id(v)}")

    def _dibujar_flecha(self, x1, y1, x2, y2, color):
        r = 22
        dist = math.hypot(x2-x1, y2-y1)
        if dist == 0:
            return
        ux, uy = (x2-x1)/dist, (y2-y1)/dist
        # Punto en el borde del vértice destino
        ex = x2 - ux * (r + 4)
        ey = y2 - uy * (r + 4)
        # Puntas de flecha
        ang = math.atan2(y2-y1, x2-x1)
        ta = 0.45
        tl = 14
        ax1 = ex - tl*math.cos(ang-ta)
        ay1 = ey - tl*math.sin(ang-ta)
        ax2 = ex - tl*math.cos(ang+ta)
        ay2 = ey - tl*math.sin(ang+ta)
        self.canvas.create_polygon(ex, ey, ax1, ay1, ax2, ay2,
            fill=color, outline=color, tags="arista")

    def _posicion_aleatoria(self):
        w = self.canvas.winfo_width()  or 600
        h = self.canvas.winfo_height() or 400
        return (random.randint(60, w-60), random.randint(60, h-60))

    def _vertice_en(self, x, y):
        r = 26
        for v, (vx, vy) in self.posiciones_vis.items():
            if math.hypot(x-vx, y-vy) <= r:
                return v
        return None

    # ── Interacción con canvas ────────────────────────────
    def _click_canvas(self, event):
        v = self._vertice_en(event.x, event.y)
        if v is None:
            self.seleccionado = None
            self._redibujar()
            return

        if self.seleccionado is None:
            self.seleccionado = v
            self._log(f"» Vértice '{v.elemento()}' seleccionado (1/2)")
        elif self.seleccionado is v:
            self.seleccionado = None
            self._log("» Selección cancelada")
        else:
            # Crear arista
            u = self.seleccionado
            self.seleccionado = None
            peso_txt = self.entry_peso.get().strip()
            peso = None
            if peso_txt and peso_txt != "Peso (opcional)":
                try:
                    peso = float(peso_txt) if '.' in peso_txt else int(peso_txt)
                except ValueError:
                    peso = peso_txt

            if self.modo_arista.get() == "dirigida":
                a = self.grafo.insertaAristaDirigida(u, v, peso)
                self._log(f"✓ insertaAristaDirigida({u.elemento()}, {v.elemento()}, {peso})")
                self._log(f"  [{a}]", "metodo")
            else:
                a = self.grafo.insertaArista(u, v, peso)
                self._log(f"✓ insertaArista({u.elemento()}, {v.elemento()}, {peso})")
                self._log(f"  [{a}]", "metodo")

        self._redibujar()

    def _arrastrar_vertice(self, event):
        v = self._vertice_en(event.x, event.y)
        if v:
            self.posiciones_vis[v] = (event.x, event.y)
            self._redibujar()

    # ── Operaciones del TDA ───────────────────────────────
    def _cambiar_tipo(self):
        dirigido = (self.tipo_var.get() == "Dirigido")
        self.grafo = Grafo(dirigido=dirigido)
        self.posiciones_vis.clear()
        self.seleccionado = None
        self._log(f"✦ Grafo reiniciado como {'Dirigido' if dirigido else 'No Dirigido'}", "info")
        self._redibujar()

    def _insertar_vertice(self):
        nombre = self.entry_v.get().strip()
        if not nombre or nombre == "Nombre vértice":
            self._log("⚠ Escribe un nombre para el vértice", "warn")
            return
        v = self.grafo.insertaVertice(nombre)
        self.posiciones_vis[v] = self._posicion_aleatoria()
        self._log(f"✓ insertaVertice('{nombre}')")
        self._log(f"  tamano() = {self.grafo.tamano()}", "metodo")
        self.entry_v.delete(0, tk.END)
        self._redibujar()

    def _eliminar_vertice(self):
        nombre = simpledialog.askstring("Eliminar vértice",
            "Nombre del vértice a eliminar:",
            parent=self.root)
        if not nombre:
            return
        v = self._buscar_vertice(nombre)
        if v is None:
            self._log(f"✗ Vértice '{nombre}' no encontrado", "error")
            return
        self.grafo.eliminaVertice(v)
        del self.posiciones_vis[v]
        if self.seleccionado is v:
            self.seleccionado = None
        self._log(f"✓ eliminaVertice('{nombre}') — y todas sus aristas")
        self._redibujar()

    def _eliminar_arista(self):
        nombres = simpledialog.askstring("Eliminar arista",
            "Ingresa 'origen,destino':", parent=self.root)
        if not nombres:
            return
        partes = [p.strip() for p in nombres.split(",")]
        if len(partes) != 2:
            self._log("✗ Formato incorrecto. Usa: origen,destino", "error")
            return
        u = self._buscar_vertice(partes[0])
        v = self._buscar_vertice(partes[1])
        if not u or not v:
            self._log("✗ Uno o ambos vértices no encontrados", "error")
            return
        a = self.grafo.obtenerArista(u, v)
        if not a:
            self._log(f"✗ No existe arista entre '{partes[0]}' y '{partes[1]}'", "error")
            return
        self.grafo.eliminaArista(a)
        self._log(f"✓ eliminaArista({partes[0]} ↔ {partes[1]})")
        self._redibujar()

    def _convierte_no_dir(self):
        nombres = simpledialog.askstring("Convertir a no dirigida",
            "Ingresa 'origen,destino':", parent=self.root)
        if not nombres:
            return
        partes = [p.strip() for p in nombres.split(",")]
        if len(partes) != 2:
            return
        u = self._buscar_vertice(partes[0])
        v = self._buscar_vertice(partes[1])
        if not u or not v:
            self._log("✗ Vértices no encontrados", "error")
            return
        a = self.grafo.obtenerArista(u, v)
        if not a:
            self._log("✗ Arista no encontrada", "error")
            return
        self.grafo.convierteNoDirigida(a)
        self._log(f"✓ convierteNoDirigida({partes[0]}, {partes[1]})")
        self._redibujar()

    def _inviertedir(self):
        nombres = simpledialog.askstring("Invertir dirección",
            "Ingresa 'origen,destino':", parent=self.root)
        if not nombres:
            return
        partes = [p.strip() for p in nombres.split(",")]
        if len(partes) != 2:
            return
        u = self._buscar_vertice(partes[0])
        v = self._buscar_vertice(partes[1])
        if not u or not v:
            self._log("✗ Vértices no encontrados", "error")
            return
        a = self.grafo.obtenerArista(u, v)
        if not a or not a.esDirigida():
            self._log("✗ Arista dirigida no encontrada", "error")
            return
        self.grafo.invierteDir(a)
        self._log(f"✓ invierteDir({partes[0]} → {partes[1]}) → ahora {partes[1]} → {partes[0]}")
        self._redibujar()

    def _info_grafo(self):
        g = self.grafo
        self._log("─" * 32, "info")
        self._log("» INFO GRAFO", "info")
        self._log(f"  numVertices()  = {g.numVertices()}", "metodo")
        self._log(f"  numAristas()   = {g.numAristas()}", "metodo")
        self._log(f"  tamano()       = {g.tamano()}", "metodo")
        self._log(f"  estaVacio()    = {g.estaVacio()}", "metodo")
        vs = [str(v.elemento()) for v in g.vertices()]
        self._log(f"  vertices()     = {vs}", "metodo")
        ar = [str(a) for a in g.aristas()]
        self._log(f"  aristas()      = {ar}", "metodo")
        dir_ar = [str(a) for a in g.aristasDirigidas()]
        nodir  = [str(a) for a in g.aristasNodirigidas()]
        self._log(f"  aristasDirigidas()    = {dir_ar}", "metodo")
        self._log(f"  aristasNodirigidas()  = {nodir}", "metodo")
        self._log("─" * 32, "info")

    def _consultar_vertice(self):
        nombre = simpledialog.askstring("Consultar vértice",
            "Nombre del vértice:", parent=self.root)
        if not nombre:
            return
        v = self._buscar_vertice(nombre)
        if v is None:
            self._log(f"✗ Vértice '{nombre}' no encontrado", "error")
            return
        g = self.grafo
        self._log("─" * 32, "info")
        self._log(f"» VÉRTICE: '{nombre}'", "info")
        self._log(f"  grado(v)       = {g.grado(v)}", "metodo")
        self._log(f"  gradoEnt(v)    = {g.gradoEnt(v)}", "metodo")
        self._log(f"  gradoSalida(v) = {g.gradoSalida(v)}", "metodo")
        adys = [str(w.elemento()) for w in g.verticesAdyacentes(v)]
        self._log(f"  verticesAdyacentes(v) = {adys}", "metodo")
        inc = [str(a) for a in g.aristasIncidentes(v)]
        self._log(f"  aristasIncidentes(v)  = {inc}", "metodo")
        ent = [str(a) for a in g.aristasIncidentesEnt(v)]
        sal = [str(a) for a in g.aristasIncidentesSal(v)]
        self._log(f"  aristasIncidentesEnt  = {ent}", "metodo")
        self._log(f"  aristasIncidentesSal  = {sal}", "metodo")
        self._log("─" * 32, "info")

    def _consultar_arista(self):
        nombres = simpledialog.askstring("Consultar arista",
            "Ingresa 'origen,destino':", parent=self.root)
        if not nombres:
            return
        partes = [p.strip() for p in nombres.split(",")]
        if len(partes) != 2:
            return
        u = self._buscar_vertice(partes[0])
        v = self._buscar_vertice(partes[1])
        if not u or not v:
            self._log("✗ Vértices no encontrados", "error")
            return
        a = self.grafo.obtenerArista(u, v)
        if not a:
            self._log(f"✗ No existe arista entre '{partes[0]}' y '{partes[1]}'", "error")
            return
        fin = a.verticesFinales()
        self._log("─" * 32, "info")
        self._log(f"» ARISTA: {a}", "info")
        self._log(f"  esDirigida()    = {a.esDirigida()}", "metodo")
        self._log(f"  verticesFinales() = ({fin[0].elemento()}, {fin[1].elemento()})", "metodo")
        if a.esDirigida():
            self._log(f"  origen()  = {a.origen().elemento()}", "metodo")
            self._log(f"  destino() = {a.destino().elemento()}", "metodo")
        op = a.opuesto(u)
        self._log(f"  opuesto({partes[0]}) = {op.elemento()}", "metodo")
        self._log("─" * 32, "info")

    def _es_adyacente(self):
        nombres = simpledialog.askstring("esAdyacente(v,w)",
            "Ingresa 'v,w':", parent=self.root)
        if not nombres:
            return
        partes = [p.strip() for p in nombres.split(",")]
        if len(partes) != 2:
            return
        u = self._buscar_vertice(partes[0])
        v = self._buscar_vertice(partes[1])
        if not u or not v:
            self._log("✗ Vértices no encontrados", "error")
            return
        res = self.grafo.esAdyacente(u, v)
        self._log(f"» esAdyacente('{partes[0]}', '{partes[1]}') = {res}",
                  "ok" if res else "warn")

    def _buscar_vertice(self, nombre):
        for v in self.grafo.vertices():
            if str(v.elemento()) == nombre:
                return v
        return None

    def _grafo_ejemplo(self):
        self._limpiar_grafo()
        g = self.grafo
        nombres = ["A", "B", "C", "D", "E", "F"]
        w = self.canvas.winfo_width()  or 700
        h = self.canvas.winfo_height() or 450
        cx, cy = w//2, h//2
        radio = min(w, h) // 3

        verts = {}
        for i, n in enumerate(nombres):
            ang = 2 * math.pi * i / len(nombres) - math.pi/2
            x = cx + radio * math.cos(ang)
            y = cy + radio * math.sin(ang)
            v = g.insertaVertice(n)
            self.posiciones_vis[v] = (x, y)
            verts[n] = v

        aristas = [("A","B",4), ("A","C",2), ("B","C",1),
                   ("B","D",5), ("C","E",3), ("D","E",2),
                   ("D","F",6), ("E","F",1)]
        for u, v, p in aristas:
            g.insertaArista(verts[u], verts[v], p)

        self._log("✦ Grafo de ejemplo cargado (6 vértices, 8 aristas)", "ok")
        self._redibujar()

    def _limpiar_grafo(self):
        dirigido = self.grafo._dirigido
        self.grafo = Grafo(dirigido=dirigido)
        self.posiciones_vis.clear()
        self.seleccionado = None
        self._log("✦ Grafo limpiado", "warn")
        self._redibujar()


# ═══════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionGrafo(root)
    root.mainloop()
