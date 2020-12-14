const fs = require('fs');

const data = fs.readFileSync('data/2.txt').toString().split(/\n/);

function isValid(line) {
    let m = line.match(/(\d+)-(\d+) (.): (.*)/);
    if (m) {
        let min = m[1];
        let max = m[2];
        let token = m[3];
        let str = m[4];
        // // part 1
        // let count = str.split(token).length - 1;
        // return count >= min && count <= max;
        // part 2
        return (str[min - 1] === token) !== (str[max - 1] === token);
    }
    return false;
}

// console.log(isValid('1-3 a: abcde'));
// console.log(isValid('1-3 b: cdefg'));
// console.log(isValid('2-9 c: ccccccccc'));

console.log(data.reduce((count, line) => isValid(line) ? count + 1 : count, 0));