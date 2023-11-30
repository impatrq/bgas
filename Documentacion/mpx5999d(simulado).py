import tkinter as tk
import pygame
import random
import numpy as np

# Configuración
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulador de Sensor de Presión MPX5999")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)

# Función para simular la lectura de presión absoluta y presión diferencial en kPa
def simular_lecturas_presion(semanas):
    # Aumentar la presión absoluta y diferencial gradualmente cada semana
    presion_inicial = 101.3  # Presión atmosférica estándar al nivel del mar en kPa
    tasa_aumento = 0.05  # Tasa de aumento en kPa por semana
    presion_absoluta = presion_inicial + (semanas * tasa_aumento)
    presion_diferencial = presion_absoluta - presion_inicial
    
    return presion_absoluta, presion_diferencial

# Función para manejar el botón "Calcular"
def calcular_presion():
    semanas = int(entrada_semanas.get())
    presion_absoluta, presion_diferencial = simular_lecturas_presion(semanas)
    
    etiqueta_resultado.config(text=f"Presión Absoluta: {presion_absoluta:.2f} kPa\nPresión Diferencial: {presion_diferencial:.2f} kPa")

# Crear una ventana de tkinter
ventana = tk.Tk()
ventana.title("Simulador de Sensor de Presión MPX5999")

# Crear una etiqueta y una entrada para ingresar la cantidad de semanas
etiqueta_semanas = tk.Label(ventana, text="Ingrese la cantidad de semanas en funcionamiento del biodigestor:")
etiqueta_semanas.pack()

entrada_semanas = tk.Entry(ventana)
entrada_semanas.pack()

# Crear un botón para calcular la presión
boton_calcular = tk.Button(ventana, text="Calcular", command=calcular_presion)
boton_calcular.pack()

# Crear una etiqueta para mostrar el resultado
etiqueta_resultado = tk.Label(ventana, text="")
etiqueta_resultado.pack()

ventana.mainloop()
