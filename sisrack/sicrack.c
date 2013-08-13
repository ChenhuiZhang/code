#include <stdlib.h>
#include <stdio.h>

size_t MAGIC[10] = {0x96, 0x95, 0x10, 0x23, 0x07, 0x15, 0x08, 0x03, 0x10, 0x11};

int main(int argc, const char *argv[])
{
	size_t init_num = rand()%999999;
	char str_num[16] = {0};

	snprintf(str_num, 16, "%d", init_num);
	printf("num: %d(%s)\n", init_num, str_num);

  size_t i;
	for (i=0; i<6; ++i)
	{
		init_num = init_num*4;
		init_num += ((int)str_num[i])^MAGIC[i];
	}
	size_t final_num = init_num%100000;

	printf("End: %d\n", final_num);
	return 0;
}
