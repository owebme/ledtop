package Core::DB::Catalog::Orders;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use Core::DB::Catalog::Category;
use Core::DB::Catalog::Orders::Product;
use strict;

my %FIELDS = (
				'order_date' => "NOW()",
				'user_id' => "NULL",
				'name' => "NULL",
				'phone' => "NULL",
				'ch_region' => "NULL",
				'city' => "NULL",
				'address' => "NULL",
				'index' => "NULL",
				'metro' => "NULL",
				'email' => "NULL",
				'comments' => "NULL",
				'delivery' => "NULL",
				'delivery_price' => "NULL",
				'dispatch' => "NULL",
				'num_dispatch' => "NULL",
				'manager' => "NULL",
				'status' => 0,
				'pay' => 0,
				'payment' => "NULL",
				'datePayment' => "NULL",
				'invoiceId' => "NULL",
				'total' => "NULL",
				'totalPayment' => "NULL",
				'start_title' => "NULL",
				'trafic_source' => "NULL",
				'keyword' => "NULL",
				'type_device' => "NULL",
			);
			
my $TABLE = 'cat_orders';
			
my %params = (
			_FIELDS => \%FIELDS,
			TABLE => $TABLE
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}

sub getEditOrder {
	my $self = shift;
	my $id = shift;
	
	my $query = "SELECT * FROM ".$self->{TABLE}." WHERE id = '".$id."'";
	my $result = $self->query($query);
	return $result if($result);
}
sub getNewAllOrders {
	my $self = shift;
	
	my $query = "SELECT *, DATE_FORMAT(order_date, \"%d-%m-%Y\") as date, DATE_FORMAT(order_date, \"%H:%i\") as time FROM ".$self->{TABLE}." WHERE status = '0' ORDER BY id DESC";
	my $result = $self->query($query);
	return $result if($result);
}
sub getReadyAllOrders {
	my $self = shift;
	
	my $query = "SELECT *, DATE_FORMAT(order_date, \"%d-%m-%Y\") as date, DATE_FORMAT(order_date, \"%H:%i\") as time FROM ".$self->{TABLE}." WHERE status = '1' ORDER BY id DESC";
	my $result = $self->query($query);
	return $result if($result);
}
sub getDelAllOrders {
	my $self = shift;
	
	my $query = "SELECT *, DATE_FORMAT(order_date, \"%d-%m-%Y\") as date, DATE_FORMAT(order_date, \"%H:%i\") as time FROM ".$self->{TABLE}." WHERE status = '2' ORDER BY id DESC";
	my $result = $self->query($query);
	return $result if($result);
}

sub getAllProductCat {
	my $self = shift;
	my $id = shift;
	my $rel = new Core::DB::Catalog::Product::Rel;
	my $cat = new Core::DB::Catalog::Category;
		
	my $query = "SELECT p.*, pl.p_pos, pl.cat_id FROM ".$self->{TABLE}." AS p JOIN ".$rel->{TABLE}." AS pl ON(pl.cat_p_id=p.p_id) JOIN ".$cat->{TABLE}." AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$id."' ORDER BY pl.p_pos ASC";
	my $result = $self->query($query);
	return $result if($result);
}

sub addOrder {
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

sub delOrder {
	my $self = shift;
	my $id = shift;
	my $rel = new Core::DB::Catalog::Product::Rel;
	$self->delete("DELETE FROM ".$self->{TABLE}." WHERE p_id = '".$id."'");
	return $self->delete("DELETE FROM ".$rel->{TABLE}." WHERE cat_p_id = '".$id."'");
}

sub editOrder {
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
	$query .= join(",", @query)." WHERE p_id = '".$id."';";
	my $res = $self->update($query) if(scalar keys %hash > 0);
	return $res;
}

sub getProduct {
	my $self = shift;
	my $id = shift;
	my $rel = new Core::DB::Catalog::Product::Rel;
	my $cat = new Core::DB::Catalog::Category;
		
	my $query = "SELECT p.*, pl.p_pos, pl.cat_id, DATE_FORMAT(p_date_add, \"%Y-%m-%d\") as date_add, DATE_FORMAT(p_date_up, \"%Y-%m-%d\") as date_up FROM ".$self->{TABLE}." AS p JOIN ".$rel->{TABLE}." AS pl ON(pl.cat_p_id=p.p_id) JOIN ".$cat->{TABLE}." AS c ON(c.c_id = pl.cat_id) WHERE p.p_id = '".$id."' LIMIT 1;";
	my $result = $self->query($query);
	return $result->[0] if($result && ref $result eq 'ARRAY');
	
}

sub lamp_on_product {
	my $self = shift;
	my $id = shift;
	$self->update("UPDATE `".$self->{TABLE}."` SET `p_show`='1' WHERE p_id='".$id."'");
}

sub lamp_off_product {
	my $self = shift;
	my $id = shift;
	$self->update("UPDATE `".$self->{TABLE}."` SET `p_show`='0' WHERE p_id='".$id."'");
}

1;