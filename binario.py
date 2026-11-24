import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext


class BusquedaBinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Búsqueda Binaria - Catálogo de Códigos")
        self.root.geometry("700x580")
        self.root.config(bg="#1e1e1e")

        self.datos = []

        tk.Label(
            root,
            text="Búsqueda Binaria: Códigos de Catálogo (#)",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#a569bd"
        ).pack(pady=10)

        frame = tk.LabelFrame(
            root,
            text=" Gestión de Códigos Ordenados ",
            font=("Arial", 10, "bold"),
            bg="#2d2d2d",
            fg="white",
            padx=10,
            pady=10
        )
        frame.pack(fill="x", padx=20, pady=5)

        tk.Button(
            frame,
            text="1. Ingresar Cantidad y Códigos",
            command=self.pedir_datos,
            bg="#2980b9",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            frame,
            text="⚡ Cargar Ejemplo (8 Códigos)",
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
            text="2. ▶ Buscar Código",
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
            cant_str = simpledialog.askstring("Cantidad", "Ingrese la cantidad de códigos:", parent=self.root)
            if not cant_str:
                return
            cant = int(cant_str)

            if cant <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.", parent=self.root)
                return

            vals_str = simpledialog.askstring(
                "Códigos",
                f"Ingrese exactamente {cant} números de código (separados por comas):",
                parent=self.root
            )
            if not vals_str:
                return

            arr = [int(x) for x in vals_str.replace(",", " ").split()]
            if len(arr) != cant:
                messagebox.showerror(
                    "Error de Cantidad",
                    f"Indicó {cant} códigos, pero introdujo {len(arr)}. Operación cancelada.",
                    parent=self.root
                )
                return

            arr.sort()
            self.datos = arr
            self.dibujar(self.datos, ["#3498db"] * len(self.datos))
            self.log.delete(1.0, tk.END)
            self.log.insert(
                tk.END,
                f"Códigos ordenados para búsqueda binaria: {self.datos}\nPaso 2: Haga clic en 'Buscar Código'.\n"
            )
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar únicamente números enteros válidos.", parent=self.root)

    def ejemplo(self):
        self.datos = [105, 140, 215, 330, 480, 590, 720, 860]
        self.dibujar(self.datos, ["#3498db"] * len(self.datos))
        self.log.delete(1.0, tk.END)
        self.log.insert(
            tk.END,
            f"Contexto: Buscar un código en un catálogo ordenado dividiendo a la mitad.\nEjemplo cargado: {self.datos}\nPaso 2: Haga clic en 'Buscar Código'.\n"
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
            obj_str = simpledialog.askstring("Buscar Código", "Ingrese el número de código a buscar:", parent=self.root)
            if not obj_str:
                return
            objetivo = int(obj_str)
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número entero válido.", parent=self.root)
            return

        self.btn_run.config(state="disabled")
        self.log.delete(1.0, tk.END)
        self.log.insert(tk.END, f"Iniciando Búsqueda Binaria del código #{objetivo}...\n\n")

        izq, der = 0, len(self.datos) - 1
        paso = 0

        while izq <= der:
            paso += 1
            medio = (izq + der) // 2
            val = self.datos[medio]

            cols = ["#34495e"] * len(self.datos)
            etiquetas = [""] * len(self.datos)
            for idx in range(izq, der + 1):
                cols[idx] = "#3498db"
            cols[medio] = "#f39c12"
            etiquetas[izq] = "IZQ"
            etiquetas[der] = "DER"
            etiquetas[medio] = "MED"

            self.dibujar(self.datos, cols, etiquetas)
            self.log.insert(tk.END, f"Paso {paso}: rango [{izq}..{der}], medio=[{medio}] -> código #{val}\n")
            self.root.update()
            self.root.after(400)

            if val == objetivo:
                cols[medio] = "#2ecc71"
                etiquetas[medio] = "HALLADO"
                self.dibujar(self.datos, cols, etiquetas)
                self.log.insert(tk.END, f"\n✔ Código #{objetivo} encontrado en el índice [{medio}] en {paso} pasos.\n")
                self.btn_run.config(state="normal")
                return
            elif val < objetivo:
                self.log.insert(tk.END, f"   #{val} < #{objetivo}: se descarta la mitad izquierda.\n")
                izq = medio + 1
            else:
                self.log.insert(tk.END, f"   #{val} > #{objetivo}: se descarta la mitad derecha.\n")
                der = medio - 1

        self.dibujar(self.datos, ["#e74c3c"] * len(self.datos))
        self.log.insert(tk.END, f"\n✘ Código #{objetivo} NO encontrado tras {paso} pasos.\n")
        self.btn_run.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    BusquedaBinariaApp(root)
    root.mainloop()