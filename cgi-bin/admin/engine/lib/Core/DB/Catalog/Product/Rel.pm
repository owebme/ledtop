package Core::DB::Catalog::Product::Rel;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use strict;

my %FIELDS = (
				'cat_p_id' => "NULL",
				'cat_id' => 0,
				'cat_main' => "NULL",
				'p_pos' => 1,
			);
			
my $TABLE = 'cat_product_rel';
			
my %params = (
			_FIELDS => \%FIELDS,
			TABLE => $TABLE
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}

sub addProductRel {
	my $self = shift;
	my $params = shift;

	my ($rows, $id);
	$self->getFields($params);
	
	
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE cat_id = ".$self->{FIELDS}->{cat_id}." ORDER BY p_pos DESC LIMIT 1");
	$self->{FIELDS}->{'p_pos'} = $res->[0]->{'p_pos'} + 1 if($res);
	
	$self->{FIELDS}->{'cat_main'} = "1";	
	my $keys = "`".join("`, `",keys %{$self->{FIELDS}} )."`";
	my $values = join(", ", values %{$self->{FIELDS}} );
	my $query = "INSERT INTO `".$self->{TABLE}."`($keys) VALUES($values);";
	my $res = $self->insert($query);

	my $c_id = $self->{FIELDS}->{cat_id};
	my $cat_p_id = $self->{FIELDS}->{cat_p_id};
	
	my $result = $self->query("SELECT cat_category.c_id, cat_category.c_pid FROM cat_category WHERE c_id = ".$c_id."");
	foreach my $line(@$result){
		recParentCatAdd($line->{c_pid}, $cat_p_id);
	}
	
	sub recParentCatAdd {
		my $parent = shift;
		my $id = shift;
		my $result="";
		my $res_parent = $self->query("SELECT cat_category.c_id, cat_category.c_pid FROM cat_category WHERE c_id='".$parent."'");
		if ($res_parent){
			foreach my $line(@$res_parent){
				my $res="";
				if (my $ids = recParentCatAdd($line->{c_pid}, $id)){
					$res = $ids;
				}
				my $pos="";
				my $rec_pos = $self->query("SELECT ".$self->{TABLE}.".p_pos, ".$self->{TABLE}.".cat_id FROM ".$self->{TABLE}." WHERE cat_id = '".$line->{c_id}."' ORDER BY p_pos DESC LIMIT 1");
				if ($rec_pos){$pos = $rec_pos->[0]->{p_pos}+1;} else {$pos = 1;}
				my $query = "INSERT INTO `".$self->{TABLE}."` (cat_p_id,cat_id,p_pos,cat_main) VALUES(".$id.",".$line->{c_id}.",".$pos.", 0)";
				$self->insert($query);
				$result = $res;				
			}
		} else {
			return 0;
		}
		return $result;
	}	
		
	if(ref($res) eq 'ARRAY'){
		$self->clearFields;
		return $res if($rows);
	} else {
		$self->clearFields;
		return \$res;
	} 	
	
}

sub editProductRel {

	my $self = shift;
	my $id = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFields($params);	
	
	my $result = $self->query("SELECT * FROM ".$self->{TABLE}." WHERE cat_id = ".$self->{FIELDS}->{cat_id}." AND cat_p_id = ".$self->{FIELDS}->{cat_p_id}." AND cat_main = '1' LIMIT 1");
	if (ref($result) ne 'ARRAY'){
		
		my $query = "DELETE FROM ".$self->{TABLE}." WHERE cat_p_id = ".$self->{FIELDS}->{cat_p_id}."";
		$self->delete($query);
		
		my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE cat_id = ".$self->{FIELDS}->{cat_id}." ORDER BY p_pos DESC LIMIT 1");
		$self->{FIELDS}->{'p_pos'} = $res->[0]->{'p_pos'} + 1 if($res);
		
		$self->{FIELDS}->{'cat_main'} = "1";	
		my $keys = "`".join("`, `",keys %{$self->{FIELDS}} )."`";
		my $values = join(", ", values %{$self->{FIELDS}} );
		my $query = "INSERT INTO `".$self->{TABLE}."`($keys) VALUES($values);";
		my $res = $self->insert($query);
		
		my $c_id = $self->{FIELDS}->{cat_id};
		
		my $result = $self->query("SELECT cat_category.c_id, cat_category.c_pid FROM cat_category WHERE c_id = ".$c_id."");
		foreach my $line(@$result){
			recParentCatEdit($line->{c_pid});
		}
		
		sub recParentCatEdit {
			my $parent = shift;
			my $result="";
			my $res_parent = $self->query("SELECT cat_category.c_id, cat_category.c_pid FROM cat_category WHERE c_id='".$parent."'");
			if ($res_parent){
				foreach my $line(@$res_parent){
					my $res="";
					if (my $ids = recParentCatEdit($line->{c_pid})){
						$res = $ids;
					}
					my $pos="";
					my $rec_pos = $self->query("SELECT ".$self->{TABLE}.".p_pos, ".$self->{TABLE}.".cat_id FROM ".$self->{TABLE}." WHERE cat_id = '".$line->{c_id}."' ORDER BY p_pos DESC LIMIT 1");
					if ($rec_pos){$pos = $rec_pos->[0]->{p_pos}+1;} else {$pos = 1;}
					my $query = "INSERT INTO `".$self->{TABLE}."` (cat_p_id,cat_id,p_pos,cat_main) VALUES(".$self->{FIELDS}->{cat_p_id}.",".$line->{c_id}.",".$pos.", 0)";
					$self->insert($query);
					$result = $res;				
				}
			} else {
				return 0;
			}
			return $result;
		}	
		
		if(ref($res) eq 'ARRAY'){
			$self->clearFields;
			return $res if($rows);
		} else {
			$self->clearFields;
			return \$res;
		} 	
	}

}

sub PosDown {
	my $self = shift;
	my $id = shift;
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE cat_p_id = '".$id."' LIMIT 1");
	my $MaxPos = $self->query("SELECT `p_pos` FROM `".$self->{TABLE}."` WHERE `cat_id`='".$res->[0]->{cat_id}."' ORDER BY p_pos DESC LIMIT 1")->[0]->{p_pos};
	$self->ChangePos($id, {'p_pos'=>($res->[0]->{p_pos}+1>$MaxPos)?$MaxPos:$res->[0]->{p_pos}+1, 'cat_id' => $res->[0]->{cat_id}} );
}

sub PosUp {
	my $self = shift;
	my $id = shift;
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE cat_p_id = '".$id."' LIMIT 1");
	$self->ChangePos($id, {'p_pos'=>($res->[0]->{p_pos}-1 > 0)?$res->[0]->{p_pos}-1:1 , 'cat_id' => $res->[0]->{cat_id} } );
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
	my $res = $self->query("SELECT * FROM `".$self->{TABLE}."` WHERE cat_p_id = '".$id."' LIMIT 1");

	if( $hash{cat_id} && $res->[0]->{cat_id} == $hash{cat_id} ){
		my $MaxPos = $self->query("SELECT `p_pos` FROM `".$self->{TABLE}."` WHERE `cat_id`='".$res->[0]->{cat_id}."' ORDER BY p_pos DESC LIMIT 1");
		if(!$MaxPos){
			$MaxPos = 1;
		} else {
			$MaxPos = $MaxPos->[0]->{p_pos};
		}
		$hash{p_pos} = $MaxPos if( $MaxPos < $hash{p_pos} || !$hash{p_pos} );
		if( $hash{p_pos} < $res->[0]->{p_pos} ){
			$self->update("UPDATE `".$self->{TABLE}."` SET `p_pos`='-1' WHERE cat_p_id='".$id."' AND cat_id='".$res->[0]->{cat_id}."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `p_pos`=`p_pos`+1 WHERE `cat_id`='".$res->[0]->{cat_id}."' AND `p_pos` >= ".$hash{p_pos}." AND `p_pos` <= '".$res->[0]->{p_pos}."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `p_pos`=".$hash{p_pos}." WHERE cat_p_id='".$id."' AND cat_id='".$res->[0]->{cat_id}."'");
		} elsif( $hash{p_pos} > $res->[0]->{p_pos} ){
			$self->update("UPDATE `".$self->{TABLE}."` SET `p_pos`='-1' WHERE cat_p_id='".$id."' AND cat_id='".$res->[0]->{cat_id}."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `p_pos`=`p_pos`-1 WHERE `cat_id`='".$res->[0]->{cat_id}."' AND `p_pos` <= ".$hash{p_pos}." AND `p_pos` >= '".$res->[0]->{p_pos}."'");
			$self->update("UPDATE `".$self->{TABLE}."` SET `p_pos`=".$hash{p_pos}." WHERE cat_p_id='".$id."' AND cat_id='".$res->[0]->{cat_id}."'");
		}
	} else {
		my $MaxPos = $self->query("SELECT `p_pos` FROM `".$self->{TABLE}."` WHERE `cat_id`='".$hash{cat_id}."' ORDER BY p_pos DESC LIMIT 1");
		if(!$MaxPos){
			$MaxPos = 1;
		} else {
			$MaxPos = $MaxPos->[0]->{p_pos};
		}
		$hash{p_pos} = $MaxPos if( $MaxPos < $hash{p_pos} || !$hash{p_pos} );
		$self->update("UPDATE `".$self->{TABLE}."` SET `p_pos`='-1', `cat_id`='".$hash{cat_id}."' WHERE cat_p_id='".$id."' AND cat_id='".$res->[0]->{cat_id}."'");
		$self->update("UPDATE `".$self->{TABLE}."` SET `p_pos`= `p_pos`-1 WHERE `cat_id`='".$res->[0]->{cat_id}."' AND `p_pos`>='".$res->[0]->{p_pos}."'");
		$self->update("UPDATE `".$self->{TABLE}."` SET `p_pos`=`p_pos`+1 WHERE `cat_id`='".$hash{cat_id}."' AND `p_pos` >= ".$hash{p_pos});
		$self->update("UPDATE `".$self->{TABLE}."` SET `p_pos`=".$hash{p_pos}." WHERE cat_p_id='".$id."' AND cat_id='".$res->[0]->{cat_id}."'");
	} 	
}

1;