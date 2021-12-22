import logging
import bspump
import bspump.lookup
import bspump.elasticsearch

import fastkafka

from .pipeline import ShovelerPipeline

L = logging.getLogger(__name__)


class BSShovelerApp(bspump.BSPumpApplication):

	def __init__(self):
		super().__init__()
		self.BSPumpService = self.get_service("bspump.PumpService")

		fast_kafka_connection = fastkafka.FastKafkaConnection(self, "FastKafkaConnection")
		self.BSPumpService.add_connection(fast_kafka_connection)
		es_connection = bspump.elasticsearch.ElasticSearchConnection(self, "ElasticSearchConnection")
		self.BSPumpService.add_connection(es_connection)
		self.BSPumpService.add_pipeline(ShovelerPipeline(self, "ShovelerPipeline"))
