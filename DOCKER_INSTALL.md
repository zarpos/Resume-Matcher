# Guía de Instalación de Docker para Windows

## Instalación de Docker Desktop

### Método 1: Descargar desde el sitio web
1. Ve a: https://www.docker.com/products/docker-desktop/
2. Descarga Docker Desktop para Windows
3. Ejecuta el instalador (.exe)
4. Reinicia tu computadora cuando se complete

### Método 2: Usando winget (si está disponible)
```cmd
winget install Docker.DockerDesktop
```

### Método 3: Usando Chocolatey (si lo tienes instalado)
```cmd
choco install docker-desktop
```

## Verificar la instalación
```cmd
docker --version
docker-compose --version
```

## Después de instalar Docker
```cmd
# Construir la imagen
docker build -t resume-matcher .

# Ejecutar el proyecto
docker-compose up
```

## Requisitos del sistema para Docker Desktop
- Windows 10/11 (64-bit)
- WSL 2 (se instala automáticamente)
- Virtualización habilitada en BIOS
- Al menos 4GB de RAM
