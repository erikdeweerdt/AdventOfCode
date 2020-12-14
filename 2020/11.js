const fs = require('fs');

const data = fs
  .readFileSync('data/11.txt')
  .toString()
  .split(/\n/)
  .filter((line) => line);
const testData = ['L.LL.LL.LL', 'LLLLLLL.LL', 'L.L.L..L..', 'LLLL.LL.LL', 'L.LL.LL.LL', 'L.LLLLL.LL', '..L.L.....', 'LLLLLLLLLL', 'L.LLLLLL.L', 'L.LLLLL.LL'];

function copySeatMap(seatMap) {
  const copy = [];
  seatMap.forEach((row) => copy.push([...row]));
  return copy;
}

function occupiedNeighbors(seatMap, x, y) {
  let occupied = 0;
  for (let xx = x - 1; xx <= x + 1; ++xx) {
    for (let yy = y - 1; yy <= y + 1; ++yy) {
      if ((xx === x && yy === y) || xx < 0 || yy < 0 || xx >= seatMap[y].length || yy >= seatMap.length) {
        continue;
      }
      if (seatMap[yy][xx]) {
        ++occupied;
      }
    }
  }
  return occupied;
}

function step(seatMap, newMap) {
  let count = 0;
  for (let y = 0; y < seatMap.length; ++y) {
    for (let x = 0; x < seatMap[y].length; ++x) {
      if (seatMap[y][x] === undefined) {
        continue;
      }
      if (seatMap[y][x]) {
        if (occupiedNeighbors(seatMap, x, y) >= 4) {
          ++count;
          newMap[y][x] = false;
        }
      } else {
        if (occupiedNeighbors(seatMap, x, y) === 0) {
          ++count;
          newMap[y][x] = true;
        }
      }
    }
  }
  return count;
}

function toString(seatMap) {
  let output = '';
  for (let row of seatMap) {
    for (let col of row) {
      output += col ? '#' : col === false ? 'L' : '.';
    }
    output += '\n';
  }
  return output;
}

// there are no seats taken initially
let seatMap = data.map((row) => row.split('').map((token) => (token === 'L' ? false : undefined)));

let iterations = 0;
let count;
do {
  const newMap = copySeatMap(seatMap);
  count = step(seatMap, newMap);
  seatMap = newMap;
  ++iterations;
} while (count > 0);
console.log(`${iterations} iterations\n`);
console.log(toString(seatMap));
console.log(seatMap.reduce((count, row) => count + row.reduce((count, col) => (col ? count + 1 : count), 0), 0));
