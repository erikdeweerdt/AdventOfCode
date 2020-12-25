#include <stdio.h>

#define PRIME 20201227
#define CARD_PK 10943862
#define DOOR_PK 12721030

// test values
// #define CARD_PK 5764801
// #define DOOR_PK 17807724

unsigned long transform(int subject, int loopSize)
{
  unsigned long value = 1;
  for (; loopSize > 0; --loopSize)
  {
    value = (value * subject) % PRIME;
  }
  return value;
}

int findLoopSize(int subject, unsigned long key)
{
  unsigned long value = 1;
  int loopSize = 0;
  for (; value != key; ++loopSize)
  {
    value = (value * subject) % PRIME;
  }
  return loopSize;
}

int main()
{
  // find loop sizes
  int cardLoopSize = findLoopSize(7, CARD_PK);
  int doorLoopSize = findLoopSize(7, DOOR_PK);
  printf("Card loop size: %d\n", cardLoopSize);
  printf("Door loop size: %d\n", doorLoopSize);
  // find encryption key
  unsigned long encryptionKey = transform(CARD_PK, doorLoopSize);
  // optionally test that it matches the key calculated the other way round
  // if (encryptionKey == transform(DOOR_PK, cardLoopSize))
  // {
  //   printf("Error finding encryption key\n");
  // }
  printf("Encryption key: %lu\n", encryptionKey);
  return 0;
}