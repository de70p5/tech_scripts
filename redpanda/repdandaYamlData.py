data="""node_uuid: 9ce16c28-a92d-11ee-a6e8-000c291b2fec
redpanda:
    data_directory: /var/lib/redpanda/data
    empty_seed_starts_cluster: true
    seed_servers: []
    rpc_server:
        address: 172.16.68.128
        port: 33145
    kafka_api:
        - address: 172.16.68.128
          port: 9092
    admin:
        - address: 172.16.68.128
          port: 9644
rpk:
    enable_usage_stats: true
    tune_network: true
    tune_disk_scheduler: true
    tune_disk_nomerges: true
    tune_disk_write_cache: true
    tune_disk_irq: true
    tune_cpu: true
    tune_aio_events: true
    tune_clocksource: true
    tune_swappiness: true
    coredump_dir: /var/lib/redpanda/coredump
    tune_ballast_file: true
pandaproxy: {}
schema_registry: {}"""