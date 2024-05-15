FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  gdal-bin postgresql-16-postgis-3 \
  python3-pip python3-venv \
  && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN /etc/init.d/postgresql start \
  && su postgres -c 'createdb population_statistics' \
  && su postgres -c 'psql -d population_statistics -c "CREATE EXTENSION postgis;"' \
  && su postgres -c 'psql -d population_statistics -c "CREATE EXTENSION postgis_raster;"' \
  && su postgres -c 'psql -d population_statistics -c "ALTER DATABASE population_statistics SET postgis.enable_outdb_rasters TO true;"' \
  && su postgres -c 'psql -d population_statistics -c "ALTER DATABASE population_statistics SET postgis.gdal_enabled_drivers TO "ENABLE_ALL";"'

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD service postgresql start && python -m app
