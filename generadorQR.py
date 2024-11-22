import qrcode
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, Canvas
from PIL import Image, ImageTk
import requests
from io import BytesIO

textos = {
    "es": {
        "titulo": "Generador de Código QR",
        "ingresa_enlace": "Ingresa el enlace:",
        "generar_qr": "Generar QR",
        "guardar_qr": "Guardar QR",
        "error_enlace": "Por favor, ingresa un enlace válido.",
        "exito_generar": "Código QR generado exitosamente.",
        "error_guardar": "Primero genera un código QR.",
        "guardar_exito": "El código QR se guardó en:",
        "guardar_cancelado": "No se seleccionó una ruta para guardar el archivo.",
        "cambio_idioma": "Cambiar idioma"
    },
    "en": {
        "titulo": "QR Code Generator",
        "ingresa_enlace": "Enter the link:",
        "generar_qr": "Generate QR",
        "guardar_qr": "Save QR",
        "error_enlace": "Please enter a valid link.",
        "exito_generar": "QR Code successfully generated.",
        "error_guardar": "Generate a QR code first.",
        "guardar_exito": "QR Code saved at:",
        "guardar_cancelado": "No file save location was selected.",
        "cambio_idioma": "Change Language"
    }
}

idioma_actual = "es"
qr_code_image = None
qr_image = None

URL_BANDERA_ES = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Flag_of_Spain.svg/2560px-Flag_of_Spain.svg.png"
URL_BANDERA_US = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Flag_of_the_United_States.svg/2560px-Flag_of_the_United_States.svg.png"


def cargar_imagen(url, ancho, alto):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        image = Image.open(image_data).convert("RGBA")
        image = image.resize((ancho, alto), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
        return None


def cambiar_idioma():
    global idioma_actual
    idioma_actual = "en" if idioma_actual == "es" else "es"
    actualizar_textos()
    actualizar_bandera()


def actualizar_textos():
    ventana.title(textos[idioma_actual]["titulo"])
    etiqueta_titulo.config(text=textos[idioma_actual]["titulo"])
    etiqueta_enlace.config(text=textos[idioma_actual]["ingresa_enlace"])
    boton_generar.config(text=textos[idioma_actual]["generar_qr"])
    boton_guardar.config(text=textos[idioma_actual]["guardar_qr"])
    etiqueta_cambio_idioma.config(text=textos[idioma_actual]["cambio_idioma"])


def actualizar_bandera():
    bandera = bandera_es if idioma_actual == "en" else bandera_us
    canvas.itemconfig(imagen_bandera, image=bandera)


def generar_qr():
    url = entrada_url.get().strip()
    if not url:
        messagebox.showerror("Error", textos[idioma_actual]["error_enlace"])
        return
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        image = qr.make_image(fill_color="black", back_color="white")
        global qr_image
        qr_image = ImageTk.PhotoImage(image.resize((200, 200)))
        etiqueta_imagen.config(image=qr_image)
        global qr_code_image
        qr_code_image = image
        messagebox.showinfo("Éxito", textos[idioma_actual]["exito_generar"])
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema al generar el QR: {e}")


def guardar_qr():
    if not qr_code_image:
        messagebox.showerror("Error", textos[idioma_actual]["error_guardar"])
        return
    ruta_destino = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title=textos[idioma_actual]["guardar_qr"]
    )
    if ruta_destino:
        qr_code_image.save(ruta_destino)
        messagebox.showinfo("Éxito", f"{textos[idioma_actual]['guardar_exito']} {ruta_destino}")
    else:
        messagebox.showwarning("Advertencia", textos[idioma_actual]["guardar_cancelado"])


ventana = Tk()
ventana.title(textos[idioma_actual]["titulo"])
ventana.geometry("400x550")
ventana.configure(bg="#f5f5f5")

tamaño_bandera = (80, 50)

bandera_es = cargar_imagen(URL_BANDERA_ES, *tamaño_bandera)
bandera_us = cargar_imagen(URL_BANDERA_US, *tamaño_bandera)

etiqueta_titulo = Label(ventana, text=textos[idioma_actual]["titulo"], font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333")
etiqueta_titulo.pack(pady=10)

etiqueta_enlace = Label(ventana, text=textos[idioma_actual]["ingresa_enlace"], bg="#f5f5f5", fg="#555", font=("Arial", 12))
etiqueta_enlace.pack()

entrada_url = Entry(ventana, width=40, font=("Arial", 12), relief="flat", borderwidth=2, highlightbackground="#ccc", highlightthickness=1)
entrada_url.pack(pady=5)

boton_generar = Button(ventana, text=textos[idioma_actual]["generar_qr"], command=generar_qr, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=10, pady=5)
boton_generar.pack(pady=10)

boton_guardar = Button(ventana, text=textos[idioma_actual]["guardar_qr"], command=guardar_qr, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=10, pady=5)
boton_guardar.pack(pady=10)

etiqueta_imagen = Label(ventana, bg="#f5f5f5")
etiqueta_imagen.pack(pady=20)

etiqueta_cambio_idioma = Label(ventana, text=textos[idioma_actual]["cambio_idioma"], font=("Arial", 12), bg="#f5f5f5", fg="#333")
etiqueta_cambio_idioma.pack(pady=5)

canvas = Canvas(ventana, width=90, height=50, highlightthickness=0, bg="#f5f5f5")
canvas.pack(pady=10)
imagen_bandera = canvas.create_image(45, 25, image=bandera_us)
canvas.tag_bind(imagen_bandera, "<Button-1>", lambda e: cambiar_idioma())

ventana.mainloop()

