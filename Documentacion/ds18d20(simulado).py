import tkinter as tk
import requests

# Función para obtener la temperatura desde un enlace externo
def obtener_temperatura():
    try:
        # Reemplaza 'URL_DEL_ENLACE_EXTERNAL_A_TU_API' con el enlace real
        response = requests.get('')
        data = response.json()
        temperatura = data['temperatura']
        return f"{temperatura} °C"
    except Exception as e:
        return "Error al obtener la temperatura"

# Crear una ventana
ventana = tk.Tk()
ventana.title("Temperatura Actual")

# Etiqueta para mostrar la temperatura
etiqueta_temperatura = tk.Label(ventana, text=obtener_temperatura(), font=("Arial", 20))
etiqueta_temperatura.pack(padx=20, pady=20)

# Botón para actualizar la temperatura
def actualizar_temperatura():
    temperatura = obtener_temperatura()
    etiqueta_temperatura.config(text=temperatura)

boton_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_temperatura)
boton_actualizar.pack()

ventana.mainloop()
