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
		self.BSPumpService = self.get_service(
			"bspump.PumpService"
		)

		kafka_connection = (
			bspump.kafka.KafkaConnection(
				self, "FastKafkaConnection"
			)
		)
		self.BSPumpService.add_connection(
			kafka_connection
		)

		if "connection:ElasticSearchConnection" in asab.Config:
			es_connection = (
				bspump.elasticsearch.ElasticSearchConnection(
					self, "ElasticSearchConnection"
				)
			)
			self.BSPumpService.add_connection(es_connection)

		elif "connection:InfluxConnection" in asab.Config:
			influxdb_connection = (
				bspump.influxdb.InfluxDBConnection(
					self, "InfluxConnection"
				)
			)
			self.BSPumpService.add_connection(influxdb_connection)

		else:
			L.error("Please add connection(s)")

		self.BSPumpService.add_pipeline(
			ShovelerPipeline(self, "ShovelerPipeline")
		)

		self.add_module(asab.web.Module)
		self.ASABApiService = asab.api.ApiService(self)
		self.ASABApiService.initialize_web()

		# Initialize ZooKeeper Service
		from asab.zookeeper import Module
		self.add_module(Module)
		self.ZooKeeperService = self.get_service("asab.ZooKeeperService")
		self.ASABApiService.initialize_zookeeper(self.ZooKeeperService.DefaultContainer)
