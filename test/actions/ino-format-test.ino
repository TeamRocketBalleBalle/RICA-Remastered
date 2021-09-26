#define touchPin T0
#define lower_bound 10
#define upper_bound 60
#define ledPin 2

int threshold = 50;
bool touch = false;
int touch_val = 0;

void toggleTouch() { int val = touchRead(touchPin);
  if (val <= 50) {touch = true;}
  else {touch = false;}
  touch_val = val;
}

void setup() {
  // put your setup code here, to run once:
	                  pinMode(ledPin, OUTPUT); // abc
  touchAttachInterrupt(touchPin, toggleTouch, 80); //cde
}

void loop() {
  if (touch) {
  digitalWrite(ledPin, HIGH);
  } 
  else 
  {
    digitalWrite(ledPin, LOW);
  }
}
