#include <Wire.h>
#include <FreqMeasure.h>
#include <LiquidCrystal_I2C.h>
 

// GND - GND
// VCC - 5V
// SDA - ANALOG Pin 4
// SCL - ANALOG pin 5
 
 
double sum = 0;
int count = 0;
 
float f;   // Frequenz
float v;   // Geschwindigkeit
 
 
// ========================
// ======== SETUP =========
// ========================
 
void setup()
   {
    Serial.begin(57600);
    
    lcd.init();                      // initialize the lcd
 
    // Print a message to the LCD.
    lcd.backlight();
    
    lcd.setCursor(0,0);
    lcd.print("Dopplerradar");
    lcd.setCursor(0,1);
    lcd.print("Version 1.0");
    
    delay(4000);
    
    lcd.setCursor(0,0);
    lcd.print("             ");
    lcd.setCursor(0,1);
    lcd.print("             ");  
    
    lcd.setCursor(0,0);
    lcd.print("f = ");
    lcd.setCursor(0,1);
    lcd.print("v = ");
    
    FreqMeasure.begin();
   }

void loop()
   {
    if (FreqMeasure.available())
       {
        // average the readings together
        sum = sum + FreqMeasure.read();
        
        count = count + 1;
    
        if (count >= 10)
           {
            f = FreqMeasure.countToFrequency(sum / count);
            
            v = f / 19.49;       // conversion from frequency to kilometers per hour
      
            lcd.setCursor(4,0);
            lcd.print("          ");
            lcd.setCursor(4,0);
            lcd.print(f);
            lcd.print(" Hz");
            
            lcd.setCursor(4,1);
            lcd.print("          ");
            lcd.setCursor(4,1);
            lcd.print(v);
            lcd.print(" km/h");
            
            Serial.print("v = ");
            Serial.println(v,1);
            
            delay(50);
                        
            sum = 0;
            count = 0;
           }
       }
   }
