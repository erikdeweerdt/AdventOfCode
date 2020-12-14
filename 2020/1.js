const fs = require('fs');

const data = fs.readFileSync('data/1.txt').toString().split(/\n/);
const numbers = data.map(i => parseInt(i));

function multiply() {
    for (let i = 0; i < numbers.length; ++i) {
        for (let j = i + 1; j < numbers.length; ++j) {
            // part 1
            // if (numbers[i] + numbers[j] === 2020) {
            //     return numbers[i] * numbers[j];
            // }
            // part 2
            for (let k = j + 1; k < numbers.length; ++k) {
                if (numbers[i] + numbers[j] + numbers[k] === 2020) {
                    return numbers[i] * numbers[j] * numbers[k];
                }
            }
        }
    }
}

console.log(multiply())