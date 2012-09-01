#define RED 5
#define GREEN 6
#define BLUE 3

void setup()  {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  Serial.begin(9600);
} 

void writeRGB(int r, int g, int b) {
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
}

void loop()  { 
  while (Serial.available() > 0) {
    int red = Serial.parseInt();
    int green = Serial.parseInt();
    int blue = Serial.parseInt();
    
    if (Serial.read() == '\n') {
      red = constrain(red, 0, 255);
      green = constrain(green, 0, 255);
      blue = constrain(blue, 0, 255);
      writeRGB(red, green, blue);
    }
  }
}


