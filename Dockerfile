FROM ubuntu:22.04
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  gdal-bin postgis postgresql-14-postgis-3 python3-pip \
  && rm -rf /var/lib/apt/lists/*

RUN /etc/init.d/postgresql start \
  && su postgres -c 'createdb population_statistics' \
  && su postgres -c 'psql -d population_statistics -c "CREATE EXTENSION postgis;"' \
  && su postgres -c 'psql -d population_statistics -c "CREATE EXTENSION postgis_raster;"' \
  && su postgres -c 'psql -d population_statistics -c "ALTER DATABASE population_statistics SET postgis.enable_outdb_rasters = true;"' \
  && su postgres -c 'psql -d population_statistics -c "ALTER DATABASE population_statistics SET postgis.gdal_enabled_drivers TO "ENABLE_ALL";"'

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY processing ./processing
