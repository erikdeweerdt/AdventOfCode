const fs = require('fs');

const data = fs.readFileSync('data/8.txt').toString().split(/\n/);
const testData = ['nop +0', 'acc +1', 'jmp +4', 'acc +3', 'jmp -3', 'acc -99', 'acc +1', 'jmp -4', 'acc +6'];

function run(instructions, pc = 0, acc = 0, mayChange = true, visited = [...instructions].fill(false)) {
  // while true is better, but this ensures termination at some point
  for (let i = 0; i < instructions.length; ++i) {
    const instr = instructions[pc];
    if (!instr) {
      return acc;
    }
    // console.log(`PC ${pc}\t${instr}\t(${acc})`);
    let operator, operand;
    [operator, operand] = instr.split(' ', 2);
    if (mayChange && operator !== 'acc') {
      console.log(`Swapping PC ${pc}`);
      const alternateInstructions = [...instructions];
      alternateInstructions[pc] = (operator === 'jmp' ? 'nop' : 'jmp') + ' ' + operand;
      const alternate = run(alternateInstructions, pc, acc, false, [...visited]);
      if (alternate) {
        return alternate;
      }
    }

    if (visited[pc]) {
      console.log('Loop detected');
      // return acc;
      return undefined;
    }
    visited[pc] = true;

    [pc, acc] = exec(operator, parseInt(operand), pc, acc);
  }
}

function exec(operator, operand, pc, acc) {
  switch (operator) {
    case 'jmp':
      pc += operand;
      break;
    case 'acc':
      acc += operand;
    default:
      ++pc;
  }
  return [pc, acc];
}

console.log(run(data));
