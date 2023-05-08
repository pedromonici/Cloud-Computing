# Temperature and Humidity Measurement - Checkpoint02

## Ideia inicial

A ideia desse trabalho é realizar a medição de temperatura e umidade de três diferentes ambientes com o auxílio de 3 microcontroladores ESP32 e 3 sensores de umidade e temperatura chamado DHT11. Conforme as medições são realizadas, o intuito é realizar o streaming desses dados para o cluster disponível, utilizando o Mosquitto com o protocolo MQTT e depois disso passar esses dados para tópicos do Kafka que serão consumidos pela nossa aplicação.

## Toolchain necessária

- 3 ESP32.
- 3 sensores DHT11.
- [ESP-IDF](https://github.com/espressif/esp-idf): framework desenvolvido pela Espressif que permite escrever aplicações para serem rodadas na ESP32.
- [ESP-MQTT]https://github.com/espressif/esp-mqtt): componente do ESPIDF que permite se comunicar pelo protocolo MQTT.
- [Kafka](https://kafka.apache.org/): necessário para realizar o streaming de dados de maneira otimizada e segura.
- [paho-mqtt](https://pypi.org/project/paho-mqtt/): biblioteca de python que permite se conectar com brokers MQTT.
- [kafka-python](https://pypi.org/project/kafka-python/): biblioteca de python que permite utilizar o Apache Kafka.
- [Docker](https://www.docker.com/).

## Como utilizar esse repositório?

### Na sua máquina

Primeiramente, é necessário instalar o ESP-IDF em sua máquina seguindo esse [tutorial](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/linux-macos-setup.html). Após isso, é necessário instalar o componente ESP-MQTT no diretório do seu ESP-IDF.

Com isso feito, entre no diretõrio *esp-mqtt* onde estã presente a nossa aplicação que irã rodar na ESP32. Rode o comando `idf.py menuconfig` > Example Connection Configuration e coloque os dados do seu WiFi. Depois entre no diretório *esp-mqtt/main* e no arquivo `app_main.c` existe um define BROKER_MQTT que pode receber 3 valores: SSC0158-2023-G2-0 ou SSC0158-2023-G2-1 ou SSC0158-2023-G2-2. Cada ESP-32 deve rodar com o seu respectivo broker.

Depois disso, podemos rodar nossa aplicação na ESP32, para isso rode o comando: `idf.py -p <YOUR-ESP32-PORT> flash monitor`. Finalmente, os dados estão sendo enviados da ESP32 para o cluster por meio do Mosquitto.

### No cluster

Entre em nosso cluster `gcloud02` e rode o comando `docker ps`. É possível notar que existem: 3 servidores de kafka, 3 bridges.py e 2 servidores de zookeeper. Cada ESP32 possui o seu respectivo servidor de kafka e o seu respectivo bridge.py. Existem 2 servidores de zookeeper para manter a redundância da nossa arquitetura, logo, se um servidor de zookeeper cair, a nossa aplicação não cai por completo.

No diretório *bridge* está presente o script escrito em python que recebe os dados da ESP32 pelo Mosquitto, utilizando o protocolo MQTT, e repassa esses dados para o tópico respectivo do Kafka.

No arquivo docker-compose.yml estão presentes as configurações de cada um dos containers do Docker (bridges, brokers do kafka, instâncias do zookeeper).

No diretório *Application* está presente o nosso script escrito em python que roda a nossa aplicação final.

## Como rodar a aplicação?

Primeiramente, entre no cluster e se certifique que as 3 ESP-32 estão ligadas e transmitindo dados. Após isso, entre no diretório *Application* e rode:

`python3 app.py`

E pronto! Vale ressaltar que para esse Checkpoint2 ainda não estamos consumindo os dados dos tópicos do Kafka de fora do cluster, isso porque não tinhamos nossos endpoints abertos ainda, logo, a aplicação ainda deve rodar de dentro do cluster. Iremos trabalhar para que no Checkpoint3 seja possível rodar a aplicação de fora do cluster.
