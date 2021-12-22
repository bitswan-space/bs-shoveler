# BS-Shoveler
When you need events shoveled from one place to another, plain and simple.

## Configuration

### Kafka to ElasticSearch

```
# Connections

[connection:ElasticSearchConnection]
url=<ES URL>

[connection:FastKafkaConnection]
bootstrap_servers=<Kafka bootstrap servers>
group_id=<desired group id (optional)>

# Pipeline

[pipeline:ShovelerPipeline:FastKafkaSource]
topic=<shovel from here>
group_id=<desired id>

[pipeline:ShovelerPipeline:ElasticSearchSink]
index=<shovel to here>

```

### Elasticsearch to Kafka

```
# Connections

[connection:ElasticSearchConnection]
url=<ES URL>

[connection:FastKafkaConnection]
bootstrap_servers=<Kafka bootstrap servers>
group_id=<desired group id (optional)>

# Pipeline

[pipeline:ShovelerPipeline:ElasticSearchSource]
index=<shovel from here>

[pipeline:ShovelerPipeline:FastKafkaSink]
topic=<shovel to here>

```
