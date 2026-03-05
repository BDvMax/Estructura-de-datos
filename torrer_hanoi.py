import tkinter as tk
import time
import math

# ═══════════════════════════════════════════════════════
#  PALETA
# ═══════════════════════════════════════════════════════
BG      = "#0d1117"
PANEL   = "#161b22"
BORDER  = "#30363d"
ACCENT  = "#58a6ff"
GREEN   = "#3fb950"
YELLOW  = "#e3b341"
RED     = "#f85149"
TEXT    = "#e6edf3"
MUTED   = "#484f58"
DARK    = "#0a0d11"

DISK_COLORS = [
    "#ff6b6b","#ffa94d","#ffe066","#69db7c",
    "#4dabf7","#cc5de8","#f783ac","#a9e34b",
    "#63e6be","#74c0fc"
]

# ═══════════════════════════════════════════════════════
#  APP
# ═══════════════════════════════════════════════════════
class AppHanoi:
    MIN_N, MAX_N = 2, 9

    def __init__(self, root):
        self.root = root
        self.root.title("Torre de Hanoi — Modo Manual")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.n          = tk.IntVar(value=4)
        self.torres     = [[], [], []]
        self.seleccion  = None      # índice de torre seleccionada
        self.movimientos = 0
        self.t_inicio   = None
        self.timer_id   = None
        self.ganado     = False

        self._build_ui()
        self._reset()

    # ──────────────────────────────────────────────────
    #  UI
    # ──────────────────────────────────────────────────
    def _build_ui(self):
        # Título
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=20, pady=(16, 4))
        tk.Label(top, text="TORRE  DE  HANOI",
                 bg=BG, fg=ACCENT,
                 font=("Courier New", 18, "bold")).pack(side="left")
        tk.Label(top, text="— modo manual —",
                 bg=BG, fg=MUTED,
                 font=("Courier New", 10)).pack(side="left", padx=10)

        # Canvas
        self.CW, self.CH = 700, 320
        self.canvas = tk.Canvas(self.root, width=self.CW, height=self.CH,
                                bg=PANEL, highlightthickness=1,
                                highlightbackground=BORDER, cursor="hand2")
        self.canvas.pack(padx=20)
        self.canvas.bind("<Button-1>", self._click)

        # Instrucción
        self.lbl_hint = tk.Label(self.root,
                                 text="Haz clic en una torre para tomar el disco del tope, luego clic en el destino.",
                                 bg=BG, fg=MUTED, font=("Courier New", 8))
        self.lbl_hint.pack(pady=(4, 0))

        # ── Controles ─────────────────────────────────
        ctrl = tk.Frame(self.root, bg=PANEL,
                        highlightthickness=1, highlightbackground=BORDER)
        ctrl.pack(fill="x", padx=20, pady=8)

        # Discos ± 
        tk.Label(ctrl, text="Discos:", bg=PANEL, fg=TEXT,
                 font=("Courier New", 10)).pack(side="left", padx=(12, 4), pady=8)

        tk.Button(ctrl, text="−", command=self._menos,
                  bg=DARK, fg=TEXT, font=("Courier New", 11, "bold"),
                  relief="flat", cursor="hand2", width=2,
                  activebackground=BORDER).pack(side="left")

        self.lbl_n = tk.Label(ctrl, textvariable=self.n,
                               bg=PANEL, fg=YELLOW,
                               font=("Courier New", 13, "bold"), width=3)
        self.lbl_n.pack(side="left")

        tk.Button(ctrl, text="+", command=self._mas,
                  bg=DARK, fg=TEXT, font=("Courier New", 11, "bold"),
                  relief="flat", cursor="hand2", width=2,
                  activebackground=BORDER).pack(side="left", padx=(0, 14))

        # Reset
        tk.Button(ctrl, text="↺  RESET", command=self._reset,
                  bg=DARK, fg=TEXT,
                  font=("Courier New", 10, "bold"),
                  relief="flat", cursor="hand2",
                  padx=10, pady=4,
                  activebackground=BORDER).pack(side="left", padx=4)

        # Resolver automático
        tk.Button(ctrl, text="⚡ AUTO-RESOLVER", command=self._auto,
                  bg=ACCENT, fg=BG,
                  font=("Courier New", 10, "bold"),
                  relief="flat", cursor="hand2",
                  padx=10, pady=4,
                  activebackground=TEXT).pack(side="left", padx=4)

        # ── Stats ──────────────────────────────────────
        stats = tk.Frame(self.root, bg=BG)
        stats.pack(fill="x", padx=20, pady=(0, 16))

        self.lbl_movs  = self._stat(stats, "Movimientos",   "0",   TEXT)
        self.lbl_opt   = self._stat(stats, "Óptimo (2ⁿ−1)", "—",   MUTED)
        self.lbl_extra = self._stat(stats, "Movs. extra",   "—",   MUTED)
        self.lbl_est   = self._stat(stats, "Tiempo estimado","—",  YELLOW)
        self.lbl_real  = self._stat(stats, "Tiempo real",   "0.000 s", TEXT)
        self.lbl_state = self._stat(stats, "Estado",        "Listo", ACCENT)

    def _stat(self, parent, label, val, color=TEXT):
        f = tk.Frame(parent, bg=PANEL,
                     highlightthickness=1, highlightbackground=BORDER)
        f.pack(side="left", expand=True, fill="x", padx=3)
        tk.Label(f, text=label.upper(), bg=PANEL, fg=MUTED,
                 font=("Courier New", 6, "bold")).pack(pady=(5, 0))
        lbl = tk.Label(f, text=val, bg=PANEL, fg=color,
                       font=("Courier New", 11, "bold"))
        lbl.pack(pady=(0, 5))
        return lbl

    # ──────────────────────────────────────────────────
    #  DIBUJO
    # ──────────────────────────────────────────────────
    def _dibujar(self):
        self.canvas.delete("all")
        n = self.n.get()
        CW, CH   = self.CW, self.CH
        BASE_Y   = CH - 28
        POST_W   = 10
        POST_H   = min(230, 50 + n * 24)
        MAX_DW   = CW // 3 - 36
        MIN_DW   = 20
        DISK_H   = min(28, max(16, (POST_H - 14) // max(n, 1)))

        # Base
        self.canvas.create_rectangle(14, BASE_Y, CW - 14, BASE_Y + 10,
                                     fill="#21262d", outline=BORDER)

        self.col_xs = [CW // 6, CW // 2, 5 * CW // 6]

        for t_idx, (cx, torre) in enumerate(zip(self.col_xs, self.torres)):
            seleccionada = (self.seleccion == t_idx)

            # Poste — resaltado si está seleccionado
            post_color = ACCENT if seleccionada else MUTED
            px = cx - POST_W // 2
            self.canvas.create_rectangle(px, BASE_Y - POST_H,
                                         px + POST_W, BASE_Y,
                                         fill=post_color, outline="")

            # Zona clickeable (rectángulo invisible para facilitar clic)
            zona_x1 = cx - MAX_DW // 2 - 10
            zona_x2 = cx + MAX_DW // 2 + 10
            tag = f"torre_{t_idx}"
            self.canvas.create_rectangle(zona_x1, BASE_Y - POST_H - 10,
                                         zona_x2, BASE_Y + 10,
                                         fill="", outline="",
                                         tags=tag)

            # Etiquetas
            nombres  = ["ORIGEN", "AUXILIAR", "DESTINO"]
            clr_lbl  = [RED, MUTED, GREEN]
            self.canvas.create_text(cx, BASE_Y + 18,
                                    text=nombres[t_idx],
                                    fill=ACCENT if seleccionada else clr_lbl[t_idx],
                                    font=("Courier New", 8, "bold"))

            # Discos
            for d_idx, disco in enumerate(torre):
                t = (disco - 1) / max(n - 1, 1)
                ancho = int(MIN_DW + t * (MAX_DW - MIN_DW))
                x1 = cx - ancho // 2
                x2 = cx + ancho // 2
                y2 = BASE_Y - d_idx * (DISK_H + 2)
                y1 = y2 - DISK_H

                # Disco en tope de torre seleccionada: brilla
                es_tope = (d_idx == len(torre) - 1)
                color   = DISK_COLORS[(disco - 1) % len(DISK_COLORS)]
                borde   = TEXT if (seleccionada and es_tope) else BG
                borde_w = 2 if (seleccionada and es_tope) else 1

                # Sombra sólida
                self.canvas.create_rectangle(x1+3, y1+3, x2+3, y2+3,
                                             fill=DARK, outline="")
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color,
                                             outline=borde, width=borde_w)
                self.canvas.create_text((x1+x2)//2, (y1+y2)//2,
                                        text=str(disco),
                                        fill=BG,
                                        font=("Courier New", 8, "bold"))

            # Flecha animada sobre torre seleccionada (disco en mano)
            if seleccionada and torre:
                disco_tope = torre[-1]
                t2 = (disco_tope - 1) / max(n - 1, 1)
                ancho2 = int(MIN_DW + t2 * (MAX_DW - MIN_DW))
                y_tope = BASE_Y - (len(torre) - 1) * (DISK_H + 2) - DISK_H
                self.canvas.create_text(cx, y_tope - 18,
                                        text="↑ SELECCIONADO",
                                        fill=YELLOW,
                                        font=("Courier New", 7, "bold"))

    # ──────────────────────────────────────────────────
    #  INTERACCIÓN CLIC
    # ──────────────────────────────────────────────────
    def _click(self, event):
        if self.ganado:
            return
        t_idx = self._torre_en(event.x)
        if t_idx is None:
            return

        if self.seleccion is None:
            # Tomar disco
            if not self.torres[t_idx]:
                self.lbl_hint.config(text="⚠  Esa torre está vacía.", fg=RED)
                return
            self.seleccion = t_idx
            self.lbl_hint.config(
                text=f"Torre {t_idx+1} seleccionada — clic en destino.",
                fg=YELLOW)
        else:
            if t_idx == self.seleccion:
                # Deseleccionar
                self.seleccion = None
                self.lbl_hint.config(
                    text="Selección cancelada.", fg=MUTED)
            else:
                # Intentar mover
                self._mover(self.seleccion, t_idx)
                self.seleccion = None

        self._dibujar()

    def _torre_en(self, x):
        """Devuelve el índice de la torre más cercana al clic."""
        for i, cx in enumerate(self.col_xs):
            if abs(x - cx) < self.CW // 6 - 4:
                return i
        return None

    def _mover(self, origen, destino):
        torre_o = self.torres[origen]
        torre_d = self.torres[destino]

        if not torre_o:
            self.lbl_hint.config(text="⚠  Torre origen vacía.", fg=RED)
            return

        disco = torre_o[-1]
        if torre_d and torre_d[-1] < disco:
            self.lbl_hint.config(
                text="✗  Movimiento inválido: no puedes poner un disco grande sobre uno pequeño.",
                fg=RED)
            return

        # Movimiento válido
        torre_o.pop()
        torre_d.append(disco)
        self.movimientos += 1

        # Arrancar cronómetro en el primer movimiento
        if self.movimientos == 1:
            self.t_inicio = time.perf_counter()
            self._tick_timer()

        self._actualizar_stats()
        self.lbl_hint.config(
            text=f"Disco {disco}: Torre {origen+1} → Torre {destino+1}",
            fg=GREEN)

        # Comprobar victoria
        if len(self.torres[2]) == self.n.get():
            self._ganar()

    # ──────────────────────────────────────────────────
    #  STATS
    # ──────────────────────────────────────────────────
    def _actualizar_stats(self):
        n   = self.n.get()
        opt = 2**n - 1
        mov = self.movimientos
        extra = max(0, mov - opt)

        self.lbl_movs.config(text=str(mov), fg=TEXT)
        self.lbl_opt.config(text=str(opt), fg=MUTED)
        self.lbl_extra.config(
            text=str(extra) if mov > 0 else "—",
            fg=RED if extra > 0 else GREEN)

        # Tiempo estimado basado en velocidad actual (mov/s)
        if self.t_inicio and mov >= 2:
            elapsed = time.perf_counter() - self.t_inicio
            vel = mov / elapsed                  # movimientos por segundo
            restantes = max(0, opt - mov)        # asume jugarás óptimo de aquí en adelante
            if vel > 0:
                est = restantes / vel
                self.lbl_est.config(text=f"~{est:.1f} s", fg=YELLOW)
            else:
                self.lbl_est.config(text="—", fg=MUTED)
        elif mov == 0:
            # Estimación estática basada en tiempo promedio por movimiento (0.8 s)
            self.lbl_est.config(text=f"~{opt * 0.8:.0f} s", fg=MUTED)

    def _tick_timer(self):
        if self.t_inicio and not self.ganado:
            elapsed = time.perf_counter() - self.t_inicio
            self.lbl_real.config(text=f"{elapsed:.3f} s", fg=YELLOW)
            self.timer_id = self.root.after(50, self._tick_timer)

    def _ganar(self):
        self.ganado = True
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        elapsed = time.perf_counter() - self.t_inicio
        n   = self.n.get()
        opt = 2**n - 1
        extra = self.movimientos - opt

        self.lbl_real.config(text=f"{elapsed:.3f} s", fg=GREEN)
        self.lbl_state.config(text="¡GANASTE! 🎉", fg=GREEN)
        self.lbl_est.config(text="—", fg=MUTED)
        self.lbl_hint.config(
            text=f"🏆  ¡Torre completada!  {self.movimientos} movs en {elapsed:.2f}s"
                 + (f"  (+{extra} extra)" if extra else "  ¡Óptimo!"),
            fg=GREEN)

    # ──────────────────────────────────────────────────
    #  AUTO-RESOLVER
    # ──────────────────────────────────────────────────
    def _auto(self):
        if self.ganado:
            return
        # Reiniciar y resolver paso a paso
        self._reset(silencioso=True)
        movs = []
        self._hanoi_movs(self.n.get(), 0, 2, 1, movs)
        self.t_inicio = time.perf_counter()
        self._tick_timer()
        self._ejecutar_movs(movs)

    def _hanoi_movs(self, n, o, d, a, lista):
        if n == 1:
            lista.append((o, d))
            return
        self._hanoi_movs(n-1, o, a, d, lista)
        lista.append((o, d))
        self._hanoi_movs(n-1, a, d, o, lista)

    def _ejecutar_movs(self, movs):
        if not movs:
            return
        o, d = movs.pop(0)
        disco = self.torres[o].pop()
        self.torres[d].append(disco)
        self.movimientos += 1
        self._dibujar()
        self._actualizar_stats()
        self.lbl_hint.config(
            text=f"AUTO: Disco {disco}: Torre {o+1} → Torre {d+1}",
            fg=ACCENT)
        if movs:
            self.root.after(120, lambda: self._ejecutar_movs(movs))
        else:
            self._ganar()

    # ──────────────────────────────────────────────────
    #  RESET / DISCOS
    # ──────────────────────────────────────────────────
    def _reset(self, silencioso=False):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        n = self.n.get()
        self.torres      = [list(range(n, 0, -1)), [], []]
        self.seleccion   = None
        self.movimientos = 0
        self.t_inicio    = None
        self.ganado      = False

        opt = 2**n - 1
        self.lbl_movs.config(text="0", fg=TEXT)
        self.lbl_opt.config(text=str(opt), fg=MUTED)
        self.lbl_extra.config(text="—", fg=MUTED)
        self.lbl_est.config(text=f"~{opt * 0.8:.0f} s", fg=MUTED)
        self.lbl_real.config(text="0.000 s", fg=TEXT)
        self.lbl_state.config(text="Listo", fg=ACCENT)
        if not silencioso:
            self.lbl_hint.config(
                text="Haz clic en una torre para tomar el disco del tope, luego clic en el destino.",
                fg=MUTED)
        self._dibujar()

    def _menos(self):
        if not self.ganado and self.n.get() > self.MIN_N:
            self.n.set(self.n.get() - 1)
            self._reset()

    def _mas(self):
        if not self.ganado and self.n.get() < self.MAX_N:
            self.n.set(self.n.get() + 1)
            self._reset()


# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    AppHanoi(root)
    root.mainloop()
    
