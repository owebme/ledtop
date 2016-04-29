package Core::DB::Catalog::Product::Rec;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				'rec_id' => "NULL",
				'p_ids' => "NULL",
				'r_pos' => 1,
				'date_add' => "NOW()",
			);
			
my $TABLE = 'cat_product_recomend';

my %params = (
			_FIELDS => \%FIELDS,
			TABLE => $TABLE
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}

sub addProductRec {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFields($params);
	
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE rec_id = ".$self->{FIELDS}->{rec_id}." ORDER BY r_pos DESC LIMIT 1");
	$self->{FIELDS}->{'r_pos'} = $res->[0]->{'r_pos'} + 1 if($res);
	
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