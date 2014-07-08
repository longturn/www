#!/usr/bin/perl

use strict;

sub max {
	my ($a, $b) = @_;
	return $a > $b ? $a : $b;
}

sub winprob {
	my ($p, $fp1, $fp2, $hp1, $hp2) = @_;
	my @dp;

	for my $i (0..$hp1) {
		for my $j (0..$hp2) {
			if ($i == 0) {
				$dp[$i]->[$j] = 0.0;
				next;
			}
			if ($j == 0) {
				$dp[$i]->[$j] = 1.0;
				next;
			}
			$dp[$i]->[$j] = $p * $dp[max(0, $i - $fp2)]->[$j]
			    + (1.0 - $p) * $dp[$i]->[max(0, $j - $fp1)];        
		}
	}
	return $dp[$hp1]->[$hp2];
}

sub exphp {
	my ($p, $fp1, $fp2, $hp1, $hp2) = @_;
	my @dp;

	for my $i (0..$hp1) {
		for my $j (0..$hp2) {
			if ($i == 0) {
				$dp[$i]->[$j] = 0.0;
				next;
			}
			if ($j == 0) {
				$dp[$i]->[$j] = $i;
				next;
			}
			$dp[$i]->[$j] = $p * $dp[max(0, $i - $fp2)]->[$j]
			    + (1.0 - $p) * $dp[$i]->[max(0, $j - $fp1)];        
		}
	}
	return $dp[$hp1]->[$hp2];
}
print "Content-type: text/html\n\n";
print "<html><head><title>Freeciv War Calculator</title></head>";
print "<body>\n";
print "<style type=\"text/css\"> body { font-family:courier, \"courier new\", monospace; font-size:1em; } </style>";

my %vals = (
	att => 12,
	afp => 1,
	ahp => 20,
	def => 4.5,
	dfp => 1,
	dhp => 20,
);
my @vals = split(/&/, $ENV{QUERY_STRING});

for (@vals) {
	if (/(\w+)=(.*)/) {
		if ($1 ~~ ["att", "afp", "ahp", "def", "dfp", "dhp"]) {
			$vals{$1} = 0 + $2;
		}
	}
}

if ($ENV{QUERY_STRING}) {
	my $p = $vals{att} / ($vals{att} + $vals{def});
	my $defhp = $vals{dhp};
	print "<h2>Results</h2>\n";

	print <<HEADER;
		<table border=1 cellspacing=0 colspacing=0>
		<tr>
			<td></td>
			<td>attprob</td>
			<td>attexphp</td>
			<td>defprob</td>
			<td>defexphp</td>
			<td>deltahp</td>
		</tr>
HEADER
	for my $i (1..20) {
		my $defprob = 100 * winprob($p, $vals{dfp}, $vals{afp}, $defhp, $vals{ahp});
		my $attprob = 100 - $defprob;
		my $dexphp = exphp($p, $vals{dfp}, $vals{afp}, $defhp, $vals{ahp});
		my $aexphp = exphp(1.0 - $p, $vals{afp}, $vals{dfp}, $vals{ahp}, $defhp);
		my $delta = $defhp - $dexphp;
		my $row = sprintf("<td>T%d:</td> <td>%6.2lf%%</td> <td>%5.2f</td> <td>%6.2lf%%</td> <td>%5.2f</td> <td>(-%.2f)</td>\n",
			$i, $attprob, $aexphp, $defprob, $dexphp, $delta);
		print "<tr>$row</tr>";

		$defhp = $dexphp;
		last if $defhp == 0;
			
	}
	print "</table>";
	print "<h2>Again</h2>\n";
} else {
	print "<h2>Calculate</h2>\n";
}

print <<FORM;
<form action="http://akfaew.jasminek.net/cgi-bin/ltcalc.pl" method="GET">
<table border=1 cellspacing=0 colspacing=0>
<tr>
	<td></td>
	<td>str (def/att)</td>
	<td>firepower</td>
	<td>hitpoints</td>
</tr>

<tr>
	<td>attacker:</td>
	<td><input type="text" name="att" size=20 value=$vals{att}></td>
	<td><input type="text" name="afp" size=20 value=$vals{afp}></td>
	<td><input type="text" name="ahp" size=20 value=$vals{ahp}></td>
</tr>

<tr>
	<td>defender:</td>
	<td><input type="text" name="def" size=20 value=$vals{def}></td>
	<td><input type="text" name="dfp" size=20 value=$vals{dfp}></td>
	<td><input type="text" name="dhp" size=20 value=$vals{dhp}></td>
</tr>
</table>
<input type="submit" value="submit">
</form>
FORM

print "</body></html>\n";
