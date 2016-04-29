package Core::DB::Goals;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				'goal' => "NULL",
				'referrer' => "NULL",
				'start_url' => "NULL",
				'user_agent' => "NULL",
				'ip' => "NULL",
				'city' => "NULL",
				'date_goal' => "NOW()",
				'order_id' => "NULL",
				'p_id' => "NULL",
				'p_name' => "NULL",
				'p_count' => "NULL",
				'p_price' => "NULL"
			);
			
my $TABLE = 'goals';
			
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