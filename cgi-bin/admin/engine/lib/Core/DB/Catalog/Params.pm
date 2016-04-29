package Core::DB::Catalog::Params;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				'p_id' => "NULL",
				'field' => "NULL",
				'value' => "NULL",
				'unic' => 0,
			);
			
my %FIELDS_set = (
				'cat_id' => 0,
				'f_name' => "NULL",
				'type' => "NULL",
				'f_pos' => 1,
			);

my %FIELDS_var = (
				'f_id' => "NULL",
				'varible' => "NULL"
			);			
			
my $TABLE = 'cat_product_fields';
my $TABLE_set = 'cat_product_fields_set';
my $TABLE_var = 'cat_product_fields_var';
			
my %params = (
			_FIELDS => \%FIELDS,
			_FIELDS_set => \%FIELDS_set,
			_FIELDS_var => \%FIELDS_var,
			TABLE => $TABLE,
			TABLE_set => $TABLE_set,
			TABLE_var => $TABLE_var
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}	

sub addParam {
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

sub addParamSet {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFieldsName($params, "FIELDS_set");
	
	my $res = $self->query("SELECT * FROM `".$self->{TABLE_set}."` WHERE cat_id = ".$self->{FIELDS_set}->{cat_id}." ORDER BY f_pos DESC LIMIT 1");
	$self->{FIELDS_set}->{'f_pos'} = $res->[0]->{'f_pos'} + 1 if($res);
	
	my $keys = "`".join("`, `",keys %{$self->{FIELDS_set}} )."`";
	my $values = join(", ", values %{$self->{FIELDS_set}} );
	my $query = "INSERT INTO `".$self->{TABLE_set}."`($keys) VALUES($values);";
	my $res = $self->insert($query);
	if(ref($res) eq 'ARRAY'){
		$self->clearFields;
		return $res if($rows);
	} else {
		$self->clearFields;
		return \$res;
	} 
}

sub addParamVar {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFieldsName($params, "FIELDS_var");

	my $keys = "`".join("`, `",keys %{$self->{FIELDS_var}} )."`";
	my $values = join(", ", values %{$self->{FIELDS_var}} );

	my $query = "INSERT INTO `".$self->{TABLE_var}."`($keys) VALUES($values);";
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