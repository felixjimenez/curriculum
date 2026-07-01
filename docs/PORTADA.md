# La Portada / Portafolio (felixjimenez.cl)

Documentación de la **portada** de `felixjimenez.cl`: qué es, cómo funciona y —lo
más importante— **cómo agregar un enlace nuevo sin tocar código**.

---

## 1. Qué es

Desde el 2026-07-01, la página principal `https://felixjimenez.cl/` ya **no** es el
currículum: es una **portada-portafolio**, una grilla de tarjetas donde cada tarjeta
lleva a un proyecto (Inglés, Tienda, Imágenes, etc.).

El currículum (el del sistema solar) se movió a **`https://felixjimenez.cl/curriculum`**
y tiene un botón "← Portafolio" arriba a la izquierda para volver.

```
felixjimenez.cl/              → Portada (grilla de tarjetas)   ← página principal
felixjimenez.cl/curriculum/   → Currículum (sistema solar)
felixjimenez.cl/admin/        → Panel de administración
```

---

## 2. La idea clave: la portada se administra sola (data-driven)

Las tarjetas **no** están escritas en el HTML. Cada tarjeta es **una fila en una
tabla de la base de datos** (modelo `Proyecto`). La página solo dibuja, con un bucle,
las filas que estén marcadas como *publicadas*.

**Consecuencia práctica:** para agregar el proyecto 16, 17… **no hay que programar
ni volver a desplegar**. Se agrega una fila desde el panel de administración y la
tarjeta aparece sola.

Es el mismo patrón que ya usa el sistema solar del CV (que lee la tabla `Habilidad`).

---

## 3. Cómo agregar / editar / ocultar un enlace (para Félix, sin programar)

1. Entra a **https://felixjimenez.cl/admin/** e inicia sesión.
2. Haz clic en **"Proyectos (portada)"**.
3. Botón **"Añadir Proyecto (portada)"** (arriba a la derecha).
4. Llena el formulario (ver campos abajo) y pulsa **Guardar**.
5. Listo: recarga `felixjimenez.cl` y la tarjeta ya está ahí.

**Para editar** una tarjeta existente: haz clic sobre su título en la lista, cambia
lo que quieras y guarda.

**Para ocultar** una tarjeta sin borrarla: en la lista, desmarca la casilla
**"Publicado"** de esa fila y pulsa **Guardar** (abajo). Vuelve a marcarla cuando
quieras que reaparezca. *(Ocultar es más seguro que borrar: no pierdes el texto.)*

**Para reordenar** las tarjetas: cambia el número de la columna **"Orden"** en la
lista (menor número = aparece primero) y guarda.

---

## 4. Qué significa cada campo del formulario

| Campo | Para qué sirve | Ejemplo |
|-------|----------------|---------|
| **Título** | El nombre grande de la tarjeta | `Aprende Inglés` |
| **Descripción** | Texto que invita a entrar (2–3 líneas) | `Practica inglés con lecciones interactivas…` |
| **Enlace** | A dónde lleva la tarjeta al hacer clic | `https://ingles.felixjimenez.cl` (externo), `/curriculum` (interno), `mailto:fvjpsg@gmail.com` (correo) |
| **Abrir en pestaña nueva** | Márcalo para enlaces a otros sitios/subdominios; desmárcalo para páginas internas como `/curriculum` | ✅ para externos |
| **Emoji** | El ícono grande de la tarjeta. Un solo emoji | `🇬🇧` `🖥️` `🛒` `📜` `🖼️` `🌐` |
| **Color de acento** | Color (hex) del ícono, la barra de arriba y el botón. Vacío = índigo | `#10b981` (verde), `#ec4899` (rosa) |
| **Oferta / destacado** | Franja amarilla resaltada, opcional | `🎉 Inauguración: 5 lecciones por $3.000 · la 1ª gratis` |
| **Etiqueta** | Pastilla pequeña en la esquina, opcional | `En vivo` · `Nuevo` · `Próximamente` |
| **Publicado** | Si se ve o no la tarjeta | ✅ |
| **Orden** | Posición (menor = primero) | `10`, `20`, `30`… |

> **Truco:** usa saltos de 10 en 10 en *Orden* (10, 20, 30…). Así, si mañana quieres
> meter una tarjeta entre la 10 y la 20, le pones 15 y no tienes que renumerar todo.

---

## 5. Las 6 tarjetas iniciales

| Orden | Título | Enlace | Etiqueta |
|-------|--------|--------|----------|
| 10 | Aprende Inglés | ingles.felixjimenez.cl | — (oferta inauguración) |
| 20 | Aprende a Administrar tu PC | aprende.felixjimenez.cl | — (oferta inauguración) |
| 30 | Tienda | tienda.felixjimenez.cl | En vivo |
| 40 | Mi Currículum | /curriculum | — |
| 50 | Imágenes | fotos.felixjimenez.cl | — |
| 60 | Aplicaciones web a tu medida | adderlyconstrucciones.cl | Caso real |

Estas 6 se crearon con la migración semilla `0011_seed_proyectos` (idempotente: se
pueden editar libremente desde el admin y `migrate` nunca las pisa).

---

## 6. Cómo está hecho por dentro (para el desarrollador / Claude)

**Modelo** — `core/models.py`, clase `Proyecto`:
campos `titulo, descripcion, url, emoji, oferta, badge, acento, externo, publicado, orden`.

**Vista** — `core/views.py`:
```python
def home(request):                                    # /  → portada
    proyectos = Proyecto.objects.filter(publicado=True)
    return render(request, 'core/portada.html', {'proyectos': proyectos})

def curriculum(request):                              # /curriculum → CV (sistema solar)
    ...
```

**URLs** — `core/urls.py`:
```python
path('', views.home, name='home'),
path('curriculum/', views.curriculum, name='curriculum'),
```

**Plantilla** — `core/templates/core/portada.html`: autocontenida (CSS embebido,
paleta índigo/violeta, fuentes Inter/Outfit), grilla responsive
`repeat(auto-fill, minmax(320px, 1fr))`. Dibuja las tarjetas con un `{% for p in proyectos %}`.

**Admin** — `core/admin.py`, `ProyectoAdmin` con `list_editable = ('orden','publicado','badge')`
para editar en la lista sin abrir cada fila.

**Migraciones** — `0010_proyecto` (crea la tabla) + `0011_seed_proyectos` (siembra las 6,
con `get_or_create` para ser idempotente).

---

## 7. Desplegar cambios de CÓDIGO (no hace falta para agregar tarjetas)

Agregar tarjetas se hace desde el admin y **no** requiere desplegar. Solo se despliega
si se cambia el código o la plantilla. Receta completa en
`docs/GUIA_DEPLOY.md` y en `~/claude-config/scripts-referencia.md` (sección 17). Resumen:

```bash
# LOCAL
git add -A && git commit -m "..." && git push origin main && git push github main
# VPS (ssh vps)
cd /srv/felix/curriculum
cp data/db.sqlite3 data/db.sqlite3.bak-$(date +%Y%m%d)   # respaldar BD persistente
git pull origin main
docker build -t curriculum . && docker stop curriculum && docker rm curriculum
docker run -d --name curriculum --restart unless-stopped -p 8001:8000 \
  -v /srv/felix/curriculum/data:/var/data \
  -e DATABASE_URL='sqlite:////var/data/db.sqlite3' -e DEBUG='False' \
  -e SECRET_KEY='<ver .env>' -e VISITAS_TOKEN='<ver contenedor>' \
  -e USE_LOCAL_MEDIA='True' -e MEDIA_ROOT='/var/data/media' curriculum
docker exec curriculum python manage.py migrate
```

> La base de datos vive en el **volumen** `/srv/felix/curriculum/data` (sobrevive a los
> rebuilds). Por eso las tarjetas que agregues desde el admin **no se pierden** cuando
> se despliega código nuevo.
