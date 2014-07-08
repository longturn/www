set terminal svg size 650 100 fsize 8
set border 31 linewidth .3
set noxlabel
set format y "%6.0f"
set yrange [0:]
set output "/tmp/joins.svg"
set ylabel "";
set nomxtics
set nomytics
set ytics 1
set y2tics 1
set xdata time
set timefmt "%Y-%m-%d"
plot \
	"/tmp/joins.dat" using 1:2 with histeps linecolor rgb "#000000" notitle
