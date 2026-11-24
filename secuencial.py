import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext


class BusquedaSecuencialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Búsqueda Secuencial - Folios en Almacén")
        self.root.geometry("700x580")
        self.root.config(bg="#1e1e1e")

        self.datos = []

        tk.Label(
            root,
            text="Búsqueda Secuencial: Folios de Paquetes (#)",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#00ffcc"
        ).pack(pady=10)

        frame = tk.LabelFrame(
            root,
            text=" Gestión de Folios en Almacén ",
            font=("Arial", 10, "bold"),
            bg="#2d2d2d",
            fg="white",
            padx=10,
            pady=10
        )
        frame.pack(fill="x", padx=20, pady=5)

        tk.Button(
            frame,
            text="1. Ingresar Cantidad y Folios",
            command=self.pedir_datos,
            bg="#2980b9",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            frame,
            text="⚡ Cargar Ejemplo (7 Folios)",
            command=self.ejemplo,
            bg="#d35400",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5
        ).grid(row=0, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        self.btn_run = tk.Button(
            btn_frame,
            text="2. ▶ Buscar Folio",
            command=self.ejecutar,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5
        )
        self.btn_run.pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="❌ Salir",
            command=root.quit,
            bg="#c0392b",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5
        ).pack(side="left", padx=10)

        self.canvas = tk.Canvas(root, width=640, height=160, bg="#111111", highlightthickness=0)
        self.canvas.pack(pady=5)

        self.log = scrolledtext.ScrolledText(
            root,
            width=78,
            height=9,
            font=("Consolas", 9),
            bg="#111111",
            fg="#00ffcc"
        )
        self.log.pack(padx=20, pady=5)

        self.ejemplo()

    def pedir_datos(self):
        try:
            cant_str = simpledialog.askstring("Cantidad", "Ingrese la cantidad de folios:", parent=self.root)
            if not cant_str:
                return
            cant = int(cant_str)

            if cant <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.", parent=self.root)
                return

            vals_str = simpledialog.askstring(
                "Folios",
                f"Ingrese exactamente {cant} números de folio (separados por comas):",
                parent=self.root
            )
            if not vals_str:
                return

            arr = [int(x) for x in vals_str.replace(",", " ").split()]
            if len(arr) != cant:
                messagebox.showerror(
                    "Error de Cantidad",
                    f"Indicó {cant} folios, pero introdujo {len(arr)}. Operación cancelada.",
                    parent=self.root
                )
                return

            self.datos = arr
            self.dibujar(self.datos, ["#3498db"] * len(self.datos))
            self.log.delete(1.0, tk.END)
            self.log.insert(tk.END, f"Folios cargados: {self.datos}\nPaso 2: Haga clic en 'Buscar Folio'.\n")
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar únicamente números enteros válidos.", parent=self.root)

    def ejemplo(self):
        self.datos = [408, 112, 905, 234, 671, 519, 830]
        self.dibujar(self.datos, ["#3498db"] * len(self.datos))
        self.log.delete(1.0, tk.END)
        self.log.insert(
            tk.END,
            f"Contexto: Buscar un folio en el orden en que llegaron los paquetes.\nEjemplo cargado: {self.datos}\nPaso 2: Haga clic en 'Buscar Folio'.\n"
        )

    def dibujar(self, arr, cols, etiquetas=None):
        self.canvas.delete("all")
        if not arr:
            return
        w = 640
        n = len(arr)
        bw = max(24, min(70, (w - 40) / n - 8))
        total_w = n * (bw + 8)
        inicio_x = max(15, (w - total_w) / 2)

        for i, v in enumerate(arr):
            x0 = inicio_x + i * (bw + 8)
            x1 = x0 + bw
            y0, y1 = 45, 105
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=cols[i], outline="white")
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=f"#{v}", fill="white", font=("Arial", 9, "bold"))
            self.canvas.create_text((x0 + x1) / 2, y1 + 14, text=f"[{i}]", fill="#aaaaaa", font=("Arial", 8))
            if etiquetas and i < len(etiquetas) and etiquetas[i]:
                self.canvas.create_text((x0 + x1) / 2, y0 - 12, text=etiquetas[i], fill="#f1c40f", font=("Arial", 8, "bold"))
        self.root.update()

    def ejecutar(self):
        if not self.datos:
            return

        try:
            obj_str = simpledialog.askstring("Buscar Folio", "Ingrese el número de folio a buscar:", parent=self.root)
            if not obj_str:
                return
            objetivo = int(obj_str)
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número entero válido.", parent=self.root)
            return

        self.btn_run.config(state="disabled")
        self.log.delete(1.0, tk.END)
        self.log.insert(tk.END, f"Iniciando Búsqueda Secuencial del folio #{objetivo}...\n\n")

        cols = ["#3498db"] * len(self.datos)
        comparaciones = 0

        for i, val in enumerate(self.datos):
            comparaciones += 1
            cols[i] = "#f39c12"
            self.dibujar(self.datos, cols, [f"paso {comparaciones}" if idx == i else "" for idx in range(len(self.datos))])
            self.log.insert(tk.END, f"Comparación {comparaciones}: posición [{i}] -> folio #{val}\n")
            self.root.update()
            self.root.after(250)

            if val == objetivo:
                cols[i] = "#2ecc71"
                self.dibujar(self.datos, cols, ["HALLADO" if idx == i else "" for idx in range(len(self.datos))])
                self.log.insert(tk.END, f"\n✔ Folio #{objetivo} encontrado en el índice [{i}] tras {comparaciones} comparaciones.\n")
                self.btn_run.config(state="normal")
                return

            cols[i] = "#7f8c8d"

        self.dibujar(self.datos, cols)
        self.log.insert(tk.END, f"\n✘ Folio #{objetivo} NO encontrado tras {comparaciones} comparaciones.\n")
        self.btn_run.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    BusquedaSecuencialApp(root)
    root.mainloop()