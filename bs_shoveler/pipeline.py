import asab
import bspump
import bspump.common
import bspump.influxdb
import bspump.elasticsearch

import bspump.kafka
import logging

L = logging.getLogger(__name__)


class ShovelerPipeline(bspump.Pipeline):
	def __init__(self, app, pipeline_id):
		super().__init__(app, pipeline_id)

		# TODO: need to rethink the rack if there will be a possibility, that one of
		# the connections does not exist. It causes error when connection is not located
		# removing ES and Influx sinks from the rack for the moment.
		shovel_rack = {
			"sink": {
				"Kafka": bspump.kafka.KafkaSink(
					app,
					self,
					"KafkaConnection",
					id="KafkaSink",
				)
			},
			"utility": {
				"JSONtoDICT": bspump.common.StdJsonToDictParser(
					app, self
				),
				"DICTtoJSON": bspump.common.StdDictToJsonParser(
					app, self
				),
				"BYTEStoSTRING": bspump.common.BytesToStringParser(
					app, self
				),
				"STRINGtoBYTES": bspump.common.StringToBytesParser(
					app, self
				),
			},
		}

		if (
			"pipeline:ShovelerPipeline:KafkaSource"
			in asab.Config
			and "pipeline:ShovelerPipeline:ElasticSearchSink"
			in asab.Config
		):
			pipeline = [
				bspump.kafka.KafkaSource(
					app,
					self,
					"KafkaConnection",
					id="KafkaSource",
				),
				shovel_rack.get("utility").get(
					"BYTEStoSTRING"
				),
				shovel_rack.get("utility").get(
					"JSONtoDICT"
				),
				bspump.elasticsearch.ElasticSearchSink(
					app, self, "ElasticSearchConnection"
				),
			]

		elif (
			"pipeline:ShovelerPipeline:ElasticSearchSource"
			in asab.Config
			and "pipeline:ShovelerPipeline:KafkaSink"
			in asab.Config
		):
			pipeline = [
				bspump.elasticsearch.ElasticSearchSource(
					app,
					self,
					"ElasticSearchConnection",
					id="ElasticSearchSource",
				),
				shovel_rack.get("utility").get(
					"DICTtoJSON"
				),
				shovel_rack.get("utility").get(
					"STRINGtoBYTES"
				),
				shovel_rack.get("sink").get("Kafka"),
			]

		elif (
			"pipeline:ShovelerPipeline:KafkaSource"
			in asab.Config
			and "connection:InfluxConnection"
			in asab.Config
		):
			pipeline = [
				bspump.kafka.KafkaSource(
					app,
					self,
					"KafkaConnection",
					id="KafkaSource",
				),
				bspump.influxdb.InfluxDBSink(
					app, self, "InfluxConnection"
				),
			]

		else:
			L.error("Please configure the pipeline")

		self.build(*pipeline)
