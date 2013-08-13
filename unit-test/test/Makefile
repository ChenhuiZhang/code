
CFLAGS	= -I ..
LDFLAGS = -L .. -lcal -lcheck 

APP	= check
OBJS	= cal_check.o

.PHONY: all clean

all: $(APP)

$(APP): $(OBJS)
	gcc $^ $(LDFLAGS) -o $@

clean:
	$(RM) *.o $(APP)
