import requests

BASE_URL = "https://t1-fastapi.onrender.com/trainee"


def mostrar_aprendiz(a):
    print("-" * 30)
    print("ID:", a.get("id", a.get("_id")))
    print("Documento:", a.get("document"))
    print("Nombres:", a.get("firstname"))
    print("Apellidos:", a.get("lastname"))
    print("Correo:", a.get("email"))
    print("Edad:", a.get("age"))
    print("Programa:", a.get("program"))
    print("Ficha:", a.get("record_number"))


def mostrar_error(respuesta):
    try:
        detalle = respuesta.json().get("detail", respuesta.text)
    except ValueError:
        detalle = respuesta.text
    print(f"Error {respuesta.status_code}: {detalle}")


def pedir_datos():
    return {
        "document": input("Documento: "),
        "firstname": input("Nombres: "),
        "lastname": input("Apellidos: "),
        "email": input("Correo: "),
        "age": int(input("Edad: ")),
        "program": input("Programa: "),
        "record_number": input("Número de ficha: "),
    }


def crear():
    datos = pedir_datos()
    r = requests.post(BASE_URL, json=datos)
    if r.status_code == 201:
        print("Aprendiz creado:")
        mostrar_aprendiz(r.json())
    else:
        mostrar_error(r)


def listar():
    r = requests.get(BASE_URL)
    if r.status_code == 200:
        aprendices = r.json()
        print(f"Total: {len(aprendices)}")
        for a in aprendices:
            mostrar_aprendiz(a)
    else:
        mostrar_error(r)


def buscar():
    id_aprendiz = input("ID del aprendiz: ")
    r = requests.get(f"{BASE_URL}/{id_aprendiz}")
    if r.status_code == 200:
        mostrar_aprendiz(r.json())
    else:
        mostrar_error(r)


def actualizar():
    id_aprendiz = input("ID del aprendiz: ")
    print("Escribe solo lo que quieras cambiar (Enter para omitir)")
    datos = {}
    for campo in ["document", "firstname", "lastname", "email", "age", "program", "record_number"]:
        valor = input(f"{campo}: ")
        if valor:
            datos[campo] = int(valor) if campo == "age" else valor
    r = requests.put(f"{BASE_URL}/{id_aprendiz}", json=datos)
    if r.status_code == 200:
        print("Aprendiz actualizado:")
        mostrar_aprendiz(r.json())
    else:
        mostrar_error(r)


def eliminar():
    id_aprendiz = input("ID del aprendiz: ")
    r = requests.delete(f"{BASE_URL}/{id_aprendiz}")
    if r.status_code == 200:
        print(r.json().get("mensaje", "Aprendiz eliminado"))
    else:
        mostrar_error(r)


def menu():
    while True:
        print("\n--- GESTIÓN DE APRENDICES ---")
        print("1. Crear aprendiz")
        print("2. Listar aprendices")
        print("3. Buscar por ID")
        print("4. Actualizar aprendiz")
        print("5. Eliminar aprendiz")
        print("0. Salir")
        opcion = input("Opción: ")

        try:
            if opcion == "1":
                crear()
            elif opcion == "2":
                listar()
            elif opcion == "3":
                buscar()
            elif opcion == "4":
                actualizar()
            elif opcion == "5":
                eliminar()
            elif opcion == "0":
                print("Hasta luego")
                break
            else:
                print("Opción no válida")
        except ValueError:
            print("Error: la edad debe ser un número")
        except requests.exceptions.RequestException:
            print("Error: no se pudo conectar con la API")


menu()