import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext


class BusquedaHashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Búsqueda Hash - IDs de Usuarios")
        self.root.geometry("700x580")
        self.root.config(bg="#1e1e1e")

        self.datos = []

        tk.Label(
            root,
            text="Búsqueda Hash: IDs de Usuarios (#)",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#1abc9c"
        ).pack(pady=10)

        frame = tk.LabelFrame(
            root,
            text=" Gestión de IDs en Tabla Hash ",
            font=("Arial", 10, "bold"),
            bg="#2d2d2d",
            fg="white",
            padx=10,
            pady=10
        )
        frame.pack(fill="x", padx=20, pady=5)

        tk.Button(
            frame,
            text="1. Ingresar Cantidad y IDs",
            command=self.pedir_datos,
            bg="#2980b9",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            frame,
            text="⚡ Cargar Ejemplo (7 IDs)",
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
            text="2. ▶ Buscar ID",
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

    def construir_tabla(self):
        tam = max(7, len(self.datos) * 2)
        tabla = [[] for _ in range(tam)]
        for clave in self.datos:
            idx = clave % tam
            tabla[idx].append(clave)
        return tam, tabla

    def pedir_datos(self):
        try:
            cant_str = simpledialog.askstring("Cantidad", "Ingrese la cantidad de IDs:", parent=self.root)
            if not cant_str:
                return
            cant = int(cant_str)

            if cant <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.", parent=self.root)
                return

            vals_str = simpledialog.askstring(
                "IDs",
                f"Ingrese exactamente {cant} IDs numéricos (separados por comas):",
                parent=self.root
            )
            if not vals_str:
                return

            arr = [int(x) for x in vals_str.replace(",", " ").split()]
            if len(arr) != cant:
                messagebox.showerror(
                    "Error de Cantidad",
                    f"Indicó {cant} IDs, pero introdujo {len(arr)}. Operación cancelada.",
                    parent=self.root
                )
                return

            self.datos = arr
            tam, tabla = self.construir_tabla()
            self.dibujar_tabla(tabla)
            self.log.delete(1.0, tk.END)
            self.log.insert(
                tk.END,
                f"IDs cargados: {self.datos} | Cubetas: {tam} (h(k) = k % {tam})\nPaso 2: Haga clic en 'Buscar ID'.\n"
            )
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar únicamente números enteros válidos.", parent=self.root)

    def ejemplo(self):
        self.datos = [101, 204, 309, 412, 515, 620, 725]
        tam, tabla = self.construir_tabla()
        self.dibujar_tabla(tabla)
        self.log.delete(1.0, tk.END)
        self.log.insert(
            tk.END,
            f"Contexto: Localizar un ID de usuario mediante función hash (k % {tam}).\nEjemplo cargado: {self.datos}\nPaso 2: Haga clic en 'Buscar ID'.\n"
        )

    def dibujar_tabla(self, tabla, cubeta_activa=None, encontrado=False):
        self.canvas.delete("all")
        if not tabla:
            return
        w = 640
        n = len(tabla)
        bw = max(26, min(68, (w - 30) / n - 6))
        total_w = n * (bw + 6)
        inicio_x = max(12, (w - total_w) / 2)

        for i, cubeta in enumerate(tabla):
            x0 = inicio_x + i * (bw + 6)
            x1 = x0 + bw
            y0, y1 = 45, 105

            color = "#3498db"
            if cubeta_activa == i:
                color = "#2ecc71" if encontrado else "#f39c12"

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white")
            texto = ",".join(str(x) for x in cubeta) if cubeta else "-"
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=texto, fill="white", font=("Arial", 8, "bold"))
            self.canvas.create_text((x0 + x1) / 2, y1 + 14, text=f"H[{i}]", fill="#aaaaaa", font=("Arial", 8))
            if cubeta_activa == i:
                self.canvas.create_text((x0 + x1) / 2, y0 - 12, text="HASH", fill="#f1c40f", font=("Arial", 8, "bold"))
        self.root.update()

    def ejecutar(self):
        if not self.datos:
            return

        try:
            obj_str = simpledialog.askstring("Buscar ID", "Ingrese el ID numérico a buscar:", parent=self.root)
            if not obj_str:
                return
            objetivo = int(obj_str)
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número entero válido.", parent=self.root)
            return

        self.btn_run.config(state="disabled")
        self.log.delete(1.0, tk.END)

        tam, tabla = self.construir_tabla()
        indice = objetivo % tam
        cubeta = tabla[indice]
        encontrado = objetivo in cubeta

        self.log.insert(tk.END, f"Calculando función hash: {objetivo} % {tam} = [{indice}]\n")
        self.log.insert(tk.END, f"Elementos en cubeta H[{indice}]: {cubeta}\n")
        self.dibujar_tabla(tabla, cubeta_activa=indice, encontrado=encontrado)
        self.root.update()
        self.root.after(250)

        if encontrado:
            self.log.insert(tk.END, f"\n✔ ID #{objetivo} encontrado directamente en la cubeta H[{indice}].\n")
        else:
            self.log.insert(tk.END, f"\n✘ ID #{objetivo} NO encontrado en la cubeta H[{indice}].\n")

        self.btn_run.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    BusquedaHashApp(root)
    root.mainloop()