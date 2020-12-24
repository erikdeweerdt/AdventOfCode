#include <stdlib.h>
#include <stdio.h>

#define MAX_VALUE 1000000
#define ITERATIONS 10000000

/*
Runs in less than 0.6 seconds while the Python solution needs about 13 seconds
*/

typedef struct Cup
{
  unsigned int value;
  struct Cup *next;
} Cup;

const int DATA[9] = {9, 7, 4, 6, 1, 8, 3, 5, 2};

void play_round(Cup *cups, Cup *head)
{
  Cup *removed[3] = {head->next, head->next->next, head->next->next->next};
  int dest_value = head->value;
  Cup *dest_cup;
  do
  {
    if (--dest_value == 0)
    {
      dest_value = MAX_VALUE;
    }
    dest_cup = cups + dest_value;
  } while (dest_cup == removed[0] || dest_cup == removed[1] || dest_cup == removed[2]);
  head->next = removed[2]->next;
  removed[2]->next = dest_cup->next;
  dest_cup->next = removed[0];
}

int main()
{
  printf("Initializing...\n");
  // the array is too big for the stack, so put it on the heap
  Cup *cups = (Cup *)malloc((MAX_VALUE + 1) * sizeof(Cup));
  for (int i = 1; i < 9; ++i)
  {
    cups[i].value = i;
    cups[DATA[i - 1]].next = cups + DATA[i];
  }
  cups[9].value = 9;
  cups[10].value = 10;
  cups[DATA[8]].next = cups + 10;
  for (int i = 11; i < MAX_VALUE + 1; ++i)
  {
    cups[i].value = i;
    cups[i - 1].next = cups + i;
  }
  cups[MAX_VALUE].next = cups + DATA[0];
  // play game
  printf("Playing game...\n");
  Cup *head = cups + DATA[0];
  for (int i = 0; i < ITERATIONS; ++i)
  {
    play_round(cups, head);
    head = head->next;
  }
  printf("%lu\n", (unsigned long)cups[1].next->value * cups[1].next->next->value);
  return 0;
}