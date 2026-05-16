╔════════════════════════════════════════════════════════════════════════════════╗
║                    🔍 NETWORK PORT SCANNER - GUÍA DE USO                         ║
║                         v1.0 - Windows, Linux, macOS                             ║
╚════════════════════════════════════════════════════════════════════════════════╝

REQUISITOS
═════════════════════════════════════════════════════════════════════════════════

- Python 3.6 o superior
- Módulos incluidos en Python (socket, tkinter, threading, json, csv, ipaddress)
- No requiere instalaciones adicionales


ARCHIVOS INCLUIDOS
═════════════════════════════════════════════════════════════════════════════════

1. port_scanner.py    - Módulo principal con toda la lógica de escaneo
2. main.py            - Interfaz de línea de comandos (CLI)
3. gui.py             - Interfaz gráfica multiplataforma
4. README.txt         - Este archivo


FORMA 1: INTERFAZ GRÁFICA (RECOMENDADA PARA PRINCIPIANTES)
═════════════════════════════════════════════════════════════════════════════════

La forma más fácil de usar la herramienta. Funciona en Windows, Linux y macOS.

INICIAR LA INTERFAZ GRÁFICA:
────────────────────────────────────────────────────────────────────────────────

En Windows:
  1. Abre PowerShell o CMD
  2. Navega a la carpeta: cd C:\Users\[tuusuario]\Desktop
  3. Ejecuta: python gui.py

En Linux o macOS:
  1. Abre Terminal
  2. Navega a la carpeta donde están los archivos
  3. Ejecuta: python3 gui.py

USAR LA INTERFAZ GRÁFICA:
────────────────────────────────────────────────────────────────────────────────

1. SELECCIONAR MODO:
   - "Escanear IP Individual": Para escanear una sola máquina
   - "Escanear Red Completa": Para escanear todas las máquinas de una red

2. INGRESAR OBJETIVO:
   - IP Individual: 192.168.1.100
   - Red CIDR: 192.168.1.0/24

3. SELECCIONAR PUERTOS:
   - "Comunes": Los 18 puertos más utilizados (FTP, SSH, HTTP, HTTPS, MySQL, etc.)
   - "Personalizado": Especifica tus propios puertos

4. PUERTOS PERSONALIZADOS:
   - Puertos individuales: 22,80,443,3306
   - Rango: 1-1000
   - Combinado: 22,80,443,1-100

5. OPCIONES AVANZADAS:
   - Timeout: Tiempo de espera para cada conexión (por defecto: 2 segundos)
   - Threads: Número de conexiones paralelas (por defecto: 100)

6. HACER CLIC EN "▶ Iniciar Escaneo"

7. VER RESULTADOS:
   - Los puertos abiertos aparecerán en el área de resultados
   - Haz clic en "💾 Exportar Resultados" para guardar en JSON

ATAJOS DE BOTONES:
   - ⏹ Detener: Cancela el escaneo en progreso
   - 📋 Limpiar: Limpia el área de resultados
   - 💾 Exportar: Guarda los resultados en un archivo


FORMA 2: LÍNEA DE COMANDOS (CLI)
═════════════════════════════════════════════════════════════════════════════════

Para usuarios avanzados que prefieren usar la terminal.

INICIAR LA CLI:

En Windows:
  python main.py [opciones]

En Linux o macOS:
  python3 main.py [opciones]


SINTAXIS GENERAL:
────────────────────────────────────────────────────────────────────────────────

python main.py [-i IP | -n RED] [-p PUERTOS] [-t TIMEOUT] [--threads N] [-e ARCHIVO]


OPCIONES DISPONIBLES:

  -i, --ip IP              Escanear una IP individual
                           Ejemplo: -i 192.168.1.100

  -n, --network RED        Escanear una red completa (CIDR)
                           Ejemplo: -n 192.168.1.0/24

  -p, --ports PUERTOS      Puertos a escanear (default: common)
                           Opciones:
                           - "common"     : Puertos comunes
                           - "22,80,443"  : Puertos específicos
                           - "1-1000"     : Rango de puertos
                           Ejemplo: -p 22,80,443,3306

  -t, --timeout SEGUNDOS   Timeout para conexiones (default: 2.0)
                           Ejemplo: -t 5

  --threads N              Número de threads paralelos (default: 100)
                           Ejemplo: --threads 200

  -e, --export ARCHIVO     Exportar resultados a archivo
                           Ejemplo: -e resultados.json

  -f, --format FORMATO     Formato de exportación (json o csv)
                           Ejemplo: -f csv


EJEMPLOS DE USO CLI:
────────────────────────────────────────────────────────────────────────────────

1. ESCANEAR UNA IP CON PUERTOS COMUNES:
   python main.py -i 192.168.1.100

2. ESCANEAR UNA IP CON PUERTOS ESPECÍFICOS:
   python main.py -i 192.168.1.100 -p 22,80,443,3306

3. ESCANEAR UN RANGO DE PUERTOS:
   python main.py -i 192.168.1.100 -p 1-1000

4. ESCANEAR TODA UNA RED:
   python main.py -n 192.168.1.0/24

5. ESCANEAR Y EXPORTAR RESULTADOS (JSON):
   python main.py -i 192.168.1.100 -e resultados.json

6. ESCANEAR Y EXPORTAR RESULTADOS (CSV):
   python main.py -i 192.168.1.100 -e resultados.csv -f csv

7. ESCANEO MÁS RÁPIDO CON MÁS THREADS:
   python main.py -i 192.168.1.100 --threads 200

8. ESCANEO CON TIMEOUT MÁS LARGO:
   python main.py -n 192.168.1.0/24 -t 5 --threads 150


ENTENDER LOS RESULTADOS
═════════════════════════════════════════════════════════════════════════════════

ESTADOS DE PUERTO:

- OPEN (ABIERTO):  El puerto está accesible y hay un servicio escuchando
- CLOSED (CERRADO): El puerto no está escuchando (firewall activo)
- FILTERED (FILTRADO): No hay respuesta (firewall bloqueando)

SERVICIOS COMUNES:

  21   → FTP          (Transferencia de archivos)
  22   → SSH          (Shell seguro / Terminal remota)
  23   → Telnet       (Terminal remota insegura)
  25   → SMTP         (Correo saliente)
  53   → DNS          (Resolución de nombres)
  80   → HTTP         (Web no encriptado)
  110  → POP3         (Correo entrante)
  143  → IMAP         (Correo entrante avanzado)
  443  → HTTPS        (Web encriptado)
  445  → SMB          (Compartir archivos Windows)
  3306 → MySQL        (Base de datos)
  3389 → RDP          (Escritorio remoto Windows)
  5432 → PostgreSQL   (Base de datos)
  8080 → HTTP-ALT     (Web alternativo)
  9200 → Elasticsearch (Motor de búsqueda)


ARCHIVOS DE EXPORTACIÓN
═════════════════════════════════════════════════════════════════════════════════

Cuando exportas resultados, se crean archivos con el siguiente formato:

JSON:
{
  "ip": "192.168.1.100",
  "port": 22,
  "state": "open",
  "service": "SSH",
  "timestamp": "2026-05-15T14:30:45.123456"
}

CSV:
IP,Puerto,Estado,Servicio,Fecha
192.168.1.100,22,open,SSH,2026-05-15T14:30:45.123456


CONFIGURACIÓN RECOMENDADA
═════════════════════════════════════════════════════════════════════════════════

ESCANEO RÁPIDO (para redes locales):
  - Timeout: 1-2 segundos
  - Threads: 150-200
  - Puertos: common

ESCANEO COMPLETO (para investigación):
  - Timeout: 3-5 segundos
  - Threads: 100
  - Puertos: 1-65535 (LENTO - puede tomar horas)

ESCANEO DE UNA SOLA IP:
  - Timeout: 2-3 segundos
  - Threads: 100-200
  - Puertos: 1-1000 o personalizado


SOLUCIÓN DE PROBLEMAS
═════════════════════════════════════════════════════════════════════════════════

PROBLEMA: "No me muestra todos los puertos abiertos"
SOLUCIÓN: Aumenta el timeout con -t 5

PROBLEMA: "El escaneo es muy lento"
SOLUCIÓN: Aumenta los threads con --threads 200

PROBLEMA: "Error: Red inválida"
SOLUCIÓN: Verifica el formato CIDR: 192.168.1.0/24 (correcto)

PROBLEMA: "ModuleNotFoundError: No module named 'tkinter'"
SOLUCIÓN: 
  - Windows: Reinstala Python y marca la opción "tcl/tk and IDLE"
  - Linux: sudo apt-get install python3-tk
  - macOS: Debería estar incluido

PROBLEMA: "Permiso denegado en Linux"
SOLUCIÓN: Haz el archivo ejecutable:
  chmod +x gui.py main.py port_scanner.py
  ./gui.py

PROBLEMA: "Puerto 80 o 443 aparece como cerrado pero debería estar abierto"
SOLUCIÓN: 
  - El firewall puede estar bloqueando
  - El servicio puede no estar escuchando en 127.0.0.1
  - Intenta con permisos de administrador


CONSIDERACIONES DE SEGURIDAD
═════════════════════════════════════════════════════════════════════════════════

AVISO LEGAL:
This tool is for educational and authorized security testing only. Unauthorized 
access to computer networks is illegal. Always obtain permission before scanning 
networks or systems that you do not own.

CONSEJOS DE SEGURIDAD:
- Solo escanea redes que te pertenecen o tienes permiso para escanear
- Los escaneos pueden ser detectados por sistemas de defensa
- Usa con cuidado en redes de producción
- Respeta la privacidad y la ley


EJEMPLOS RÁPIDOS
═════════════════════════════════════════════════════════════════════════════════

WINDOWS - GUI:
  cd Desktop
  python gui.py

WINDOWS - CLI (Escanear 192.168.1.100):
  python main.py -i 192.168.1.100

LINUX - GUI:
  python3 gui.py

LINUX - CLI (Escanear red 192.168.1.0/24):
  python3 main.py -n 192.168.1.0/24

EXPORTAR A JSON:
  python main.py -i 192.168.1.100 -e resultados.json

EXPORTAR A CSV:
  python main.py -i 192.168.1.100 -e resultados.csv -f csv


INFORMACIÓN ADICIONAL
═════════════════════════════════════════════════════════════════════════════════

PLATAFORMAS SOPORTADAS:
- ✓ Windows 10, 11
- ✓ Linux (Ubuntu, Debian, CentOS, Fedora, etc.)
- ✓ macOS

VERSIÓN: 1.0
ÚLTIMA ACTUALIZACIÓN: Mayo 2026

CONTACTO:
Para reportar bugs o sugerencias, revisa el código fuente.


¡LISTO PARA ESCANEAR!
═════════════════════════════════════════════════════════════════════════════════

Recomendación: Si es tu primera vez, usa la interfaz gráfica (gui.py).
Es más amigable y intuitiva.

¡Disfruta escaneando tu red de forma segura!

═════════════════════════════════════════════════════════════════════════════════
