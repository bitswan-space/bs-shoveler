import asab
import bspump
import logging
import fastkafka
import bspump.common
import bspump.influxdb
import bspump.elasticsearch

from .processors.convert_to_influx_string import InfluxStringConvertProcessor


L = logging.getLogger(__name__)


class ShovelerPipeline(bspump.Pipeline):
	def __init__(self, app, pipeline_id):
		super().__init__(app, pipeline_id)

		# TODO: need to rethink the rack if there will be a possibility, that one of
		# the connections does not exist. It causes error when connection is not located
		# removing ES:
		# influx added
		shovel_rack = {
			"sink": {
				"FastKafka": fastkafka.FastKafkaSink(
					app,
					self,
					"FastKafkaConnection",
					id="FastKafkaSink",
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
			"pipeline:ShovelerPipeline:FastKafkaSource"
			in asab.Config
			and "pipeline:ShovelerPipeline:ElasticSearchSink"
			in asab.Config
		):
			pipeline = [
				fastkafka.FastKafkaSource(
					app,
					self,
					"FastKafkaConnection",
					id="FastKafkaSource",
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
			and "pipeline:ShovelerPipeline:FastKafkaSink"
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
				shovel_rack.get("sink").get("FastKafka"),
			]

		elif (
			"pipeline:ShovelerPipeline:FastKafkaSource"
			in asab.Config
			and "connection:InfluxConnection"
			in asab.Config
		):
			pipeline = [
				fastkafka.FastKafkaSource(
					app,
					self,
					"FastKafkaConnection",
					id="FastKafkaSource",
				),
				bspump.common.BytesToStringParser(app, self),
				bspump.common.StdJsonToDictParser(app, self),
				InfluxStringConvertProcessor(app, self),
				bspump.influxdb.InfluxDBSink(
					app, self, "InfluxConnection"
				),
			]

		else:
			L.error("Please configure the pipeline")

		self.build(*pipeline)
