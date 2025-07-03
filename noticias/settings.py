# Scrapy settings for noticias project

BOT_NAME = "noticias"

SPIDER_MODULES = ["noticias.spiders"]
NEWSPIDER_MODULE = "noticias.spiders"

# Identifica tu bot (mejor para rastreo responsable)
USER_AGENT = 'NoticiasScraperBot/1.0 (+https://tusitio.com)'

# Obedece el archivo robots.txt
ROBOTSTXT_OBEY = True

# Control de velocidad y rendimiento
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
AUTOTHROTTLE_ENABLED = True

# Codificación por defecto para feeds/exportaciones
FEED_EXPORT_ENCODING = "utf-8"

# Configuración de pipelines (actualizada)
ITEM_PIPELINES = {
    'noticias.pipelines.NormalizeTextPipeline':    300,
    'noticias.pipelines.SentimentPipeline':        350,
    'noticias.pipelines.SQLiteStorePipeline':      400,
    'noticias.pipelines.CSVStorePipeline':         500,
}

# Puedes sobreescribir rutas de salida con estas dos opciones (opcionales)
# SQLITE_DB_PATH = "datos/noticias.db"
# CSV_FILE_PATH = "datos/noticias.csv"
