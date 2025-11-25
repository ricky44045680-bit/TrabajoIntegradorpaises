# main.py
import csv
import os

ARCHIVO = "paises.csv"

# ==================== CARGA Y GUARDADO ====================
def cargar_paises():
    """Carga los países desde el CSV. Crea lista vacía si no existe."""
    paises = []
    if not os.path.exists(ARCHIVO):
        print(f"{ARCHIVO} no encontrado. Se creará uno nuevo al guardar.")
        return paises
    
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            lector = csv.reader(f)
            next(lector, None)  # Saltar encabezado
            for fila in lector:
                if len(fila) >= 4:
                    nombre = fila[0].strip()
                    try:
                        poblacion = int(fila[1].strip())
                        superficie = int(fila[2].strip())
                    except ValueError:
                        print(f"Línea inválida ignorada: {fila}")
                        continue
                    continente = fila[3].strip()
                    if nombre and poblacion > 0 and superficie > 0:
                        paises.append({
                            "nombre": nombre.capitalize(),
                            "poblacion": poblacion,
                            "superficie": superficie,
                            "continente": continente.capitalize()
                        })
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
    return paises


def guardar_paises(paises):
    """Guarda toda la lista en el CSV con encabezado."""
    try:
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["nombre", "poblacion", "superficie", "continente"])
            for p in paises:
                escritor.writerow([p["nombre"], p["poblacion"], p["superficie"], p["continente"]])
        print(f"Datos guardados correctamente en {ARCHIVO}")
    except Exception as e:
        print(f"Error al guardar: {e}")


# ==================== UTILIDADES ====================
def mostrar_pais(p):
    print(f"{p['nombre']:25} | {p['continente']:12} | Población: {p['poblacion']:12,} | Superficie: {p['superficie']:10,} km²")

def existe_pais(paises, nombre):
    return any(p["nombre"].lower() == nombre.lower() for p in paises)


# ==================== FUNCIONALIDADES ====================
def agregar_pais(paises):
    print("\n=== AGREGAR NUEVO PAÍS ===")
    nombre = input("Nombre del país: ").strip()
    if not nombre:
        print("Error: el nombre no puede estar vacío.")
        return
    if existe_pais(paises, nombre):
        print("Error: ya existe un país con ese nombre.")
        return

    while True:
        pob = input("Población: ").strip()
        if pob.isdigit() and int(pob) > 0:
            poblacion = int(pob)
            break
        print("Ingrese un número entero mayor a 0.")

    while True:
        sup = input("Superficie (km²): ").strip()
        if sup.isdigit() and int(sup) > 0:
            superficie = int(sup)
            break
        print("Ingrese un número entero mayor a 0.")

    continente = input("Continente: ").strip().capitalize()
    if not continente:
        print("Error: el continente no puede estar vacío.")
        return

    nuevo = {"nombre": nombre.capitalize(), "poblacion": poblacion,
             "superficie": superficie, "continente": continente}
    paises.append(nuevo)
    print(f"→ {nombre.capitalize()} agregado exitosamente.")
    guardar_paises(paises)


def actualizar_pais(paises):
    print("\n=== ACTUALIZAR PAÍS ===")
    nombre = input("Nombre del país a modificar: ").strip()
    pais = next((p for p in paises if p["nombre"].lower() == nombre.lower()), None)
    if not pais:
        print("País no encontrado.")
        return

    print(f"País encontrado: {pais['nombre']}")
    print(f"Población actual : {pais['poblacion']:,}")
    print(f"Superficie actual: {pais['superficie']:,} km²")

    cambios = False
    while True:
        entrada = input("Nueva población (Enter para mantener): ").strip()
        if entrada == "":
            break
        if entrada.isdigit() and int(entrada) > 0:
            pais["poblacion"] = int(entrada)
            cambios = True
            break
        print("Número inválido.")

    while True:
        entrada = input("Nueva superficie (Enter para mantener): ").strip()
        if entrada == "":
            break
        if entrada.isdigit() and int(entrada) > 0:
            pais["superficie"] = int(entrada)
            cambios = True
            break
        print("Número inválido.")

    if cambios:
        print("Datos actualizados correctamente.")
        guardar_paises(paises)
    else:
        print("No se realizaron cambios.")


def buscar_pais(paises):
    print("\n=== BUSCAR PAÍS ===")
    termino = input("Texto a buscar en el nombre: ").strip().lower()
    if not termino:
        print("Debe ingresar algo.")
        return
    encontrados = [p for p in paises if termino in p["nombre"].lower()]
    if not encontrados:
        print("No se encontraron coincidencias.")
        return
    print(f"\n{len(encontrados)} resultado(s) encontrado(s):")
    print("-" * 90)
    for p in encontrados:
        mostrar_pais(p)
    print("-" * 90)


def filtrar_paises(paises):
    print("\n=== FILTRAR PAÍSES ===")
    print("1. Por continente")
    print("2. Por rango de población")
    print("3. Por rango de superficie")
    op = input("Opción: ").strip()

    resultados = []
    if op == "1":
        cont = input("Continente: ").strip().lower()
        resultados = [p for p in paises if p["continente"].lower() == cont.lower()]
    elif op == "2":
        try:
            min_p = int(input("Población mínima: "))
            max_p = int(input("Población máxima: "))
            if min_p > max_p:
                print("Error: mínimo no puede ser mayor que máximo.")
                return
            resultados = [p for p in paises if min_p <= p["poblacion"] <= max_p]
        except ValueError:
            print("Ingrese números válidos.")
            return
    elif op == "3":
        try:
            min_s = int(input("Superficie mínima: "))
            max_s = int(input("Superficie máxima: "))
            if min_s > max_s:
                print("Error: mínimo no puede ser mayor que máximo.")
                return
            resultados = [p for p in paises if min_s <= p["superficie"] <= max_s]
        except ValueError:
            print("Ingrese números válidos.")
            return

    if resultados:
        print(f"\n{len(resultados)} país(es) encontrado(s):")
        print("-" * 90)
        for p in resultados:
            mostrar_pais(p)
        print("-" * 90)
    else:
        print("No se encontraron países con ese criterio.")


def ordenar_paises(paises):
    print("\n=== ORDENAR PAÍSES ===")
    print("1. Por nombre")
    print("2. Por población")
    print("3. Por superficie")
    criterio = input("Criterio: ").strip()
    clave = {"1": "nombre", "2": "poblacion", "3": "superficie"}.get(criterio)
    if not clave:
        print("Opción inválida.")
        return
    desc = input("¿Orden descendente? (s/n): ").strip().lower() == "s"

    # Trabajamos con copia para no modificar la lista original
    ordenada = sorted(paises, key=lambda x: x[clave], reverse=desc)
    
    orden = "descendente" if desc else "ascendente"
    campo = ["nombre", "población", "superficie"][int(criterio)-1]
    print(f"\nLista ordenada por {campo} ({orden}):")
    print("-" * 90)
    for p in ordenada:
        mostrar_pais(p)
    print("-" * 90)


def mostrar_estadisticas(paises):
    if not paises:
        print("No hay datos.")
        return
    print("\n=== ESTADÍSTICAS ===")
    total = len(paises)
    pob_total = sum(p["poblacion"] for p in paises)
    sup_total = sum(p["superficie"] for p in paises)
    mas_poblado = max(paises, key=lambda x: x["poblacion"])
    menos_poblado = min(paises, key=lambda x: x["poblacion"])

    print(f"Total de países          : {total}")
    print(f"Población promedio       : {pob_total/total:,.0f} habitantes")
    print(f"Superficie promedio      : {sup_total/total:,.0f} km²")
    print(f"País más poblado         : {mas_poblado['nombre']} ({mas_poblado['poblacion']:,} hab.)")
    print(f"País menos poblado       : {menos_poblado['nombre']} ({menos_poblado['poblacion']:,} hab.)")
    print("\nPaíses por continente:")
    conteo = {}
    for p in paises:
        conteo[p["continente"]] = conteo.get(p["continente"], 0) + 1
    for cont, cant in sorted(conteo.items()):
        print(f"   • {cont}: {cant}")


# ==================== MENÚ PRINCIPAL ====================
def menu():
    paises = cargar_paises()
    print(f"Base de datos cargada: {len(paises)} países encontrados.\n")
    
    while True:
        print("="*70)
        print("        GESTIÓN DE PAÍSES - MENÚ PRINCIPAL")
        print("="*70)
        print("1. Agregar país")
        print("2. Actualizar población/superficie")
        print("3. Buscar país")
        print("4. Filtrar países")
        print("5. Ordenar países")
        print("6. Estadísticas")
        print("0. Guardar y salir")
        print("="*70)
        op = input("→ Elija una opción: ").strip()

        if op == "1": agregar_pais(paises)
        elif op == "2": actualizar_pais(paises)
        elif op == "3": buscar_pais(paises)
        elif op == "4": filtrar_paises(paises)
        elif op == "5": ordenar_paises(paises)
        elif op == "6": mostrar_estadisticas(paises)
        elif op == "0":
            guardar_paises(paises)
            print("¡Gracias por usar el sistema! Hasta luego.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()