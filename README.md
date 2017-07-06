# A simple stack for connecting a Leonardo to The Things Network

A proof of concept to connect a Leonardo with an MTDOT-915 to The Things Network and sending the data to a simple dashboard.

**Description of the directories**

- `sketch_leonardo_lora` contains the Arduino sketch used to connect the Leonardo to a sensor (HX-711) and sending the data over LoraWan.
- `dashboard` contains a simple dashboard to present the data collected.
- `payload_functions` contains the functions to decode/convert/validate the messages send over LoraWan.

## Note

In order to send data from The Things Network to your server, you need to activate either the **Data** or **HTTP** integration in your TTN application.
