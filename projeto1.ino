#include <SoftwareSerial.h>
SoftwareSerial mySerial(0, 1);

const int buttonPin = 12;  // Pino ao qual o botão está conectado
const int ledPin = 7; 
const int ledPin1 = 2; // Pino ao qual o LED está conectado
int buttonState = 0;       // Variável para armazenar o estado do botão


void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(ledPin1, OUTPUT);// Configura o pino do LED como saída
  pinMode(buttonPin, INPUT);  // Configura o pino do botão como entrada
}

void loop() {
  // Lê o estado do botão
  buttonState = digitalRead(buttonPin);

  // Verifica se o botão foi pressionado
  if (buttonState == HIGH) {
    // Liga o LED
    digitalWrite(ledPin, HIGH);
    Serial.println("ligado");
    delay(500);
  }
}
