# Actividad 5 - Ejercicio 8.5: Gestion de contenido - Hotel
# Programacion Orientada a Objetos 2026-2S - Juan Diego Toro Zuluaga

import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime


class Huesped:

    def __init__(self, nombres, apellidos, documento_identidad, fecha_ingreso):
        self.nombres = nombres
        self.apellidos = apellidos
        self.documento_identidad = documento_identidad
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = None

    def obtener_dias_alojamiento(self):
        return (self.fecha_salida - self.fecha_ingreso).days


class Habitacion:

    def __init__(self, numero_habitacion, precio_dia):
        self.numero_habitacion = numero_habitacion
        self.disponible = True
        self.precio_dia = precio_dia
        self.huesped = None

    def get_disponible(self):
        return self.disponible

    def set_disponible(self, disponible):
        self.disponible = disponible

    def get_huesped(self):
        return self.huesped

    def set_huesped(self, huesped):
        self.huesped = huesped


class Hotel:

    def __init__(self):
        self.lista_habitaciones = []
        for numero in range(1, 11):
            if numero <= 5:
                self.lista_habitaciones.append(Habitacion(numero, 120000))
            else:
                self.lista_habitaciones.append(Habitacion(numero, 160000))

    def obtener_habitacion(self, numero):
        return self.lista_habitaciones[numero - 1]

    def buscar_habitacion_ocupada(self, numero):
        return not self.obtener_habitacion(numero).get_disponible()

    def buscar_fecha_ingreso_habitacion(self, numero):
        habitacion = self.obtener_habitacion(numero)
        return habitacion.get_huesped().fecha_ingreso.strftime("%Y-%m-%d")


class VentanaIngreso(tk.Toplevel):

    def __init__(self, hotel, numero, ventana_habitaciones):
        super().__init__()
        self.title("Ingreso de huésped")
        self.resizable(False, False)
        self.hotel = hotel
        self.numero = numero
        self.ventana_habitaciones = ventana_habitaciones

        tk.Label(self, text="Habitación " + str(numero)).grid(row=0, column=0, columnspan=2,
                                                              padx=10, pady=10)

        etiquetas = ["Fecha de ingreso (aaaa-mm-dd)", "Nombres", "Apellidos",
                     "Documento de identidad"]
        self.campos = []
        for i, texto in enumerate(etiquetas):
            tk.Label(self, text=texto).grid(row=1 + i, column=0, padx=10, pady=5, sticky="w")
            campo = tk.Entry(self, width=20)
            campo.grid(row=1 + i, column=1, padx=10, pady=5)
            self.campos.append(campo)

        tk.Button(self, text="Guardar", width=10,
                  command=self.guardar).grid(row=5, column=0, columnspan=2, pady=10)

    def guardar(self):
        try:
            fecha_ingreso = datetime.strptime(self.campos[0].get(), "%Y-%m-%d")
            documento = int(self.campos[3].get())
        except ValueError:
            messagebox.showerror("Error", "Fecha o documento con formato incorrecto")
            return

        huesped = Huesped(self.campos[1].get(), self.campos[2].get(), documento,
                          fecha_ingreso)
        habitacion = self.hotel.obtener_habitacion(self.numero)
        habitacion.set_huesped(huesped)
        habitacion.set_disponible(False)

        messagebox.showinfo("Ingreso", "La habitación quedó registrada como no disponible.")
        self.ventana_habitaciones.actualizar()
        self.destroy()


class VentanaSalida(tk.Toplevel):

    def __init__(self, hotel, numero):
        super().__init__()
        self.title("Salida de huésped")
        self.resizable(False, False)
        self.hotel = hotel
        self.numero = numero
        self.habitacion = hotel.obtener_habitacion(numero)

        tk.Label(self, text="Habitación " + str(numero)).grid(row=0, column=0, columnspan=2,
                                                              padx=10, pady=10)

        tk.Label(self, text="Fecha de ingreso").grid(row=1, column=0, padx=10, pady=5,
                                                     sticky="w")
        tk.Label(self, text=hotel.buscar_fecha_ingreso_habitacion(numero)).grid(
            row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Fecha de salida (aaaa-mm-dd)").grid(row=2, column=0, padx=10,
                                                                 pady=5, sticky="w")
        self.campo_salida = tk.Entry(self, width=18)
        self.campo_salida.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self, text="Calcular", width=12,
                  command=self.calcular).grid(row=3, column=0, padx=10, pady=10)
        self.boton_registrar = tk.Button(self, text="Registrar salida", width=14,
                                         state="disabled", command=self.registrar_salida)
        self.boton_registrar.grid(row=3, column=1, padx=10, pady=10)

        self.etiqueta_dias = tk.Label(self, text="Días de alojamiento =")
        self.etiqueta_dias.grid(row=4, column=0, columnspan=2, padx=10, sticky="w")

        self.etiqueta_total = tk.Label(self, text="Total a pagar =")
        self.etiqueta_total.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 10),
                                 sticky="w")

    def calcular(self):
        huesped = self.habitacion.get_huesped()
        try:
            fecha_salida = datetime.strptime(self.campo_salida.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Fecha con formato incorrecto")
            return

        if fecha_salida <= huesped.fecha_ingreso:
            messagebox.showerror("Error", "La fecha de salida debe ser posterior a la de "
                                          "ingreso.")
            return

        huesped.fecha_salida = fecha_salida
        dias = huesped.obtener_dias_alojamiento()
        total = dias * self.habitacion.precio_dia

        self.etiqueta_dias.config(text="Días de alojamiento = " + str(dias))
        self.etiqueta_total.config(text="Total a pagar = %.2f" % total)
        self.boton_registrar.config(state="normal")

    def registrar_salida(self):
        self.habitacion.set_huesped(None)
        self.habitacion.set_disponible(True)
        messagebox.showinfo("Salida", "La habitación quedó disponible.")
        self.destroy()


class VentanaHabitaciones(tk.Toplevel):

    def __init__(self, hotel):
        super().__init__()
        self.title("Consultar habitaciones")
        self.resizable(False, False)
        self.hotel = hotel

        tk.Label(self, text="Habitación").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self, text="Estado").grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self, text="Precio por día").grid(row=0, column=2, padx=10, pady=5)

        self.etiquetas = []
        for i, habitacion in enumerate(hotel.lista_habitaciones):
            tk.Label(self, text=str(habitacion.numero_habitacion)).grid(row=1 + i, column=0)
            etiqueta = tk.Label(self, text="")
            etiqueta.grid(row=1 + i, column=1)
            self.etiquetas.append(etiqueta)
            tk.Label(self, text="%.2f" % habitacion.precio_dia).grid(row=1 + i, column=2)

        tk.Label(self, text="Habitación a reservar").grid(row=11, column=0, padx=10,
                                                          pady=10)
        self.selector = tk.Spinbox(self, from_=1, to=10, width=8)
        self.selector.grid(row=11, column=1, pady=10)
        tk.Button(self, text="Reservar", width=10,
                  command=self.reservar).grid(row=11, column=2, padx=10, pady=10)

        self.actualizar()

    def actualizar(self):
        for etiqueta, habitacion in zip(self.etiquetas, self.hotel.lista_habitaciones):
            if habitacion.get_disponible():
                etiqueta.config(text="Disponible")
            else:
                etiqueta.config(text="No disponible")

    def reservar(self):
        numero = int(self.selector.get())
        if self.hotel.buscar_habitacion_ocupada(numero):
            messagebox.showerror("Error", "La habitación ya está ocupada.")
            return
        VentanaIngreso(self.hotel, numero, self)


class VentanaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Hotel")
        self.geometry("420x120")
        self.hotel = Hotel()

        barra = tk.Menu(self)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Consultar habitaciones",
                             command=self.consultar_habitaciones)
        opciones.add_command(label="Salida de huéspedes", command=self.salida_huespedes)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.config(menu=barra)

        tk.Label(self, text="Administración de habitaciones del hotel").pack(pady=(25, 5))
        tk.Label(self, text="Use el menú Opciones para reservar y registrar salidas").pack()

    def consultar_habitaciones(self):
        VentanaHabitaciones(self.hotel)

    def salida_huespedes(self):
        texto = simpledialog.askstring("Salida de huéspedes",
                                       "Número de habitación a desocupar:")
        if texto is None:
            return

        try:
            numero = int(texto)
        except ValueError:
            messagebox.showerror("Error", "El número de habitación debe ser numérico.")
            return

        if numero < 1 or numero > 10:
            messagebox.showerror("Error", "El número de habitación debe estar entre 1 y 10.")
            return

        if not self.hotel.buscar_habitacion_ocupada(numero):
            messagebox.showerror("Error", "La habitación no está ocupada.")
            return

        VentanaSalida(self.hotel, numero)


ventana = VentanaPrincipal()
ventana.mainloop()
