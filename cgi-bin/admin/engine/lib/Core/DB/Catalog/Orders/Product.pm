package Core::DB::Catalog::Orders::Product;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				'order_id' => "NULL",
				'p_art' => "NULL",
				'p_name' => "NULL",
				'p_price' => "NULL",
				'p_price_value' => "NULL",
				'p_count' => "NULL",
			);
			
my $TABLE = 'cat_orders_product';
			
my %params = (
			_FIELDS => \%FIELDS,
			TABLE => $TABLE
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}

sub addOrderProduct {
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