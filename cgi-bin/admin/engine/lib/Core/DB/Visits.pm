package Core::DB::Visits;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				'referrer' => "NULL",
				'start_url' => "NULL",
				'user_agent' => "NULL",
				'ip' => "NULL",
				'date' => "NOW()"
			);
			
my $TABLE = 'visitors';
			
my %params = (
			_FIELDS => \%FIELDS,
			TABLE => $TABLE
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}

sub add {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFields($params);
	
	my $keys = "`".join("`, `",keys %{$self->{FIELDS}} )."`";
	my $values = join(", ", values %{$self->{FIELDS}} );
	my $query = "INSERT INTO `".$self->{TABLE}."`($keys) VALUES($values);";
	my $res = $self->insert($query);
	if(ref($res) eq 'ARRAY'){
		$self->clearFields;
		return $res if($rows);
	} else {
		$self->clearFields;
		return \$res;
	} 
}

1;