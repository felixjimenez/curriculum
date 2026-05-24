# Logros recientes con Claude Code — versiones para CV en PDF

**Félix Valois Jiménez Parada** — 2026-05-13

Estas dos versiones están pensadas para incluir en CVs en PDF que se envían a LinkedIn, Computrabajo, Indeed, Get on Board, etc.

---

## VERSIÓN CORTA (un solo párrafo, ideal para sección "Perfil profesional" o "Resumen")

> En los últimos meses, con la asistencia de **Claude Code** (IA aplicada al desarrollo de software y la administración de sistemas), he podido ejercer en la práctica funciones que tradicionalmente corresponden a perfiles de **Administrador de Sistemas Linux, Ingeniero DevOps, Desarrollador Backend Python (Django/Flask), Administrador de Redes/DNS e Ingeniero de Visión por Computadora**: desplegué un VPS propio en Hetzner (Debian 13) con Docker, Caddy y HTTPS automático; migré mi DNS a un esquema *self-hosted* con NSD y un secundario en Buddyns delegado desde NIC.cl; puse en producción dos aplicaciones web reales (Django y Flask) bajo mi dominio `felixjimenez.cl`; construí un pipeline completo de IA aplicada a ~3.400 fotografías personales (OpenCV, `face_recognition`/dlib, DBSCAN, Chinese Whispers); e instalé mi propio Gitea para gestionar el código. Esta experiencia me ha permitido recuperar y modernizar mis fundamentos de ingeniería de sistemas en un entorno productivo real, asistido por IA.

---

## VERSIÓN LARGA CON MÉTRICAS (para sección "Proyectos" o "Logros recientes")

### Proyectos personales recientes (2026) — con la ayuda de Claude Code

A continuación se listan trabajos reales realizados en infraestructura, desarrollo web e inteligencia artificial aplicada. Entre paréntesis indico el perfil profesional que tradicionalmente desempeña cada labor.

**Infraestructura y administración de sistemas**

- Levanté un **VPS propio en Hetzner (CPX22, Nuremberg, Debian 13)** desde cero: instalación de Docker, Caddy como reverse-proxy con HTTPS automático vía Let's Encrypt, organización de `/srv/felix` para múltiples servicios y endurecimiento de seguridad con `sudo NOPASSWD` controlado, llaves SSH dedicadas y separación de credenciales por proyecto. *(Administrador de Sistemas Linux / Ingeniero DevOps)*

- Migré mi DNS a un esquema **self-hosted con NSD (autoritativo) y Buddyns como slave secundario gratuito**, delegado directamente desde NIC.cl. Administro la zona `felixjimenez.cl` y sus subdominios (`fotos.`, `manuales.`, `git.`, raíz). Dominio registrado a mi nombre, vigente hasta 2027-06-01. *(Ingeniero de Redes / Administrador DNS)*

- Migré mi PC personal de **Debian 12 a Debian 13 (trixie) sobre disco NVMe**, manteniendo Debian 12 en el disco SATA como red de seguridad (dual boot vía GRUB). Resolví las trampas propias de Python 3.13: PEP 668, `python3.13-venv` separado, `setuptools<81` para `pkg_resources` legado y `face_recognition_models` instalado desde git. *(Administrador de Sistemas Linux)*

- Diseñé un **flujo de sincronización entre dos equipos físicos** (SATA y NVMe) que mantiene configuración, memoria de Claude Code y proyectos consistentes contra un origen único en Gitea, con scripts propios de `push`/`pull` al abrir y cerrar cada sesión. *(Ingeniero DevOps)*

**Desarrollo web en producción**

- Desplegué **este sitio web personal en Django 5.2** (`felixjimenez.cl`), con SQLite, media local servida por Caddy y panel de administración Django. *(Desarrollador Backend Python / Django)*

- Puse en producción una **aplicación Flask para Adderly Construcciones** con base de datos real (3 categorías, 6 proyectos), integración con Cloudinary para imágenes y panel de administración protegido por código de sesión. *(Desarrollador Full-Stack Python)*

- Desarrollé y desplegué una **galería web privada para ~3.400 fotos personales** (`fotos.felixjimenez.cl`), con autenticación de administrador, vista pública sin login y herramientas masivas para clasificar personas en categorías (familia, amigos, conocidos, especiales). *(Desarrollador Full-Stack)*

**Inteligencia Artificial / Visión por Computadora**

- Construí un **pipeline completo de Visión por Computadora aplicado a ~3.400 fotografías personales**:
  - Detección de rostros con **OpenCV Haar Cascades**.
  - Extracción y normalización de caras frontales con **dlib** (`face_recognition`).
  - Agrupación automática por similitud con **scikit-learn (DBSCAN)** y **Chinese Whispers**.
  - División de super-clusters, generación de mosaicos preview 3x3 y renombrado automático por persona y fecha.
  - Estructura del pipeline: `coleccion/` → `pipeline/` → `biblioteca/` → `personas/` → `duplicados/`.

  *(Ingeniero de Visión por Computadora / Data Scientist en IA aplicada)*

**DevOps y documentación**

- Instalé y administro mi propio **Gitea** (`git.felixjimenez.cl`) como reemplazo de GitHub para repositorios privados, con dos equipos físicos sincronizados contra un mismo origen. *(Ingeniero DevOps / SRE)*

- Publiqué un **sitio de documentación técnica** (`manuales.felixjimenez.cl`) con **MkDocs Material**: 13 capítulos progresivos sobre Visión por Computadora aplicada, bitácora de aprendizaje y 4 manuales en PDF, protegido por autenticación básica de Caddy. *(Technical Writer / Documentation Engineer)*

- Gestión de **entornos Python aislados (`venv`) por proyecto** cumpliendo PEP 668 de Debian, con dependencias específicas y reproducibles para Flask, Django, Web2py, OpenCV/dlib y MkDocs, sin contaminar el sistema. *(Desarrollador Python senior)*

---

**Stack técnico ejercitado en el período:**
Python 3.13 · Django 5.2 · Flask 3.x · Web2py · OpenCV · dlib (`face_recognition`) · scikit-learn (DBSCAN) · Chinese Whispers · PostgreSQL · SQLite · Cloudinary · Docker · Caddy · NSD · Gitea · MkDocs Material · Debian 13 (trixie) · Bash / SSH · Git.

---

> *Nota personal:* asistido por Claude Code he podido ejercer en la práctica perfiles para los que individualmente no tendría todas las certificaciones formales, pero cuyo conocimiento de base — fundamentos de sistemas, redes y bases de datos — sí domino tras décadas de experiencia. Esta combinación de fundamentos sólidos con asistencia de IA me permite hoy entregar resultados productivos reales.
