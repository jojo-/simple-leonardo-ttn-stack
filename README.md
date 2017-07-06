# Binary beer

A proof of concept to connect a smart beer keg on the Internet of Things using LoraWan.

- `sketch_leonardo_lora` contains the Arduino sketch used to connect the keg to a sensor and sending the data over LoraWan.
- `HX-711_Test` contains an example of how to use the HX-711 library to connect load cells to an Arduino.
- `dashboard` contains a simple dashboard to present the data collected.
- `payload_functions` contains the functions to decode/convert/validate the messages send over LoraWan.