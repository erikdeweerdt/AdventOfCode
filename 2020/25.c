#include <stdio.h>

/*
Note: day 25 only has 1 part
*/

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

unsigned long findKey()
{
  // find loop sizes
  int cardLoopSize = findLoopSize(7, CARD_PK);
  int doorLoopSize = findLoopSize(7, DOOR_PK);
  printf("Card loop size: %d\n", cardLoopSize);
  printf("Door loop size: %d\n", doorLoopSize);
  // find encryption key
  // alternatively return transform(DOOR_PK, cardLoopSize) and/or check that they match
  return transform(CARD_PK, doorLoopSize);
}

// faster implementation that uses a single loop to break the key
unsigned long findKeyFast()
{
  unsigned long publicKey = 1;
  unsigned long encryptionKeys[2] = {1, 1};
  while (1)
  {
    publicKey = (publicKey * 7) % PRIME;
    encryptionKeys[0] = (encryptionKeys[0] * CARD_PK) % PRIME;
    encryptionKeys[1] = (encryptionKeys[1] * DOOR_PK) % PRIME;
    // encryption key is obtained by encrypting the card's public key with the door's loop size
    // -> if the card loop is found, return the encrypted door key (or vice-versa)
    if (publicKey == CARD_PK)
    {
      return encryptionKeys[1];
    }
    if (publicKey == DOOR_PK)
    {
      return encryptionKeys[0];
    }
  }
}

int main()
{
  // findKeyFast runs too fast to be measurable
  // findKey runs within .1s
  // printf("Encryption key: %lu\n", findKey()); // 5025281
  printf("Encryption key: %lu\n", findKeyFast()); // 5025281
  return 0;
}