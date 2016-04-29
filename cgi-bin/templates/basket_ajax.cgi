# Статус корзины

sub build_BasketAjax
{
	my $count = shift;
	my $price = shift;

	if ($count > 0){
		$price =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
	}	
	return ($count."|".$price);
}

1;