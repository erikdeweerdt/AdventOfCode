const fs = require('fs');

const data = fs.readFileSync('data/6.txt').toString();

function answerCode(answer) {
  // a is char code 97
  // letters can only occur once, but using bitwise or emphasizes bit operation
  return [...answer].reduce((code, char) => code | (1 << (char.charCodeAt() - 97)), 0);
}

function countOnes(number) {
  // https://prismoskills.appspot.com/lessons/Bitwise_Operators/Count_ones_in_an_integer.jsp
  let count = 0;
  let n = number;
  while (n != 0) {
    n = n & (n - 1);
    count++;
  }
  return count;
}

// console.log(answerCode("a"));
// console.log(answerCode("b"));
// console.log(answerCode("c"));
// console.log(answerCode("abc"));

const groups = data.split(/\n\n/);
const yesCounts = groups
  .map((group) =>
    group
      .split(/\n/)
      // remove superfluous empty lines (important for part 2)
      .filter(p => p)
      .map(answerCode)
      // part 1
      // .reduce((aggregate, code) => aggregate | code)
      // part 2
      .reduce((aggregate, code) => aggregate & code)
  )
  .map(countOnes);

// console.log(yesCounts);
console.log(yesCounts.reduce((sum, count) => sum + count));
