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
const buses = data[1].split(',').map((bus) => parseInt(bus, 10));

// part 1
// let bus, departure;
// [bus, departure] = earliestBus(time, buses.filter(bus => !isNaN(bus)));
// console.log(`Bus ${bus} departs at ${departure} => ${bus * (departure - time)}`);

// part 2
// brute forcing this is not an option due to the huge search space size
// a more efficient approach is to solve for bus n and then for bus n + 1 without violating previous constraints
// i.e. since all bus numbers are prime, for bus n:
//  * the step is the product of all previous numbers (prime numbers have no common divisors)
//  * the smallest accepted departure time is the smallest (offsetted) multiple of step divisible by n
function nextMultiple(startValue, target, stepSize, offset) {
  let i = startValue;
  // there _may_ be a better, mathematical way of finding i, but I don't currently see it
  for (; (i + offset) % target !== 0; i += stepSize);
  return i;
}
// strip x'es and sort descending for performance
const filtered = buses.map((bus, index) => [bus, index]).filter((bus) => !isNaN(bus[0]));
filtered.sort((a, b) => b[0] - a[0]);
console.log(filtered);

let stepSize = filtered[0][0];
let departure = stepSize - filtered[0][1];
for (let i = 1; i < filtered.length; ++i) {
  departure = nextMultiple(departure, filtered[i][0], stepSize, filtered[i][1]);
  stepSize *= filtered[i][0];
}
console.log(departure);