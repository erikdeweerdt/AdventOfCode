const fs = require('fs');

const data = fs
  .readFileSync('data/12.txt')
  .toString()
  .split(/\n/)
  .filter((line) => line);
const testData = ['F10', 'N3', 'F7', 'R90', 'F11'];

class Boat {
  constructor(bearing = 0, latitude = 0, longitude = 0, waypointLatitude = 0, waypointLongitude = 0) {
    this.bearing = bearing;
    this.latitude = latitude; // north-south
    this.longitude = longitude; // east-west
    this.waypointLatitude = waypointLatitude; // north-south
    this.waypointLongitude = waypointLongitude; // east-west
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
        break;
    }
  }

  moveWaypoint(instr) {
    const action = instr[0];
    const value = parseInt(instr.substr(1));
    switch (action) {
      case 'N':
        this.waypointLatitude += value;
        break;
      case 'E':
        this.waypointLongitude += value;
        break;
      case 'S':
        this.waypointLatitude -= value;
        break;
      case 'W':
        this.waypointLongitude -= value;
        break;
      case 'L':
        this.rotateWaypoint(360 - value);
        break;
      case 'R':
        this.rotateWaypoint(value);
        break;
      case 'F':
        this.latitude += value * this.waypointLatitude;
        this.longitude += value * this.waypointLongitude;
        break;
    }
  }

  rotateWaypoint(degrees) {
    const lat = this.waypointLatitude;
    const long = this.waypointLongitude;
    switch (degrees) {
      case 90:
        this.waypointLatitude = -long;
        this.waypointLongitude = lat;
        break;
      case 180:
        this.waypointLatitude *= -1;
        this.waypointLongitude *= -1;
        break;
      case 270:
        this.waypointLatitude = long;
        this.waypointLongitude = -lat;
        break;
    }
  }

  static getDirection(degrees) {
    switch (degrees) {
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

// part 1
// const boat = new Boat(90); // start facing east
// data.forEach((instr) => boat.move(instr));
// console.log(boat);
// console.log(Math.abs(boat.latitude) + Math.abs(boat.longitude));

// part 2
const boat = new Boat(0, 0, 0, 1, 10);
data.forEach((instr) => boat.moveWaypoint(instr));
console.log(boat);
console.log(Math.abs(boat.latitude) + Math.abs(boat.longitude));
