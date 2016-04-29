package Core::DB::Pages;

require Core::DB;
@ISA=qw(Core::DB);

use Core::DB::Pages::Strukture;
use Core::DB::Que::Questions;
use strict;

sub new {
	my $class = shift;
	my $self = $class->SUPER::new() || return undef;
	
	return $self;
}

sub add {
	my $self = shift;
	my $params = shift;
	
	my $pages = new Core::DB::Pages::Strukture;
	
	return $pages->add($params);
}

sub addQuestion {
	my $self = shift;
	my $params = shift;
	
	my $que = new Core::DB::Que::Questions;
	
	return $que->addQuestion($params);
}

sub PosUp {
	my $self = shift;
	my $params = shift;
	
	my $pages = new Core::DB::Pages::Strukture;
	
	return $pages->PosUp($params);
}

sub PosDown {
	my $self = shift;
	my $params = shift;
	
	my $pages = new Core::DB::Pages::Strukture;
	
	return $pages->PosDown($params);
}

sub edit {
	my $self = shift;
	my $id = shift;
	my $params = shift;

	my $pages = new Core::DB::Pages::Strukture;
	
	my %hash;
	my $query = "UPDATE `".$pages->{TABLE}."` SET ";
	my @query;
	foreach my $item(keys %$params){
		if($pages->{_FIELDS}->{$item} ne ""){
			$hash{$item} = $pages->checked( $params->{$item} );
		}
	}
	
	$pages->ChangePos($id, {'pos'=>$hash{pos}, 'parent'=>$hash{parent}} );
	delete($hash{pos});
	delete($hash{parent});
	
	
	foreach my $item(keys %hash){
		push(@query , "`$item` = ".$pages->ignored( $hash{$item} ) );
	}
	$query .= join(",", @query)." WHERE id = '".$id."';";
	my $res = $pages->update($query) if(scalar keys %hash > 0);
	return $res;
}

sub del {
	my $self = shift;
	my $id = shift || undef;
	
	my $pages = new Core::DB::Pages::Strukture;
	subdel($id);
	
	sub subdel{
		my $id = shift;
		while(my $res = $self->query("SELECT id FROM `".$pages->{TABLE}."` WHERE parent = '".$id."' OR id='".$id."' LIMIT 1") ){
			my $query = "DELETE FROM `".$pages->{TABLE}."` ";
			$query .= "WHERE id='".$id."'" if($id);
			$pages->delete($query);
			subdel($res->[0]->{id});
		}
	}
}

sub lamp_on {
	my $self = shift;
	my $params = shift;
	
	my $pages = new Core::DB::Pages::Strukture;
	
	return $pages->lamp_on($params);
}

sub lamp_off {
	my $self = shift;
	my $params = shift;
	
	my $pages = new Core::DB::Pages::Strukture;
	
	return $pages->lamp_off($params);
}


1;