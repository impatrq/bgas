#include <SPI.h>
#include <LoRa.h>

#define NSS 15
#define RST 22
#define DIO0 36

void setup() {
  Serial.begin(115200);
  Serial.println("LoRa Sensor Receiver");

  delay(500);

  LoRa.setPins(NSS, RST, DIO0);

  if (!LoRa.begin(868E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  LoRa.receive();
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // Lee el paquete recibido
    String receivedData = "";
    while (LoRa.available()) {
      receivedData += (char)LoRa.read();
    }

    // Muestra los valores en el puerto serie
    Serial.println("Received data: " + receivedData);
  }
}
