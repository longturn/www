#!/usr/bin/perl -w

use DBI;
use Digest::MD5 qw(md5_base64);

my $plotdir = "/home/longturn-www/media/plots";
my %global;
my $game = shift or die "need arg";
my $tmpdir = "/tmp/genplots";
my $dbh;
my $sth;
qx(mkdir -p $tmpdir);

sub query {
	$query = shift;
	$sth = $dbh->prepare($query);
	$sth->execute
	    or die "Got error $DBI::errstr while inserting values\n";
}

$dbh = DBI->connect('DBI:Pg:dbname=longturn', 'longturn', 'ajtDRtLN')
    or die "Got error $DBI::errstr while connecting to database\n";

$cols = "turn, cities, population, pollution, production, trade, units, units_killed, pollution";
query("SELECT $cols FROM serv_servglobaldata WHERE game_id = '$game' ORDER BY turn");

open $cities, ">$tmpdir/cities.dat" or die "$!";
open $population, ">$tmpdir/population.dat" or die "$!";
open $pollution, ">$tmpdir/pollution.dat" or die "$!";
open $production, ">$tmpdir/production.dat" or die "$!";
open $trade, ">$tmpdir/trade.dat" or die "$!";
open $units, ">$tmpdir/units.dat" or die "$!";
open $kills, ">$tmpdir/kills.dat" or die "$!";
open $pollution, ">$tmpdir/pollution.dat" or die "$!";

while (@vector = $sth->fetchrow) {
	print $cities "$vector[0] $vector[1]\n";
	print $population ("$vector[0] " . ($vector[2]/1000) . "\n");
	print $pollution "$vector[0] $vector[3]\n";
	print $production "$vector[0] $vector[4]\n";
	print $trade "$vector[0] $vector[5]\n";
	print $units "$vector[0] $vector[6]\n";
	print $kills "$vector[0] $vector[7]\n";
	print $pollution "$vector[0] $vector[8]\n";
}

close $cities;
close $population;
close $pollution;
close $production;
close $trade;
close $units;
close $kills;
close $pollution;

sub plot {
	my $cat = shift;
	my $args = shift || "";
	qx(gnuplot -e 'load "/home/longturn-www/longturn/plots/default.p"; set output "$tmpdir/$cat.svg"; set ylabel "$cat"; $args; plot "$tmpdir/$cat.dat" with lines linecolor rgb "#000000"');
}
plot "cities";
#plot "population", 'set format y "%.1fM";';
plot "population";
plot "pollution";
plot "production";
plot "trade";
plot "units";
plot "kills";
plot "pollution";
qx(mkdir -p $plotdir/$game 2>/dev/null);
qx(mv $tmpdir/*.svg $plotdir/$game);

query("SELECT turn FROM game_game WHERE name = '$game'");
$turn = ($sth->fetchrow)[0];
qx(mkdir -p $plotdir/$game/user 2>/dev/null);
query("SELECT DISTINCT user_id FROM serv_servuserdata WHERE game_id = '$game'");
while (@vector = $sth->fetchrow) {
	qx(mkdir $plotdir/$game/user/$vector[0] 2>/dev/null);
	$sth2 = $sth;
	genuser($vector[0]);
	$sth = $sth2;
}



sub genuser {
	$user_id = shift;
	$hash = md5_base64 sprintf("ABsoHCop-%d-%s-%03d", $user_id, $game, $turn);
	$hash =~ s#/#x#g;
	$hash =~ s#=##g;
	sub userplot {
		my $cat = shift;
		qx(gnuplot -e 'load "/home/longturn-www/longturn/plots/default.p"; set output "$tmpdir/$hash-$cat.svg"; set ylabel "$cat"; plot "$tmpdir/$cat.dat" with lines linecolor rgb "#000000"');
	}

	$cols = "turn, cities, population, pollution, production, trade, units, units_killed, 
		units_lost, settledarea, landarea, citizens, score, bulbs";
# bulbs cities citizens content corruption food gold govt happy idle landarea literacy munits pollution
# population production score settledarea shields techs trade unhappy units units_built units_killed units_lost
	query("SELECT $cols FROM serv_servuserdata WHERE user_id = '$user_id' AND game_id = '$game' ORDER BY turn");

	open $cities, ">$tmpdir/cities.dat" or die "$!";
	open $population, ">$tmpdir/population.dat" or die "$!";
	open $pollution, ">$tmpdir/pollution.dat" or die "$!";
	open $production, ">$tmpdir/production.dat" or die "$!";
	open $trade, ">$tmpdir/trade.dat" or die "$!";
	open $units, ">$tmpdir/units.dat" or die "$!";
	open $kills, ">$tmpdir/kills.dat" or die "$!";
	open $units_lost, ">$tmpdir/units_lost.dat" or die "$!";
	open $settled_area, ">$tmpdir/settled_area.dat" or die "$!";
	open $land_area, ">$tmpdir/land_area.dat" or die "$!";
	open $citizens, ">$tmpdir/citizens.dat" or die "$!";
	open $score, ">$tmpdir/score.dat" or die "$!";
	open $bulbs, ">$tmpdir/bulbs.dat" or die "$!";
	while (@vector = $sth->fetchrow) {
		print $cities "$vector[0] $vector[1]\n";
		print $population "$vector[0] $vector[2]\n";
		print $pollution "$vector[0] $vector[3]\n";
		print $production "$vector[0] $vector[4]\n";
		print $trade "$vector[0] $vector[5]\n";
		print $units "$vector[0] $vector[6]\n";
		print $kills "$vector[0] $vector[7]\n";
		print $units_lost "$vector[0] $vector[8]\n";
		print $settled_area "$vector[0] $vector[9]\n";
		print $land_area "$vector[0] $vector[10]\n";
		print $citizens "$vector[0] $vector[11]\n";
		print $score "$vector[0] $vector[12]\n";
		print $bulbs "$vector[0] $vector[13]\n";
	}
	close $cities;
	close $population;
	close $pollution;
	close $production;
	close $trade;
	close $units;
	close $kills;
	close $units_lost;
	close $settled_area;
	close $units_lost;
	close $land_area;
	close $citizens;
	close $score;
	close $bulbs;

	userplot "cities";
	userplot "population";
	userplot "pollution";
	userplot "production";
	userplot "trade";
	userplot "units";
	userplot "kills";
	userplot "units_lost";
	userplot "settled_area";
	userplot "land_area";
	userplot "citizens";
	userplot "score";
	userplot "bulbs";

	qx(rm $plotdir/$game/user/$user_id/*.svg);
	qx(mv $tmpdir/*.svg $plotdir/$game/user/$user_id);
	qx(rm $tmpdir/*.dat);
}
qx(rm -r $tmpdir);
