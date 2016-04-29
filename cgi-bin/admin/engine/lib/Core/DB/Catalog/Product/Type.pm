package Core::DB::Catalog::Product::Type;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				't_name' => "NULL",
				't_pos' => 1,
				't_pid' => 0,				
				't_desc' => "NULL",
				't_title' => "NULL",
				't_meta_desc' => "NULL",
				't_meta_key' => "NULL",				
				't_date_add' => "NOW()",
				't_date_up' => "NOW()",
				't_show' => 1,
				't_show_head' => 1,			
				't_alias' => "NULL",
			);
			
my $TABLE = 'cat_product_type';
			
my %params = (
			_FIELDS => \%FIELDS,
			TABLE => $TABLE
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}

sub addProductType {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFields($params);
	
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE t_pid = ".$self->{FIELDS}->{t_pid}." ORDER BY t_pos DESC LIMIT 1");
	$self->{FIELDS}->{'t_pos'} = $res->[0]->{'t_pos'} + 1 if($res);
	
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

sub editProductType {
	my $self = shift;
	my $id = shift;
	my $params = shift;

	my %hash;
	my $query = "UPDATE `".$self->{TABLE}."` SET ";
	my @query;
	foreach my $item(keys %$params){
		if($self->{_FIELDS}->{$item} ne ""){
			$hash{$item} = $self->checked( $params->{$item} );
		}
	}
	
	foreach my $item(keys %hash){
		push(@query , "`$item` = ".$self->ignored( $hash{$item} ) );
	}
	$query .= join(",", @query)." WHERE t_id = '".$id."';";
	my $res = $self->update($query) if(scalar keys %hash > 0);
	return $res;
}

sub getProductType {
	my $self = shift;
	my $id = shift;
	
	my $result = $self->query("SELECT *, DATE_FORMAT(t_date_add, \"%Y-%m-%d\") as date_add, DATE_FORMAT(t_date_up, \"%Y-%m-%d\") as date_up FROM ".$self->{TABLE}." WHERE `t_id`='".$id."' LIMIT 1");
	return $result->[0] if($result && ref $result eq 'ARRAY');
}


1;