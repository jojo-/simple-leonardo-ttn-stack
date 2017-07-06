function Decoder(bytes, port) {
  // Decode an uplink message from a buffer
  // (array) of bytes to an object of fields.
  var decoded = {};
  decoded.msg = String.fromCharCode.apply(null,bytes);
  return decoded;
}
