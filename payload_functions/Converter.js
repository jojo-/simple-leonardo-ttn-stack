function Converter(decoded, port) {
  // Merge, split or otherwise
  // mutate decoded fields.
  var converted = decoded;
  var str_split = converted.msg.split(";");
  converted.val = parseInt(str_split[2]);
  return converted;
}
