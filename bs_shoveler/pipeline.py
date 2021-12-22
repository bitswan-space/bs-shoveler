import asab
import bspump
import bspump.common
import bspump.elasticsearch

import fastkafka

import logging

L = logging.getLogger(__name__)


class ShovelerPipeline(bspump.Pipeline):
	def __init__(self, app, pipeline_id):
		super().__init__(app, pipeline_id)

		shovel_rack = {
			"source": {
				"ElasticSearch": bspump.elasticsearch.ElasticSearchSource(
					app,
					self,
					"FastKafkaConnection",
					id="FastKafkaSource",
				),
				"FastKafka": fastkafka.FastKafkaSource(
					app,
					self,
					"FastKafkaConnection",
					id="FastKafkaSource",
				),
			},
			"sink": {
				"ElasticSearch": bspump.elasticsearch.ElasticSearchSink(
					app, self, "ElasticSearchConnection"
				),
				"FastKafka": fastkafka.FastKafkaSink(
					app,
					self,
					"FastKafkaConnection",
					id="FastKafkaSink",
				),
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
			"pipeline:ShovelerPipeline:ElasticSearchSink"
			in asab.Config
			and "pipeline:ShovelerPipeline:FastKafkaSource"
			in asab.Config
		):
			pipeline = [
				shovel_rack.get("source").get("FastKafka"),
				shovel_rack.get("utility").get(
					"BYTEStoSTRING"
				),
				shovel_rack.get("utility").get(
					"JSONtoDICT"
				),
				shovel_rack.get("sink").get(
					"ElasticSearch"
				),
			]

		elif (
			"pipeline:ShovelerPipeline:ElasticSearchSource"
			in asab.Config
			and "pipeline:ShovelerPipeline:FastKafkaSink"
			in asab.Config
		):
			pipeline = [
				shovel_rack.get("source").get(
					"ElasticSearch"
				),
				shovel_rack.get("utility").get(
					"DICTtoJSON"
				),
				shovel_rack.get("utility").get(
					"STRINGtoBYTES"
				),
				shovel_rack.get("sink").get("FastKafka"),
			]

		else:
			L.error("Please configure the pipeline")

		self.build(*pipeline)
