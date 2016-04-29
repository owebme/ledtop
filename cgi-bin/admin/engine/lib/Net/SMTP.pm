# Net::SMTP.pm
#
# Copyright (c) 1995-1997 Graham Barr <gbarr@pobox.com>. All rights reserved.

package Net::SMTP;

require 5.001;

use strict;
use vars qw($VERSION @ISA);
use Socket 1.3;
use Carp;
use IO::Socket;
use Net::Cmd;
use Net::Config;

$VERSION = "2.10"; # $Id: //depot/libnet/Net/SMTP.pm#5$

@ISA = qw(Net::Cmd IO::Socket::INET);

sub new
{
 my $self = shift;
 my $type = ref($self) || $self;
 my $host = shift if @_ % 2;
 my %arg  = @_; 
 my $hosts = defined $host ? [ $host ] : $NetConfig{smtp_hosts};
 my $obj;

 my $h;
 foreach $h (@{$hosts})
  {
   $obj = $type->SUPER::new(PeerAddr => ($host = $h), 
			    PeerPort => $arg{Port} || 'smtp(25)',
			    Proto    => 'tcp',
			    Timeout  => defined $arg{Timeout}
						? $arg{Timeout}
						: 120
			   ) and last;
  }

 return undef
	unless defined $obj;

 $obj->autoflush(1);

 $obj->debug(exists $arg{Debug} ? $arg{Debug} : undef);

 unless ($obj->response() == CMD_OK)
  {
   $obj->close();
   return undef;
  }

 ${*$obj}{'net_smtp_host'} = $host;

 (${*$obj}{'net_smtp_domain'}) = $obj->message =~ /\A\s*(\S+)/;

 $obj->hello($arg{Hello} || "");

 $obj;
}

##
## User interface methods
##

sub domain
{
 my $me = shift;

 return ${*$me}{'net_smtp_domain'} || undef;
}

sub hello
{
 my $me = shift;
 my $domain = shift ||
	      eval {
		    require Net::Domain;
		    Net::Domain::hostfqdn();
		   } ||
		"";
 my $ok = $me->_EHLO($domain);
 my $msg;

 if($ok)
  {
   $msg = $me->message;

   my $h = ${*$me}{'net_smtp_esmtp'} = {};
   my $ext;
   foreach $ext (qw(8BITMIME CHECKPOINT DSN SIZE))
    {
     $h->{$ext} = 1
	if $msg =~ /\b${ext}\b/;
    }
  }
 else
  {
   $msg = $me->message
	if $me->_HELO($domain);
  }

 $ok && $msg =~ /\A(\S+)/
	? $1
	: undef;
}

sub _addr
{
 my $addr = shift || "";

 return $1
    if $addr =~ /(<[^>]+>)/so;

 $addr =~ s/\n/ /sog;
 $addr =~ s/(\A\s+|\s+\Z)//sog;

 return "<" . $addr . ">";
}


sub mail
{
 my $me = shift;
 my $addr = _addr(shift);
 my $opts = "";

 if(@_)
  {
   my %opt = @_;
   my($k,$v);

   if(exists ${*$me}{'net_smtp_esmtp'})
    {
     my $esmtp = ${*$me}{'net_smtp_esmtp'};

     if(defined($v = delete $opt{Size}))
      {
       if(exists $esmtp->{SIZE})
        {
         $opts .= sprintf " SIZE=%d", $v + 0
        }
       else
        {
	 carp 'Net::SMTP::mail: SIZE option not supported by host';
        }
      }

     if(defined($v = delete $opt{Return}))
      {
       if(exists $esmtp->{DSN})
        {
	 $opts .= " RET=" . uc $v
        }
       else
        {
	 carp 'Net::SMTP::mail: DSN option not supported by host';
        }
      }

     if(defined($v = delete $opt{Bits}))
      {
       if(exists $esmtp->{'8BITMIME'})
        {
	 $opts .= $v == 8 ? " BODY=8BITMIME" : " BODY=7BIT"
        }
       else
        {
	 carp 'Net::SMTP::mail: 8BITMIME option not supported by host';
        }
      }

     if(defined($v = delete $opt{Transaction}))
      {
       if(exists $esmtp->{CHECKPOINT})
        {
	 $opts .= " TRANSID=" . _addr($v);
        }
       else
        {
	 carp 'Net::SMTP::mail: CHECKPOINT option not supported by host';
        }
      }

     if(defined($v = delete $opt{Envelope}))
      {
       if(exists $esmtp->{DSN})
        {
	 $v =~ s/([^\041-\176]|=|\+)/sprintf "+%02x", ord($1)/sge;
	 $opts .= " ENVID=$v"
        }
       else
        {
	 carp 'Net::SMTP::mail: DSN option not supported by host';
        }
      }

     carp 'Net::SMTP::recipient: unknown option(s) '
		. join(" ", keys %opt)
		. ' - ignored'
	if scalar keys %opt;
    }
   else
    {
     carp 'Net::SMTP::mail: ESMTP not supported by host - options discarded :-(';
    }
  }

 $me->_MAIL("FROM:".$addr.$opts);
}

sub send	  { shift->_SEND("FROM:" . _addr($_[0])) }
sub send_or_mail  { shift->_SOML("FROM:" . _addr($_[0])) }
sub send_and_mail { shift->_SAML("FROM:" . _addr($_[0])) }

sub reset
{
 my $me = shift;

 $me->dataend()
	if(exists ${*$me}{'net_smtp_lastch'});

 $me->_RSET();
}


sub recipient
{
 my $smtp = shift;
 my $ok = 1;
 my $opts = "";

 if(@_ && ref($_[-1]))
  {
   my %opt = %{pop(@_)};
   my $v;

   if(exists ${*$smtp}{'net_smtp_esmtp'})
    {
     my $esmtp = ${*$smtp}{'net_smtp_esmtp'};

     if(defined($v = delete $opt{Notify}))
      {
       if(exists $esmtp->{DSN})
        {
	 $opts .= " NOTIFY=" . join(",",map { uc $_ } @$v)
        }
       else
        {
	 carp 'Net::SMTP::recipient: DSN option not supported by host';
        }
      }

     carp 'Net::SMTP::recipient: unknown option(s) '
		. join(" ", keys %opt)
		. ' - ignored'
	if scalar keys %opt;
    }
   else
    {
     carp 'Net::SMTP::recipient: ESMTP not supported by host - options discarded :-(';
    }
  }

 while($ok && scalar(@_))
  {
   $ok = $smtp->_RCPT("TO:" . _addr(shift) . $opts);
  }

 return $ok;
}

sub to { shift->recipient(@_) }

sub data
{
 my $me = shift;

 my $ok = $me->_DATA() && $me->datasend(@_);

 $ok && @_ ? $me->dataend
	   : $ok;
}

sub expand
{
 my $me = shift;

 $me->_EXPN(@_) ? ($me->message)
		: ();
}


sub verify { shift->_VRFY(@_) }

sub help
{
 my $me = shift;

 $me->_HELP(@_) ? scalar $me->message
	        : undef;
}

sub quit
{
 my $me = shift;

 $me->_QUIT;
 $me->close;
}

sub DESTROY
{
 my $me = shift;
 defined(fileno($me)) && $me->quit
}

##
## RFC821 commands
##

sub _EHLO { shift->command("EHLO", @_)->response()  == CMD_OK }   
sub _HELO { shift->command("HELO", @_)->response()  == CMD_OK }   
sub _MAIL { shift->command("MAIL", @_)->response()  == CMD_OK }   
sub _RCPT { shift->command("RCPT", @_)->response()  == CMD_OK }   
sub _SEND { shift->command("SEND", @_)->response()  == CMD_OK }   
sub _SAML { shift->command("SAML", @_)->response()  == CMD_OK }   
sub _SOML { shift->command("SOML", @_)->response()  == CMD_OK }   
sub _VRFY { shift->command("VRFY", @_)->response()  == CMD_OK }   
sub _EXPN { shift->command("EXPN", @_)->response()  == CMD_OK }   
sub _HELP { shift->command("HELP", @_)->response()  == CMD_OK }   
sub _RSET { shift->command("RSET")->response()	    == CMD_OK }   
sub _NOOP { shift->command("NOOP")->response()	    == CMD_OK }   
sub _QUIT { shift->command("QUIT")->response()	    == CMD_OK }   
sub _DATA { shift->command("DATA")->response()	    == CMD_MORE } 
sub _TURN { shift->unsupported(@_); } 			   	  

1;

