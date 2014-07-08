#!/usr/bin/perl -w

use DBI;

my $plotdir = "/home/longturn-www/media/plots";
my %global;
my $game = shift or die "need arg";
my $dbh;
my $sth;

sub query {
	$query = shift;
	$sth = $dbh->prepare($query);
	$sth->execute
	    or die "Got error $DBI::errstr while inserting values\n";
}

$dbh = DBI->connect('DBI:Pg:dbname=longturn', 'longturn', 'ajtDRtLN')
    or die "Got error $DBI::errstr while connecting to database\n";

query("
SELECT 
    dg.date_joined, COALESCE(ile, 0)
FROM 
    (SELECT date_joined::date AS date_joined, count(*) AS ile FROM game_joined WHERE game_id = '$game' GROUP BY date_joined::date) AS d
    RIGHT JOIN 
    (
        SELECT 
            generate_series(
                COALESCE(
                    (SELECT date_joined FROM game_joined ORDER BY date_joined ASC LIMIT 1),
                    now()
                ),
                now(),
                '1 day'::interval
            )::date AS date_joined
    ) AS dg
    USING (date_joined)
    ORDER BY dg.date_joined ASC;
");
open $joins, ">/tmp/joins.dat" or die "$!";

my %joins;
while (@vector = $sth->fetchrow) {
	$joins{$vector[0]} = $vector[1];
}
for (sort keys %joins) {
	print $joins "$_ $joins{$_}\n";
}
close $joins;

qx(gnuplot -e 'load "/home/longturn-www/longturn/plots/join-rate.p";');
qx(mkdir -p $plotdir/$game 2>/dev/null);
qx(cp /tmp/joins.svg $plotdir/$game);
qx(rm /tmp/joins.dat /tmp/joins.svg);
