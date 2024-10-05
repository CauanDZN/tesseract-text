import cv2
import pytesseract
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Capturar Imagem da Câmera")
        self.root.geometry("1280x720")
        
        self.camera_on = False

        self.label_video = tk.Label(root)
        self.label_video.pack()

        self.btn_start = tk.Button(root, text="Iniciar Câmera", command=self.iniciar_camera)
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_capture = tk.Button(root, text="Capturar Imagem", command=self.capturar_imagem)
        self.btn_capture.pack(side=tk.LEFT, padx=10)

        self.btn_stop = tk.Button(root, text="Encerrar Câmera", command=self.encerrar_camera)
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        self.btn_ocr = tk.Button(root, text="Realizar OCR", command=self.realizar_ocr)
        self.btn_ocr.pack(side=tk.LEFT, padx=10)

        self.frame_capturado = None
        self.cam = None

    def iniciar_camera(self):
        if not self.camera_on:
            self.cam = cv2.VideoCapture(0)
            if not self.cam.isOpened():
                messagebox.showerror("Erro", "Não foi possível acessar a câmera.")
                return
            self.camera_on = True
            self.atualizar_frame()

    def atualizar_frame(self):
        if self.camera_on:
            ret, frame = self.cam.read()
            if ret:
                self.frame_capturado = frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label_video.imgtk = imgtk
                self.label_video.configure(image=imgtk)
            self.root.after(10, self.atualizar_frame)

    def capturar_imagem(self):
        if self.frame_capturado is not None:
            nome_arquivo = f'foto_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            cv2.imwrite(nome_arquivo, self.frame_capturado)
            messagebox.showinfo("Captura", f"Imagem capturada e salva como {nome_arquivo}")
            self.caminho_imagem = nome_arquivo
        else:
            messagebox.showwarning("Atenção", "Nenhuma imagem capturada.")

    def realizar_ocr(self):
        if self.frame_capturado is not None:
            imagem = self.frame_capturado
            imagem_preprocessada = self.preprocessar_imagem(imagem)

            config = '--psm 6'
            texto = pytesseract.image_to_string(imagem_preprocessada, config=config, lang='por')  # Especifica o idioma

            if texto:
                messagebox.showinfo("Texto OCR", f"Texto extraído: \n{texto}")
            else:
                messagebox.showinfo("Texto OCR", "Nenhum texto encontrado.")
        else:
            messagebox.showwarning("Atenção", "Capture uma imagem antes de realizar OCR.")

    def preprocessar_imagem(self, imagem):
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        imagem_suavizada = cv2.GaussianBlur(imagem_cinza, (5, 5), 0)

        _, imagem_thresh = cv2.threshold(imagem_suavizada, 150, 255, cv2.THRESH_BINARY_INV)

        imagem_redimensionada = cv2.resize(imagem_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        return imagem_redimensionada

    def encerrar_camera(self):
        if self.camera_on:
            self.cam.release()
            self.camera_on = False
            self.label_video.config(image='')
            messagebox.showinfo("Encerrado", "Câmera encerrada.")

root = tk.Tk()
app = App(root)
root.mainloop()
