package Core::DB::Catalog;

require Core::DB;
@ISA=qw(Core::DB);

use Core::DB::Catalog::Category;
use Core::DB::Catalog::Product;
use Core::DB::Catalog::Params;
use Core::DB::Catalog::Filters;
use Core::DB::Catalog::Orders;

use strict;

sub new {
	my $class = shift;
	my $self = $class->SUPER::new() || return undef;
	return $self;
}

sub getCat {
	my $self = shift;
	my $id = shift;
	
	my $cat = new Core::DB::Catalog::Category;
	return $cat->getCat($id);
}

sub PosUpCat {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Category;
	
	return $cat->PosUp($params);
}

sub PosDownCat {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Category;
	
	return $cat->PosDown($params);
}

sub PosUpProduct {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Product::Rel;
	
	return $cat->PosUp($params);
}

sub PosDownProduct {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Product::Rel;
	
	return $cat->PosDown($params);
}

sub editCat {
	my $self = shift;
	my $id = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Category;
	
	return $cat->editCat($id, $params);
}

sub delCat {
	my $self = shift;
	my $id = shift;
	
	my $cat = new Core::DB::Catalog::Category;
	
	return $cat->delCat($id);
}

sub addCat {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Category;

	return $cat->addCat($params);
}

sub treeCat
{
	my $self = shift;
	my $id = shift || undef;
	my $parent = shift || undef;
	
	my $cat = new Core::DB::Catalog::Category;
	
    return $cat->treeCat($id, $parent);
}

sub buildCatAlias {
	my $self = shift;
	my $name = shift;
	my $parent = shift;
	
	my $cat = new Core::DB::Catalog::Category;

	return $cat->buildCatAlias($name, $parent);
}

sub lamp_on_cat {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Category;
	
	return $cat->lamp_on_cat($params);
}

sub lamp_off_cat {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Category;
	
	return $cat->lamp_off_cat($params);
}

sub getAllProduct {
	my $self = shift;
	my $id = shift;	
	my $p = new Core::DB::Catalog::Product;
	return $p->getAllProduct($id);
}

sub getAllProductCat {
	my $self = shift;
	my $id = shift;
	my $p = new Core::DB::Catalog::Product;
	return $p->getAllProductCat($id);
}

sub getEditOrder {
	my $self = shift;
	my $id = shift;	
	my $p = new Core::DB::Catalog::Orders;
	return $p->getEditOrder;
}
sub getNewAllOrders {
	my $self = shift;
	my $p = new Core::DB::Catalog::Orders;
	return $p->getNewAllOrders;
}
sub getReadyAllOrders {
	my $self = shift;
	my $p = new Core::DB::Catalog::Orders;
	return $p->getReadyAllOrders;
}
sub getDelAllOrders {
	my $self = shift;
	my $p = new Core::DB::Catalog::Orders;
	return $p->getDelAllOrders;
}

sub addProduct {
	my $self = shift;
	my $params = shift;
	my $p = new Core::DB::Catalog::Product;
	return $p->addProduct($params);
}

sub addProductRel {
	my $self = shift;
	my $params = shift;
	my $p = new Core::DB::Catalog::Product::Rel;
	return $p->addProductRel($params);
}

sub getProductType {
	my $self = shift;
	my $id = shift;
	
	my $cat = new Core::DB::Catalog::Product::Type;
	return $cat->getProductType($id);
}

sub addProductType {
	my $self = shift;
	my $params = shift;
	my $p = new Core::DB::Catalog::Product::Type;
	return $p->addProductType($params);
}

sub editProductType {
	my $self = shift;
	my $id = shift;
	my $params = shift;
	my $p = new Core::DB::Catalog::Product::Type;
	return $p->editProductType($id, $params);
}

sub addProductRec {
	my $self = shift;
	my $params = shift;
	my $p = new Core::DB::Catalog::Product::Rec;
	return $p->addProductRec($params);
}

sub addProductHit {
	my $self = shift;
	my $params = shift;
	my $p = new Core::DB::Catalog::Product::Hit;
	return $p->addProductHit($params);
}

sub delProduct {
	my $self = shift;
	my $id = shift;
	my $p = new Core::DB::Catalog::Product;
	return $p->delProduct($id);
}

sub editProduct {
	my $self = shift;
	my $id = shift;
	my $params = shift;
	my $p = new Core::DB::Catalog::Product;
	return $p->editProduct($id, $params);
}

sub editProductRel {
	my $self = shift;
	my $id = shift;
	my $params = shift;
	my $p = new Core::DB::Catalog::Product::Rel;
	return $p->editProductRel($id, $params);
}

sub getProduct {
	my $self = shift;
	my $id = shift;
	my $p = new Core::DB::Catalog::Product;
	return $p->getProduct($id);
}

sub lamp_on_product {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Product;
	
	return $cat->lamp_on_product($params);
}

sub lamp_off_product {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Product;
	
	return $cat->lamp_off_product($params);
}

sub addOrder {
	my $self = shift;
	my $params = shift;
	my $p = new Core::DB::Catalog::Orders;
	return $p->addOrder($params);
}

sub addOrderProduct {
	my $self = shift;
	my $params = shift;
	my $p = new Core::DB::Catalog::Orders::Product;
	return $p->addOrderProduct($params);
}

sub delType {
	my $self = shift;
	my $id = shift || undef;
	
	my $type = new Core::DB::Catalog::Product::Type;
	subdel($id);
	
	sub subdel{
		my $id = shift;
		while(my $res = $self->query("SELECT t_id FROM `".$type->{TABLE}."` WHERE t_pid = '".$id."' OR t_id='".$id."' LIMIT 1") ){
			my $query = "DELETE FROM `".$type->{TABLE}."` ";
			$query .= "WHERE t_id='".$id."'" if($id);
			$type->delete($query);
			subdel($res->[0]->{t_id});
		}
	}
}

sub addParam {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Params;

	return $cat->addParam($params);
}

sub addParamSet {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Params;

	return $cat->addParamSet($params);
}

sub addParamVar {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Params;

	return $cat->addParamVar($params);
}

sub addFilter {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Filters;

	return $cat->addFilter($params);
}

sub addFilterSet {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Filters;

	return $cat->addFilterSet($params);
}

sub addFilterGroup {
	my $self = shift;
	my $params = shift;
	
	my $cat = new Core::DB::Catalog::Filters;

	return $cat->addFilterGroup($params);
}

sub getPrivateCategories {
	my $self = shift;
	my $id = shift;
	
	my $category = new Core::DB::Catalog::Product;

	return $category->getPrivateCategories($id);
}

sub getPrivateProducts {
	my $self = shift;
	my $id = shift;
	my $params = shift;
	my $group_id = shift;
	my $group = shift;
	
	my $products = new Core::DB::Catalog::Product;

	return $products->getPrivateProducts($id, $params, $group_id, $group);
}

sub getDiscountPrice {
	my $self = shift;
	my $id = shift;
	my $price = shift;
	my $price_opt = shift;
	my $price_opt_large = shift;
	my $group = shift;
	my $category = shift;
	
	my $products = new Core::DB::Catalog::Product;

	return $products->getDiscountPrice($id, $price, $price_opt, $price_opt_large, $group, $category);
}

sub getPrivateGroupPrice {
	my $self = shift;
	my $id = shift;
	my $params = shift;
	
	my $products = new Core::DB::Catalog::Product;

	return $products->getPrivateGroupPrice($id, $params);
}

sub getPrivateBasket {
	my $self = shift;
	my $ids = shift;
	
	my $basket = new Core::DB::Catalog::Product;

	return $basket->getPrivateBasket($ids);
}
