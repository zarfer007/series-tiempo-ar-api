#! coding: utf-8
from __future__ import division

import json
import logging

from django.utils import timezone
from pydatajson import DataJson
from .database_loader import DatabaseLoader
from .indexer import Indexer

from . import strings
from series_tiempo_ar_api.apps.api.models import Dataset, Distribution
from series_tiempo_ar_api.libs.indexing.scraping import get_scraper

logger = logging.getLogger(__name__)


def index_catalog(catalog, catalog_id, task, read_local=False, async=True, whitelist=False):
    """Ejecuta el pipeline de lectura, guardado e indexado de datos
    y metadatos sobre el catálogo especificado

    Args:
        catalog (DataJson): DataJson del catálogo a parsear
        catalog_id (str): ID único del catálogo a parsear
        read_local (bool): Lee las rutas a archivos fuente como archivo
        local o como URL. Default False
        task (ReadDataJsonTask): Task a loggear acciones
        async (bool): Hacer las tareas de indexación asincrónicamente. Default True
        whitelist (bool): Marcar los datasets nuevos como indexables por defecto. Default False
    """
    logger.info(strings.PIPELINE_START, catalog_id)
    scraper = get_scraper(read_local)
    scraper.run(catalog)
    distributions = scraper.distributions

    loader = DatabaseLoader(read_local, default_whitelist=whitelist)
    loader.run(catalog, catalog_id, distributions)

    # Indexo todos los datasets whitelisteados, independientemente de cuales fueron
    # scrapeados / cargados
    datasets = Dataset.objects.filter(catalog__identifier=catalog_id,
                                      present=True,
                                      indexable=True)
    distribution_models = Distribution.objects.filter(dataset__in=datasets, indexable=True)
    Indexer(async=async).run(distribution_models)

    stats = loader.get_stats()
    task_stats = json.loads(task.stats)
    task_stats[catalog_id] = stats
    task.stats = json.dumps(task_stats)

    if async and not distribution_models:  # No hay nada para indexar, marco como finalizado
        task.finished = timezone.now()
        task.status = task.FINISHED
        task.generate_email()

    task.save()
