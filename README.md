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

# Zookeeper module

[asab:zookeeper]
servers=<server1:port>,<server2:port>,<server3:port>
path=/<path where to advertise>

[asab:docker]
name_prefix=<server im shoveling on>-
socket=/var/run/docker.sock # Needs to be mapped inside of a container
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


# kafka-connection test tmp
#kafkasink
[connection:KafkaConnectionSource]
bootstrap_servers=10.42.131.21:9092,10.42.131.22:9092,10.42.131.23:9092

#kafkasource
[connection:KafkaConnection]
bootstrap_servers=o2sk-kafka-1:9092,o2sk-kafka-2:9092,o2sk-kafka-3:9092

[pipeline:ShovelerPipeline:KafkaSource]
topic=mob-ossr-o2ind
group_id=la-bs-telco-sbr-test

[pipeline:ShovelerPipeline:KafkaSink]
topic=test_B


```

## Motto

> Je kachnam zima na nohy?
> _Vladimira Teskova_
