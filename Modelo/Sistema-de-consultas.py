from pymongo import MongoClient
import os
import re #esto lo usé para verificar los correos antes de realizar consultas

mongosito = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.8.1" 
nombreDB = "Sumativa"
col1 = "eventos"
col2 = "invitados"
#  11.098.760-0 asiste en evento 1. (para testeo)
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


def verificacion(coleccion, col1, col2, inputUser):
    if coleccion == col2:
        if "@" in inputUser or ".cl" in inputUser or ".com" in inputUser:
            filtro_ctdo = {"correo": inputUser}
        else:
            filtro_ctdo = {"rut": inputUser}
    elif coleccion == col1:
        filtro_ctdo = {"codigo": {"$regex": inputUser}}
    try:
        filtro = filtro_ctdo
        resultados = list(coleccion.find(filtro))
        encontrados = list(resultados)
        if not encontrados:
           return False
        else:
            return True   
    except Exception as e:
        print(f"⚠️ Error al verificar el dato ingresado: {e}")

######################################################
######          Consultas AGGREGATE )     ############
######################################################

def cruzada(coleccion, pipeline, tipo, numeroValido):
    os.system('cls')
    print("-"*75)
    print("-📖 Resultados de la consulta-")
    print(f"-🔎 Tipo consulta: {tipo}")
    try:
        resultados = list(coleccion.aggregate(pipeline))
        if not resultados:
            print("⚠️ No se encontraron registros.")
        else:
            if tipo == f"Top {numeroValido} eventos con más confirmados":
                cta = 1
                for documento in resultados:
                    print(f"{cta}.-", documento)
                    cta = cta + 1
            else:
                for documento in resultados:
                    print(documento)
                
    except Exception as e:
        print(f"⚠️ Error al realizar la consulta: {e}")



###############################################
################# INPUTS ######################  PARA CAMBIAR VALORES DE filtro_ctdo y proyeccion_ctdo
###############################################

def inputNombre():
    os.system('cls')
    nombre = input("Ingrese el nombre / apellido del invitado: ")
    #la i es para hacerlo case insentitive (q de igual si hay mayúsculas o no)
    filtro_ctdo = {"nombre": {"$regex": nombre, "$options": "i" }}
    proyeccion_ctdo = {"_id": 0, "correo": 0, "empresa": 0, "estado": 0}
    return filtro_ctdo, proyeccion_ctdo

def inputCategoria():
    os.system('cls')
    print("Las categorías son: \n1.- Charla\n2.-Meetup\n3.-Workshop")
    categoria = input ("Ingrese la categoria del evento: ")
    #requerimniento categoria 
    filtro_ctdo = {"categoria": {"$regex": categoria, "$options": "i"}}
    proyeccion_ctdo = {"_id": 0, "codigo": 1, "nombre": 1, "fecha": 1, "lugar": 1}
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

#esto lo reutilicé de intro a la progra año pasado
def validar_dominio(dominio):
    patron = r'^@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.fullmatch(patron, dominio):
        return True
    return False
    
def trynum(numero):
    try: 
        numero = int(numero)
    except Exception:
        return False, numero
    return True, numero

def listarEventos(coleccion):
    filtro_ctdo = {}
    proyeccion_ctdo = {"_id": 0, "invitados": 0}
    tipo = "Todos los eventos"
    estandar(coleccion, filtro_ctdo, proyeccion_ctdo, tipo)
    
def listarInvitados(coleccion, filtro):
    if filtro == "correo":
        filtro_ctdo = {}
        proyeccion_ctdo = {"_id": 0, "rut": 0, "empresa": 0, "estado": 0}
    else:
        filtro_ctdo = {}
        proyeccion_ctdo = {"_id": 0, "correo": 0, "empresa": 0, "estado": 0}
    tipo = "Todos los invitados3"
    estandar(coleccion, filtro_ctdo, proyeccion_ctdo, tipo)
    
def errorVerificar():
    os.system('cls')
    print("⁉️ El valor especificado no existe en los registros. Asegúrese de escribirlo correctamente")
    input("ENTER para volver a ingresar...")


#############################################
############################################
### aggregate
######################################

def inputConfirmacion(coleccion1, coleccion2):
    while True:
        os.system('cls')
        print("¿Desea buscar empleados por correo o RUT? \n 1.- Correo \n 2.- RUT")
        busqueda_seleccion = input("Ingrese: ")
        if busqueda_seleccion == '1':
            filtro = "correo"
            break
        elif busqueda_seleccion == '2':
            filtro = "rut"
            break
        else: 
            print("❗Ingrese solo números enteros del 1 al 2")
            input('ENTER para continuar')
            continue
    while True:
        os.system('cls')
        listarInvitados(coleccion2, filtro) 
        rut_seleccion = input("Ingrese RUT / Correo del invitado: ")
        col_sel = coleccion2
        valido_rut = verificacion(col_sel, coleccion1, coleccion2, rut_seleccion)
        if valido_rut:
            break
        else:
            errorVerificar()
            continue
    while True:
        os.system('cls')
        listarEventos(coleccion1)
        print("-"*75)
        codigo_seleccion = input("Ingrese código del evento: ")
        codigo_seleccion = codigo_seleccion.upper()
        col_sel = coleccion1
        valido_cod = verificacion(col_sel, coleccion1, coleccion2, codigo_seleccion)
        if valido_cod:
            break
        else:
            errorVerificar()
            continue
    if filtro == "rut":
        pipeline = [
                {"$match": {"codigo": codigo_seleccion}
                },
                {"$unwind": "$invitados"},
                {"$match": {"invitados.rut": rut_seleccion, "invitados.estado": "confirmado"}
                },
                {"$lookup": {"from": "invitados", "localField": "invitados.rut", "foreignField": "rut", "as": "info_persona"}
                },
                {"$match": {"info_persona.estado": {"$ne": "bloqueado"}}
                },
                {"$project": {
                        "_id": 0,
                        "rut": "$invitados.rut",
                        "nombre": {"$arrayElemAt": ["$info_persona.nombre", 0]},
                        "nombre_evento": "$nombre",
                        "fecha_evento": "$fecha",
                        "lugar": "$lugar",
                        "checkin": "$invitados.checkin"}
                }
            ]
    else:
        pipeline = [
            {"$match": {"codigo": codigo_seleccion}},
            {"$unwind": "$invitados"},
            {
                "$lookup": {
                    "from": "invitados", 
                    "localField": "invitados.rut", 
                    "foreignField": "rut", 
                    "as": "info_persona"
                }
            },
            {
                "$match": {
                    "invitados.estado": "confirmado",
                    "info_persona.correo": rut_seleccion,
                    "info_persona.estado": {"$ne": "bloqueado"} 
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "rut": "$invitados.rut",
                    "nombre": {"$arrayElemAt": ["$info_persona.nombre", 0]},
                    "nombre_evento": "$nombre",
                    "fecha_evento": "$fecha",
                    "lugar": "$lugar",
                    "checkin": "$invitados.checkin"
                }
            }
        ]

        
    return pipeline

def pipelineTop3(numero):
    pipeline = [
        {"$unwind": "$invitados"},
        {"$match": {"invitados.estado": "confirmado"}},
        {
            "$group": {
                "_id": "$_id",
                "codigo": {"$first": "$codigo"},
                "nombre": {"$first": "$nombre"},
                "fecha": {"$first": "$fecha"},
                "total_confirmados": {"$sum": 1}
            }
        },
        {"$sort": {"total_confirmados": -1}},
        {"$limit": numero},
        {
            "$project": {
                "_id": 0,
                "codigo": 1,
                "nombre": 1,
                "fecha": 1,
                "total_confirmados": 1
            }
        }
    ]
    return pipeline
###############################################
############## MENÚ ###########################
###############################################

def menu():
    os.system('cls')
    print("="*75)
    print("SISTEMA CONSULTAS MONGODB")
    print("="*75)
    print("\n 1.- Listar eventos")
    print(" 2.- Buscar invitados por nombre / apellido ")
    print(" 3.- Confirmar asistencia de invitado a evento (usando correo o rut)") #se reutilizo, pq la habiamos hecho con rut
    print(" 4.- Top 3 eventos más asistidos")
    print(" 5.- Buscar invitados por dominio de correo")
    print(" 6.- Buscar eventos por categoria")
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
            listarEventos(col_eventos)
            input("ENTER para continuar")

        elif seleccion == 2:
            filtro_ctdo, proyeccion_ctdo = inputNombre()
            tipo = "Nombre / Apellido"
            estandar(col_invitados, filtro_ctdo, proyeccion_ctdo, tipo)
            input("ENTER para continuar")

        elif seleccion == 3:
            pipeline = inputConfirmacion(col_eventos, col_invitados)
            tipo = "Confirmación de invitado"
            numeroValido = 1
            cruzada(col_eventos, pipeline, tipo, numeroValido)
            input("ENTER para continuar")
        elif seleccion == 4:
            while True:
                os.system('cls')
                numero = input("Ingrese el número de eventos que desea ordenar ")
                valido, numeroValido = trynum(numero)
                if valido == False:
                    print("⚠️ Ingrese solo números enteros")
                    input("ENTER para continuar")
                    continue
                break
            
            pipeline = pipelineTop3(numeroValido)
            tipo = f"Top {numero} eventos con más confirmados"
            cruzada(col_eventos, pipeline, tipo, numeroValido)
            input("ENTER para continuar")
        elif seleccion == 5:
            while True:
                filtro_ctdo, proyeccion_ctdo = inputCorreo()
                if filtro_ctdo and proyeccion_ctdo:
                    tipo = "Dominio de correo"
                    estandar(col_invitados, filtro_ctdo, proyeccion_ctdo, tipo)
                    input("ENTER para continuar")
                else:
                    print("⚠️ Ingrese un dominio válido (Ej: @ejemplo.cl)")
                    input("ENTER para continuar")
                    continue
                break
        elif seleccion == 6:
            filtro_ctdo, proyeccion_ctdo = inputCategoria()
            tipo = "Categoria"
            estandar(col_eventos, filtro_ctdo, proyeccion_ctdo, tipo)
            input("ENTER para continuar")
            
        elif seleccion == 7:
            input("Presione ENTER para continuar...")
            os.system('cls')
            break

    client.close()

main() 