package Core::DB::Catalog::Filters;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				'field' => "NULL",
				'name' => "NULL",
				'f_pid' => 0,
				'gid' => "NULL",
				'f_alias' => "NULL",
				'f_pos' => "NULL",
			);
			
my %FIELDS_set = (
				'field' => "NULL",
				'name' => "NULL",
				'f_pid' => 0,
			);

my %FIELDS_group = (
				'c_ids' => "NULL",
				'g_name' => "NULL",
			);			
			
my $TABLE = 'cat_product_filters';
my $TABLE_set = 'cat_product_filters_set';
my $TABLE_group = 'cat_product_filters_group';
			
my %params = (
			_FIELDS => \%FIELDS,
			_FIELDS_set => \%FIELDS_set,
			_FIELDS_group => \%FIELDS_group,
			TABLE => $TABLE,
			TABLE_set => $TABLE_set,
			TABLE_group => $TABLE_group
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}	

sub addFilter {
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

sub addFilterSet {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFieldsName($params, "FIELDS_set");
	
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

sub addFilterGroup {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFieldsName($params, "FIELDS_group");

	my $keys = "`".join("`, `",keys %{$self->{FIELDS_group}} )."`";
	my $values = join(", ", values %{$self->{FIELDS_group}} );

	my $query = "INSERT INTO `".$self->{TABLE_group}."`($keys) VALUES($values);";
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