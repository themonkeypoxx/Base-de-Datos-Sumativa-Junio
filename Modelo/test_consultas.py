from pymongo import MongoClient
import os

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

##CONSULTAR A PROFE
def inputAcceso():
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
    print(" 7.- Salir")

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
            print("⚠️ Ingrese solo números enteros entre 1 y 7")
            input("ENTER para continuar")
            continue
        if seleccion <1 or seleccion >7:
            print("⚠️ Ingrese solo números enteros entre 1 y 7")
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

        elif seleccion == 5:
            input("Presione ENTER para continuar...")
            break

    client.close()

main()