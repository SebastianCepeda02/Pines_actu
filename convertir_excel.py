"""
Conversor de Excel/CSV → datos.json para TokensApp
Uso: python convertir_excel.py archivo1.xlsx archivo2.xlsx ...
"""
import sys
import json
import os


def limpiar_serial(val):
    """Convierte 14288846588.0 → '14288846588', respeta strings alfanuméricos."""
    if val is None:
        return ''
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    s = str(val).strip()
    if s.endswith('.0') and s[:-2].lstrip('-').isdigit():
        return s[:-2]
    return s


def leer_archivo(ruta):
    """Lee un Excel o CSV y devuelve un dict {serial: [t1, t2]}."""
    nombre = os.path.basename(ruta).lower()
    registros = {}

    if nombre.endswith('.csv'):
        import csv
        with open(ruta, encoding='utf-8-sig') as f:
            lector = csv.reader(f)
            primera = True
            for fila in lector:
                if primera:
                    primera = False
                    try:
                        float(fila[0])
                    except (ValueError, IndexError):
                        continue
                if len(fila) < 1 or not fila[0].strip():
                    continue
                serial = limpiar_serial(fila[0])
                if not serial:
                    continue
                t1 = fila[1].strip() if len(fila) > 1 else ''
                t2 = fila[2].strip() if len(fila) > 2 else ''
                registros[serial] = [t1, t2]
    else:
        try:
            import openpyxl
        except ImportError:
            print("Instalando openpyxl...")
            os.system(f"{sys.executable} -m pip install openpyxl --quiet")
            import openpyxl
        wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
        ws = wb.active
        primera = True
        for fila in ws.iter_rows(values_only=True):
            if primera:
                primera = False
                if fila[0] is not None and not str(fila[0]).strip().lstrip('-').replace('.', '', 1).isdigit():
                    continue
            if not fila[0]:
                continue
            serial = limpiar_serial(fila[0])
            if not serial:
                continue
            t1 = str(fila[1]).strip() if fila[1] is not None else ''
            t2 = str(fila[2]).strip() if len(fila) > 2 and fila[2] is not None else ''
            registros[serial] = [t1, t2]
        wb.close()

    return registros


def convertir(rutas):
    """Combina todos los archivos en un solo datos.json."""
    if isinstance(rutas, str):
        rutas = [rutas]  # compatibilidad si se llama con un solo string

    registros_combinados = {}
    for ruta in rutas:
        parcial = leer_archivo(ruta)
        duplicados = len(set(parcial) & set(registros_combinados))
        if duplicados:
            print(f"⚠️  {duplicados} seriales duplicados en {os.path.basename(ruta)} (se sobreescribirán)")
        registros_combinados.update(parcial)
        print(f"   {os.path.basename(ruta)}: {len(parcial):,} registros leídos")

    total = len(registros_combinados)
    salida = {
        "v": 1,
        "total": total,
        "d": registros_combinados
    }

    # datos.json se guarda junto al primer archivo
    ruta_salida = os.path.join(os.path.dirname(rutas[0]), 'datos.json')
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, separators=(',', ':'))

    tam = os.path.getsize(ruta_salida) / (1024 * 1024)
    print(f"✅ {total:,} registros totales → datos.json ({tam:.1f} MB)")
    return ruta_salida


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python convertir_excel.py archivo1.xlsx archivo2.xlsx ...")
        print("      python convertir_excel.py archivo1.csv archivo2.xlsx")
        sys.exit(1)

    convertir(sys.argv[1:])