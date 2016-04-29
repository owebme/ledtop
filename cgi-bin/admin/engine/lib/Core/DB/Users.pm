package Core::DB::Users;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

my %FIELDS_users = (
				'date_create' => "NULL",
				'name_f' => "NULL",
				'name' => "NULL",
				'name_m' => "NULL",
				'phone' => "NULL",
				'email' => "NULL",
				'pass' => "NULL",
				'person' => 1,
				'sendmail' => 1,
				'group' => "NULL"
			);	

my %FIELDS_users_data = (
				'user_id' => "NULL",
				'company' => "NULL",
				'ogrn' => "NULL",
				'inn' => "NULL",
				'kpp' => "NULL",
				'okpo' => "NULL",
				'raschet' => "NULL",
				'korchet' => "NULL",
				'bik' => "NULL"
			);	
			
my %FIELDS_users_group = (
				'g_name' => "NULL"
			);

my %FIELDS_users_group_category = (
				'group_id' => "NULL",
				'cat_id' => "NULL",
				'type' => "NULL"
			);			
			
my $TABLE_users = 'users';
my $TABLE_users_data = 'users_data';
my $TABLE_users_group = 'users_group';
my $TABLE_users_group_category = 'users_group_category';
			
my %params = (
			_FIELDS_users => \%FIELDS_users,
			_FIELDS_users_data => \%FIELDS_users_data,
			_FIELDS_users_group => \%FIELDS_users_group,
			_FIELDS_users_group_category => \%FIELDS_users_group_category,
			TABLE_users => $TABLE_users,
			TABLE_users_data => $TABLE_users_data,
			TABLE_users_group => $TABLE_users_group,
			TABLE_users_group_category => $TABLE_users_group_category
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}				

sub addUser {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFieldsName($params, "FIELDS_users");

	my $keys = "`".join("`, `",keys %{$self->{FIELDS_users}} )."`";
	my $values = join(", ", values %{$self->{FIELDS_users}} );

	my $query = "INSERT INTO `".$self->{TABLE_users}."`($keys) VALUES($values);";
	my $res = $self->insert($query);
}

sub addUserData {
	my $self = shift;
	my $id = shift;
	my $params = shift;
	
	my $result = $self->query("SELECT user_id FROM ".$self->{TABLE_users_data}." WHERE user_id = '".$id."'");

	if ($result){
		my %hash;
		my $query = "UPDATE `".$self->{TABLE_users_data}."` SET ";
		my @query;
		foreach my $item(keys %$params){
			if($self->{_FIELDS_users_data}->{$item} ne ""){
				$hash{$item} = $self->checked( $params->{$item} );
			}
		}
		
		foreach my $item(keys %hash){
			push(@query , "`$item` = ".$self->ignored( $hash{$item} ) );
		}
		$query .= join(",", @query)." WHERE user_id = '".$id."';";
		my $res = $self->update($query) if(scalar keys %hash > 0);
		return $res;
	}
	else {
		my ($rows, $id);
		$self->getFieldsName($params, "FIELDS_users_data");

		my $keys = "`".join("`, `",keys %{$self->{FIELDS_users_data}} )."`";
		my $values = join(", ", values %{$self->{FIELDS_users_data}} );

		my $query = "INSERT INTO `".$self->{TABLE_users_data}."`($keys) VALUES($values);";
		my $res = $self->insert($query);
	}
}

sub addUserGroup {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFieldsName($params, "FIELDS_users_group");

	my $keys = "`".join("`, `",keys %{$self->{FIELDS_users_group}} )."`";
	my $values = join(", ", values %{$self->{FIELDS_users_group}} );

	my $query = "INSERT INTO `".$self->{TABLE_users_group}."`($keys) VALUES($values);";
	my $res = $self->insert($query);
}

sub addUserGroupCategory {
	my $self = shift;
	my $params = shift;
	
	my ($rows, $id);
	$self->getFieldsName($params, "FIELDS_users_group_category");

	my $keys = "`".join("`, `",keys %{$self->{FIELDS_users_group_category}} )."`";
	my $values = join(", ", values %{$self->{FIELDS_users_group_category}} );

	my $query = "INSERT INTO `".$self->{TABLE_users_group_category}."`($keys) VALUES($values);";
	my $res = $self->insert($query);
}

sub editUser {
	my $self = shift;
	my $id = shift;
	my $params = shift;
	
	my %hash;
	my $query = "UPDATE `".$self->{TABLE_users}."` SET ";
	my @query;
	foreach my $item(keys %$params){
		if($self->{_FIELDS_users}->{$item} ne ""){
			$hash{$item} = $self->checked( $params->{$item} );
		}
	}
	
	foreach my $item(keys %hash){
		push(@query , "`$item` = ".$self->ignored( $hash{$item} ) );
	}
	$query .= join(",", @query)." WHERE id = '".$id."';";
	my $res = $self->update($query) if(scalar keys %hash > 0);
	return $res;
}

1;