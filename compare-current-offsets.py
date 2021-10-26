from kafka import TopicPartition, KafkaAdminClient
from kafka.errors import KafkaError
import json
import argparse
from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument("--source-broker", type=str)
parser.add_argument("--destination-broker", type=str)
parser.add_argument("--consumer-group", type=str)
args = parser.parse_args()

source_cllient = KafkaAdminClient(
    bootstrap_servers=[args.source_broker],
)

destination_client = KafkaAdminClient(
    bootstrap_servers=[args.destination_broker],
)

source_consumer_group_offset = source_cllient.list_consumer_group_offsets(
    group_id=args.consumer_group
)
destination_consumer_group_offset = destination_client.list_consumer_group_offsets(
    group_id=args.consumer_group
)

offsets = {}
for k, v in source_consumer_group_offset.items():
    offsets[args.consumer_group + ":" + str(k.topic) + str(k.partition)] = {
        "consumer-group": args.consumer_group,
        "topic": k.topic,
        "partition": k.partition,
        "source-offset": v.offset,
        "destination-offset": None,
    }
for k, v in destination_consumer_group_offset.items():
    offsets[args.consumer_group + ":" + str(k.topic) + str(k.partition)][
        "destination-offset"
    ] = v.offset

listofValues = offsets.values()

data = []
for val in listofValues:
    data.append(
        [
            val["consumer-group"],
            val["topic"],
            val["partition"],
            val["source-offset"],
            val["destination-offset"],
            val["source-offset"] == val["destination-offset"],
        ]
    )
print(
    tabulate(
        data,
        headers=[
            "consumer-group",
            "topic",
            "partition",
            "source-current-offset",
            "destination-current-offset",
            "synced",
        ],
    )
)
