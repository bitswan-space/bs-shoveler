import asab
import bspump
import logging
import bspump.kafka
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

        if (
            "pipeline:ShovelerPipeline:KafkaSource" in asab.Config
            and "pipeline:ShovelerPipeline:ElasticSearchSink" in asab.Config
        ):
            pipeline = [
                bspump.kafka.KafkaSource(
                    app,
                    self,
                    "KafkaConnection",
                    id="KafkaSource",
                ),
                bspump.common.BytesToStringParser(app, self),
                bspump.common.StdJsonToDictParser(app, self),
                bspump.elasticsearch.ElasticSearchSink(
                    app, self, "ElasticSearchConnection"
                ),
            ]

        elif (
            "pipeline:ShovelerPipeline:ElasticSearchSource" in asab.Config
            and "pipeline:ShovelerPipeline:KafkaSink" in asab.Config
        ):
            pipeline = [
                bspump.elasticsearch.ElasticSearchSource(
                    app,
                    self,
                    "ElasticSearchConnection",
                    id="ElasticSearchSource",
                ),
                bspump.common.StdDictToJsonParser(app, self),
                bspump.common.StringToBytesParser(app, self),
                bspump.kafka.KafkaSink(
                    app,
                    self,
                    "KafkaConnection",
                    id="KafkaSink",
                ),
            ]

        elif (
            "pipeline:ShovelerPipeline:KafkaSource" in asab.Config
            and "connection:InfluxConnection" in asab.Config
        ):
            pipeline = [
                bspump.kafka.KafkaSource(
                    app,
                    self,
                    "KafkaConnection",
                    id="KafkaSource",
                ),
                bspump.common.BytesToStringParser(app, self),
                bspump.common.StdJsonToDictParser(app, self),
                bspump.common.PPrintProcessor(app, self),
                InfluxStringConvertProcessor(app, self),
                bspump.common.StringToBytesParser(app, self),
                bspump.influxdb.InfluxDBSink(app, self, "InfluxConnection"),
            ]

        elif (
            "connection:KafkaConnectionSource" in asab.Config
            and "pipeline:ShovelerPipeline:KafkaSource" in asab.Config
            and "pipeline:ShovelerPipeline:KafkaSink" in asab.Config
            and "connection:KafkaConnection" in asab.Config
        ):
            pipeline = [
                bspump.kafka.KafkaSource(
                    app,
                    self,
                    "KafkaConnectionSource",
                    id="KafkaSource",
                ),
                bspump.common.BytesToStringParser(app, self),
                bspump.common.StringToBytesParser(app, self),
                bspump.kafka.KafkaSink(
                    app,
                    self,
                    "KafkaConnection",
                    id="KafkaSink",
                ),
            ]

        elif (
            "pipeline:ShovelerPipeline:KafkaSource" in asab.Config
            and "pipeline:ShovelerPipeline:KafkaSink" in asab.Config
        ):
            pipeline = [
                bspump.kafka.KafkaSource(
                    app,
                    self,
                    "KafkaConnection",
                    id="KafkaSource",
                ),
                bspump.common.BytesToStringParser(app, self),
                bspump.common.StringToBytesParser(app, self),
                bspump.kafka.KafkaSink(
                    app,
                    self,
                    "KafkaConnection",
                    id="KafkaSink",
                ),
            ]
        else:
            L.error("Please configure the pipeline")

        self.build(*pipeline)
