#!/usr/bin/env perl

use strict;
use warnings;

use Text::CSV;

if (int(@ARGV) != 2) {
   printf("Usage: $0 <csv-filename> <group-filename>\n");
   exit(-1);
}

my $csvFilename = $ARGV[0];
my $groupFilename = $ARGV[1];

# parse the group names first

my %users = ();

open (my $groupFile, '<', $groupFilename) or die "Could not open '$groupFilename' $!\n";

while (!eof($groupFile)) {
   my $line = <$groupFile>;
   chomp $line;
   my $niceName = $line;

   $line = <$groupFile>;
   chomp $line;
   my $userName = $line;

   $users{$userName} = $niceName;
}

foreach my $username (keys %users) {
   my $nicename = $users{$username};
   # printf("%-30.30s %s\n", $username, $nicename);
}

my $csv = Text::CSV->new({
   sep_char => ','
});

open(my $csvFile, '<', $csvFilename) or die "Could not open '$csvFilename' $!\n";

my $tableHtml = "<table class='table table-bordered'>\n";

$tableHtml .= "    <tr>\n";
$tableHtml .= "        <th>Student Name</th>\n";
$tableHtml .= "        <th>Profile Page</th>\n";
$tableHtml .= "        <th>Blog</th>\n";
$tableHtml .= "        <th>Marking</th>\n";
$tableHtml .= "        <th>Progress</th>\n";
$tableHtml .= "        <th>Comments</th>\n";
$tableHtml .= "        <th>Karma</th>\n";
$tableHtml .= "    </tr>\n";

my $numStudents = 0;
my $totalProgress = 0;

while (my $line = <$csvFile>) {
   chomp $line;

   # ^M characters at the end of the line
   $line =~ s/\r//g;

   if ($csv->parse($line)) {
 
      my @fields = $csv->fields();

      #Enrolment Date,End Date,Student Name,Student Profile Name,Progress,Country,Comments,Karma,What is your CSE email address?,What is your Quest?,What is your favourite colour?

      die "Wrong number of fields" if (int (@fields) != 11);

      my $enrolmentDate = $fields[0];
      my $endDate = $fields[1];
      my $studentName = $fields[2];
      my $studentProfileName = $fields[3];
      my $progress = $fields[4];
      my $country = $fields[5];
      my $comments = $fields[6];
      my $karma = $fields[7];
      my $email = $fields[8];
      my $quest = $fields[9];
      my $colour = $fields[10];

      my $profilePageLink = 'https://www.openlearning.com/u/' . $studentProfileName;
      my $prettyProfilePageLink = sprintf("<a href='%s'>%s</a>\n", $profilePageLink, $studentProfileName);

      my $blogLink = 'https://www.openlearning.com/u/' . $studentProfileName . '/blog';
      my $prettyBlogLink = sprintf("<a href='%s'>Blog</a>\n", $blogLink);

      my $markingLink = "https://www.openlearning.com/marking?cohort=courses/99luftballons/Cohorts/ClassOf2014&student=" . $studentProfileName;
      my $prettyMarkingLink = sprintf("<a href='%s'>Marking</a>\n", $markingLink);

      if (defined($users{$studentProfileName})) {
         # make a pretty table

         my $backgroundColour; 
         if ($progress >= 60) {
            $backgroundColour = "#CCFFCC";
         } elsif ($progress >= 40) {
            $backgroundColour = "#FFE5CC";
         } else {
            $backgroundColour = "#FFAAAA";
         }

         $tableHtml .= "    <tr>\n";
         $tableHtml .= "        <td style='background-color: $backgroundColour'>$studentName</td>\n";
         $tableHtml .= "        <td style='background-color: $backgroundColour'>$prettyProfilePageLink</td>\n";
         $tableHtml .= "        <td style='background-color: $backgroundColour'>$prettyBlogLink</td>\n";
         $tableHtml .= "        <td style='background-color: $backgroundColour'>$prettyMarkingLink</td>\n";
         $tableHtml .= sprintf("        <td style='background-color: %s'>%3.1f%%</td>\n", $backgroundColour, $progress);
         $tableHtml .= "        <td style='background-color: $backgroundColour'>$comments</td>\n";
         $tableHtml .= "        <td style='background-color: $backgroundColour'>$karma</td>\n";
         $tableHtml .= "    </tr>\n";

         $totalProgress += $progress;
         $numStudents += 1;
      }

   } else {
      die "Line could not be parsed: $line\n";
   }
}

$tableHtml .= "</table>\n";

printf ("%s", $tableHtml);

my $averageProgress = (1.0 * $totalProgress) / $numStudents;

printf("<p>Average progress: %3.1f%%</p>\n", $averageProgress);
