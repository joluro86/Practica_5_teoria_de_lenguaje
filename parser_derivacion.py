"""
Práctica #5 - Árboles de Derivación y Análisis Sintáctico
==========================================================
Gramática:
    S --> aAb | aBb | λ
    A --> aAb | a
    B --> aBb | b | λ

"""

import tkinter as tk
from tkinter import ttk, messagebox


# Nodo del árbol

class Nodo:
    def __init__(self, etiqueta, terminal=False, regla=None):
        self.etiqueta = etiqueta
        self.terminal = terminal
        self.regla = regla          # e.g. "S → aAb"
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)


# Parser recursivo descendente

class Parser:
    def __init__(self, cadena):
        self.entrada = list(cadena)
        self.pos = 0

    # ── S → aAb | aBb | λ 
    def parse_S(self):
        nodo = Nodo("S")

        # S → λ (cadena vacía o posición al final)
        if self.pos >= len(self.entrada):
            nodo.regla = "S → λ"
            nodo.agregar_hijo(Nodo("λ", terminal=True))
            return nodo

        if self.entrada[self.pos] == 'a':
            self.pos += 1
            pos_guardada = self.pos

            # Intentar S → aAb
            hijo_A = self.parse_A()
            if hijo_A and self.pos < len(self.entrada) and self.entrada[self.pos] == 'b':
                self.pos += 1
                nodo.regla = "S → aAb"
                nodo.agregar_hijo(Nodo("a", terminal=True))
                nodo.agregar_hijo(hijo_A)
                nodo.agregar_hijo(Nodo("b", terminal=True))
                return nodo

            # Backtrack e intentar S → aBb
            self.pos = pos_guardada
            hijo_B = self.parse_B()
            if hijo_B and self.pos < len(self.entrada) and self.entrada[self.pos] == 'b':
                self.pos += 1
                nodo.regla = "S → aBb"
                nodo.agregar_hijo(Nodo("a", terminal=True))
                nodo.agregar_hijo(hijo_B)
                nodo.agregar_hijo(Nodo("b", terminal=True))
                return nodo

            # Ninguna producción funcionó
            self.pos -= 1

        return None

    # ── A → aAb | a ──────────────────────────────────────────────────────────
    def parse_A(self):
        nodo = Nodo("A")

        if self.pos < len(self.entrada) and self.entrada[self.pos] == 'a':
            self.pos += 1
            pos_guardada = self.pos

            # Intentar A → aAb
            hijo_A = self.parse_A()
            if hijo_A and self.pos < len(self.entrada) and self.entrada[self.pos] == 'b':
                self.pos += 1
                nodo.regla = "A → aAb"
                nodo.agregar_hijo(Nodo("a", terminal=True))
                nodo.agregar_hijo(hijo_A)
                nodo.agregar_hijo(Nodo("b", terminal=True))
                return nodo

            # Backtrack e intentar A → a
            self.pos = pos_guardada
            nodo.regla = "A → a"
            nodo.agregar_hijo(Nodo("a", terminal=True))
            return nodo

        return None

    # ── B → aBb | b | λ 
    def parse_B(self):
        nodo = Nodo("B")
        pos_guardada = self.pos

        # Intentar B → aBb
        if self.pos < len(self.entrada) and self.entrada[self.pos] == 'a':
            self.pos += 1
            hijo_B = self.parse_B()
            if hijo_B and self.pos < len(self.entrada) and self.entrada[self.pos] == 'b':
                self.pos += 1
                nodo.regla = "B → aBb"
                nodo.agregar_hijo(Nodo("a", terminal=True))
                nodo.agregar_hijo(hijo_B)
                nodo.agregar_hijo(Nodo("b", terminal=True))
                return nodo
            self.pos = pos_guardada

        # Intentar B → b
        if self.pos < len(self.entrada) and self.entrada[self.pos] == 'b':
            self.pos += 1
            nodo.regla = "B → b"
            nodo.agregar_hijo(Nodo("b", terminal=True))
            return nodo

        # B → λ
        nodo.regla = "B → λ"
        nodo.agregar_hijo(Nodo("λ", terminal=True))
        return nodo

    # ── Punto de entrada principal
    def analizar(self):
        self.pos = 0
        arbol = self.parse_S()
        if arbol and self.pos == len(self.entrada):
            return arbol
        return None


# Utilidades del árbol

def recolectar_reglas(nodo, reglas=None):
    if reglas is None:
        reglas = []
    if nodo.regla:
        reglas.append(nodo.regla)
    for hijo in nodo.hijos:
        recolectar_reglas(hijo, reglas)
    return reglas


def imprimir_arbol(nodo, prefijo="", es_ultimo=True):
    conector = "└── " if es_ultimo else "├── "
    print(prefijo + conector + nodo.etiqueta)
    prefijo_hijo = prefijo + ("    " if es_ultimo else "│   ")
    for i, hijo in enumerate(nodo.hijos):
        imprimir_arbol(hijo, prefijo_hijo, i == len(nodo.hijos) - 1)


# Interfaz gráfica (tkinter)

COLORES = {
    "S":  {"fondo": "#534AB7", "texto": "#FFFFFF"},
    "A":  {"fondo": "#D97706", "texto": "#FFFFFF"},
    "B":  {"fondo": "#DC2626", "texto": "#FFFFFF"},
    "a":  {"fondo": "#0F6E56", "texto": "#FFFFFF"},
    "b":  {"fondo": "#0F6E56", "texto": "#FFFFFF"},
    "λ":  {"fondo": "#6B7280", "texto": "#FFFFFF"},
}

NODO_W  = 48
NODO_H  = 28
H_GAP   = 14
V_GAP   = 60


class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Árbol de Derivación — Práctica #5")
        self.root.configure(bg="#1E1E2E")
        self.root.minsize(800, 600)
        self._construir_ui()

    # UI
    def _construir_ui(self):
        # Encabezado
        frame_top = tk.Frame(self.root, bg="#1E1E2E", pady=12)
        frame_top.pack(fill="x", padx=20)

        tk.Label(
            frame_top, text="Árboles de Derivación",
            font=("Helvetica", 18, "bold"), fg="#CDD6F4", bg="#1E1E2E"
        ).pack(anchor="w")

        tk.Label(
            frame_top,
            text="S → aAb | aBb | λ     A → aAb | a     B → aBb | b | λ",
            font=("Courier", 11), fg="#6C7086", bg="#1E1E2E"
        ).pack(anchor="w", pady=(2, 0))

        # Input
        frame_inp = tk.Frame(self.root, bg="#1E1E2E")
        frame_inp.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(frame_inp, text="Cadena:", font=("Helvetica", 12),
                 fg="#CDD6F4", bg="#1E1E2E").pack(side="left")

        self.entrada_var = tk.StringVar(value="aab")
        self.campo = tk.Entry(
            frame_inp, textvariable=self.entrada_var,
            font=("Courier", 14), width=20,
            bg="#313244", fg="#CDD6F4", insertbackground="#CDD6F4",
            relief="flat", bd=6
        )
        self.campo.pack(side="left", padx=8)
        self.campo.bind("<Return>", lambda e: self._analizar())

        tk.Button(
            frame_inp, text="Analizar", command=self._analizar,
            font=("Helvetica", 11, "bold"), bg="#534AB7", fg="white",
            relief="flat", padx=14, pady=4, cursor="hand2"
        ).pack(side="left")

        # Ejemplos
        frame_ej = tk.Frame(self.root, bg="#1E1E2E")
        frame_ej.pack(fill="x", padx=20, pady=(0, 8))
        tk.Label(frame_ej, text="Ejemplos:", font=("Helvetica", 10),
                 fg="#6C7086", bg="#1E1E2E").pack(side="left")
        for ej in ["(vacía)", "ab", "aab", "abb", "aabb", "aaabb", "ba✗", "abc✗"]:
            valor = "" if ej == "(vacía)" else ej.replace("✗", "")
            tk.Button(
                frame_ej, text=ej,
                command=lambda v=valor: self._set_ejemplo(v),
                font=("Courier", 9), bg="#313244", fg="#CDD6F4",
                relief="flat", padx=6, pady=2, cursor="hand2"
            ).pack(side="left", padx=3)

        # Estado
        self.lbl_estado = tk.Label(
            self.root, text="", font=("Helvetica", 12, "bold"),
            bg="#1E1E2E", anchor="w"
        )
        self.lbl_estado.pack(fill="x", padx=20, pady=(0, 4))

        # Reglas
        self.lbl_reglas = tk.Label(
            self.root, text="", font=("Courier", 10),
            fg="#6C7086", bg="#1E1E2E", anchor="w", justify="left"
        )
        self.lbl_reglas.pack(fill="x", padx=20, pady=(0, 8))

        # Canvas con scroll
        frame_canvas = tk.Frame(self.root, bg="#181825")
        frame_canvas.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        self.canvas = tk.Canvas(
            frame_canvas, bg="#181825", highlightthickness=0
        )
        sb_x = tk.Scrollbar(frame_canvas, orient="horizontal",
                             command=self.canvas.xview)
        sb_y = tk.Scrollbar(frame_canvas, orient="vertical",
                             command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=sb_x.set, yscrollcommand=sb_y.set)

        sb_x.pack(side="bottom", fill="x")
        sb_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Leyenda
        self._dibujar_leyenda()
        self._analizar()

    def _set_ejemplo(self, v):
        self.entrada_var.set(v)
        self._analizar()

    # ── Análisis
    def _analizar(self):
        cadena = self.entrada_var.get().strip()
        parser = Parser(cadena)
        arbol  = parser.analizar()

        if arbol:
            self.lbl_estado.config(
                text=f'✓  "{cadena or "λ"}" es aceptada',
                fg="#A6E3A1"
            )
            reglas = recolectar_reglas(arbol)
            self.lbl_reglas.config(
                text="Reglas: " + "  →  ".join(reglas)
            )
            self._dibujar_arbol(arbol)
        else:
            self.lbl_estado.config(
                text=f'✗  "{cadena}" NO es aceptada por la gramática',
                fg="#F38BA8"
            )
            self.lbl_reglas.config(text="")
            self.canvas.delete("arbol")

    # ── Layout del árbol
    def _medir(self, nodo):
        if not nodo.hijos:
            nodo.ancho = NODO_W
            return
        for h in nodo.hijos:
            self._medir(h)
        total = sum(h.ancho for h in nodo.hijos) + H_GAP * (len(nodo.hijos) - 1)
        nodo.ancho = max(NODO_W, total)

    def _posicionar(self, nodo, x, y):
        nodo.cx = x + nodo.ancho / 2
        nodo.cy = y
        cx = x
        for h in nodo.hijos:
            self._posicionar(h, cx, y + V_GAP)
            cx += h.ancho + H_GAP

    def _dibujar_arbol(self, raiz):
        self.canvas.delete("arbol")
        self._medir(raiz)
        self._posicionar(raiz, 20, 30)

        # Calcular bounding box
        xs, ys = [], []
        def _bbox(n):
            xs.append(n.cx); ys.append(n.cy)
            for h in n.hijos: _bbox(h)
        _bbox(raiz)
        w = max(xs) + NODO_W + 20
        h = max(ys) + NODO_H + 20
        self.canvas.configure(scrollregion=(0, 0, w, h))

        self._dibujar_nodos(raiz)

    def _dibujar_nodos(self, nodo):
        col = COLORES.get(nodo.etiqueta, {"fondo": "#6C7086", "texto": "#FFFFFF"})
        x1 = nodo.cx - NODO_W / 2
        y1 = nodo.cy - NODO_H / 2
        x2 = nodo.cx + NODO_W / 2
        y2 = nodo.cy + NODO_H / 2

        # Líneas a hijos
        for h in nodo.hijos:
            self.canvas.create_line(
                nodo.cx, y2, h.cx, h.cy - NODO_H / 2,
                fill="#45475A", width=1.5, tags="arbol"
            )

        # Rectángulo redondeado (simulado con óvalo + rect)
        r = 6
        self.canvas.create_oval(x1, y1, x1+2*r, y1+2*r, fill=col["fondo"], outline="", tags="arbol")
        self.canvas.create_oval(x2-2*r, y1, x2, y1+2*r, fill=col["fondo"], outline="", tags="arbol")
        self.canvas.create_oval(x1, y2-2*r, x1+2*r, y2, fill=col["fondo"], outline="", tags="arbol")
        self.canvas.create_oval(x2-2*r, y2-2*r, x2, y2, fill=col["fondo"], outline="", tags="arbol")
        self.canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=col["fondo"], outline="", tags="arbol")
        self.canvas.create_rectangle(x1, y1+r, x2, y2-r, fill=col["fondo"], outline="", tags="arbol")

        # Texto
        self.canvas.create_text(
            nodo.cx, nodo.cy, text=nodo.etiqueta,
            fill=col["texto"], font=("Helvetica", 10, "bold"), tags="arbol"
        )

        # Tooltip con la regla
        if nodo.regla:
            self.canvas.tag_bind(
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="", tags="arbol"),
                "<Enter>",
                lambda e, r=nodo.regla: self.lbl_reglas.config(text=f"Regla: {r}")
            )

        for h in nodo.hijos:
            self._dibujar_nodos(h)

    def _dibujar_leyenda(self):
        leyenda = [("S", "Símbolo inicial"),
                   ("A", "No terminal A"),
                   ("B", "No terminal B"),
                   ("a/b", "Terminal"),
                   ("λ", "Cadena vacía")]
        f = tk.Frame(self.root, bg="#1E1E2E")
        f.pack(fill="x", padx=20, pady=(0, 4))
        for etq, desc in leyenda:
            col = COLORES.get(etq[0], {"fondo": "#6C7086", "texto": "#FFFFFF"})
            tk.Label(f, text=f"  {etq}  ", font=("Courier", 9, "bold"),
                     bg=col["fondo"], fg=col["texto"],
                     relief="flat", padx=4).pack(side="left", padx=2)
            tk.Label(f, text=desc, font=("Helvetica", 9),
                     fg="#6C7086", bg="#1E1E2E").pack(side="left", padx=(0, 10))


# Modo consola

def modo_consola():
    print("=" * 55)
    print("  Árbol de Derivación — Práctica #5")
    print("  S → aAb | aBb | λ")
    print("  A → aAb | a")
    print("  B → aBb | b | λ")
    print("=" * 55)
    print("(Escribe 'salir' para terminar)\n")

    while True:
        cadena = input("Ingresa una cadena: ").strip()
        if cadena.lower() == "salir":
            break

        parser = Parser(cadena)
        arbol  = parser.analizar()

        if arbol:
            print(f"\n✓  '{cadena or 'λ'}' ES ACEPTADA\n")
            reglas = recolectar_reglas(arbol)
            print("Reglas aplicadas:")
            for i, r in enumerate(reglas, 1):
                print(f"  {i}. {r}")
            print("\nÁrbol de derivación:")
            imprimir_arbol(arbol)
        else:
            print(f"\n✗  '{cadena}' NO ES ACEPTADA por la gramática\n")

        print()


# ─────────────────────────────────────────────────────────────────────────────
# Entrada principal
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app  = VentanaPrincipal(root)
        root.mainloop()
    except Exception:
        print("tkinter no disponible — ejecutando en modo consola.\n")
        modo_consola()
