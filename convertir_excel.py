#!/usr/bin/env python3
"""
Conversor de Excel → datos.json para TokensApp
Uso: python convertir_excel.py archivo.xlsx
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
    # si viene como string "14288846588.0" limpiar el .0 final
    if s.endswith('.0') and s[:-2].lstrip('-').isdigit():
        return s[:-2]
    return s

def convertir(ruta_excel):
    nombre = os.path.basename(ruta_excel).lower()

    if nombre.endswith('.csv'):
        import csv
        registros = {}
        with open(ruta_excel, encoding='utf-8-sig') as f:
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

        wb = openpyxl.load_workbook(ruta_excel, read_only=True, data_only=True)
        ws = wb.active
        registros = {}
        primera = True
        for fila in ws.iter_rows(values_only=True):
            if primera:
                primera = False
                if fila[0] is not None and not str(fila[0]).strip().lstrip('-').replace('.','',1).isdigit():
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

    total = len(registros)
    salida = {
        "v": 1,
        "total": total,
        "d": registros
    }

    ruta_salida = os.path.join(os.path.dirname(ruta_excel), 'datos.json')
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, separators=(',', ':'))

    tam = os.path.getsize(ruta_salida) / (1024 * 1024)
    print(f"✅ {total:,} registros exportados → datos.json ({tam:.1f} MB)")
    return ruta_salida

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python convertir_excel.py archivo.xlsx")
        print("      python convertir_excel.py archivo.csv")
        sys.exit(1)
    convertir(sys.argv[1])
