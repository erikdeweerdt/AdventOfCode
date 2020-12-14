const fs = require('fs');

const data = fs
  .readFileSync('data/10.txt')
  .toString()
  .split(/\n/)
  .filter((line) => line)
  .map((line) => parseInt(line, 10));
const testData = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4];
const testData2 = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3];

// since all adapters have to be used and can only take lower jolts, this is a simple sorting problem

const adapters = data.sort((a, b) => a - b);
adapters.push(adapters[adapters.length - 1] + 3); // internal adapter

console.log(adapters);
const diffs = [adapters[0]];
for (let i = 1; i < adapters.length; ++i) {
  diffs.push(adapters[i] - adapters[i - 1]);
}
console.log(diffs);
// part 1
// simply count the number of times a difference 1 and 3 occurs
// const count1 = diffs.reduce((count, diff) => (diff === 1 ? count + 1 : count), 0);
// const count3 = diffs.reduce((count, diff) => (diff === 3 ? count + 1 : count), 0);
// console.log(count1);
// console.log(count3);
// console.log(count1 * count3);

// part 2
// the problem can be stated as the number of ways a sequence of ones can be rewritten using 1, 2 and 3
// 3 can never be left out and can be ignored
// the final result is simply the product of the number of valid alternatives for all those sequences
const sequences = [];
let current = 0;
for (let diff of diffs) {
  // note: there are no differences of 2
  if (diff === 1) {
    ++current;
  } else if (current > 0) {
    sequences.push(current);
    current = 0;
  }
}
console.log(sequences);

// 1 remains 1 and 2 remains 2
// only need to expand >= 3
// longest sequence = 4, so we can do this manually
// general formula is: (n1 + n2 + n3)!/(n1! * n2! * n3!) summed for every valid combo of 1, 2 and 3
// 3 -> 4 (111 + 12 + 21 + 3)
// 4 -> 7 (1111 + 13 + 31 + 22 + 112 + 211 + 212)
const mapped = sequences.map((sequence) => (sequence === 1 ? 1 : sequence === 2 ? 2 : sequence === 3 ? 4 : 7));
console.log(mapped);
console.log(mapped.reduce((product, item) => product * item));
