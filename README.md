# BS-Shoveler

When you need events shoveled from one place to another, plain and simple.

# Coniguration options

shoveler pump will decide what to do with the data based on the configuration file.
There are some available options for the configuration file.

## Kafka Source with ElasticSearch sink


### Config example
```
[pipeline:ShovelerPipeline:KafkaSource]
topic=<topic name>
group_id=<group id>

[pipeline:ShovelerPipeline:ElasticSearchSink]
index=<index name>
doctype=<type name> (usually '_doc')

[pipeline:ShovelerPipeline:KafkaConnection]
bootstrap_servers=<kafka server>

[pipeline:ShoevelerPipeline:ElasticSearchConnection]
host=<elasticsearch host>
```

## ElasticSearch Source to Kafka sink

### Config example
```
[pipeline:ShovelerPipeline:ElasticSearchSource]
index=<index name>
doctype=<type name> (usually '_doc')

[pipeline:ShovelerPipeline:KafkaSink]
topic=<topic name>

[pipeline:ShovelerPipeline:KafkaConnection]
bootstrap_servers=<kafka server>

[pipeline:ShoevelerPipeline:ElasticSearchConnection]
host=<elasticsearch host>

```

## Kafka Source to InfluxDB sink

in this case we have to configure a processor responsible for converting the data from dict to the influxdb format.

### Config example
```
[pipeline:ShovelerPipeline:KafkaSource]
topic=<topic name>
group_id=<group id>

[connection:InfluxConnection]
url=<influxdb url>
db=<influxdb database>

[pipeline:ShovelerPipeline:InfluxStringConvertProcessor]
measurement_name=<measurement name>
timestamp_name=<name of timestamp in event>
site_key=<event field that will be used for tag1>
cell_key=<event field that will be used for tag2>
ignore_fields=<fields that should be ignored, so tags and timestamp and maybe additional field that does not have to be in influxDB>
```

## Kafka Source to Kafka sink

### Config example
```
[pipeline:ShovelerPipeline:KafkaSource]
topic=<topic name>
group_id=<group id>

[pipeline:ShovelerPipeline:KafkaSink]
topic=<topic name>

[pipeline:ShovelerPipeline:KafkaConnection]
bootstrap_servers=<kafka server>
```

## Kafka Source to Kafka sink on two different servers

in this case we have configuration for two connections, one for source and one for sink.

### Config example
```
[pipeline:ShovelerPipeline:KafkaSource]
topic=<topic name>

[pipeline:ShovelerPipeline:KafkaSink]
topic=<topic name>

[pipeline:ShovelerPipeline:KafkaConnectionSource]
bootstrap_servers=<kafka server>

[pipeline:ShovelerPipeline:KafkaConnection]
bootstrap_servers=<kafka server>
```
