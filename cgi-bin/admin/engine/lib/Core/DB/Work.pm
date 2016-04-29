package Core::DB::Work;

require Core::DB;
@ISA=qw(Core::DB);

use strict;

			
sub new {
	my $class = shift;
	my $params = shift;
	
	my $self = $class->SUPER::new() || return undef;
	
	if(ref($params) eq 'HASH'){
		foreach my $item(keys %$params ){
			$self->{$item} = $params->{$item};
		}
	}
	
	return $self;
}

sub clearFields{
	my $self = shift;
	delete($self->{FIELDS});
	my %hash = %{$self->{_FIELDS}};
	$self->{FIELDS} = \%hash;
}

sub ignored {
	my $self = shift;
	my $string = shift;
	
	my %ignored = ("NOW()", "NULL");
	(!$ignored{$string})?(return "'$string'"):(return $string);
}

sub checked {
	my $self = shift;
	my $status = shift;
	
	if( $status eq "on") {
		return 1;
	} else {
		return $status;
	}
}

sub getFields{
	my $self = shift;
	my $params = shift;
	
	my %hash = %{$self->{_FIELDS}};
	$self->{FIELDS} = \%hash;
	
	foreach my $field(keys %{$self->{FIELDS}} ){
		$self->{FIELDS}->{$field} = $self->ignored( $params->{$field} ) if( $params->{$field} && $params->{$field} ne "");
	}
}

sub getFieldsName{
	my $self = shift;
	my $params = shift;
	my $name = shift;
	
	my %hash = %{$self->{"_".$name}};
	$self->{$name} = \%hash;
	
	foreach my $field(keys %{$self->{$name}} ){
		$self->{$name}->{$field} = $self->ignored( $params->{$field} ) if( $params->{$field} && $params->{$field} ne "");
	}
}

sub translit
{
  my $text = shift;
  $text =~ s/^\s+//g;
  $text =~ s/\s+$//g;
  $text =~ s/\\'//g;
  $text =~ s/\"//g;
  $text =~ s/ – /-/g;
  $text =~ s/ - /-/g;
  $text =~ s/ — /-/g;
  $text =~ s/\_/-/g;  
  $text =~ y/àáâãäå¸çèéêëìíîïðñòóôõúûüý/abvgdeezijklmnoprstufh_y_e/;
  $text =~ y/ÀÁÂÃÄÅ¨ÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÚÛÜÝ/abvgdeezijklmnoprstufh_y_e/;
  $text =~ y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/;  
  my %mchars = ('æ'=>'zh','ö'=>'c','÷'=>'ch','ø'=>'sh','ù'=>'sch',
     'þ'=>'yu','ÿ'=>'ya', 'Æ'=>'zh','Ö'=>'c','×'=>'ch', 'Ø'=>'sh',
     'Ù'=>'sch','Þ'=>'yu','ß'=>'ya',' '=>'-');
  for my $c (keys %mchars) {
      $text =~ s/$c/$mchars{$c}/g;
  }
  $text =~ s/\,/-/g;
  $text =~ s/\.//g;
  $text =~ s/\?//g;
  $text =~ s/\!//g;
  $text =~ s/\@//g;
  $text =~ s/\%//g;
  $text =~ s/\¹//g;
  $text =~ s/\:/-/g;
  $text =~ s/\;/-/g; 
  $text =~ s/\«//g;
  $text =~ s/\»//g;
  $text =~ s/\_//g;
  $text =~ s/\(/-/g;
  $text =~ s/\)//g;
  $text =~ s/\[/-/g;
  $text =~ s/\]//g;  
  $text =~ s/\{/-/g;
  $text =~ s/\}//g;  
  $text =~ s/\°//g; 
  $text =~ s/\+/-/g;
  $text =~ s/\//-/g;
  $text =~ s/(-)+/-/g;
  return $text;
}


sub trans_html
{
  my $text = shift;
  
	$text =~ s/\'/\\'/g;
	
  return $text;
}

sub trans_new
{
  my $text = shift;
	$text =~ s/^\s+//g;
	$text =~ s/\s+$//g;  
	$text =~ s/\'/\\'/g;
	$text =~ s/&quot;/"/g;
	
  return $text;
}

sub trans_edit
{
  my $text = shift;
  
  $text =~ s/\"/&quot;/g;
  
  return $text;
}

sub upperString {

	my $text = shift; 

	return transformString($text, "upper");
}

sub upperFirstLetter {

	my $text = shift; 

	return transformString($text, "upperFirstLetter");
}

sub lowerString {

	my $text = shift; 

	return transformString($text, "lower");
}

sub transformString {
	my $text = shift;
	my $params = shift;
	if ($text && $params){
	
		my %mchars = ('à'=>'À','á'=>'Á','â'=>'Â','ã'=>'Ã','ä'=>'Ä',
		 'å'=>'Å','¸'=>'¨','æ'=>'Æ','ç'=>'Ç','è'=>'È','é'=>'É',
		 'ê'=>'Ê','ë'=>'Ë','ì'=>'Ì','í'=>'Í','î'=>'Î','ï'=>'Ï',
		 'ð'=>'Ð','ñ'=>'Ñ','ò'=>'Ò','ó'=>'Ó','ô'=>'Ô','õ'=>'Õ',
		 'ö'=>'Ö','÷'=>'×','ø'=>'Ø','ù'=>'Ù','ú'=>'Ú','û'=>'Û',
		 'ü'=>'Ü','ý'=>'Ý','þ'=>'Þ','ÿ'=>'ß','a'=>'A','b'=>'B',
		 'c'=>'C','d'=>'D','e'=>'E','f'=>'F','g'=>'G','h'=>'H',
		 'i'=>'I','j'=>'J','k'=>'K','l'=>'L','m'=>'M','n'=>'N',
		 'o'=>'O','p'=>'P','q'=>'Q','r'=>'R','s'=>'S','t'=>'T',
		 'u'=>'U','o'=>'O','u'=>'U','v'=>'V','w'=>'W','x'=>'X',
		 'y'=>'Y','z'=>'Z');
		 
		if ($params eq "upper"){
			for my $c (keys %mchars) {
				$text =~ s/$c/$mchars{$c}/g;
			}
		}
		elsif ($params eq "lower"){
			for my $c (keys %mchars) {
				$text =~ s/$mchars{$c}/$c/g;
			}
		}	
		return $text;
	}
	elsif ($params eq "upperFirstLetter"){
		$text =~ s/^à/À/g;
		$text =~ s/^á/Á/g;
		$text =~ s/^â/Â/g;
		$text =~ s/^ã/Ã/g;
		$text =~ s/^ä/Ä/g;
		$text =~ s/^å/Å/g;
		$text =~ s/^¸/¨/g;
		$text =~ s/^æ/Æ/g;
		$text =~ s/^ç/Ç/g;
		$text =~ s/^è/È/g;
		$text =~ s/^é/É/g;
		$text =~ s/^ê/Ê/g;
		$text =~ s/^ë/Ë/g;
		$text =~ s/^ì/Ì/g;
		$text =~ s/^í/Í/g;
		$text =~ s/^î/Î/g;
		$text =~ s/^ï/Ï/g;
		$text =~ s/^ð/Ð/g;
		$text =~ s/^ñ/Ñ/g;
		$text =~ s/^ò/Ò/g;
		$text =~ s/^ó/Ó/g;
		$text =~ s/^ô/Ô/g;
		$text =~ s/^õ/Õ/g;
		$text =~ s/^ö/Ö/g;
		$text =~ s/^÷/×/g;
		$text =~ s/^ø/Ø/g;
		$text =~ s/^ù/Ù/g;
		$text =~ s/^ú/Ú/g;
		$text =~ s/^û/Û/g;
		$text =~ s/^ü/Ü/g;
		$text =~ s/^ý/Ý/g;
		$text =~ s/^þ/Þ/g;
		$text =~ s/^ÿ/ß/g;
		$text =~ s/^a/A/g;
		$text =~ s/^b/B/g;
		$text =~ s/^c/C/g;
		$text =~ s/^d/D/g;
		$text =~ s/^e/E/g;
		$text =~ s/^f/F/g;
		$text =~ s/^g/G/g;
		$text =~ s/^h/H/g;
		$text =~ s/^i/I/g;
		$text =~ s/^j/J/g;
		$text =~ s/^k/K/g;
		$text =~ s/^l/L/g;
		$text =~ s/^m/M/g;
		$text =~ s/^n/N/g;
		$text =~ s/^o/O/g;
		$text =~ s/^p/P/g;
		$text =~ s/^q/Q/g;
		$text =~ s/^r/R/g;
		$text =~ s/^s/S/g;
		$text =~ s/^t/T/g;
		$text =~ s/^u/U/g;
		$text =~ s/^v/V/g;
		$text =~ s/^w/W/g;
		$text =~ s/^x/X/g;
		$text =~ s/^y/Y/g;
		$text =~ s/^z/Z/g;
		return $text;
	}
}

1;