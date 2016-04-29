package Core::DB::Articles;

require Core::DB;
@ISA=qw(Core::DB);

use Core::DB::Pages::Articles;
use strict;

sub new {
	my $class = shift;
	my $self = $class->SUPER::new() || return undef;
	
	return $self;
}

sub add {
	my $self = shift;
	my $params = shift;
	
	my $articles = new Core::DB::Pages::Articles;
	
	return $articles->add($params);
}

sub edit {
	my $self = shift;
	my $id = shift;
	my $params = shift;

	my $articles = new Core::DB::Pages::Articles;
	
	my %hash;
	my $query = "UPDATE `".$articles->{TABLE}."` SET ";
	my @query;
	foreach my $item(keys %$params){
		if($articles->{_FIELDS}->{$item} ne ""){
			$hash{$item} = $articles->checked( $params->{$item} );
		}
	}
	
	$articles->ChangePos($id, {'pos'=>$hash{pos}, 'parent'=>$hash{parent}} );
	delete($hash{pos});
	delete($hash{parent});
	
	
	foreach my $item(keys %hash){
		push(@query , "`$item` = ".$articles->ignored( $hash{$item} ) );
	}
	$query .= join(",", @query)." WHERE id = '".$id."';";
	my $res = $articles->update($query) if(scalar keys %hash > 0);
	return $res;
}

sub del {
	my $self = shift;
	my $id = shift || undef;
	
	my $articles = new Core::DB::Pages::Articles;
	subdel($id);
	
	sub subdel{
		my $id = shift;
		while(my $res = $self->query("SELECT id FROM `".$articles->{TABLE}."` WHERE parent = '".$id."' OR id='".$id."' LIMIT 1") ){
			my $query = "DELETE FROM `".$articles->{TABLE}."` ";
			$query .= "WHERE id='".$id."'" if($id);
			$articles->delete($query);
			subdel($res->[0]->{id});
		}
	}
}


1;