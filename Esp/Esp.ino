#include <SRF05.h>
#include "BluetoothSerial.h"

String device_name = "ESP32-BT-Slave";

// Verifica si Bluetooth está habilitado
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth no está habilitado. Habilítalo desde el menú de configuración.
#endif

// Verifica el Perfil de Puerto Serial
#if !defined(CONFIG_BT_SPP_ENABLED)
#error El Perfil de Puerto Serial (SPP) no está habilitado. Solo disponible para ESP32.
#endif

BluetoothSerial SerialBT;


const int motor1[2] = {12,14};
const int motor2[2] = {13,15};

void setup() {
  pinMode(motor1[0],OUTPUT);
  pinMode(motor1[1],OUTPUT);
  pinMode(motor2[0],OUTPUT);
  pinMode(motor2[1],OUTPUT);
  Serial.begin(115200);
  SerialBT.begin(device_name);  // Nombre del dispositivo Bluetooth
  Serial.printf("El dispositivo con nombre \"%s\" está iniciado.\nAhora puedes emparejarlo con Bluetooth.\n", device_name.c_str());
}

void loop() {

  // Verifica si hay datos entrantes desde Bluetooth
  if (SerialBT.available()) {
    char received = SerialBT.read(); // Lee un carácter desde Bluetooth

    if (received == 'F') {
      avanzar();
    }
    else if (received == 'B'){
      retroceder();
    }
    else if (received == 'R'){
      derecha();
    }
    else if (received == 'L'){
      izquierda();
    }
    if (received == 'S') {
      detener();
    }
  }

  delay(20); // Pequeño retraso para evitar sobrecarga de CPU
}

  void avanzar(){
    motor(motor1, -1);
    motor(motor2, 1);
  }
  void retroceder(){
    motor(motor1, 1);
    motor(motor2, -1);
  }
  void derecha(){
    motor(motor1, -1);
    motor(motor2, -1);
  }
  void izquierda(){
    motor(motor1, 1);
    motor(motor2, 1);
  }
  void detener(){
    motor(motor1, 0);
    motor(motor2, 0);
  }

  double mapDouble(double x, double in_min, double in_max, double out_min, double out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

/**
 * Controla el movimiento de un motor.
 * 
 * @param motor Arreglo con los pines del motor
 * @param velocidad Velocidad del motor (entre -1 y 1)
 */
  void motor(const int motor[2], double velocidad) {
  // Verificar si la velocidad está fuera del rango permitido
  if (velocidad > 1 || velocidad < -1) {
    Serial.println("Error: Velocidad fuera del rango permitido (-1 a 1)");
    while (true); // Detener el programa en un bucle infinito
  }
  
  int v = 0;

  if (velocidad == 0) {
    analogWrite(motor[0], 0);
    analogWrite(motor[1], 0);
  } else if (velocidad > 0.00) {
    v = (int)mapDouble(velocidad, 0, 1, 0, 255);
    analogWrite(motor[0], v);
    analogWrite(motor[1], 0);
  } else if (velocidad < 0.00) {
    v = (int)mapDouble(velocidad, -1, 0, 255, 0);
    analogWrite(motor[0], 0);
    analogWrite(motor[1], v);
  }
}
