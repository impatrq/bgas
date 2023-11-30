import tkinter as tk
import numpy as np

# Configuración
ventana = tk.Tk()
ventana.title("Simulador de Sensor de Gas MQ-2")

# Constantes
radio_balde = 16  # Radio en centímetros
altura_balde = 53  # Altura en centímetros
constante_degradacion = 0.01  # Constante de velocidad de degradación (ajústala según el tipo de material)
volumen_balde = np.pi * (radio_balde ** 2) * altura_balde  # Volumen del balde en cm³

# Función para simular la generación de gas metano
def simular_generacion_gas(dias, cantidad_materia, constante_degradacion):
    produccion_metano = []

    for dia in range(dias):
        tiempo_dias = dia
        produccion = (volumen_balde / volumen_balde) * (60 / 100) * (1 - np.exp(-constante_degradacion * tiempo_dias))
        produccion_metano.append(produccion * cantidad_materia * 1e9)  # Convertir a mm³

    return produccion_metano

# Función para calcular la concentración de metano en ppm
def calcular_concentracion_ppm(produccion_metano):
    concentraciones_ppm = [produccion / volumen_balde * 1e6 for produccion in produccion_metano]
    return concentraciones_ppm

# Función para manejar el botón "Calcular"
def calcular_simulacion():
    dias = int(entrada_dias.get())
    cantidad_materia_kg = float(entrada_materia.get())  # Cantidad de materia en kilogramos ingresada por el usuario
    cantidad_materia_g = cantidad_materia_kg * 1000  # Convertir de kg a g

    opcion_material = opcion_material_var.get()  # Obtener la opción seleccionada

    if opcion_material == "Fecal":
        constante_degradacion = 0.02
    elif opcion_material == "Carnes":
        constante_degradacion = 0.015
    elif opcion_material == "Vegetales":
        constante_degradacion = 0.01

    produccion_metano = simular_generacion_gas(dias, cantidad_materia_g, constante_degradacion)
    concentraciones_ppm = calcular_concentracion_ppm(produccion_metano)

    # Mostrar resultados
    etiqueta_concentracion.config(text="Concentración de Metano en ppm: " + ", ".join(map(lambda x: f"{x:.2f}", concentraciones_ppm)))

# Crear una etiqueta y una entrada para ingresar la cantidad de días en funcionamiento del biodigestor
etiqueta_dias = tk.Label(ventana, text="Ingrese la cantidad de días en funcionamiento del biodigestor:")
etiqueta_dias.pack()

entrada_dias = tk.Entry(ventana)
entrada_dias.pack()

# Crear una etiqueta y una entrada para ingresar la cantidad de materia en el balde (en kilogramos)
etiqueta_materia = tk.Label(ventana, text="Ingrese la cantidad de materia en el balde (en kilogramos):")
etiqueta_materia.pack()

entrada_materia = tk.Entry(ventana)
entrada_materia.pack()

# Opciones de material
opcion_material_var = tk.StringVar()
opcion_material_var.set("Fecal")  # Opción predeterminada

etiqueta_material = tk.Label(ventana, text="Seleccione el tipo de material:")
etiqueta_material.pack()

opciones_material = tk.OptionMenu(ventana, opcion_material_var, "Fecal", "Carnes", "Vegetales")
opciones_material.pack()

# Crear un botón para calcular la simulación
boton_calcular = tk.Button(ventana, text="Calcular", command=calcular_simulacion)
boton_calcular.pack()

# Crear etiqueta para mostrar la concentración de metano en ppm
etiqueta_concentracion = tk.Label(ventana, text="")
etiqueta_concentracion.pack()

ventana.mainloop()
