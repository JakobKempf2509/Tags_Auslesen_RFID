#Dieses Programm dient zum lesen und schreiben von Informationen via RFID
#mit diesem ersten Programmteil, wird die lese Funktion realisiert
#J. Kempf 2020-04-17

#bestehende Biblitothek runterladen und einbinden
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py
sudo python setup.py install

#Bilbliotheken importieren
import RPI.GPIO as GPIO
import MFRC522
import signal

#Variablen und Texte
continue_reading = True
my_message_1 = "Ctrl + C stop the reading process."
my_message_2 = "Welcome to RFID-RC522 data read example"
my_message_3 = "A card was detected"
my_message_4 = "An error occurred during the authentifications process"

#Definitionen 
def my_read(signal , frame):
    global continue_reading 
    print(my_message_1)
    continue_reading = False
    GPIO.cleanup()

#auf Tastatur Interrupt warten
signal.signal(signal.SIGINT , my_read)

#Objekt erzeugen in der zuvor importierten Bibliothek
MIFAREReader = MFRC522.MFRC522()

#Wilkommensnachricht
print(my_message_2 + "\n" + my_message_1)

#Schleife zum ständigen Suchen nach RFID-Chips, falls ein Chip erkannt wird die automatische Erfassung (UID = Unique Identifier)
while continue_reading:
    #Nach Teilnehmern scannen
    (status , TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    #Falls ein Teilnehmer gefunden wird
    if (status == MIFAREReader.MI_OK):
        print(my_message_3)

    #Erfassen der UID
    (status , uid) = MIFAREReader.MFRC522_Anticoll()

    if (status == MIFAREReader.MI_OK):
        #UID anzeigen
        print("The UID of the read card is: %s,%s,%s,%s" % (uid[0] , uid[1] , uid[2] , uid[3])) 

        #so lautet der Standard Key für die Authentifizierung
        standard_key = [0xff , 0xff , 0xff , 0xff , 0xff , 0xff]

        #gescannten Tag wählen
        MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_Authentia , 8 , key , uid)

        #Die Authentifizierung kontrollieren
        if (status == MIFAREReader.MI_OK):
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print(my_message_4)

