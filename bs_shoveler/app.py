import bspump
import bspump.lookup
import bspump.elasticsearch
import bspump.influxdb
import asab
import asab.api
import asab.zookeeper

import bspump.kafka

import logging

from .pipeline import ShovelerPipeline

L = logging.getLogger(__name__)


class BSShovelerApp(bspump.BSPumpApplication):
    def __init__(self):
        super().__init__()
        self.BSPumpService = self.get_service("bspump.PumpService")

        kafka_connection = bspump.kafka.KafkaConnection(self, "KafkaConnection")
        self.BSPumpService.add_connection(kafka_connection)

        if "connection:KafkaConnectionSource" in asab.Config:
            kafka_connection_source = bspump.kafka.KafkaConnection(
                self, "KafkaConnectionSource"
            )

            self.BSPumpService.add_connection(kafka_connection_source)

        elif "connection:ElasticSearchConnection" in asab.Config:
            es_connection = bspump.elasticsearch.ElasticSearchConnection(
                self, "ElasticSearchConnection"
            )
            self.BSPumpService.add_connection(es_connection)

        elif "connection:InfluxConnection" in asab.Config:
            influxdb_connection = bspump.influxdb.InfluxDBConnection(
                self, "InfluxConnection"
            )
            self.BSPumpService.add_connection(influxdb_connection)

        else:
            L.error("Please add connection(s)")

        self.BSPumpService.add_pipeline(ShovelerPipeline(self, "ShovelerPipeline"))
