#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const char message[] = "Bem-vindo ao";
const char message2[] = "Libras Arcade!";
int messageLength = sizeof(message) - 1; // Tamanho da mensagem (exclui o terminador nulo)

String currentDisplay = ""; // Variável para armazenar a mensagem atual exibida

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);

  // Exibe a mensagem inicial
  lcd.setCursor(0, 0);
  lcd.print(message);
  lcd.setCursor(0, 1);
  lcd.print(message2);

}

void loop() {
  if (Serial.available()) {
    // Lê a mensagem da porta serial
    String ard = Serial.readStringUntil('\n');

    // Atualiza a variável de controle e o display apenas se a nova mensagem for diferente da atual
    if (ard != currentDisplay) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(ard);
      currentDisplay = ard; // Atualiza a mensagem atual
    }
  }
  
  // Se não houver nova mensagem serial, mantenha a mensagem padrão
  if (currentDisplay == "") {
    lcd.setCursor(0, 0);
    lcd.print(message);
    lcd.setCursor(0, 1);
    lcd.print(message2);
    currentDisplay = String(message) + "\n" + String(message2);
  }
}
