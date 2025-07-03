
```markdown
# 📰 Scraper de Noticias Colombianas con Análisis de Sentimiento

Este proyecto automatiza la recolección de titulares de medios colombianos usando **Scrapy**, los almacena en formatos CSV y SQLite, y aplica análisis de sentimiento con **VADER**. Está pensado para ejecutarse cada 6 horas mediante **GitHub Actions**.

---

## 📌 Objetivo

Recolectar y analizar noticias de medios regionales de Colombia para alimentar sistemas de monitoreo, análisis de tendencias o dashboards de comunicación.

---

## 🕸️ Medios cubiertos

- La República (`https://www.larepublica.co/rss`)
- Crónica del Quindío (`https://www.cronicadelquindio.com/rss`)
- El Pilón (`https://www.elpilon.com.co/rss`)
- La Silla Vacía (`https://lasillavacia.com/feed`)
- Eje 21 (`https://www.eje21.com.co/rss2`)

---

## 🧠 Funcionalidades

- Scraping vía feeds RSS
- Limpieza y normalización de datos
- Análisis de sentimiento con VADER (positivo, negativo, neutral)
- Persistencia en:
  - `noticias.csv` (acumulativo, sin duplicados)
  - `noticias.db` (SQLite, clave primaria: URL)
- Automatización cada 6 horas vía GitHub Actions

---

## 📁 Estructura del repositorio

```

noticias\_Scraper/
│
├── noticias/
│   ├── spiders/              # Spider principal: titulares.py
│   ├── pipelines.py          # Limpieza, sentimiento, persistencia
│   └── items.py              # Definición de campos
│
├── tests/                    # Pruebas unitarias (pytest)
│   ├── test\_clean.py
│   ├── test\_sentiment.py
│   └── test\_spider.py
│
├── .github/workflows/
│   └── scraper.yml           # GitHub Actions: ejecuta cada 6h
│
├── requirements.txt          # Dependencias
└── README.md                 # Este archivo

````

---

## ⚙️ Instalación local

```bash
git clone https://github.com/tu-usuario/scraper_noticias.git
cd scraper_noticias
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
````

---

## ▶️ Ejecución manual

```bash
scrapy crawl titulares
```

Los resultados se guardan en `noticias.csv` y `noticias.db`.

---

## ✅ Pruebas

```bash
pytest
```

Incluye validación de limpieza, análisis de sentimiento y comportamiento del spider.

---

## 🔄 Automatización con GitHub Actions

El flujo de trabajo se ejecuta automáticamente cada 6 horas:

* Lint (opcional)
* Test con `pytest`
* Ejecución del spider
* Subida de artefactos (`noticias.csv`, `noticias.db`)

Puedes forzar la ejecución manual desde la pestaña "Actions".

---

## 📦 Requisitos principales

* Python 3.11+
* Scrapy
* vaderSentiment
* pytest

---

## 📬 Contacto

Desarrollado por [José Álvarez](https://www.linkedin.com/in/jose-alvarez-dev/)
Licencia: MIT

```

