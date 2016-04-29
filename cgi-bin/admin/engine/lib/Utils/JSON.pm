package Utils::JSON;

use Exporter;
our @ISA	= qw(Exporter);
our @EXPORT = qw(JSON_take JSON_result);

use JSON;

sub JSON_take {

	my $params = shift;
	
	if ($params){
		return JSON->new()->decode($params);
	}
}

sub JSON_result {

	my $params = shift;
	
	if ($params){
		return JSON->new->allow_nonref()->encode({%{$params}});
	}
}

1;