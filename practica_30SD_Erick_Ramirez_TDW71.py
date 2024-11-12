import serial
import serial.tools.list_ports
from threading import Thread, Event
from tkinter import StringVar

class Comunicacion():
    def __init__(self, *args):
        super().__init__(*args)
        self.datos_recibidos = StringVar()

        self.arduino = serial.Serial()  # Se puede configurar el timeout
        self.arduino.timeout = 0.5

        self.baudrates = ['1200', '2400', '4800', '9600', '19200', '38400', '115200']
        self.puertos = []

        self.señal = Event()
        self.hilo = None

    def puertos_disponibles(self):
        # Obtener lista de puertos disponibles
        self.puertos = [port.device for port in serial.tools.list_ports.comports()]
        print("Puertos disponibles:", self.puertos)  # Imprimir los puertos disponibles para depuración

    def conexion_serial(self):
        try:
            self.arduino.open()

        except:
            pass
        if(self.arduino.is_open):
            self.iniciar_hilo()
            print('Conectado')

    def enviar_datos(self, data):
        if (self.arduino.is_open):
            datos = str(data) + "\n"
            self.arduino.write(datos.encode())
        else:
            print('Error')

    def leer_dato(self):
        try:
            while (self.señal.isSet() and self.arduino.is_open):
                data = self.arduino.readline().decode('utf-8').strip()
                if(len(data)>1):
                    self.datos_recibidos.set(data)
        except TypeError:
            pass

    def iniciar_hilo(self):
        self.hilo = Thread(target=self.leer_dato)
        self.hilo.setDaemon(1)
        self.señal.set()
        self.hilo.start()

    def stop_hilo(self):
        if(self.hilo is not None):
            self.señal.clear()
            self.hilo.join()
            self.hilo = None

    def desconectar(self):
       self.arduino.close()
       self.stop_hilo()