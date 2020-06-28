#include <SoftwareSerial.h>
#include <DHT.h>
#include <avr/sleep.h>

#define type DHT11
#define dht 12
#define pir 2
#define pi 3
#define motor 5

int water=0;
int count=0;
float hum;
float temp;

DHT dhtSensor(dht, type);

void setup() {
  // put your setup code here, to run once:
  pinMode(pir, INPUT_PULLUP);
  pinMode(pi, INPUT_PULLUP);
  pinMode(motor, OUTPUT);
  
  Serial.begin(9600);
  dhtSensor.begin();
  while(!Serial){
    ;
  }

  delay(2000);
}

void loop() {
  delay(500);
  sleepNow();   /* 절전모드 */
  
  /****온도 측정****/
  temp = dhtSensor.readTemperature();

  if (digitalRead(pi)==LOW) {
    if (isnan(temp) || isnan(hum)) {
      Serial.println("Temp");
      Serial.println("Read Fail");
    } else {
      if (temp > 36 || temp < 0){       /* 온도 범위 지정 */
        Serial.println("Warning T");
        Serial.println(temp);
      }
      Serial.println("Temp");
      Serial.println(temp);
    }

    /****토양 습도 & 물펌프 ****/
    water = analogRead(A3);

    if(water>800) {           /*                */
      if(water>=1000){        /* 습도 기준치 지정 */
        Serial.println("Warning S");
      }
      Serial.println("Soil");
      digitalWrite(motor,HIGH);
      Serial.println(water);
      delay(3000);
      digitalWrite(motor,LOW);
    } else {
      Serial.println("Soil");
      Serial.println(water);
      digitalWrite(motor,LOW);
    }
  }
  
  
  /****움직임 감지 & 전송****/
  if(digitalRead(pir)==HIGH){
    Serial.println("Motion");
    delay(5000);
  }
  
  delay(3000);
  count++;
}

void wakeUp() {
  
}
void sleepNow() {
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  attachInterrupt(0, wakeUp, RISING);
  attachInterrupt(1, wakeUp, FALLING);
  sleep_cpu();
  sleep_disable();
}
