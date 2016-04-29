package Core::DB::Pages::Articles;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				'parent' => 0,
				'pos' => 1,
				'name' => "NULL",
				'title' => "NULL",
				'meta_desc' => "NULL",
				'meta_key' => "NULL",
				'alias' => "NULL",
				'redirect' => "NULL",
				'show' => 1,
				'show_head' => 1,
				'show_menu' => 1,
				'date' => "NOW()",
				'html' => "NULL",
				'maket' => "NULL",
			);
			
my $TABLE = 'articles';
			
my %params = (
			_FIELDS => \%FIELDS,
			TABLE => $TABLE
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}

sub add {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFields($params);
	
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE parent = ".$self->{FIELDS}->{parent}." ORDER BY pos DESC LIMIT 1");
	$self->{FIELDS}->{'pos'} = $res->[0]->{'pos'} + 1 if($res);
	
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

sub ChangePos {
	my $self = shift;
	my $id = shift;	
	my $params = shift;
	my %hash;
	
	foreach my $item(keys %$params){
		if($self->{_FIELDS}->{$item} ne ""){
			$hash{$item} = $params->{$item};
		}
	}
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE id = '".$id."' LIMIT 1");

	if( $hash{parent} && $res->[0]->{parent} == $hash{parent} ){
		my $MaxPos = $self->query("SELECT `pos` FROM `".$self->{TABLE}."` WHERE `parent`='".$res->[0]->{parent}."' ORDER BY pos DESC LIMIT 1");
		if(!$MaxPos){
			$MaxPos = 1;
		} else {
			$MaxPos = $MaxPos->[0]->{pos};
		}
		$hash{pos} = $MaxPos if( $MaxPos < $hash{pos} || !$hash{pos} );
		if( $hash{pos} < $res->[0]->{pos} ){
			$self->update("UPDATE `".$self->{TABLE}."` SET `pos`='-1' WHERE id='".$id."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `pos`=`pos`+1 WHERE `parent`='".$res->[0]->{parent}."' AND `pos` >= ".$hash{pos}." AND `pos` <= '".$res->[0]->{pos}."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `pos`=".$hash{pos}." WHERE id='".$id."'");
		} elsif( $hash{pos} > $res->[0]->{pos} ){
			$self->update("UPDATE `".$self->{TABLE}."` SET `pos`='-1' WHERE id='".$id."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `pos`=`pos`-1 WHERE `parent`='".$res->[0]->{parent}."' AND `pos` <= ".$hash{pos}." AND `pos` >= '".$res->[0]->{pos}."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `pos`=".$hash{pos}." WHERE id='".$id."'");
		}
	} else {
		my $MaxPos = $self->query("SELECT `pos` FROM `".$self->{TABLE}."` WHERE `parent`='".$hash{parent}."' ORDER BY pos DESC LIMIT 1");
		if(!$MaxPos){
			$MaxPos = 1;
		} else {
			$MaxPos = $MaxPos->[0]->{pos};
		}
		$hash{pos} = $MaxPos if( $MaxPos < $hash{pos} || !$hash{pos} );
		$self->update("UPDATE `".$self->{TABLE}."` SET `pos`='-1', `parent`='".$hash{parent}."' WHERE id='".$id."'");
		$self->update("UPDATE `".$self->{TABLE}."` SET `pos`= `pos`-1 WHERE `parent`='".$res->[0]->{parent}."' AND `pos`>='".$res->[0]->{pos}."'");
		$self->update("UPDATE `".$self->{TABLE}."` SET `pos`=`pos`+1 WHERE `parent`='".$hash{parent}."' AND `pos` >= ".$hash{pos});
		$self->update("UPDATE `".$self->{TABLE}."` SET `pos`=".$hash{pos}." WHERE id='".$id."'");
	} 	
}

1;