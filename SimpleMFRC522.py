# Code by Simon Monk https://github.com/simonmonk/

import MFRC522
try: # Raspberry Pi
    import RPi.GPIO as GPIO
except ImportError: # Other system
    GPIO = None #work in systems with not gpio
import binascii
  
class SimpleMFRC522:

  READER = None
  
  KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
  
  def __init__(self):
    self.READER = MFRC522.MFRC522()

  def trailer_addr(self, sector):
    """
    Returns block address of spec. block in spec. sector.
    """
    return sector * 4 + 3

  def sector(sel, Snum):
      Snum = Snum * 4
      return Snum
      
  def read(self, Bnum, key_a=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
      id, text = self.read_block(Bnum, key_a)
      while not id:
          id, text = self.read_block(Bnum, key_a)
      return id, text
  
  def read_sector(self, Snum, key_a=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):

      num = self.sector(Snum)
      id, text = self.read_no_block(num, key_a)
      while not id:
          id, text = self.read_no_block(num, key_a)
      return id, text

  def read_id(self):
    id = self.read_id_no_block()
    while not id:
      id = self.read_id_no_block()
    return id

  def read_id_no_block(self):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None
      return self.uid_to_num(uid)

  def read_block(self, Bnum, key=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
    (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.MFRC522_SelectTag(uid)
    status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, Bnum, key, uid)
    text_read = ''
    if status == self.READER.MI_OK:
      data = self.READER.MFRC522_Read(Bnum) 
      if data:
        #text_read = ''.binascii.unhexlify(j).decode() for j in data)
        text_read = ''.join(chr(i) for i in data)
    self.READER.MFRC522_StopCrypto1()
    return id, text_read
  
  def read_no_block(self, Snum, key=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
    (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.MFRC522_SelectTag(uid)
    status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, Snum, key, uid)
    data = []
    text_read = ''
    if status == self.READER.MI_OK:
        for block_num in range(Snum, Snum+3):
            block = self.READER.MFRC522_Read(block_num) 
            if block:
              data += block
        if data:
            #text_read = ''.binascii.unhexlify(j).decode() for j in data)
            text_read = ''.join(chr(i) for i in data)
    self.READER.MFRC522_StopCrypto1()
    return id, text_read
    
  def read_trailer(self, Snum, key_a = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
    addr = self.trailer_addr(Snum)
    (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    #print('uno',status)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.MFRC522_SelectTag(uid)
    status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, addr-3, key_a, uid)
    #data = []
    text_read = ''
    #print('dos',status)
    if status == self.READER.MI_OK:
      data = self.READER.MFRC522_Read(addr) 
      #print(addr)
      if data:
        #text_read = ''.binascii.unhexlify(j).decode() for j in data)
        #text_read = ''.join(chr(i) for i in binascii.unhexlify(data).decode())
        text_read = ''.join(chr(i) for i in data)
    self.READER.MFRC522_StopCrypto1()
    return id, text_read
    
  def read_Dump(self, key=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):  
    (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.MFRC522_SelectTag(uid)
    #data = [] ''
    data = self.READER.MFRC522_DumpClassic1K(key, uid)
    self.READER.MFRC522_StopCrypto1()
    return id, data

  def write(self, Bnum, text, key_a=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
      id, text_in = self.write_block(Bnum, text, key_a)
      while not id:
          id, text_in = self.write_block(Bnum, text, key_a)
      return id, text_in

  def write_sector(self, Snum, text, key_a=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]): 
      num = self.sector(Snum)
      id, text_in = self.write_no_block(num, text, key_a)
      while not id:
          id, text_in = self.write_no_block(num, text, key_a)
      return id, text_in

  def write_block(self, Bnum, text, key=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None, None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None, None
      id = self.uid_to_num(uid)
      data2 = ''
      self.READER.MFRC522_SelectTag(uid)
      status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, Bnum, key, uid)
      self.READER.MFRC522_Read(Bnum)
      if status == self.READER.MI_OK:
          #data = bytearray
          #data = bytearray(binascii.hexlify(text.ljust(16).encode()))
          data = bytearray(text.ljust(16).encode('ascii'))
          data2 = text.ljust(16)
          self.READER.MFRC522_Write(Bnum, data[0:16])
      self.READER.MFRC522_StopCrypto1()
      return id, data2

  def write_no_block(self, Snum, text, key=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None, None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None, None
      id = self.uid_to_num(uid)
      data2 = ''
      self.READER.MFRC522_SelectTag(uid)
      status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, Snum, key, uid)
      self.READER.MFRC522_Read(Snum)
      j = 0
      if status == self.READER.MI_OK:
          #data = bytearray()
          if( Snum == 0):
            j = 1
          data = bytearray(text.ljust(len(range(Snum+j, Snum+3)) * 16).encode('ascii'))
          #data = bytearray(text.ljust(len(range(Snum+j, Snum+3)) * 16).encode('hex'))
          #data = bytearray(binascii.hexlify(text.ljust(len(range(Snum+j, Snum+3)) * 16).encode()))
          data2 = text.ljust(len(range(Snum+j, Snum+3)) * 16)
          i = 0
          for block_num in range(Snum+j, Snum+3):
            self.READER.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
            i += 1
      self.READER.MFRC522_StopCrypto1()
      return id, data2

  def write_trailer(self, sector, key_now=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], key_a=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], auth_bits=[0xFF, 0x07, 0x80], 
                  user_data=0x69, key_b=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
    """
    Writes sector trailer of specified sector. Tag and auth must be set - does auth.
    If value is None, value of byte is kept.
    Returns error state.
    """
    addr = self.trailer_addr(sector)
    return self.write_block(addr, key_a[:6] + auth_bits[:3] + (user_data, ) + key_b[:6], key_now)

  def format_card(self, valor=[0x00], key=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
    """
    datos = []
    for x in range(0, 3*16):
      datos.append(valor)
    text_write = ''.join(chr(i) for i in datos)
    """
    for i in range(16):
      data = self.write_sector(i, valor, key)
    return data

  def change_passwords(self, Snum, key_new, key_now=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):

    #for i in range(16):
      addr = self.trailer_addr(Snum)
      text_write = ''
      datos = self.read_block(addr, key_now)
      print(addr)
      print('//', datos[1])
      datos = datos[1][:10] + key_new
      text_write = ''.join(chr(i) for i in datos)
      print(text_write)
      print(datos)
      data = self.write(addr, text_write, key_now) 
      return datos

  def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
          n = n * 256 + uid[i]
      return n

  def num_to_hex(self, num):
    strHex = "0x%0.2X" % num
    return "".join([x if x.lower() in 'abcdef0123456789' else '' for x in strHex])

  def hex_to_weigand(self, hex):
    return None

  def Close_MFRC522(self):
    self.READER.Close_MFRC522()
