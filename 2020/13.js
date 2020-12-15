const fs = require('fs');

const data = fs
  .readFileSync('data/13.txt')
  .toString()
  .split(/\n/)
  .filter((line) => line);
const testData = ['939', '7,13,x,x,59,x,31,19'];

function earliestBus(time, buses) {
  const nextDepartures = buses.map((bus) => bus * Math.ceil(time / bus));
  const earliestIndex = nextDepartures.reduce(
    (earliest, departure, index) => (nextDepartures[earliest] > departure ? index : earliest),
    0
  );
  return [buses[earliestIndex], nextDepartures[earliestIndex]];
}

const time = parseInt(data[0]);
const buses = data[1]
  .split(',')
  .map((bus) => parseInt(bus, 10));

// part 1
let bus, departure;
[bus, departure] = earliestBus(time, buses.filter(bus => !isNaN(bus)));
console.log(`Bus ${bus} departs at ${departure} => ${bus * (departure - time)}`);
