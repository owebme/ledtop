package Core::DB::Catalog::Product::Hit;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				'hit_id' => "NULL",
				'p_ids' => "NULL",
				'p_pos' => 1,
			);
			
my $TABLE = 'cat_product_hits';

my %params = (
			_FIELDS => \%FIELDS,
			TABLE => $TABLE
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}

sub addProductHit {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFields($params);
	
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE hit_id = ".$self->{FIELDS}->{hit_id}." ORDER BY p_pos DESC LIMIT 1");
	$self->{FIELDS}->{'p_pos'} = $res->[0]->{'p_pos'} + 1 if($res);
	
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