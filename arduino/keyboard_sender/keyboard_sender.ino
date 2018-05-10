#include "Keyboard.h"

#define Button1 9
#define LEDpin 2

int state = HIGH;
int last = 0;
int current = 0;

void setup() {
  Keyboard.begin();
  pinMode(Button1, INPUT_PULLUP);
  pinMode(LEDpin,OUTPUT);
  digitalWrite(LEDpin,state);
}

void loop() {
  current = digitalRead(Button1);
  if(current == LOW){  
    if(last==LOW){
      //ON
      Keyboard.press('a');
      last = HIGH;
      digitalWrite(LEDpin,last);
    } else if(last==HIGH){
      //OFF
      Keyboard.press('b');
      last = LOW;
      state = !state;
      digitalWrite(LEDpin,last);    
    }

    delay(100);
    Keyboard.releaseAll();
    
    while(digitalRead(Button1) == LOW);
  }
  delay(100);
}

