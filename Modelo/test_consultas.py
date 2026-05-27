from pymongo import MongoClient
from datetime import datetime
import os
class Conexion:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client["Formativa"]
        except Exception as err:
            print(f"Error conectando a la base de datos: {err}")
            self.db = None
        else:
            print(f"Conexión exitosa a la base de datos")
            print("Operando en: " + str(self.db.name))
        input("Presione Enter para continuar...")
        os.system('cls')
    def cerrar(self):
        if self.client:
            self.client.close()

conexion = Conexion()


def consultar_fecha():
    os.system('cls')
    print("-"*75)
    print("-🗓️ Consultar por fecha-")
    fecha_str = input("Ingrese la fecha (YYYY-MM-DD): ").strip()
    try:
        fecha_obj = fecha_str.strptime(fecha_str, "%Y-%m-%d")