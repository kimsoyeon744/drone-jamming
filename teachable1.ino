#include <Servo.h>

Servo servo;
const int servoPin = 9; // 서보모터 핀
const int piezoPin = 8; // 피에조 스피커 핀

void setup() {
  Serial.begin(9600); // 시리얼 통신 시작
  servo.attach(servoPin); // 서보모터 핀 연결
  pinMode(piezoPin, OUTPUT); // 피에조 스피커 핀 설정
  
}

void loop() {
  byte actionCode;

  if (Serial.available() > 0) { // 시리얼 데이터 수신
    actionCode = Serial.read();
    Serial.println(actionCode);
    switch (actionCode) {
      case 1: // 새 식별
        servo.write(0); // 서보모터 0도
        break;

      case 2: // DJI 드론 식별
        servo.write(90); // 서보모터 90도
        tone(piezoPin, 261); // '도' 음 출력 (C4 = 261Hz)
        delay(500); // 0.5초 동안 소리 유지
        noTone(piezoPin); // 소리 끄기
        break;

      case 3: // S107 프로 드론 식별
        servo.write(180); // 서보모터 180도
        tone(piezoPin, 392); // '솔' 음 출력 (G4 = 392Hz)
        delay(500); // 짧게 소리
        noTone(piezoPin); // 소리 끄기
        break;

      default:
        break;
    }
  }
}
