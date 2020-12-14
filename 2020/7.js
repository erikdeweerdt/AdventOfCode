const fs = require('fs');

const data = fs.readFileSync('data/7.txt').toString().split(/\n/);
const testData = [
  'light red bags contain 1 bright white bag, 2 muted yellow bags.',
  'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
  'bright white bags contain 1 shiny gold bag.',
  'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
  'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
  'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
  'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
  'faded blue bags contain no other bags.',
  'dotted black bags contain no other bags.',
];

function parseRule(rule) {
  if (rule) {
    let bag, rawContents;
    [bag, rawContents] = rule.split(' bags contain ', 2);
    let contents = {};
    for (let match of rawContents.matchAll(/(\d+) (.*?) bags?/g)) {
      contents[match[2]] = parseInt(match[1]);
    }
    return { [bag]: contents };
  }
}

function resolve(rules, bag, current, cache) {
  if (current in cache) {
    return cache[current];
  }
  const contents = Object.keys(rules[current]);
  let found = contents.includes(bag);
  if (!found) {
    for (const nestedBag of contents) {
      found = resolve(rules, bag, nestedBag, cache);
      if (found) {
        break;
      }
    }
  }
  cache[current] = found;
  return found;
}

function findBag(rules, bag) {
  const cache = {};
  for (const current in rules) {
    resolve(rules, bag, current, cache);
  }
  return Object.keys(cache).filter((key) => cache[key]);
}

function countContents(rules, bag) {
  let count = 0;
  for (const nestedBag in rules[bag]) {
    count += rules[bag][nestedBag] * (1 + countContents(rules, nestedBag));
  }
  return count;
}

const rules = {};
// testData.map(parseRule).forEach((rule) => Object.assign(rules, rule));
data.map(parseRule).forEach((rule) => Object.assign(rules, rule));

// part 1
console.log(findBag(rules, 'shiny gold').length);

// part 2
console.log(countContents(rules, 'shiny gold'));