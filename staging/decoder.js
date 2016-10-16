function (bytes) {

  //http://stackoverflow.com/questions/38298412/convert-two-bytes-into-signed-16-bit-integer-in-javascript
  
  bytes2int = function(byteB, byteA) {
    var sign = byteA & (1 << 7);
    var x = (((byteA & 0xFF) << 8) | (byteB & 0xFF));
    if (sign) {
     return 0xFFFF0000 | x;  // fill in most significant bits with 1's
    } else {
      return x;
    }
  }

  return {
   x: bytes2int(bytes[0],bytes[1]), y: bytes2int(bytes[2],bytes[3]),
      z:  bytes2int(bytes[4],bytes[5])
  };

}