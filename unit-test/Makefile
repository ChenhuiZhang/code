
CFLAGS	= -fpic -fprofile-arcs -ftest-coverage
LDFLAGS = -shared -fprofile-arcs -ftest-coverage

LIB	= libcal.so

CHECK_DIR = test
REPORT_DIR= report
GCOV_FILE = $(REPORT_DIR)/cal.info

OBJS	= cal.o

.PHONY: all clean

$(LIB): $(OBJS)
	gcc $(LDFLAGS) $^ -o $@

all: $(LIB)

check: $(LIB)
	$(MAKE) -C $(CHECK_DIR)

report: check
	mkdir -p report
	@find . -maxdepth 1 -name "*.gcno" | xargs -i mv {} $(REPORT_DIR)
	@find . -maxdepth 1 -name "*.gcda" | xargs -i mv {} $(REPORT_DIR)
	lcov -q -b . -c -d $(REPORT_DIR) -o $(GCOV_FILE)
	genhtml -q -o $(REPORT_DIR) $(GCOV_FILE)

clean:
	$(MAKE) -C $(CHECK_DIR) clean
	$(RM) *.o $(LIB)
	$(RM) -r report
