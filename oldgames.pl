#!/usr/bin/perl

while (<DATA>) {
	@F = split(/;/);
	print "insert into old_oldgame (name, descr, mode, version, admin, turn, ranking) ";
	print "values ('$F[0]', '', '$F[1]', '$F[2]', 'maho', $F[3], false);\n";
}

__DATA__
LT17;team game;2.2;0;;
LT18;teamless;2.2;0;;
LT19;team game;2.2;0;;
LT20;teamless;2.2;0;;
LT21;team game;2.2;0;;
LT23;teamless;2.2;0;;
LT24;teamless;2.2;178;;
LT16;teamless;2.1;0;;
LT26;teamless;2.2;145;2011-01-17;2011-07-08
LT27;team game;2.2;150;2011-03-03;2011-07-27
LT28;teamless;2.2;156;2011-06-07;2011-11-06
LT29;team game;2.2;115;2011-07-27;2011-11-20
LT15;team game;2.1;0;;
LT12;teamless;2.0;0;;
LT14;teamless;2.0;0;;
LT9;teamless;2.0;0;;
LT11;teamless;2.0;0;;
LT0;teamless;2.0;0;;
LT1;teamless;2.0;0;;
LT2;teamless;2.0;0;;
LT3;teamless;2.0;0;;
LT4;teamless;2.0;0;;
LT5;teamless;2.0;0;;
LT6;teamless;2.0;0;;
LT7;teamless;2.0;0;;
LT8;teamless;2.0;0;;
LTXIV;teamless;2.0;0;;
LTXV;team game;2.1;0;;
LTXVI;teamless;2.1;0;;
LTXVII;team game;2.2;0;;
LTXVIII;teamless;2.2;0;;
LT13;teamless;2.0;0;;
LTXIII;teamless;2.0;0;;
