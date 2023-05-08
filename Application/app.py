from rich.console import Console
from rich.table import Table
from rich.layout import Layout

from kafka import KafkaConsumer

import json
import time

console = Console()


def create_table(title):
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Temperature", style="dim", width=12)
    table.add_column("Humidity")

    return table

# Define server with port
bootstrap_servers = ['localhost:29092']

# Define topic name from where the message will recieve
topicName0 = 'measurements0'
topicName1 = 'measurements1'
topicName2 = 'measurements2'

# Initialize consumer variable
consumer0 = KafkaConsumer(topicName0, bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest')
consumer1 = KafkaConsumer(topicName1, bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest')
consumer2 = KafkaConsumer(topicName2, bootstrap_servers=bootstrap_servers)

# Read and print message from consumer
for msg0, msg1, msg2 in zip(consumer0, consumer1, consumer2):
    table0 = create_table('Measurements0')
    table1 = create_table('Measurements1')
    table2 = create_table('Measurements2')

    temperature0 = json.loads(msg0.value)['temperature']
    humidity0 = json.loads(msg0.value)['humidity']
    temperature1 = json.loads(msg1.value)['temperature']
    humidity1 = json.loads(msg1.value)['humidity']
    temperature2 = json.loads(msg2.value)['temperature']
    humidity2 = json.loads(msg2.value)['humidity']

    table0.add_row(str(temperature0), str(humidity0))
    table1.add_row(str(temperature1), str(humidity1))
    table2.add_row(str(temperature2), str(humidity2))

    console.clear()

    console.print('[bold]Temperature and Humidity Measurement', justify='center', height=100)

    console.rule('[bold red] ESP32_0')

    console.print(table0, justify='center')
    console.print()
    console.rule('[bold red] ESP32_1')
    console.print(table1, justify='center')
    console.print()
    console.rule('[bold red] ESP32_2')
    console.print(table2, justify='center')

    time.sleep(1)
