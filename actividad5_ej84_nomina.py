# Actividad 5 - Ejercicio 8.4: Cuadros de dialogo - Nomina
# Programacion Orientada a Objetos 2026-2S - Juan Diego Toro Zuluaga

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from enum import Enum


class TipoCargo(Enum):
    DIRECTIVO = 1
    ESTRATEGICO = 2
    OPERATIVO = 3


class TipoGenero(Enum):
    MASCULINO = 1
    FEMENINO = 2


class Empleado:

    def __init__(self, nombre, apellidos, cargo, genero, salario_dia, dias_trabajados,
                 otros_ingresos, pagos_salud, aporte_pensiones):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.salario_dia = salario_dia
        self.dias_trabajados = dias_trabajados
        self.otros_ingresos = otros_ingresos
        self.pagos_salud = pagos_salud
        self.aporte_pensiones = aporte_pensiones

    def calcular_nomina(self):
        return (self.salario_dia * self.dias_trabajados + self.otros_ingresos
                - self.pagos_salud - self.aporte_pensiones)


class ListaEmpleados:

    def __init__(self):
        self.empleados = []

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)

    def calcular_total_nomina(self):
        total = 0
        for empleado in self.empleados:
            total += empleado.calcular_nomina()
        return total

    def obtener_matriz(self):
        matriz = []
        for empleado in self.empleados:
            matriz.append([empleado.nombre, empleado.apellidos,
                           "%.2f" % empleado.calcular_nomina()])
        return matriz

    def convertir_texto(self):
        texto = "NOMINA DE LA EMPRESA\n\n"
        for empleado in self.empleados:
            texto += "Nombre = " + empleado.nombre + "\n"
            texto += "Apellidos = " + empleado.apellidos + "\n"
            texto += "Cargo = " + empleado.cargo.name + "\n"
            texto += "Género = " + empleado.genero.name + "\n"
            texto += "Sueldo = %.2f\n\n" % empleado.calcular_nomina()
        texto += "Total nómina = %.2f\n" % self.calcular_total_nomina()
        return texto


class VentanaAgregarEmpleado(tk.Toplevel):

    def __init__(self, lista):
        super().__init__()
        self.title("Agregar empleado")
        self.resizable(False, False)
        self.lista = lista

        tk.Label(self, text="Nombre").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.campo_nombre = tk.Entry(self, width=22)
        self.campo_nombre.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Apellidos").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.campo_apellidos = tk.Entry(self, width=22)
        self.campo_apellidos.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Cargo").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.combo_cargo = ttk.Combobox(self, width=19, state="readonly",
                                        values=[c.name for c in TipoCargo])
        self.combo_cargo.current(0)
        self.combo_cargo.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Género").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.genero = tk.StringVar(value=TipoGenero.MASCULINO.name)
        marco = tk.Frame(self)
        marco.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        for genero in TipoGenero:
            tk.Radiobutton(marco, text=genero.name.capitalize(), value=genero.name,
                           variable=self.genero).pack(side="left")

        tk.Label(self, text="Salario por día").grid(row=4, column=0, padx=10, pady=5,
                                                    sticky="w")
        self.campo_salario = tk.Entry(self, width=22)
        self.campo_salario.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self, text="Días trabajados").grid(row=5, column=0, padx=10, pady=5,
                                                    sticky="w")
        self.selector_dias = tk.Spinbox(self, from_=1, to=31, width=20)
        self.selector_dias.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self, text="Otros ingresos").grid(row=6, column=0, padx=10, pady=5,
                                                   sticky="w")
        self.campo_otros = tk.Entry(self, width=22)
        self.campo_otros.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(self, text="Pagos por salud").grid(row=7, column=0, padx=10, pady=5,
                                                    sticky="w")
        self.campo_salud = tk.Entry(self, width=22)
        self.campo_salud.grid(row=7, column=1, padx=10, pady=5)

        tk.Label(self, text="Aportes a pensiones").grid(row=8, column=0, padx=10, pady=5,
                                                        sticky="w")
        self.campo_pension = tk.Entry(self, width=22)
        self.campo_pension.grid(row=8, column=1, padx=10, pady=5)

        tk.Button(self, text="Agregar", width=10,
                  command=self.agregar).grid(row=9, column=0, padx=10, pady=10)
        tk.Button(self, text="Limpiar", width=10,
                  command=self.limpiar).grid(row=9, column=1, padx=10, pady=10)

    def agregar(self):
        try:
            empleado = Empleado(self.campo_nombre.get(),
                                self.campo_apellidos.get(),
                                TipoCargo[self.combo_cargo.get()],
                                TipoGenero[self.genero.get()],
                                float(self.campo_salario.get()),
                                int(self.selector_dias.get()),
                                float(self.campo_otros.get()),
                                float(self.campo_salud.get()),
                                float(self.campo_pension.get()))
        except ValueError:
            messagebox.showerror("Error", "Campo nulo o error en formato de número")
            return

        self.lista.agregar_empleado(empleado)
        messagebox.showinfo("Agregar empleado", "El empleado fue agregado a la nómina.")
        self.limpiar()

    def limpiar(self):
        for campo in [self.campo_nombre, self.campo_apellidos, self.campo_salario,
                      self.campo_otros, self.campo_salud, self.campo_pension]:
            campo.delete(0, tk.END)


class VentanaNomina(tk.Toplevel):

    def __init__(self, lista):
        super().__init__()
        self.title("Nómina")
        self.resizable(False, False)

        self.tabla = ttk.Treeview(self, columns=("nombre", "apellidos", "sueldo"),
                                  show="headings", height=8)
        for columna, titulo in [("nombre", "Nombre"), ("apellidos", "Apellidos"),
                                ("sueldo", "Sueldo")]:
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=130)
        self.tabla.pack(padx=10, pady=10)

        for fila in lista.obtener_matriz():
            self.tabla.insert("", tk.END, values=fila)

        tk.Label(self, text="Total nómina = %.2f" % lista.calcular_total_nomina()).pack(
            padx=10, pady=(0, 10))


class VentanaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Nómina")
        self.geometry("360x120")
        self.lista = ListaEmpleados()

        barra = tk.Menu(self)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Agregar empleado", command=self.agregar_empleado)
        opciones.add_command(label="Calcular nómina", command=self.calcular_nomina)
        opciones.add_command(label="Guardar archivo", command=self.guardar_archivo)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.config(menu=barra)

        tk.Label(self, text="Nómina de empleados de la empresa").pack(pady=(25, 5))
        tk.Label(self, text="Use el menú Opciones para registrar y calcular").pack()

    def agregar_empleado(self):
        VentanaAgregarEmpleado(self.lista)

    def calcular_nomina(self):
        VentanaNomina(self.lista)

    def guardar_archivo(self):
        carpeta = filedialog.askdirectory()
        if carpeta == "":
            return
        ruta = os.path.join(carpeta, "Nomina.txt")
        archivo = open(ruta, "w", encoding="utf-8")
        archivo.write(self.lista.convertir_texto())
        archivo.close()
        messagebox.showinfo("Guardar archivo", "El archivo fue creado en:\n" + ruta)


ventana = VentanaPrincipal()
ventana.mainloop()
