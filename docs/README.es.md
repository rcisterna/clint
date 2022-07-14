<p align="center">
    <a href="README.md">English</a> - Español
</p>

# CLint: Conventional commits linter

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`CLint` es una herramienta de línea de commandos, que permite validar de distintas formas los mensajes asociados a
commits de git, de tal forma que sean compatibles con
la [especificación de Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#specification).

## Tecnologías

- [Python](https://www.python.org/) 3.7.2+
- [Poetry](https://python-poetry.org/)

## Instalación

Por ahora, la única forma de instalar `CLint` es a través de `pip` (o de herramientas como `poetry` y `pipenv`, que
utilizan `pip` por detrás), pero estamos trabajando para que `CLint` esté disponible a través de gestores de paquetes,
como `homebrew`, `chocolatey` y otros.

```sh
# Instalar con pip
$ pip install clint-cli

# Instalar con poetry
$ poetry add clint-cli

# Instalar con pipenv
$ pipenv install clint-cli
```

## Características principales

- Valida un mensaje en la línea de comandos.
- Permitir funcionar como manejador del hook `commit-msg` de git.
- Valida un mensaje en la línea de comandos a través de pipes.

## Características planificadas

- Hacer compatible con [pre-commit](https://pre-commit.com/).
- Permite construir un mensaje de commit a través de preguntas en la línea de comandos.

## Ejemplos de uso

```sh
# Valida un mensaje particular
$ clint "feat(scope): validate this message"
Your commit message is CC compliant!
```

```sh
# Valida desde archivo
$ echo "feat(scope): validate this message" > commit_message.txt
$ clint --file commit_message.txt
Your commit message is CC compliant!
```

```sh
# Valida a través de pipes
$ cat commit_message.txt | clint
Your commit message is CC compliant!
```

```sh
# Error por tipo incorrecto (en este caso, un error al escribir)
$ echo "feta(scope): validate this message" | clint
type_valid: Type 'feta' is not valid.
```

```sh
# Habilitar hook de git en /path/to/repo
$ clint --enable-hook
Enable hook: Hook enabled at /path/to/repo/.git/hooks/commit-msg
```

```sh
# Deshabilitar hook de git en /path/to/repo
$ clint --disable-hook
Disable hook: Hook disabled at /path/to/repo/.git/hooks/commit-msg
```

## Registro de cambios

Puedes ver el historial de cambios en el [changelog](../CHANGELOG.md) del proyecto.

## Estado del proyecto

`CLint` está actualmente en estado **beta**, y está bajo desarrollo activo. El objetivo es alcanzar al menos
las [características planificadas](#caractersticas-planificadas), para luego continuar manteniendo el código compatible
con futuras versiones de Python y de las bibliotecas que utiliza.

## Inspiración

`CLint` intenta lograr ser lo que ya son otras herramientas similares, como el
excelente [commitlint](https://github.com/conventional-changelog/commitlint). La diferencia
con [herramientas similares](https://www.conventionalcommits.org/en/about/#tooling-for-conventional-commits),
es que ellas están basadas sobre `Node.js`, y por tanto están orientadas a desarrolladores `Javascript`. Si no es tu
caso, te verás obligado a instalar `Node.js` sólo para utilizar esas herramientas.

## Licencia

`CLint` se distribuye bajo la [licencia GPL v3](../COPYING).
