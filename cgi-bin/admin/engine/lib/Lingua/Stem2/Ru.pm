package Lingua::Stem2::Ru;

use Exporter;
our @ISA	= qw(Exporter);
our @EXPORT = qw(stem_word);

my $Stem_Caching  = 0;
my $Stem_Cache    = {};

my $VOWEL        = qr/���������/;
my $PERFECTIVEGROUND = qr/((��|����|������|��|����|������)|((?<=[��])(�|���|�����)))$/;
my $REFLEXIVE    = qr/(�[��])$/;
my $ADJECTIVE    = qr/(��|��|��|��|���|���|��|��|��|��|��|��|��|��|���|���|���|��|��|��|��|��|��)$/;
my $PARTICIPLE   = qr/((���|���|���)|((?<=[��])(��|��|��|��|�)))$/;
my $VERB         = qr/((���|���|���|����|����|���|���|���|��|��|��|��|��|��|���|���|���|���|��|�)|((?<=[��])(��|��|���|���|��|�|�|��|�|��|��|��|��|��|��|���|���)))$/;
my $NOUN         = qr/(�|��|��|��|��|�|����|���|���|��|��|�|���|��|��|��|�|�|�|�|��|��|�|��|��|�)$/;
my $RVRE         = qr/^(.*?[$VOWEL])(.*)$/;
my $DERIVATIONAL = qr/[^$VOWEL][$VOWEL]+[^$VOWEL]+[$VOWEL].*(?<=�)���?$/;

sub stem_word {
    my $word = lc shift;

    # Check against cache of stemmed words
    if ($Stem_Caching && exists $Stem_Cache->{$word}) {
        return $Stem_Cache->{$word};
    }
	
	 $word =~ s/��$//;
	 $word =~ s/�$//;
	 $word =~ s/��$//;

     my ($start, $RV) = $word =~ /$RVRE/;
     return $word unless $RV;

     # Step 1
     unless ($RV =~ s/$PERFECTIVEGROUND//) {
         $RV =~ s/$REFLEXIVE//;

         if ($RV =~ s/$ADJECTIVE//) {
             $RV =~ s/$PARTICIPLE//;
         } else {
             $RV =~ s/$NOUN// unless $RV =~ s/$VERB//;
         }
     }

     # Step 2
     $RV =~ s/�$//;

     # Step 3
     $RV =~ s/����?$// if $RV =~ /$DERIVATIONAL/;

     # Step 4
     unless ($RV =~ s/�$//) {
         $RV =~ s/����?//;
         $RV =~ s/��$/�/;	
     }

     return $start.$RV;
}

1;