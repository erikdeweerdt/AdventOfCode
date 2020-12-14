const fs = require('fs');

const data = fs
  .readFileSync('data/9.txt')
  .toString()
  .split(/\n/)
  .map((line) => parseInt(line, 10));
const testData = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576];

class XNode {
  constructor(num) {
    this.num = num;
    this.sums = [];
    this.next = undefined;
  }

  append(xnode) {
    let valid = this.sums.includes(xnode.num);
    this.sums.push(this.num + xnode.num);
    if (this.next) {
      valid |= this.next.append(xnode);
    } else {
      this.next = xnode;
    }
    return valid;
  }

  size() {
    if (this.next) {
      return this.next.size() + 1;
    }
    return 1;
  }

  tail() {
    if (this.next) {
      return this.next.tail();
    }
    return this;
  }

  toArray(array = []) {
    array.push(this.num);
    if (this.next) {
      this.next.toArray(array);
    }
    return array;
  }
}

function makeValidList(numbers, windowSize) {
  const head = new XNode(numbers[0]);
  let list = head;
  for (let i = 1; i < numbers.length; ++i) {
    const valid = list.append(new XNode(numbers[i]));
    if (list.size() > windowSize) {
      list = list.next;
    }
    if (i >= windowSize && !valid) {
      return head;
    }
  }
}

function findSum(sum, numbers, windowSize) {
  for (let i = 0; i + windowSize <= numbers.length; ++i) {
    const window = numbers.slice(i, i + windowSize);
    const windowSum = window.reduce((sum, number) => sum + number);
    if (windowSum === sum) {
      return window;
    }
  }
}

const list = makeValidList(data, 25);
const listSize = list.size();
const invalidNumber = list.tail().num;
console.log(listSize);
// part 1
console.log(invalidNumber);

// part 2
const numbers = list.toArray();
for (let i = 2; i < numbers.length; ++i) {
  console.log(`Window size = ${i}`);
  const window = findSum(invalidNumber, numbers, i);
  if (window) {
    console.log(window);
    const min = window.reduce((min, number) => (number < min ? number : min));
    const max = window.reduce((max, number) => (number > max ? number : max));
    console.log(min + max);
    break;
  }
}
