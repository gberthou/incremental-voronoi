BIN=c
GPP=g++

CPPFLAGS=-std=c++2a -Wall -Wextra -Werror -pedantic -O3 -g
INCLUDES=-I/usr/include/python3.8
LFLAGS=-lpython3.8 -lX11 -lGLX -lGL

OFILES=main.o VoronoiExplorer.o VoronoiGraph.o VoronoiDisplay.o Noise.o OpenSimplexNoise.o ui.o gl.o glutils.o

%.o: %.cpp
	$(GPP) $(CPPFLAGS) $(INCLUDES) -c $< -o $@ 

$(BIN): $(OFILES)
	$(GPP) $(LFLAGS) -o $(BIN) $^

clean:
	rm -f $(BIN) $(OFILES)
