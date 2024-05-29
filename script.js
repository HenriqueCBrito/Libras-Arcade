const { SerialPort } = require('serialport');
const arduino = new SerialPort({path: 'COM4', baudRate: 9600});

