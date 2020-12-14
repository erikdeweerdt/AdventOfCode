const fs = require('fs');

const data = fs.readFileSync('data/5.txt').toString().split(/\n/);

function Seat(row, col) {
  this.row = row;
  this.col = col;
  this.id = row * 8 + col;
}

function getSeat(seatCode) {
  let row = 0;
  let col = 0;
  let i = 0;
  for (let chr = seatCode[i]; chr === 'F' || chr === 'B'; ++i, chr = seatCode[i]) {
    row = row * 2 + (chr === 'B' ? 1 : 0);
  }
  for (let chr = seatCode[i]; chr === 'L' || chr === 'R'; ++i, chr = seatCode[i]) {
    col = col * 2 + (chr === 'R' ? 1 : 0);
  }
  return new Seat(row, col);
}

// console.log(getSeat('BFFFBBFRRR'));
// console.log(getSeat('FFFBBBFRRR'));
// console.log(getSeat('BBFFBBFRLL'));

// part 1
const seats = data.map(getSeat);
const maxSeatId = seats.reduce((max, seat) => (seat.id > max ? seat.id : max), 0);
console.log(`Max id = ${maxSeatId}`);

// part 2
const seatsById = Array.from(Array(maxSeatId + 1));
seats.forEach(seat => seatsById[seat.id] = seat);
// the answer is clearly visible from this output
// if you really want you can use a proper loop to find it
seatsById.forEach((seat, id) => seat || console.log(`Missing: ${id}`));
