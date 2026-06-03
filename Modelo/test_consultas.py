from pymongo import MongoClient
import os
import re #esto lo usé para verificar los correos antes de realizar consultas

mongosito = "mongodb://localhost:27017/"
nombreDB = "Sumativa"
col1 = "eventos"
col2 = "invitados"

def conexion():
    try:
        client = MongoClient(mongosito)
        db = client[nombreDB]
        return client, db
    except Exception as e:
        print(f"⚠️ Error al establecer conexión: {e}")
        return None, None

######################################################
################# CONSULTAS ########################## ###Estandarizadas (soy entero bkn)
######################################################


def estandar(coleccion, filtro_ctdo, proyeccion_ctdo, tipo):
    os.system('cls')
    print("-"*75)
    print("-📖 Resultados de la consulta-")
    print(f"-🔎 Tipo consulta: {tipo}")
    try:
        filtro = filtro_ctdo
        proyeccion = proyeccion_ctdo
        resultados = list(coleccion.find(filtro, proyeccion))
        encontrados = list(resultados)
        # CONSULTA DENTRO DE MONGODB !!!! db.eventos.find({},{"_id": 0, "invitados": 0})
        #                                                 (FILTRO CTDO)         (PROYECCION_CTDO)
        if not encontrados:
            print("⚠️No se encontraron registros.")
        else:
            for evento in encontrados:
                print(evento)     
    except Exception as e:
        print(f"⚠️ Error al realizar la consulta: {e}")
    input("ENTER para continuar")

def cruzada(coleccion, filtro_ctdo, proyeccion_ctdo, tipo):
    os.system('cls')
    os.system('cls')
    print("-"*75)
    print("-📖 Resultados de la consulta-")
    print(f"-🔎 Tipo consulta: {tipo}")
    try:
        pass
    except:
        pass



###############################################
################# INPUTS ######################  PARA CAMBIAR VALORES DE filtro_ctdo y proyeccion_ctdo
###############################################

def inputNombre():
    os.system('cls')
    nombre = input("Ingrese el nombre del invitado: ")
    #la i es para hacerlo case insentitive (q de igual si hay mayúsculas o no)
    filtro_ctdo = {"nombre": {"$regex": nombre, "$options": "i" }}
    proyeccion_ctdo = {"_id": 0, "rut": 0}
    return filtro_ctdo, proyeccion_ctdo


def inputCorreo():
    os.system('cls')
    dominio = input("Ingrese el dominio: ")
    correcto = validar_dominio(dominio)
    if correcto:
        filtro_ctdo = {"correo": {"$regex": dominio, "$options": "i" }}
        proyeccion_ctdo = {"_id": 0, "rut": 0}
    else:
        filtro_ctdo = None
        proyeccion_ctdo= None
    return filtro_ctdo, proyeccion_ctdo

def validar_dominio(dominio):
    patron = r'^@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.fullmatch(patron, dominio):
        return True
    return False

def inputConfirmacion():
    pass
###############################################
############## MENÚ ###########################
###############################################

def menu():
    os.system('cls')
    print("="*75)
    print("SISTEMA CONSULTA AAAAAA XDSAKADS")
    print("="*75)
    print("\n 1.- Listar eventos")
    print(" 2.- Buscar invitados por nombre ")
    print(" 3.- ")
    print(" 4.- ")
    print(" 5.- Buscar por dominio de correo")
    print(" 6.- Salir")

def main():
    client, db = conexion()
    if db is None: 
        return
    col_eventos = db[col1]
    col_invitados = db[col2]    
    while True:
        menu()
        seleccion = input("Ingrese el número de lo que desea hacer: ")
        try:
            seleccion = int(seleccion)
        except ValueError:
            print("⚠️ Ingrese solo números enteros entre 1 y 6")
            input("ENTER para continuar")
            continue
        if seleccion <1 or seleccion >6:
            print("⚠️ Ingrese solo números enteros entre 1 y 6")
            input("ENTER para continuar")
            continue
        elif seleccion == 1:
            filtro_ctdo = {}
            proyeccion_ctdo = {"_id": 0, "invitados": 0}
            tipo = "Todos los eventos"
            estandar(col_eventos, filtro_ctdo, proyeccion_ctdo, tipo)

        elif seleccion == 2:
            filtro_ctdo, proyeccion_ctdo = inputNombre()
            tipo = "Nombre"
            estandar(col_invitados, filtro_ctdo, proyeccion_ctdo, tipo)

        elif seleccion == 3:
            filtro_ctdo, proyeccion_ctdo = inputConfirmacion()
            tipo = "Confirmación de invitado"
            pass
            #cruzada()
        elif seleccion == 5:
            while True:
                filtro_ctdo, proyeccion_ctdo = inputCorreo()
                if filtro_ctdo and proyeccion_ctdo:
                    tipo = "Dominio de correo"
                    estandar(col_invitados, filtro_ctdo, proyeccion_ctdo, tipo)
                else:
                    print("⚠️ Ingrese un dominio válido (Ej: @ejemplo.cl)")
                    input("ENTER para continuar")
                    continue
                break
        elif seleccion == 6:
            input("Presione ENTER para continuar...")
            break

    client.close()

main()