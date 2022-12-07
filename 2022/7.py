from abc import ABC
from io import StringIO
from textwrap import indent

testdata = '''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''


class Node(ABC):
    def __init__(self, parent) -> None:
        self.__parent = parent

    def get_parent(self):
        return self.__parent

    def size(self):
        raise NotImplementedError()

    def flatten(self, list):
        raise NotImplementedError()


class Dir(Node):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.__contents = {}

    def size(self):
        return sum(node.size() for node in self.__contents.values())

    def add_node(self, name, entry):
        self.__contents[name] = entry

    def get_node(self, name):
        return self.__contents[name]

    def flatten(self, list):
        list.append(self)
        for node in self.__contents.values():
            node.flatten(list)

    def __str__(self):
        return '(dir)\n' + indent('\n'.join(f'- {name} {str(node)}' for name, node in self.__contents.items()), '  ')


class File(Node):
    def __init__(self, parent, size) -> None:
        super().__init__(parent)
        self.__size = size

    def size(self):
        return self.__size

    def flatten(self, list):
        list.append(self)

    def __str__(self):
        return f'(file, size={self.__size})'


def part1():
    root = read()
    print('- / ' + str(root))
    flat = []
    root.flatten(flat)
    total = 0
    for node in flat:
        if isinstance(node, Dir):
            s=node.size()
            if s <= 100000:
                total += s
    print (total)
    
def part2():
    root = read()
    space = 70000000
    required = 30000000
    available = space - root.size()
    to_free = required - available
    flat = []
    root.flatten(flat)
    candidates = []
    for node in flat:
        if isinstance(node, Dir):
            s = node.size()
            if s >= to_free:
                candidates.append(s)
    print(sorted(candidates))


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        data = list(map(str.strip, f.readlines()))
    root = Dir(None)
    cwd = root
    for line in data:
        if not line:
            continue
        if line.startswith('$'):
            cmd = line[2:]
            if cmd.startswith('cd'):
                name = cmd[3:]
                if name == '/':
                    cwd = root
                elif name == '..':
                    cwd = cwd.get_parent()
                else:
                    cwd = cwd.get_node(name)
            elif cmd == 'ls':
                pass
            else:
                raise Exception(f'Unknown command [{cmd}]')
        else:
            if line.startswith('dir'):
                name = line[4:]
                cwd.add_node(name, Dir(cwd))
            else:
                size, name = line.split(' ', 1)
                cwd.add_node(name, File(cwd, int(size)))
    return root


if __name__ == '__main__':
    # part1()
    part2()
