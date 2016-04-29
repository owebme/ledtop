package Core::DB::Catalog::Category;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				'c_name' => "NULL",
				'c_name_short' => "NULL",
				'c_name_org' => "NULL",
				'c_name_id' => "NULL",
				'c_pos' => 1,
				'c_pid' => 0,
				'c_supplier' => 0,
				'c_desc_top' => "NULL",
				'c_desc_bottom' => "NULL",
				'c_desc_sm' => "NULL",
				'c_title' => "NULL",
				'c_meta_desc' => "NULL",
				'c_meta_key' => "NULL",				
				'c_date_add' => "NOW()",
				'c_date_up' => "NOW()",
				'c_show' => 1,
				'c_show_head' => 1,
				'c_show_menu' => 1,
				'c_hide_child' => 0,
				'c_show_child_count' => "NULL",	
				'c_alias' => "NULL",
				'c_redirect' => "NULL",
				'c_maket' => "NULL",
			);
			
my $TABLE = 'cat_category';
			
my %params = (
			_FIELDS => \%FIELDS,
			TABLE => $TABLE
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}

sub addCat {
	my $self = shift;
	my $params = shift;
	
	$self->getFields($params);
	
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE c_pid = ".$self->{FIELDS}->{c_pid}." ORDER BY c_pos DESC LIMIT 1");
	$self->{FIELDS}->{'c_pos'} = $res->[0]->{'c_pos'} + 1 if($res);
	
	my $keys = "`".join("`, `",keys %{$self->{FIELDS}} )."`";
	my $values = join(", ", values %{$self->{FIELDS}} );
	my $query = "INSERT INTO `".$self->{TABLE}."`($keys) VALUES($values);";
	my $res = $self->insert($query);
	if(ref($res) eq 'ARRAY'){
		$self->clearFields;
		return $res;
	} else {
		$self->clearFields;
		return $res;
	} 
}

sub editCat {
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
	
	$self->ChangePos($id, {'c_pos'=>$hash{c_pos}, 'c_pid'=>$hash{c_pid}} );
	delete($hash{c_pos});
	delete($hash{c_pid});
	
	
	foreach my $item(keys %hash){
		push(@query , "`$item` = ".$self->ignored( $hash{$item} ) );
	}
	$query .= join(",", @query)." WHERE c_id = '".$id."';";
	my $res = $self->update($query) if(scalar keys %hash > 0);
	return $res;
}

sub delCat {
	my $self = shift;
	my $id = shift || undef;

	subdel($id);
	
	sub subdel{
		my $id = shift;
		while(my $res = $self->query("SELECT c_id FROM `".$self->{TABLE}."` WHERE c_pid = '".$id."' OR c_id='".$id."' LIMIT 1") ){
			my $query = "DELETE FROM `".$self->{TABLE}."` ";
			$query .= "WHERE c_id='".$id."'" if($id);
			$self->delete($query);
			my $res_rel = $self->query("SELECT cat_p_id FROM `cat_product_rel` WHERE cat_id IN (".$id.", ".$res->[0]->{c_id}.") AND cat_main='1'");
			if ($res_rel){
				foreach my $line(@$res_rel){
					$self->delete("DELETE FROM `cat_product` WHERE p_id = '".$line->{cat_p_id}."'");
					$self->delete("DELETE FROM `cat_product_fields` WHERE p_id = '".$line->{cat_p_id}."'");
					$self->delete("DELETE FROM `cat_product_rel` WHERE cat_p_id = '".$line->{cat_p_id}."'");
				}
			}
			$self->delete("DELETE FROM `cat_product_fields_set` WHERE cat_id IN (".$id.", ".$res->[0]->{c_id}.")");
			subdel($res->[0]->{c_id});
		}
	}
}

sub getCat {
	my $self = shift;
	my $id = shift;
	
	my $result = $self->query("SELECT *, DATE_FORMAT(c_date_add, \"%Y-%m-%d\") as date_add, DATE_FORMAT(c_date_up, \"%Y-%m-%d\") as date_up FROM ".$self->{TABLE}." WHERE `c_id`='".$id."' LIMIT 1");
	return $result->[0] if($result && ref $result eq 'ARRAY');
}

sub PosDown {
	my $self = shift;
	my $id = shift;
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE c_id = '".$id."' LIMIT 1");
	my $MaxPos = $self->query("SELECT `c_pos` FROM `".$self->{TABLE}."` WHERE `c_pid`='".$res->[0]->{c_pid}."' ORDER BY c_pos DESC LIMIT 1")->[0]->{c_pos};
	$self->ChangePos($id, {'c_pos'=>($res->[0]->{c_pos}+1>$MaxPos)?$MaxPos:$res->[0]->{c_pos}+1, 'c_pid' => $res->[0]->{c_pid}} );
}

sub PosUp {
	my $self = shift;
	my $id = shift;
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE c_id = '".$id."' LIMIT 1");
	$self->ChangePos($id, {'c_pos'=>($res->[0]->{c_pos}-1 > 0)?$res->[0]->{c_pos}-1:1 , 'c_pid' => $res->[0]->{c_pid} } );
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
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE c_id = '".$id."' LIMIT 1");

	if( $hash{c_pid} && $res->[0]->{c_pid} == $hash{c_pid} ){
		my $MaxPos = $self->query("SELECT `c_pos` FROM `".$self->{TABLE}."` WHERE `c_pid`='".$res->[0]->{c_pid}."' ORDER BY c_pos DESC LIMIT 1");
		if(!$MaxPos){
			$MaxPos = 1;
		} else {
			$MaxPos = $MaxPos->[0]->{c_pos};
		}
		$hash{c_pos} = $MaxPos if( $MaxPos < $hash{c_pos} || !$hash{c_pos} );
		if( $hash{c_pos} < $res->[0]->{c_pos} ){
			$self->update("UPDATE `".$self->{TABLE}."` SET `c_pos`='-1' WHERE c_id='".$id."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `c_pos`=`c_pos`+1 WHERE `c_pid`='".$res->[0]->{c_pid}."' AND `c_pos` >= ".$hash{c_pos}." AND `c_pos` <= '".$res->[0]->{c_pos}."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `c_pos`=".$hash{c_pos}." WHERE c_id='".$id."'");
		} elsif( $hash{c_pos} > $res->[0]->{c_pos} ){
			$self->update("UPDATE `".$self->{TABLE}."` SET `c_pos`='-1' WHERE c_id='".$id."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `c_pos`=`c_pos`-1 WHERE `c_pid`='".$res->[0]->{c_pid}."' AND `c_pos` <= ".$hash{c_pos}." AND `c_pos` >= '".$res->[0]->{c_pos}."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `c_pos`=".$hash{c_pos}." WHERE c_id='".$id."'");
		}
	} else {
		my $MaxPos = $self->query("SELECT `c_pos` FROM `".$self->{TABLE}."` WHERE `c_pid`='".$hash{c_pid}."' ORDER BY c_pos DESC LIMIT 1");
		if(!$MaxPos){
			$MaxPos = 1;
		} else {
			$MaxPos = $MaxPos->[0]->{c_pos};
		}
		$hash{c_pos} = $MaxPos if( $MaxPos < $hash{c_pos} || !$hash{c_pos} );
		$self->update("UPDATE `".$self->{TABLE}."` SET `c_pos`='-1', `c_pid`='".$hash{c_pid}."' WHERE c_id='".$id."'");
		$self->update("UPDATE `".$self->{TABLE}."` SET `c_pos`= `c_pos`-1 WHERE `c_pid`='".$res->[0]->{c_pid}."' AND `c_pos`>='".$res->[0]->{c_pos}."'");
		$self->update("UPDATE `".$self->{TABLE}."` SET `c_pos`=`c_pos`+1 WHERE `c_pid`='".$hash{c_pid}."' AND `c_pos` >= ".$hash{c_pos});
		$self->update("UPDATE `".$self->{TABLE}."` SET `c_pos`=".$hash{c_pos}." WHERE c_id='".$id."'");
	} 	
}

sub buildCatAlias {
	my $self = shift;
	my $name = shift;
	my $parent = shift;
	
	my $alias = Core::DB::Work::translit($name);
	
	my $result = $self->query("SELECT c_alias FROM `".$self->{TABLE}."` WHERE c_alias = '".$alias."';");
	if (ref($result) eq 'ARRAY'){$alias = $alias."2";}
	elsif ($parent ne "0"){
		my $p_alias ="";
		my $res = $self->query("SELECT c_id, c_alias FROM `".$self->{TABLE}."` WHERE c_id = '".$parent."';");		
		foreach my $item(@$res){
			$p_alias = $item->{c_alias};
		}
		$alias = $p_alias."/".$alias;
	}
	
	return $alias;
}


sub lamp_on_cat {
	my $self = shift;
	my $id = shift;
	$self->update("UPDATE `".$self->{TABLE}."` SET `c_show`='1' WHERE c_id='".$id."'");
}

sub lamp_off_cat {
	my $self = shift;
	my $id = shift;
	$self->update("UPDATE `".$self->{TABLE}."` SET `c_show`='0' WHERE c_id='".$id."'");
}

1;