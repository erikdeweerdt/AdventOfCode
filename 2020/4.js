const fs = require('fs');

const data = fs.readFileSync('data/4.txt').toString().split(/\n\n/);

const keys = {
    byr: input => isValidNumber(input, 1920, 2002),
    iyr: input => isValidNumber(input, 2010, 2020),
    eyr: input => isValidNumber(input, 2020, 2030),
    hgt: input => {
        const m = input.match(/^(\d+)(cm|in)$/);
        if (m) {
            return (m[2] === 'cm') ?
                isValidNumber(m[1], 150, 193) :
                isValidNumber(m[1], 59, 76)
        }
        return false;
    },
    hcl: RegExp.prototype.test.bind(/^#[0-9a-f]{6}$/),
    ecl: RegExp.prototype.test.bind(/^(amb|blu|brn|gry|grn|hzl|oth)$/),
    pid: RegExp.prototype.test.bind(/^\d{9}$/),
    cid: () => true,
}

function isValidNumber(input, min, max) {
    const num = parseInt(input);
    return num >= min && num <= max;
}

function makePassport(entry) {
    const passport = {};
    const matches = entry.matchAll(/(...):(\S+)/g);
    for (const match of matches) {
        passport[match[1]] = match[2];
    }
    return passport;
}

function isValidPassport(passport) {
    for (const key in keys) {
        if (!keys[key](passport[key] || '')) {
            return false;
        }
    }
    return true;
}

const passports = data.map(makePassport);
const validCount = passports.filter(isValidPassport).length;

console.log(validCount);