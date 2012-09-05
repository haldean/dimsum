/*
 * Scrolling text for the lolshield.
 * by Will Brown <will.h.brown@gmail.com>
 */
 
#include "Charliplexing.h"
#include "Font.h"

String display;
int initial_offset = 14;// + FONT_FULL_WIDTH * 2;
int offset = initial_offset;
int limit = 0;

void WriteCharacter(char c, byte x_offset) {
  int charset_offset;
  if ('0' <= c && c <= '9') {
    charset_offset = ('Z' - 'A' + 1) + c - '0';
  } else if ('A' <= c && c <= 'Z') {
    charset_offset = c - 'A';
  } else return;

  byte y_offset = 1;
  int table_offset = FONT_WIDTH * FONT_HEIGHT * charset_offset;
  for (int b = 0; b < FONT_WIDTH * FONT_HEIGHT; b++) {
    LedSign::Set(
        x_offset + (b % FONT_WIDTH),
        y_offset + (b / FONT_WIDTH),
        FONT[table_offset + b]);
  }
}

void WriteDisplay(byte x_offset) {
  for (int i = 0; i < display.length(); i++) {
    int char_offset = x_offset + i * FONT_FULL_WIDTH;
    if (char_offset > -FONT_FULL_WIDTH && char_offset < 14) {
      WriteCharacter(display.charAt(i), char_offset);
    }
  }
}

void InitWithString(String new_string) {
  display = new_string;
  offset = initial_offset;
  limit = -FONT_FULL_WIDTH * display.length();
}

void setup() {
  Serial.begin(9600);
  LedSign::Init();
  LedSign::Clear();
  InitWithString("TEST");
}

void loop() {
  LedSign::Clear();
  WriteDisplay(--offset);
  if (offset < limit) {
    offset = initial_offset;
  }
  delay(100);
}
