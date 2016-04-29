# Net::Cmd.pm
#
# Copyright (c) 1995-1997 Graham Barr <gbarr@pobox.com>. All rights reserved.

package Net::Cmd;

require 5.001;
require Exporter;

use strict;
use vars qw(@ISA @EXPORT $VERSION);
use Carp;

$VERSION = "2.12";
@ISA     = qw(Exporter);
@EXPORT  = qw(CMD_INFO CMD_OK CMD_MORE CMD_REJECT CMD_ERROR CMD_PENDING);

sub CMD_INFO	{ 1 }
sub CMD_OK	{ 2 }
sub CMD_MORE	{ 3 }
sub CMD_REJECT	{ 4 }
sub CMD_ERROR	{ 5 }
sub CMD_PENDING { 0 }

my %debug = ();

sub _print_isa
{
 no strict qw(refs);

 my $pkg = shift;
 my $cmd = $pkg;

 $debug{$pkg} ||= 0;

 my %done = ();
 my @do   = ($pkg);
 my %spc = ( $pkg , "");

 print STDERR "\n";
 while ($pkg = shift @do)
  {
   next if defined $done{$pkg};

   $done{$pkg} = 1;

   my $v = defined ${"${pkg}::VERSION"}
                ? "(" . ${"${pkg}::VERSION"} . ")"
                : "";

   my $spc = $spc{$pkg};
   print STDERR "$cmd: ${spc}${pkg}${v}\n";

   if(defined @{"${pkg}::ISA"})
    {
     @spc{@{"${pkg}::ISA"}} = ("  " . $spc{$pkg}) x @{"${pkg}::ISA"};
     unshift(@do, @{"${pkg}::ISA"});
    }
  }

 print STDERR "\n";
}

sub debug
{
 @_ == 1 or @_ == 2 or croak 'usage: $obj->debug([LEVEL])';

 my($cmd,$level) = @_;
 my $pkg = ref($cmd) || $cmd;
 my $oldval = 0;

 if(ref($cmd))
  {
   $oldval = ${*$cmd}{'net_cmd_debug'} || 0;
  }
 else
  {
   $oldval = $debug{$pkg} || 0;
  }

 return $oldval
    unless @_ == 2;

 $level = $debug{$pkg} || 0
    unless defined $level;

 _print_isa($pkg)
    if($level && !exists $debug{$pkg});

 if(ref($cmd))
  {
   ${*$cmd}{'net_cmd_debug'} = $level;
  }
 else
  {
   $debug{$pkg} = $level;
  }

 $oldval;
}

sub message
{
 @_ == 1 or croak 'usage: $obj->message()';

 my $cmd = shift;

 wantarray ? @{${*$cmd}{'net_cmd_resp'}}
    	   : join("", @{${*$cmd}{'net_cmd_resp'}});
}

sub debug_text { $_[2] }

sub debug_print
{
 my($cmd,$out,$text) = @_;
 print STDERR $cmd,($out ? '>>> ' : '<<< '), $cmd->debug_text($out,$text);
}

sub code
{
 @_ == 1 or croak 'usage: $obj->code()';

 my $cmd = shift;

 ${*$cmd}{'net_cmd_code'} = "000"
	unless exists ${*$cmd}{'net_cmd_code'};

 ${*$cmd}{'net_cmd_code'};
}

sub status
{
 @_ == 1 or croak 'usage: $obj->status()';

 my $cmd = shift;

 substr(${*$cmd}{'net_cmd_code'},0,1);
}

sub set_status
{
 @_ == 3 or croak 'usage: $obj->set_status(CODE, MESSAGE)';

 my $cmd = shift;
 my($code,$resp) = @_;

 $resp = [ $resp ]
	unless ref($resp);

 (${*$cmd}{'net_cmd_code'},${*$cmd}{'net_cmd_resp'}) = ($code, $resp);

 1;
}

sub command
{
 my $cmd = shift;

 $cmd->dataend()
    if(exists ${*$cmd}{'net_cmd_lastch'});

 if (scalar(@_))
  {
   local $SIG{PIPE} = 'IGNORE';

   my $str =  join(" ",@_) . "\015\012";
   my $len = length $str;
   my $swlen;
   
   $cmd->close
	unless (defined($swlen = syswrite($cmd,$str,$len)) && $swlen == $len);

   $cmd->debug_print(1,$str)
	if($cmd->debug);

   ${*$cmd}{'net_cmd_resp'} = [];      # the response
   ${*$cmd}{'net_cmd_code'} = "000";	# Made this one up :-)
  }

 $cmd;
}

sub ok
{
 @_ == 1 or croak 'usage: $obj->ok()';

 my $code = $_[0]->code;
 0 < $code && $code < 400;
}

sub unsupported
{
 my $cmd = shift;

 ${*$cmd}{'net_cmd_resp'} = [ 'Unsupported command' ];
 ${*$cmd}{'net_cmd_code'} = 580;
 0;
}

sub getline
{
 my $cmd = shift;

 ${*$cmd}{'net_cmd_lines'} ||= [];

 return shift @{${*$cmd}{'net_cmd_lines'}}
    if scalar(@{${*$cmd}{'net_cmd_lines'}});

 my $partial = ${*$cmd}{'net_cmd_partial'} || "";
 my $fd = fileno($cmd);
 
 return undef
	unless defined $fd;

 my $rin = "";
 vec($rin,$fd,1) = 1;

 my $buf;

 until(scalar(@{${*$cmd}{'net_cmd_lines'}}))
  {
   my $timeout = $cmd->timeout || undef;
   my $rout;
   if (select($rout=$rin, undef, undef, $timeout))
    {
     unless (sysread($cmd, $buf="", 1024))
      {
       carp ref($cmd) . ": Unexpected EOF on command channel"
		if $cmd->debug;
       $cmd->close;
       return undef;
      } 

     substr($buf,0,0) = $partial;	## prepend from last sysread

     my @buf = split(/\015?\012/, $buf);	## break into lines

     $partial = length($buf) == 0 || substr($buf, -1, 1) eq "\012"
		? ''
	  	: pop(@buf);

     map { $_ .= "\n" } @buf;

     push(@{${*$cmd}{'net_cmd_lines'}},@buf);

    }
   else
    {
     carp "$cmd: Timeout" if($cmd->debug);
     return undef;
    }
  }

 ${*$cmd}{'net_cmd_partial'} = $partial;

 shift @{${*$cmd}{'net_cmd_lines'}};
}

sub ungetline
{
 my($cmd,$str) = @_;

 ${*$cmd}{'net_cmd_lines'} ||= [];
 unshift(@{${*$cmd}{'net_cmd_lines'}}, $str);
}

sub parse_response
{
 return ()
    unless $_[1] =~ s/^(\d\d\d)(.?)//o;
 ($1, $2 eq "-");
}

sub response
{
 my $cmd = shift;
 my($code,$more) = (undef) x 2;

 ${*$cmd}{'net_cmd_resp'} ||= [];

 while(1)
  {
   my $str = $cmd->getline();

   return CMD_ERROR
	unless defined($str);

   $cmd->debug_print(0,$str)
     if ($cmd->debug);

   ($code,$more) = $cmd->parse_response($str);
   unless(defined $code)
    {
     $cmd->ungetline($str);
     last;
    }

   ${*$cmd}{'net_cmd_code'} = $code;

   push(@{${*$cmd}{'net_cmd_resp'}},$str);

   last unless($more);
  } 

 substr($code,0,1);
}

sub read_until_dot
{
 my $cmd = shift;
 my $arr = [];

 while(1)
  {
   my $str = $cmd->getline() or return undef;

   $cmd->debug_print(0,$str)
     if ($cmd->debug & 4);

   last if($str =~ /^\.\r?\n/o);

   $str =~ s/^\.\././o;

   push(@$arr,$str);
  }

 $arr;
}

sub datasend
{
 my $cmd = shift;
 my $arr = @_ == 1 && ref($_[0]) ? $_[0] : \@_;
 my $line = join("" ,@$arr);

 return 1
    unless length($line);

 if($cmd->debug)
  {
   my $b = "$cmd>>> ";
   print STDERR $b,join("\n$b",split(/\n/,$line)),"\n";
  }

 $line =~ s/\n/\015\012/sgo;

 ${*$cmd}{'net_cmd_lastch'} ||= " ";
 $line = ${*$cmd}{'net_cmd_lastch'} . $line;

 $line =~ s/(\012\.)/$1./sog;

 ${*$cmd}{'net_cmd_lastch'} = substr($line,-1,1);

 my $len = length($line) - 1;

 return $len == 0 ||
	syswrite($cmd, $line, $len, 1) == $len;
}

sub dataend
{
 my $cmd = shift;

 return 1
    unless(exists ${*$cmd}{'net_cmd_lastch'});

 if(${*$cmd}{'net_cmd_lastch'} eq "\015")
  {
   syswrite($cmd,"\012",1);
   print STDERR "\n"
    if($cmd->debug);
  }
 elsif(${*$cmd}{'net_cmd_lastch'} ne "\012")
  {
   syswrite($cmd,"\015\012",2);
   print STDERR "\n"
    if($cmd->debug);
  }

 print STDERR "$cmd>>> .\n"
    if($cmd->debug);

 syswrite($cmd,".\015\012",3);

 delete ${*$cmd}{'net_cmd_lastch'};

 $cmd->response() == CMD_OK;
}

1;

