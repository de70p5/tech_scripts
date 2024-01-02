import yaml
from repdandaYamlData import data

dataDirPath=""
rpcServerAddress=""
kafkaApiAddress=""
adminAddress=""
coredumpDirPath=""

listConfContent=[{'redpanda': \
                {'data_directory': {dataDirPath}, 'empty_seed_starts_cluster': True, 'seed_servers': [], \
                    'rpc_server': {'address': {rpcServerAddress}, 'port': 33145}, \
                    'kafka_api': [{'address': {kafkaApiAddress}, 'port': 9092}], \
                    'admin': [{'address': {adminAddress}, 'port': 9644}]}, \
                'rpk': {'enable_usage_stats': True, 'tune_network': True, 'tune_disk_scheduler': True, 'tune_disk_nomerges': True, 'tune_disk_write_cache': True, 'tune_disk_irq': True, 'tune_cpu': True, 'tune_aio_events': True, 'tune_clocksource': True, 'tune_swappiness': True, 'coredump_dir': {coredumpDirPath}, 'tune_ballast_file': True}, \
                'pandaproxy': {},\
                 'schema_registry': {}}]

yaml_output = yaml.dump_all(data, sort_keys=False)

try:
    with open("/etc/redpanda/redpanda.yaml", "w") as file:
        file.write(yaml_output)
except IOError as e:
    print("Error writing to file:", e)