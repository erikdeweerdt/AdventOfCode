const fs = require('fs');

const data = fs
  .readFileSync('data/13.txt')
  .toString()
  .split(/\n/)
  .filter((line) => line);
const testData = ['939', '7,13,x,x,59,x,31,19'];

const time = parseInt(data[0]);
const buses = data[1]
  .split(',')
  .filter((bus) => bus !== 'x')
  .map((bus) => parseInt(bus, 10));

const nextDepartures = buses.map((bus) => bus * Math.ceil(time / bus));
const earliestIndex = nextDepartures.reduce((earliest, departure, index) => (nextDepartures[earliest] > departure ? index : earliest), 0);

console.log(time);
console.log(buses);
console.log(nextDepartures);
console.log(earliestIndex);
console.log(buses[earliestIndex] * (nextDepartures[earliestIndex] - time));
