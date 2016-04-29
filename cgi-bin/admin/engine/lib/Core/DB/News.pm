package Core::DB::News;

require Core::DB;
@ISA=qw(Core::DB);

use Core::DB::News::Strukture;
use strict;

sub new {
	my $class = shift;
	my $self = $class->SUPER::new() || return undef;
	
	return $self;
}

sub add {
	my $self = shift;
	my $params = shift;
	
	my $news = new Core::DB::News::Strukture;
	
	return $news->add($params);
}

sub PosUp {
	my $self = shift;
	my $params = shift;
	
	my $news = new Core::DB::News::Strukture;
	
	return $news->PosUp($params);
}

sub PosDown {
	my $self = shift;
	my $params = shift;
	
	my $news = new Core::DB::News::Strukture;
	
	return $news->PosDown($params);
}

sub edit {
	my $self = shift;
	my $id = shift;
	my $params = shift;

	my $news = new Core::DB::News::Strukture;
	
	my %hash;
	my $query = "UPDATE `".$news->{TABLE}."` SET ";
	my @query;
	foreach my $item(keys %$params){
		if($news->{_FIELDS}->{$item} ne ""){
			$hash{$item} = $news->checked( $params->{$item} );
		}
	}
	
	$news->ChangePos($id, {'pos'=>$hash{pos}, 'parent'=>$hash{parent}} );
	delete($hash{pos});
	delete($hash{parent});
	
	
	foreach my $item(keys %hash){
		push(@query , "`$item` = ".$news->ignored( $hash{$item} ) );
	}
	$query .= join(",", @query)." WHERE id = '".$id."';";
	my $res = $news->update($query) if(scalar keys %hash > 0);
	return $res;
}

sub del {
	my $self = shift;
	my $id = shift || undef;
	
	my $news = new Core::DB::News::Strukture;
	subdel($id);
	
	sub subdel{
		my $id = shift;
		while(my $res = $self->query("SELECT id FROM `".$news->{TABLE}."` WHERE parent = '".$id."' OR id='".$id."' LIMIT 1") ){
			my $query = "DELETE FROM `".$news->{TABLE}."` ";
			$query .= "WHERE id='".$id."'" if($id);
			$news->delete($query);
			subdel($res->[0]->{id});
		}
	}
}

sub lamp_on {
	my $self = shift;
	my $params = shift;
	
	my $news = new Core::DB::News::Strukture;
	
	return $news->lamp_on($params);
}

sub lamp_off {
	my $self = shift;
	my $params = shift;
	
	my $news = new Core::DB::News::Strukture;
	
	return $news->lamp_off($params);
}


1;