package Lingua::Stem2::Ru;

use Exporter;
our @ISA	= qw(Exporter);
our @EXPORT = qw(stem_word);

my $Stem_Caching  = 0;
my $Stem_Cache    = {};

my $VOWEL        = qr/аеиоуыэю€/;
my $PERFECTIVEGROUND = qr/((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[а€])(в|вши|вшись)))$/;
my $REFLEXIVE    = qr/(с[€ь])$/;
my $ADJECTIVE    = qr/(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|еых|ую|юю|а€|€€|ою|ею)$/;
my $PARTICIPLE   = qr/((ивш|ывш|ующ)|((?<=[а€])(ем|нн|вш|ющ|щ)))$/;
my $VERB         = qr/((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ены|ить|ыть|ишь|ую|ю)|((?<=[а€])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$/;
my $NOUN         = qr/(а|ев|ов|ие|ье|е|и€ми|€ми|ами|еи|ии|и|ией|ей|ой|ий|й|и|ы|ь|ию|ью|ю|и€|ь€|€)$/;
my $RVRE         = qr/^(.*?[$VOWEL])(.*)$/;
my $DERIVATIONAL = qr/[^$VOWEL][$VOWEL]+[^$VOWEL]+[$VOWEL].*(?<=о)сть?$/;

sub stem_word {
    my $word = lc shift;

    # Check against cache of stemmed words
    if ($Stem_Caching && exists $Stem_Cache->{$word}) {
        return $Stem_Cache->{$word};
    }
	
	 $word =~ s/ам$//;
	 $word =~ s/и$//;
	 $word =~ s/и€$//;

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
     $RV =~ s/…$//;

     # Step 3
     $RV =~ s/ѕ”‘Ў?$// if $RV =~ /$DERIVATIONAL/;

     # Step 4
     unless ($RV =~ s/Ў$//) {
         $RV =~ s/≈ џ≈?//;
         $RV =~ s/ќќ$/ќ/;	
     }

     return $start.$RV;
}

1;