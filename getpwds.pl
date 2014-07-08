#!/usr/bin/perl

my @pwds = qx(echo 'select username, pass_md5 from auth_user as a join player_player as p on a.id = p.user_id;' | psql -U longturn -d longturn);
my @cooked = ();
for (@pwds) {
	push @cooked, "$1:$2" if /^\s*(\S+)\s*\|\s*(\S+)\s*$/;
}

$" = "\n";
print "@cooked\n";
