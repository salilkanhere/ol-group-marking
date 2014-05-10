#!/usr/bin/env perl

use strict;
use warnings;

use File::Path qw(make_path);

use Text::CSV;

use constant GROUPS_DIRECTORY => 'groups';

use constant GENERATE_HTML_SCRIPT => 'make-page.pl';

if (int(@ARGV) != 2) {
   printf("Usage: $0 <csv-filename> <report-output-directory>\n");
   exit(-1);
}

my $csvFilename = $ARGV[0];
my $reportOutputDirectory = $ARGV[1];

make_path($reportOutputDirectory);

my $groupsDirectory = GROUPS_DIRECTORY;

opendir(my $groupsFh, $groupsDirectory) or die $!;

while (my $filename = readdir($groupsFh)) {
    next if ($filename =~ m/^\./);

    printf ("Generating report for group: '%s'\n", $filename);	

    my $reportFilename = sprintf("%s/%s.html", $reportOutputDirectory, $filename);

    my $execCommand = sprintf("./%s %s %s/%s > %s", GENERATE_HTML_SCRIPT, $csvFilename, GROUPS_DIRECTORY, $filename, $reportFilename);

    system($execCommand);

    if ($? == 0) {
        printf("OK\n");
    } else {
        printf("ERROR\n");
    }
}

closedir($groupsFh);
