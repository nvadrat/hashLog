#!/usr/bin/env python3

import os
import sys
import hashlib
import argparse


LOG_FILE = "hashLog.txt"
BLOCK_SIZE = 1024 * 1024


def calcular_hash(ruta):
    """Calcula SHA-256 de un archivo."""
    sha256 = hashlib.sha256()

    with open(ruta, "rb") as archivo:
        while bloque := archivo.read(BLOCK_SIZE):
            sha256.update(bloque)

    return sha256.hexdigest()


def obtener_archivos():
    """Obtiene todos los archivos del directorio actual recursivamente,
    excluyendo el propio script y hashLog.txt.
    """

    archivos = []

    # Ruta absoluta del script actualmente ejecutado
    script_actual = os.path.abspath(sys.argv[0])

    # Ruta absoluta del log
    log_actual = os.path.abspath(LOG_FILE)

    for raiz, directorios, nombres in os.walk("."):

        for nombre in nombres:

            ruta = os.path.normpath(os.path.join(raiz, nombre))
            ruta_absoluta = os.path.abspath(ruta)

            # Excluir el propio script
            if ruta_absoluta == script_actual:
                continue

            # Excluir hashLog.txt
            if ruta_absoluta == log_actual:
                continue

            archivos.append(ruta)

    return archivos


def crear_hash():
    """Genera un nuevo hashLog.txt."""

    archivos = obtener_archivos()

    print(f"Calculando SHA-256 de {len(archivos)} archivos...\n")

    try:
        with open(LOG_FILE, "w", encoding="utf-8") as log:

            for ruta in sorted(archivos):

                try:
                    hash_archivo = calcular_hash(ruta)

                    # Quitamos "./" para mantener el log limpio
                    ruta_log = ruta[2:] if ruta.startswith("./") else ruta

                    log.write(f"{hash_archivo}  {ruta_log}\n")

                    print(f"[OK] {ruta_log}")

                except (PermissionError, OSError) as e:
                    print(f"[ERROR] {ruta}: {e}")

    except OSError as e:
        print(f"[ERROR] No se pudo crear {LOG_FILE}: {e}")
        sys.exit(1)

    print(f"\nHash generado correctamente: {LOG_FILE}")


def leer_log():
    """Lee hashLog.txt y devuelve {ruta: hash}."""

    if not os.path.isfile(LOG_FILE):
        print(f"[ERROR] No existe {LOG_FILE}.")
        print("Ejecuta primero:")
        print(f"    {sys.argv[0]} hash")
        sys.exit(1)

    registros = {}

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as log:

            for numero_linea, linea in enumerate(log, 1):

                linea = linea.strip()

                if not linea:
                    continue

                partes = linea.split(None, 1)

                if len(partes) != 2:
                    print(
                        f"[ADVERTENCIA] Línea {numero_linea} "
                        f"inválida en {LOG_FILE}"
                    )
                    continue

                hash_guardado, ruta = partes

                registros[ruta] = hash_guardado

    except OSError as e:
        print(f"[ERROR] No se pudo leer {LOG_FILE}: {e}")
        sys.exit(1)

    return registros


def verificar_hash():
    """Compara el estado actual con hashLog.txt."""

    registros = leer_log()

    modificados = []
    eliminados = []
    nuevos = []
    correctos = 0

    # Archivos registrados anteriormente
    for ruta, hash_original in registros.items():

        if not os.path.isfile(ruta):
            eliminados.append(ruta)
            continue

        try:
            hash_actual = calcular_hash(ruta)

            if hash_actual != hash_original:
                modificados.append(ruta)
            else:
                correctos += 1

        except (PermissionError, OSError) as e:
            print(f"[ERROR] No se pudo leer {ruta}: {e}")

    # Buscar archivos que no estaban en el log
    archivos_actuales = obtener_archivos()

    for ruta in archivos_actuales:

        ruta_log = ruta[2:] if ruta.startswith("./") else ruta

        if ruta_log not in registros:
            nuevos.append(ruta_log)

    # Resultado
    print("\n" + "=" * 60)
    print("RESULTADO DE VERIFICACIÓN")
    print("=" * 60)

    print(f"\nCorrectos   : {correctos}")
    print(f"Modificados : {len(modificados)}")
    print(f"Eliminados  : {len(eliminados)}")
    print(f"Nuevos      : {len(nuevos)}")

    if modificados:
        print("\n[!] ARCHIVOS MODIFICADOS:")
        for ruta in modificados:
            print(f"    {ruta}")

    if eliminados:
        print("\n[!] ARCHIVOS ELIMINADOS:")
        for ruta in eliminados:
            print(f"    {ruta}")

    if nuevos:
        print("\n[!] ARCHIVOS NUEVOS:")
        for ruta in nuevos:
            print(f"    {ruta}")

    if not modificados and not eliminados and not nuevos:
        print("\n[OK] No se detectaron cambios.")

    print()


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Herramienta de integridad de archivos mediante SHA-256. "
            "Genera y verifica hashLog.txt de forma recursiva."
        ),
        epilog=(
            "Ejemplos:\n"
            "  %(prog)s hash\n"
            "  %(prog)s verify\n"
            "  %(prog)s --help"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "accion",
        choices=["hash", "verify"],
        help=(
            "hash = generar nuevo hashLog.txt | "
            "verify = verificar archivos contra el log"
        )
    )

    args = parser.parse_args()

    if args.accion == "hash":
        crear_hash()

    elif args.accion == "verify":
        verificar_hash()


if __name__ == "__main__":
    main()