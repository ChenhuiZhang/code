#include <check.h>
#include "cal.h"

START_TEST(check_cal_add)
{
  fail_unless(add(2, 3) == 5);
}
END_TEST

Suite *
cal_suite()
{
  Suite *s = suite_create("Cal Suite");
  TCase *tc_cal = tcase_create("Cal tests");

  tcase_add_test(tc_cal, check_cal_add);

  suite_add_tcase(s, tc_cal);
  return s;
}

int
main(int argc, const char *argv[])
{
  SRunner *sr = srunner_create(NULL);

  /* Setup the test suites */
  srunner_add_suite(sr, cal_suite());

  /* Run the tests */
  srunner_run_all(sr, CK_NORMAL);
  srunner_free(sr);
  
  return 0;
}

