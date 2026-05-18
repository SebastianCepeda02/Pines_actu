# TokensApp — Guía del Administrador

## Estructura de archivos

```
tokensapp/
├── index.html              ← App principal (no modificar)
├── sw.js                   ← Service Worker offline (no modificar)
├── manifest.json           ← Configuración PWA (no modificar)
├── icon.svg                ← Ícono de la app
├── datos.json              ← ⭐ BASE DE DATOS (tú la generas)
├── convertir_excel.py      ← Script para generar datos.json
└── README.md               ← Esta guía
```

---

## Primera vez: configurar y publicar

### Paso 1 — Generar datos.json desde tu Excel

**Requisito:** Python 3 instalado (https://python.org)

```bash
python convertir_excel.py tu_archivo.xlsx
```

Esto genera `datos.json` en la misma carpeta. El script:
- Detecta automáticamente si la primera fila es encabezado
- Usa columna A = serial, B = token1, C = token2
- Funciona con .xlsx, .xls y .csv

### Paso 2 — Publicar en la web

**Opción A — Netlify (recomendado, más fácil):**
1. Ve a https://netlify.com y crea cuenta gratuita
2. Arrastra la carpeta `tokensapp/` completa al panel de Netlify
3. ✅ Obtienes una URL tipo `https://tu-nombre.netlify.app`

**Opción B — GitHub Pages:**
1. Crea un repositorio en https://github.com
2. Sube todos los archivos (incluyendo datos.json)
3. Ve a Settings → Pages → Source: main branch
4. URL: `https://tu-usuario.github.io/nombre-repo/`

**Opción C — Cloudflare Pages:**
1. Ve a https://pages.cloudflare.com
2. Arrastra la carpeta → despliegue automático

### Paso 3 — Compartir con operarios

Envía la URL por WhatsApp. El operario:
1. Abre el link en Chrome
2. Ve la pantalla "Instalar App" y toca el botón azul
3. Confirma la instalación
4. La app descarga los datos automáticamente (necesita internet esta vez)
5. ✅ Desde ahora puede usarla **sin internet**

---

## Actualizar datos (cuando cambia el Excel)

```bash
# 1. Generar nuevo datos.json
python convertir_excel.py nuevo_archivo.xlsx

# 2. Subir datos.json al mismo sitio (reemplazar el anterior)
#    En Netlify: arrastrar solo el archivo datos.json al panel
#    En GitHub: git add datos.json && git commit -m "actualizar datos" && git push
```

La próxima vez que un operario abra la app con internet, verá un banner:
> "Hay datos nuevos disponibles → [Actualizar]"

Al tocar Actualizar, descarga los nuevos datos en segundo plano.

---

## Comportamiento de la app por escenario

| Situación | Qué hace la app |
|-----------|-----------------|
| Primera apertura (navegador) | Muestra pantalla de instalación |
| Instala la app | Descarga datos automáticamente |
| Abre instalada, con internet | Consulta local + verifica actualizaciones |
| Abre instalada, sin internet | Consulta local, funciona normal |
| Hay datos nuevos en servidor | Muestra banner "Actualizar" |

---

## Formato del Excel

| Columna A | Columna B | Columna C |
|-----------|-----------|-----------|
| Serial    | Token 1   | Token 2   |
| 100000001 | ABC12345  | XYZ98765  |

- La primera fila puede ser encabezado o datos (se detecta automáticamente)
- El serial es la clave de búsqueda (columna A)
- Probado con hasta 200.000 filas sin problemas

---

## Requisitos técnicos

- **Navegador:** Chrome para Android (recomendado), Edge, Firefox
- **iOS:** Safari (instalación manual vía "Agregar a pantalla de inicio")
- **HTTPS:** Requerido para PWA — Netlify/GitHub/Cloudflare lo incluyen gratis
- **Internet:** Solo para instalación inicial y actualizaciones de datos

---

## Tamaño estimado de datos.json

| Registros | Tamaño aprox. |
|-----------|---------------|
| 10.000    | ~1 MB         |
| 50.000    | ~5 MB         |
| 99.000    | ~10 MB        |

La descarga inicial toma 5–30 segundos según la velocidad del celular.
