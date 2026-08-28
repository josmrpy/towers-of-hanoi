# Towers of Hanoi

## Sobre este proyecto

Este repositorio contiene una **recreación histórica e incompleta** de un juego de las Torres de Hanoi que hice en 2024 usando [Pygame](https://www.pygame.org/).

La recreación se basa únicamente en lo que se pudo encontrar del proyecto original. Por ese motivo, puede no representar exactamente la versión que existía en 2024 y todavía puede contener errores, decisiones provisionales o partes sin terminar.

El archivo principal es `tows_of_hanoi.py`. La carpeta `old` conserva los archivos `.py` que se encontraron durante la recuperación, para no perder ese material y mantener el contexto de las versiones anteriores.

## Estado actual

La versión recreada permite:

- Elegir entre 1 y 13 discos.
- Mover los discos entre las tres torres con el ratón.
- Contar los movimientos realizados.
- Mostrar el número mínimo de movimientos posible.
- Reiniciar la partida.
- Indicar cuándo se ha resuelto el rompecabezas.

Al tratarse de una recuperación incompleta, el proyecto se conserva principalmente como referencia histórica y no como una versión final o mantenida del juego.

## Estructura

```text
.
├── tows_of_hanoi.py       # Recreación principal
└── old/                   # Archivos encontrados del proyecto anterior
    ├── __towers of hanoi.py
    ├── 2towers of hanoi.py
    └── towers of hanoi.py
```

## Requisitos

- Python 3
- Pygame
- Colorama

Instala las dependencias con:

```bash
pip install pygame colorama
```

## Ejecución

Desde la raíz del repositorio, ejecuta:

```bash
python tows_of_hanoi.py
```

Al iniciar, el programa solicita el número de discos. Si la entrada no es válida, utiliza 5 discos por defecto.

## Nota sobre `old`

Los archivos dentro de `old` se guardan como documentación y respaldo de lo que se pudo recuperar. No es necesario ejecutarlos para usar la recreación principal, y su funcionamiento puede diferir del archivo actual.
