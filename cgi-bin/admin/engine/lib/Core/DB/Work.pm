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
  $text =~ s/ � /-/g;
  $text =~ s/ - /-/g;
  $text =~ s/ � /-/g;
  $text =~ s/\_/-/g;  
  $text =~ y/�������������������������/abvgdeezijklmnoprstufh_y_e/;
  $text =~ y/�����Ũ�������������������/abvgdeezijklmnoprstufh_y_e/;
  $text =~ y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/;  
  my %mchars = ('�'=>'zh','�'=>'c','�'=>'ch','�'=>'sh','�'=>'sch',
     '�'=>'yu','�'=>'ya', '�'=>'zh','�'=>'c','�'=>'ch', '�'=>'sh',
     '�'=>'sch','�'=>'yu','�'=>'ya',' '=>'-');
  for my $c (keys %mchars) {
      $text =~ s/$c/$mchars{$c}/g;
  }
  $text =~ s/\,/-/g;
  $text =~ s/\.//g;
  $text =~ s/\?//g;
  $text =~ s/\!//g;
  $text =~ s/\@//g;
  $text =~ s/\%//g;
  $text =~ s/\�//g;
  $text =~ s/\:/-/g;
  $text =~ s/\;/-/g; 
  $text =~ s/\�//g;
  $text =~ s/\�//g;
  $text =~ s/\_//g;
  $text =~ s/\(/-/g;
  $text =~ s/\)//g;
  $text =~ s/\[/-/g;
  $text =~ s/\]//g;  
  $text =~ s/\{/-/g;
  $text =~ s/\}//g;  
  $text =~ s/\�//g; 
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
	
		my %mchars = ('�'=>'�','�'=>'�','�'=>'�','�'=>'�','�'=>'�',
		 '�'=>'�','�'=>'�','�'=>'�','�'=>'�','�'=>'�','�'=>'�',
		 '�'=>'�','�'=>'�','�'=>'�','�'=>'�','�'=>'�','�'=>'�',
		 '�'=>'�','�'=>'�','�'=>'�','�'=>'�','�'=>'�','�'=>'�',
		 '�'=>'�','�'=>'�','�'=>'�','�'=>'�','�'=>'�','�'=>'�',
		 '�'=>'�','�'=>'�','�'=>'�','�'=>'�','a'=>'A','b'=>'B',
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
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
		$text =~ s/^�/�/g;
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