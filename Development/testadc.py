# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep

SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8

# {{{ class TestReadAdc
class TestReadAdc():
    u'''
    試作のため輻輳などの制御は考慮されていないので
    技術的問題解決用等の用途で利用すること
    @Author satoshi-sasaki@comodo-so.co.jp
    '''
    def open(self):
        GPIO.setmode(GPIO.BCM)
        # Pin Number

        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICS, GPIO.OUT)
        GPIO.setup(25, GPIO.OUT)

    def close(self):
        GPIO.cleanup()

    def readSensor(self):
        return self.readAdc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)

    def readAdc(self, adcnum, clockpin, mosipin, misopin, cspin):
        if adcnum > 7 or adcnum < 0:
            return -1
        # 通信を開始するには High にしてから Low に戻すことが必要です。
        # 図5.1より、クロックもLOW状態に。
        GPIO.output(cspin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        GPIO.output(cspin, GPIO.LOW)

        commandout = adcnum
        commandout |= 0x18
        commandout <<= 3
        for i in range(5):
            if commandout & 0x80:
                GPIO.output(mosipin, GPIO.HIGH)
            else:
                GPIO.output(mosipin, GPIO.LOW)
            commandout <<= 1
            GPIO.output(clockpin, GPIO.HIGH)
            GPIO.output(clockpin, GPIO.LOW)
        adcout = 0
        for i in range(13):
            GPIO.output(clockpin, GPIO.HIGH)
            GPIO.output(clockpin, GPIO.LOW)
            adcout <<= 1
            if i > 0 and GPIO.input(misopin) == GPIO.HIGH:
                adcout |= 0x1
        GPIO.output(cspin, GPIO.HIGH)
        return adcout

