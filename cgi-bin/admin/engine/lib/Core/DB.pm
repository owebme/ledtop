package Core::DB;

use strict;
use Core::Config;

use DBI;

sub new {
	my $class = shift;
	my $encoding = shift;
	
	my $self = {};
	bless $self, $class;
	
	$self->{host} = %Core::Config::DB->{host};
	$self->{user} = %Core::Config::DB->{user};
	$self->{password} = %Core::Config::DB->{password};
	$self->{db} = %Core::Config::DB->{db};	
	
	my $dsn = "DBI:mysql:database=".$self->{db}.";host=".$self->{host}.";port=3306";
	
	$self->{dbh} = DBI->connect( $dsn, $self->{user}, $self->{password} ) or die("MYSQL: Connect for base error!");
	
	if ($encoding eq "utf8"){
		$self->{dbh}->do("SET CHARACTER SET utf8");
		$self->{dbh}->do("SET NAMES utf8");
	}
	else {
		$self->{dbh}->do("SET CHARACTER SET cp1251");
		$self->{dbh}->do("SET NAMES cp1251");
	}
		
	return($self);
}

sub check_connect {
	my $class = shift;
	
	my $self = {};
	bless $self, $class;
	
	$self->{host} = %Core::Config::DB->{host};
	$self->{user} = %Core::Config::DB->{user};
	$self->{password} = %Core::Config::DB->{password};
	$self->{db} = %Core::Config::DB->{db};
	
	my $dsn = "DBI:mysql:database=".$self->{db}.";host=".$self->{host}.";port=3306";
	
	$self->{dbh} = DBI->connect( $dsn, $self->{user}, $self->{password} );
		
	return($self->{dbh});
}

sub query{
	my $self = shift;
	
	my $query = shift;
	my $sth = $self->{dbh}->prepare($query);
	
	$sth->execute or return $self->{dbh}->errstr;
	
	if($sth->rows > 0){
		my @result;
		while(my $row = $sth->fetchrow_hashref){
			push(@result, $row);
		}
		$sth->finish;
		return \@result;
	} else {
		$sth->finish;
		return 0;
	}
}

sub insert {
	my $self = shift;
	my $query = shift;
	my $rows = $self->{dbh}->do($query) or return $self->errors( $self->{dbh}->err );

	return $self->{dbh}->{mysql_insertid} if($rows);
}

sub delete{
	my $self = shift;
	my $query = shift;
	return $self->{dbh}->do($query) or return $self->errors( $self->{dbh}->err );
}

sub update{
	my $self = shift;
	my $query = shift;
	my $rows = $self->{dbh}->do($query) or return $self->errors( $self->{dbh}->err );
	
	my @rHash = ( $rows );
	return \@rHash if($rows);
}

sub errors{
	my $self = shift;
	my $code = shift;
	
	my %ERRORS = (
					1062 => 'В базе существует такая запись.'
				);
	
	return $ERRORS{$code};
}
1;

