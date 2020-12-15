const fs = require('fs');

const data = fs
  .readFileSync('data/12.txt')
  .toString()
  .split(/\n/)
  .filter((line) => line);
const testData = ['F10', 'N3', 'F7', 'R90', 'F11'];

class Boat {
  constructor(bearing = 0, latitude = 0, longitude = 0) {
    this.bearing = bearing;
    this.latitude = latitude; // north-south
    this.longitude = longitude; // east-west
  }

  move(instr, val = undefined) {
    const action = typeof val === 'number' ? instr : instr[0];
    const value = typeof val === 'number' ? val : parseInt(instr.substr(1));
    switch (action) {
      case 'N':
        this.latitude += value;
        break;
      case 'E':
        this.longitude += value;
        break;
      case 'S':
        this.latitude -= value;
        break;
      case 'W':
        this.longitude -= value;
        break;
      case 'L':
        // use 360 - value to avoid negative values
        this.bearing = (this.bearing + 360 - value) % 360;
        break;
      case 'R':
        this.bearing = (this.bearing + value) % 360;
        break;
      case 'F':
        this.move(Boat.getDirection(this.bearing), value);
    }
  }

  static getDirection(bearing) {
    switch (bearing) {
      case 0:
        return 'N';
      case 90:
        return 'E';
      case 180:
        return 'S';
      case 270:
        return 'W';
    }
  }
}

const boat = new Boat(90); // start facing east
data.forEach((instr) => boat.move(instr));
console.log(boat);
console.log(Math.abs(boat.latitude) + Math.abs(boat.longitude));
