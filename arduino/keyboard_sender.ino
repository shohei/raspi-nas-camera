#include "Keyboard.h"

#define Button1 9
#define LEDpin 2

int state = HIGH;

void setup() {
  Keyboard.begin();
  pinMode(Button1, INPUT_PULLUP);
  pinMode(LEDpin,OUTPUT);
  digitalWrite(LEDpin,state);
}

void loop() {
  if(digitalRead(Button1) == LOW){  
    Keyboard.press('a');
    state = !state;
    digitalWrite(LEDpin,state);    
    delay(100);
    Keyboard.releaseAll();

    while(digitalRead(Button1) == LOW);
  }
  delay(100);
}

