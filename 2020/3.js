const fs = require('fs');

const data = fs.readFileSync('data/3.txt').toString().split(/\n/);

function countTrees(dx, dy) {
    // let x = 0;
    // let y = 0;
    let count = 0;
    for (let x = 0, y = 0; y < data.length; x = (x + dx) % data[0].length, y += dy) {
        if (data[y][x] === '#') {
            ++count;
        }
    }
    // while (y < data.length) {
    //     if (data[y][x] === '#') {
    //         ++count;
    //     }
    //     y += dy;
    //     x = (x + dx) % data[0].length;
    // }
    return count;
}

// part 1
// console.log(countTrees(3, 1));
// part 2
console.log(countTrees(1, 1) * countTrees(3, 1) * countTrees(5, 1) * countTrees(7, 1) * countTrees(1, 2));
// 5813773056