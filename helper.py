#!/usr/bin/env python3
import curses

COMMANDS = [
    # Navegación
    ("ls",        "Navegación",  "Lista archivos y directorios",                   "ls [opciones] [ruta]",          ["ls -la", "ls -lh /home"],                          ["-l formato largo", "-a mostrar ocultos", "-h tamaño legible", "-R recursivo", "-t ordenar por fecha"]),
    ("cd",        "Navegación",  "Cambia de directorio",                           "cd [ruta]",                     ["cd /home/user", "cd ..", "cd ~", "cd -"],           [".. directorio padre", "~  directorio home", "-  directorio anterior"]),
    ("pwd",       "Navegación",  "Muestra la ruta actual",                         "pwd",                           ["pwd"],                                              []),
    ("find",      "Navegación",  "Busca archivos y directorios",                   "find [ruta] [condiciones]",     ["find . -name '*.txt'", "find . -size +100M"],       ["-name por nombre", "-type f=archivo d=dir", "-mtime modificado hace N días", "-size por tamaño"]),
    ("locate",    "Navegación",  "Busca archivos usando base de datos",            "locate [patrón]",               ["locate nginx.conf", "locate -i readme"],            ["-i ignorar mayúsculas", "-n N limitar resultados"]),
    ("tree",      "Navegación",  "Muestra árbol de directorios",                   "tree [ruta]",                   ["tree", "tree -L 2", "tree -a"],                     ["-L N profundidad máxima", "-a mostrar ocultos", "-d solo directorios"]),
    # Archivos
    ("cp",        "Archivos",    "Copia archivos o directorios",                   "cp [opciones] origen destino",  ["cp archivo.txt /backup/", "cp -r carpeta/ /bkp/"],  ["-r recursivo", "-p preservar permisos", "-i confirmar sobreescritura", "-v verbose"]),
    ("mv",        "Archivos",    "Mueve o renombra archivos",                      "mv [opciones] origen destino",  ["mv viejo.txt nuevo.txt", "mv f.txt /otro/dir/"],    ["-i confirmar sobreescritura", "-v verbose", "-n no sobreescribir"]),
    ("rm",        "Archivos",    "Elimina archivos o directorios",                 "rm [opciones] archivo",         ["rm archivo.txt", "rm -rf carpeta/", "rm -i *.log"], ["-r recursivo", "-f forzar sin confirmar", "-i pedir confirmación", "-v verbose"]),
    ("mkdir",     "Archivos",    "Crea directorios",                               "mkdir [opciones] nombre",       ["mkdir proyecto", "mkdir -p a/b/c"],                 ["-p crear padres si no existen", "-m permisos octal", "-v verbose"]),
    ("touch",     "Archivos",    "Crea archivo vacío o actualiza fecha",           "touch [opciones] archivo",      ["touch nuevo.txt"],                                  ["-t fecha/hora específica", "-a solo actualizar acceso"]),
    ("ln",        "Archivos",    "Crea enlaces simbólicos o duros",                "ln [opciones] origen enlace",   ["ln -s /ruta/real enlace", "ln archivo hardlink"],   ["-s enlace simbólico", "-f forzar sobreescritura"]),
    ("chmod",     "Archivos",    "Cambia permisos de archivos",                    "chmod [modo] archivo",          ["chmod 755 script.sh", "chmod +x archivo"],          ["+x agregar ejecución", "755 rwx r-x r-x", "644 rw- r-- r--"]),
    ("chown",     "Archivos",    "Cambia propietario de archivos",                 "chown usuario:grupo archivo",   ["chown user archivo.txt", "chown -R u:g dir/"],      ["-R recursivo", "-v verbose"]),
    # Texto
    ("cat",       "Texto",       "Muestra contenido de archivos",                  "cat [opciones] archivo",        ["cat archivo.txt", "cat -n archivo.txt"],            ["-n numerar líneas", "-A mostrar caracteres especiales"]),
    ("less",      "Texto",       "Visualiza archivos página por página",           "less archivo",                  ["less log.txt", "less +G log.txt"],                  ["q salir", "/ buscar", "G ir al final", "g ir al inicio"]),
    ("grep",      "Texto",       "Busca patrones en texto",                        "grep [opciones] patrón [arch]", ["grep 'error' log.txt", "grep -ri 'todo' ."],        ["-i ignorar mayúsculas", "-r recursivo", "-v líneas que NO coinciden", "-n número de línea", "-l solo nombres", "-c contar"]),
    ("sed",       "Texto",       "Editor de flujo para transformar texto",         "sed [opciones] 'cmd' archivo",  ["sed 's/viejo/nuevo/g' file", "sed -i 's/a/b/' f"],  ["-i editar en lugar", "s/a/b/g reemplazar todo"]),
    ("awk",       "Texto",       "Procesa y analiza texto estructurado",           "awk 'programa' archivo",        ["awk '{print $1}' file", "awk -F: '{print $1}' f"],  ["-F separador de campos", "$1 campo 1", "$NF último campo", "NR número de línea"]),
    ("sort",      "Texto",       "Ordena líneas de texto",                         "sort [opciones] archivo",       ["sort lista.txt", "sort -rn numeros.txt"],           ["-r orden inverso", "-n orden numérico", "-u eliminar duplicados", "-k N columna N"]),
    ("uniq",      "Texto",       "Filtra líneas duplicadas",                       "uniq [opciones] archivo",       ["sort file | uniq", "sort file | uniq -c"],          ["-c contar ocurrencias", "-d solo duplicados", "-u solo únicos"]),
    ("wc",        "Texto",       "Cuenta palabras, líneas y caracteres",           "wc [opciones] archivo",         ["wc -l archivo.txt", "cat f | wc -w"],               ["-l líneas", "-w palabras", "-c bytes"]),
    ("diff",      "Texto",       "Compara archivos línea por línea",               "diff [opciones] arch1 arch2",   ["diff a.txt b.txt", "diff -u a.txt b.txt"],          ["-u formato unificado", "-r comparar directorios", "-i ignorar mayúsculas"]),
    ("head",      "Texto",       "Muestra las primeras líneas",                    "head [opciones] archivo",       ["head archivo.txt", "head -n 20 log.txt"],           ["-n N mostrar N líneas (def 10)"]),
    ("tail",      "Texto",       "Muestra las últimas líneas",                     "tail [opciones] archivo",       ["tail log.txt", "tail -f /var/log/syslog"],          ["-n N mostrar N líneas", "-f seguir en tiempo real"]),
    # Procesos
    ("ps",        "Procesos",    "Lista procesos en ejecución",                    "ps [opciones]",                 ["ps aux", "ps aux | grep nginx"],                    ["a todos los usuarios", "u formato usuario", "x sin terminal", "-e todos los procesos"]),
    ("top",       "Procesos",    "Monitor interactivo de procesos",                "top",                           ["top", "top -u usuario"],                            ["q salir", "k matar proceso", "M ordenar por memoria", "P ordenar por CPU"]),
    ("htop",      "Procesos",    "Monitor de procesos mejorado con colores",       "htop",                          ["htop", "htop -u usuario"],                          ["F9 matar proceso", "F6 ordenar", "F5 árbol de procesos"]),
    ("kill",      "Procesos",    "Envía señal a un proceso por PID",               "kill [señal] PID",              ["kill 1234", "kill -9 1234"],                        ["-9  SIGKILL forzar", "-15 SIGTERM graceful", "-1  SIGHUP recargar"]),
    ("killall",   "Procesos",    "Mata procesos por nombre",                       "killall [opciones] nombre",     ["killall firefox", "killall -9 proceso"],            ["-9 forzar", "-i confirmar", "-u por usuario"]),
    ("pkill",     "Procesos",    "Mata procesos por nombre o patrón",              "pkill [opciones] patrón",       ["pkill nginx", "pkill -u usuario firefox"],          ["-f buscar en línea completa", "-u por usuario"]),
    ("jobs",      "Procesos",    "Lista trabajos en segundo plano",                "jobs",                          ["jobs", "jobs -l"],                                  ["-l incluir PID"]),
    ("bg",        "Procesos",    "Envía proceso al fondo",                         "bg [job]",                      ["bg", "bg %1"],                                      []),
    ("fg",        "Procesos",    "Trae proceso al frente",                         "fg [job]",                      ["fg", "fg %2"],                                      []),
    ("nohup",     "Procesos",    "Ejecuta comando inmune a hangups",               "nohup comando &",               ["nohup ./script.sh &"],                              []),
    # Red
    ("ping",      "Red",         "Comprueba conectividad con un host",             "ping [opciones] host",          ["ping google.com", "ping -c 4 8.8.8.8"],             ["-c N enviar N paquetes", "-i N intervalo segundos"]),
    ("curl",      "Red",         "Transfiere datos desde/hacia URLs",              "curl [opciones] URL",           ["curl https://example.com", "curl -O https://url/f"],["O guardar original", "-X método HTTP", "-H cabecera", "-d datos POST", "-s silencioso"]),
    ("wget",      "Red",         "Descarga archivos desde la web",                 "wget [opciones] URL",           ["wget https://url/file.zip"],                        ["-O nombre salida", "-r recursivo", "-q silencioso", "-c continuar"]),
    ("ssh",       "Red",         "Conexión segura a servidor remoto",              "ssh [usuario@]host",            ["ssh user@192.168.1.1", "ssh -p 2222 host"],         ["-p puerto", "-i clave privada", "-L túnel local"]),
    ("scp",       "Red",         "Copia archivos entre hosts via SSH",             "scp origen destino",            ["scp f.txt user@host:/ruta/"],                       ["-r recursivo", "-p preservar permisos", "-P puerto"]),
    ("rsync",     "Red",         "Sincroniza archivos local o remotamente",        "rsync [opciones] origen dest",  ["rsync -avz src/ dest/"],                            ["-a modo archivo", "-v verbose", "-z comprimir", "-n dry-run", "--delete borrar en destino"]),
    ("ss",        "Red",         "Muestra sockets (reemplazo moderno de netstat)", "ss [opciones]",                 ["ss -tulpn", "ss -s"],                               ["-t TCP", "-u UDP", "-l escuchando", "-p proceso"]),
    ("ip",        "Red",         "Gestión de interfaces de red y rutas",           "ip [objeto] [comando]",         ["ip addr", "ip route", "ip link show"],              ["addr direcciones IP", "route tabla de rutas", "link interfaces"]),
    ("nmap",      "Red",         "Escáner de puertos y redes",                     "nmap [opciones] objetivo",      ["nmap 192.168.1.0/24", "nmap -sV -p 80,443 host"],   ["-sV detectar versiones", "-p puertos específicos", "-sn solo ping"]),
    # Sistema
    ("df",        "Sistema",     "Muestra uso del espacio en disco",               "df [opciones]",                 ["df -h", "df -h /home"],                             ["-h tamaño legible", "-T tipo de filesystem", "-i mostrar inodos"]),
    ("du",        "Sistema",     "Muestra uso de espacio por directorio",          "du [opciones] [ruta]",          ["du -sh *", "du -h --max-depth=1 /"],                ["-s solo total", "-h tamaño legible", "--max-depth=N profundidad"]),
    ("free",      "Sistema",     "Muestra uso de memoria RAM y swap",              "free [opciones]",               ["free -h", "free -m"],                               ["-h legible", "-m en MB", "-g en GB"]),
    ("uname",     "Sistema",     "Información del SO y kernel",                    "uname [opciones]",              ["uname -a", "uname -r"],                             ["-a toda la info", "-r versión del kernel", "-m arquitectura"]),
    ("uptime",    "Sistema",     "Tiempo que lleva encendido el sistema",          "uptime",                        ["uptime", "uptime -p"],                              ["-p formato legible"]),
    ("whoami",    "Sistema",     "Muestra el usuario actual",                      "whoami",                        ["whoami"],                                           []),
    ("sudo",      "Sistema",     "Ejecuta un comando como superusuario",           "sudo [opciones] comando",       ["sudo apt update", "sudo -i"],                       ["-i shell como root", "-u otro usuario", "-l listar permisos"]),
    ("su",        "Sistema",     "Cambia de usuario",                              "su [usuario]",                  ["su root", "su - usuario"],                          ["- cargar entorno del usuario", "-c ejecutar comando"]),
    ("history",   "Sistema",     "Muestra historial de comandos",                  "history [n]",                   ["history", "history 20", "history | grep git"],      ["-c limpiar historial", "!! repetir último comando"]),
    ("systemctl", "Sistema",     "Gestiona servicios del sistema (systemd)",       "systemctl [acción] [servicio]", ["systemctl start nginx", "systemctl status ssh"],    ["start/stop/restart controlar", "enable/disable autoarranque", "status ver estado"]),
    ("journalctl","Sistema",     "Lee logs del sistema (systemd)",                 "journalctl [opciones]",         ["journalctl -u nginx", "journalctl -f"],             ["-u por servicio", "-f tiempo real", "-n N últimas N líneas"]),
    ("dmesg",     "Sistema",     "Muestra mensajes del kernel",                    "dmesg [opciones]",              ["dmesg", "dmesg -T | tail"],                         ["-T timestamps legibles", "-w tiempo real"]),
    ("lsblk",     "Sistema",     "Lista dispositivos de bloque (discos)",          "lsblk [opciones]",              ["lsblk", "lsblk -f"],                                ["-f mostrar filesystem", "-m mostrar permisos"]),
    ("env",       "Sistema",     "Muestra variables de entorno",                   "env [nombre=valor] [cmd]",      ["env", "env | grep PATH"],                           []),
    ("export",    "Sistema",     "Exporta variables al entorno del shell",         "export VARIABLE=valor",         ["export PATH=$PATH:/nuevo", "export DEBUG=1"],       []),
    # Compresión
    ("tar",       "Compresión",  "Empaqueta y comprime archivos",                  "tar [opciones] archivo.tar",    ["tar -czf bkp.tar.gz dir/", "tar -xzf bkp.tar.gz"], ["-c crear", "-x extraer", "-z gzip", "-j bzip2", "-f archivo tar", "-v verbose", "-t listar"]),
    ("zip",       "Compresión",  "Comprime en formato ZIP",                        "zip [opciones] arch.zip archs", ["zip arch.zip *.txt", "zip -r bkp.zip dir/"],        ["-r recursivo", "-9 máxima compresión"]),
    ("unzip",     "Compresión",  "Extrae archivos ZIP",                            "unzip [opciones] archivo.zip",  ["unzip archivo.zip", "unzip arch.zip -d /dest/"],    ["-d directorio destino", "-l listar contenido"]),
    ("gzip",      "Compresión",  "Comprime archivos con gzip",                     "gzip [opciones] archivo",       ["gzip archivo.txt", "gzip -d archivo.txt.gz"],       ["-d descomprimir", "-k mantener original", "-9 máxima compresión"]),
    # Permisos
    ("umask",     "Permisos",    "Define permisos por defecto de nuevos archivos", "umask [máscara]",               ["umask", "umask 022", "umask 077"],                  []),
    ("passwd",    "Permisos",    "Cambia contraseña de usuario",                   "passwd [usuario]",              ["passwd", "passwd otro_usuario"],                    []),
    ("useradd",   "Permisos",    "Crea un nuevo usuario",                          "useradd [opciones] usuario",    ["useradd -m -s /bin/bash nuevo"],                    ["-m crear home", "-s shell predeterminada", "-G grupos adicionales"]),
    ("usermod",   "Permisos",    "Modifica cuenta de usuario",                     "usermod [opciones] usuario",    ["usermod -aG sudo usuario"],                         ["-aG agregar a grupo", "-s cambiar shell", "-L bloquear cuenta"]),
    # Miscelánea
    ("echo",      "Miscelánea",  "Imprime texto en la terminal",                   "echo [opciones] texto",         ["echo 'Hola mundo'", "echo $PATH"],                  ["-e interpretar \\n \\t", "-n sin salto de línea"]),
    ("alias",     "Miscelánea",  "Crea atajos para comandos",                      "alias nombre='comando'",        ["alias ll='ls -la'", "alias gs='git status'"],       []),
    ("xargs",     "Miscelánea",  "Construye comandos desde stdin",                 "comando | xargs [comando]",     ["find . -name '*.log' | xargs rm"],                  ["-I {} marcador de posición", "-n N args por vez", "-P N paralelo"]),
    ("tee",       "Miscelánea",  "Lee stdin y escribe a stdout y archivos",        "comando | tee archivo",         ["ls | tee lista.txt"],                               ["-a agregar en vez de sobreescribir"]),
    ("cut",       "Miscelánea",  "Extrae secciones de cada línea",                 "cut [opciones] archivo",        ["cut -d: -f1 /etc/passwd", "cut -c1-10 file"],       ["-d delimitador", "-f N campo N", "-c N carácter N"]),
    ("tr",        "Miscelánea",  "Traduce o elimina caracteres",                   "tr [opciones] set1 [set2]",     ["echo 'hello' | tr 'a-z' 'A-Z'"],                   ["-d eliminar caracteres", "-s comprimir repetidos"]),
    ("date",      "Miscelánea",  "Muestra o cambia la fecha y hora",               "date [formato]",                ["date", "date '+%Y-%m-%d'"],                         ["+%Y año", "+%m mes", "+%d día", "+%H hora"]),
    ("man",       "Miscelánea",  "Manual de ayuda para cualquier comando",         "man [sección] comando",         ["man ls", "man 5 passwd"],                           ["-k buscar en manuales"]),
    ("which",     "Miscelánea",  "Muestra la ruta del ejecutable de un comando",   "which comando",                 ["which python3", "which node"],                      ["-a mostrar todas las rutas"]),
    ("watch",     "Miscelánea",  "Ejecuta un comando repetidamente",               "watch [opciones] comando",      ["watch -n 2 df -h", "watch -d ls -la"],              ["-n N intervalo segundos", "-d resaltar cambios"]),
]

CATEGORY_ORDER = ["Navegación","Archivos","Texto","Procesos","Red","Sistema","Compresión","Permisos","Miscelánea"]
CAT_COLORS = {
    "Navegación": 1, "Archivos": 2, "Texto": 3, "Procesos": 4,
    "Red": 5, "Sistema": 6, "Compresión": 7, "Permisos": 8, "Miscelánea": 9,
}

def build_list(query):
    q = query.lower().strip()
    items = []
    for cat in CATEGORY_ORDER:
        cmds = [c for c in COMMANDS if c[1] == cat and (
            not q or q in c[0] or q in c[2].lower()
            or any(q in e for e in c[4]) or any(q in f for f in c[5])
        )]
        if cmds:
            if items:
                items.append(("blank", None))
            items.append(("header", cat))
            for c in cmds:
                items.append(("cmd", c))
    return items

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1,  curses.COLOR_CYAN,    -1)
    curses.init_pair(2,  curses.COLOR_GREEN,   -1)
    curses.init_pair(3,  curses.COLOR_YELLOW,  -1)
    curses.init_pair(4,  curses.COLOR_RED,     -1)
    curses.init_pair(5,  curses.COLOR_MAGENTA, -1)
    curses.init_pair(6,  curses.COLOR_YELLOW,  -1)
    curses.init_pair(7,  curses.COLOR_MAGENTA, -1)
    curses.init_pair(8,  curses.COLOR_CYAN,    -1)
    curses.init_pair(9,  curses.COLOR_WHITE,   -1)
    curses.init_pair(10, curses.COLOR_BLACK,   curses.COLOR_WHITE)
    curses.init_pair(12, curses.COLOR_GREEN,   -1)

    query   = ""
    sel_idx = 0
    scroll  = 0

    while True:
        stdscr.erase()
        H, W = stdscr.getmaxyx()
        LIST_W   = 20
        DETAIL_X = LIST_W + 1

        items      = build_list(query)
        selectables = [i for i, it in enumerate(items) if it[0] == "cmd"]
        if sel_idx >= len(selectables): sel_idx = max(0, len(selectables) - 1)
        sel_item_idx = selectables[sel_idx] if selectables else -1

        # border
        for y in range(H):
            try: stdscr.addch(y, LIST_W, curses.ACS_VLINE, curses.color_pair(9) | curses.A_DIM)
            except: pass

        # search bar
        prompt = " > "
        stdscr.addstr(0, 0, prompt, curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(0, len(prompt), (query + "_")[:LIST_W - len(prompt)], curses.color_pair(2))
        stdscr.addstr(1, 0, "─" * LIST_W, curses.color_pair(9) | curses.A_DIM)

        # auto-scroll
        LIST_START = 2
        LIST_H = H - LIST_START
        if sel_item_idx >= 0:
            vis = sel_item_idx - scroll
            if vis < 0:
                anchor = sel_item_idx
                while anchor > 0 and items[anchor - 1][0] in ("header", "blank"):
                    anchor -= 1
                scroll = anchor
            elif vis >= LIST_H: scroll = sel_item_idx - LIST_H + 1

        # list
        for row_off in range(LIST_H):
            item_i = scroll + row_off
            if item_i >= len(items): break
            kind, data = items[item_i]
            y = LIST_START + row_off
            is_sel = (item_i == sel_item_idx)

            if kind == "blank":
                pass
            elif kind == "header":
                cp = curses.color_pair(CAT_COLORS.get(data, 9)) | curses.A_BOLD
                try: stdscr.addstr(y, 0, f" -{data}"[:LIST_W].ljust(LIST_W), cp)
                except: pass
            else:
                name = data[0]
                cp_cat = curses.color_pair(CAT_COLORS.get(data[1], 9))
                if is_sel:
                    try: stdscr.addstr(y, 0, f"  {name}"[:LIST_W].ljust(LIST_W), curses.color_pair(10) | curses.A_BOLD)
                    except: pass
                else:
                    try:
                        stdscr.addstr(y, 0, "  ", 0)
                        stdscr.addstr(y, 2, f"{name}"[:LIST_W - 2], cp_cat | curses.A_BOLD)
                    except: pass

        # detail panel
        if sel_item_idx >= 0:
            name, cat, desc, syntax, examples, flags = items[sel_item_idx][1]
            cp_cat = curses.color_pair(CAT_COLORS.get(cat, 9))
            dw = W - DETAIL_X - 1

            def dp(y, x, text, attr=curses.A_NORMAL):
                if y >= H or x >= dw: return
                try: stdscr.addstr(y, DETAIL_X + x, text[:dw - x], attr)
                except: pass

            row = 0
            dp(row, 0, name, cp_cat | curses.A_BOLD)
            dp(row, len(name) + 1, f"[{cat}]", cp_cat | curses.A_DIM)
            row += 1
            dp(row, 0, desc, curses.color_pair(9)); row += 2

            dp(row, 0, "SINTAXIS", curses.color_pair(12) | curses.A_BOLD); row += 1
            dp(row, 0, f"  $ {syntax}", curses.color_pair(2)); row += 2

            if examples:
                dp(row, 0, "EJEMPLOS", curses.color_pair(12) | curses.A_BOLD); row += 1
                for ex in examples:
                    dp(row, 0, f"  $ {ex}", curses.color_pair(3)); row += 1
                row += 1

            if flags:
                dp(row, 0, "OPCIONES", curses.color_pair(12) | curses.A_BOLD); row += 1
                for fl in flags:
                    parts = fl.split(" ", 1)
                    dp(row, 0, f"  {parts[0]:<8}", curses.color_pair(2) | curses.A_BOLD)
                    if len(parts) > 1:
                        dp(row, 12, parts[1], curses.color_pair(9) | curses.A_DIM)
                    row += 1
        else:
            msg = "Sin resultados"
            mid = H // 2
            try: stdscr.addstr(mid, DETAIL_X + (W - DETAIL_X - len(msg)) // 2, msg, curses.color_pair(9) | curses.A_DIM)
            except: pass

        # status bar
        bar = " ↑↓ navegar   escribe para buscar   ESC limpiar   q salir "
        try: stdscr.addstr(H - 1, 0, bar.ljust(W)[:W], curses.color_pair(10))
        except: pass

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q') and not query:
            break
        elif key == curses.KEY_UP:
            sel_idx = max(0, sel_idx - 1)
        elif key == curses.KEY_DOWN:
            sel_idx = min(len(selectables) - 1, sel_idx + 1)
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            query = query[:-1]; sel_idx = 0; scroll = 0
        elif key == 27:
            query = ""; sel_idx = 0; scroll = 0
        elif 32 <= key <= 126:
            query += chr(key); sel_idx = 0; scroll = 0

curses.wrapper(main)