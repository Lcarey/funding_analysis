#!/usr/bin/env perl
use warnings;
use strict;
use Lingua::StopWords qw( getStopWords ); #optional, just comment out the marked lines

#  count the unique words in grant abstract files
# reads csv files from http://exporter.nih.gov/ExPORTER_Catalog.aspx?sid=0&index=1
# output a tab file w/words, counts and year
#
#  ./NIH_count_words.pl *csv > word_counts.tab
#
# LBC 01/15

my $min_word_length = 2 ; 
my $min_total_word_count = 10 ; # only print words present at least this # of times in ALL grants
my $stopwords = getStopWords('en'); #
my %wc_all ; 
my %h ;

print "word\tcount\tyear\n";

# 1) read files and build a hash of word counts
foreach my $fn (@ARGV) {
    if($fn =~ m/(\d+)\.csv$/){
        my $year = $1 ; 
        print STDERR "reading $fn , year = $year ... \n";
        open(F,$fn) || die $!;
        while(<F>){
            chomp;
            $_ = lc($_);
            s/[^\w\s]//g;
            my @l = split(/\s/);
            @l = grep { !$stopwords->{$_} } @l ; #
            foreach (@l){
                $h{$year}{$_}++;
                $wc_all{$_}++;
            }
        }
        close(F);
    }
}

# 2) for words that occur enough, print their counts
foreach my $year (keys %h){
    foreach my $word (keys $h{$year}){
        if(length($word)>$min_word_length && $wc_all{$word} > $min_total_word_count ){
           print "$word\t$h{$year}{$word}\t$year\n";
       }
   }
}


