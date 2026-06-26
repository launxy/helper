# helper

Una herramienta de línea de comandos interactiva para consultar comandos de Linux sin salir de la terminal. Navega por categorías, busca en tiempo real y consulta sintaxis, ejemplos y opciones al instante.

```
 > grep_                          │  grep
──────────────────────            │  [Texto]
 -Texto                           │  Busca patrones en texto
   grep                           │
                                  │  SINTAXIS
                                  │    $ grep [opciones] patrón [archivo]
                                  │
                                  │  EJEMPLOS
                                  │    $ grep 'error' log.txt
                                  │    $ grep -ri 'todo' .
                                  │
                                  │  OPCIONES
                                  │    -i       ignorar mayúsculas
                                  │    -r       recursivo
                                  │    -v       líneas que NO coinciden
                                  │    -n       número de línea
```

---

## Características

- **Búsqueda en tiempo real** — filtra por nombre, descripción, ejemplos u opciones mientras escribes
- **Panel de detalle** — sintaxis completa, ejemplos de uso y todas las opciones disponibles
- **11 categorías** — Navegación, Archivos, Texto, Procesos, Red, Sistema, Compresión, Permisos, Miscelánea, Python, npm
- **60+ comandos** cubiertos
- **Sin dependencias** — solo Python 3 estándar

---

## Instalación

### Requisitos

- Python 3.6 o superior
- Terminal con soporte de colores (cualquier terminal moderna)

### Instalación global (recomendada)

Esto te permite ejecutar `helper` desde cualquier directorio:

```bash
# Clona el repositorio
git clone https://github.com/launxy/helper.git
cd helper

# Mueve al PATH y dale permisos de ejecución
sudo mv helper.py /usr/local/bin/helper
sudo chmod +x /usr/local/bin/helper
```

### Instalación local (sin sudo)

```bash
# Clona el repositorio
git clone https://github.com/launxy/helper.git

# Copia a ~/.local/bin (asegúrate de que esté en tu PATH)
cp helper/helper.py ~/.local/bin/helper
chmod +x ~/.local/bin/helper
```

Si `~/.local/bin` no está en tu PATH, añade esto a tu `~/.bashrc` o `~/.zshrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## Uso

```bash
helper
```

### Controles

| Tecla | Acción |
|-------|--------|
| `↑` `↓` | Navegar por los comandos |
| Escribir | Buscar en tiempo real |
| `ESC` | Limpiar búsqueda |
| `q` | Salir |

---

## Categorías disponibles

| Categoría | Comandos incluidos |
|-----------|-------------------|
| Navegación | `ls`, `cd`, `pwd`, `find`, `locate`, `tree` |
| Archivos | `cp`, `mv`, `rm`, `mkdir`, `touch`, `ln`, `chmod`, `chown` |
| Texto | `cat`, `less`, `grep`, `sed`, `awk`, `sort`, `uniq`, `wc`, `diff`, `head`, `tail` |
| Procesos | `ps`, `top`, `htop`, `kill`, `killall`, `pkill`, `jobs`, `bg`, `fg`, `nohup` |
| Red | `ping`, `curl`, `wget`, `ssh`, `scp`, `rsync`, `ss`, `ip`, `nmap` |
| Sistema | `df`, `du`, `free`, `uname`, `uptime`, `whoami`, `sudo`, `su`, `history`, `systemctl`, `journalctl`, `dmesg`, `lsblk`, `env`, `export`, `shutdown`, `reboot` |
| Compresión | `tar`, `zip`, `unzip`, `gzip` |
| Permisos | `umask`, `passwd`, `useradd`, `usermod` |
| Miscelánea | `echo`, `alias`, `xargs`, `tee`, `cut`, `tr`, `date`, `man`, `which`, `watch` |
| Python | `python`, `python3`, `pip`, `pip3`, `venv`, `pipx`, `pyenv`, `black`, `ruff`, `mypy`, `pytest`, `pydoc`, `ipython`, `jupyter`, `poetry`, `uv` |
| npm | `npm`, `npx`, `node`, `pnpm`, `yarn`, `nvm`, `tsc`, `eslint`, `prettier`, `vite`, `webpack` |
---

## Desinstalación

```bash
sudo rm /usr/local/bin/helper
```
