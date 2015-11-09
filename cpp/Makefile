
BUILD_DIR=build

.phony: all clean

all:
	mkdir -p ${BUILD_DIR}
	cd ${BUILD_DIR} \
	&& cmake .. \
	&& make

clean:
	rm -R ${BUILD_DIR}
