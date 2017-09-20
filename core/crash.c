#include <stdio.h>

int main(int argc, const char *argv[])
{
  printf("Hello, crash\n");
  int value = 42/0;

  printf("Are you ok? %d\n", value);
  return 0;
}
