package MIME::Lite;

require 5.004;     ### for /c modifier in m/\G.../gc modifier

use Carp;
use FileHandle;

use strict;
use vars qw(
            $AUTO_CC 
            $AUTO_ENCODE
            $AUTO_VERIFY            
            $PARANOID 
            $QUIET
            $VANILLA
            $VERSION 
            );

# GLOBALS, EXTERNAL/CONFIGURATION...

### The package version, both in 1.23 style *and* usable by MakeMaker:
$VERSION = substr q$Revision: 2.106 $, 10;

### Don't warn me about dangerous activities:
$QUIET = "true";

### Set this true if you don't want to use MIME::Base64/MIME::QuotedPrint:
$PARANOID = "true";

### Unsupported (for tester use): don't qualify boundary with time/pid:
$VANILLA = 0;

### Automatically choose encoding from content type:
$AUTO_ENCODE = 1;

### Automatically interpret CC/BCC for SMTP:
$AUTO_CC = 1;

### Check paths right before printing:
$AUTO_VERIFY = 1;

# GLOBALS, INTERNAL...

### Our sending facilities:
my $Sender     = "sendmail";
my %SenderArgs = (
    "sendmail" => ["/usr/lib/sendmail -t -oi -oem"],
    "smtp"     => [],
    "sub"      => [],
);

### Boundary counter:
my $BCount = 0;

### Known Mail/MIME fields... these, plus some general forms like 
### "x-*", are recognized by build():
my %KnownField = map {$_=>1} 
qw(
   bcc         cc          comments      date          encrypted 
   from        keywords    message-id    mime-version  organization
   received    references  reply-to      return-path   sender        
   subject     to
   );

### What external packages do we use for encoding?
my @Uses;


# PRIVATE UTILITY FUNCTIONS...

sub fold {
    my $str = shift;
    $str =~ s/^\s*|\s*$//g;    ### trim
    $str =~ s/\n/\n /g;      
    $str;
}


sub gen_boundary {
    return ("_----------=_".($VANILLA ? '' : int(time).$$).$BCount++);
}


sub known_field {
    my $field = lc(shift);
    $KnownField{$field} or ($field =~ m{^(content|resent|x)-.});
}


sub is_mime_field {
    $_[0] =~ /^(mime\-|content\-)/i;
}

my $ATOM      = '[^ \000-\037()<>@,;:\134"\056\133\135]+';
my $QSTR      = '".*?"';
my $WORD      = '(?:' . $QSTR . '|' . $ATOM . ')';
my $DOMAIN    = '(?:' . $ATOM . '(?:' . '\\.' . $ATOM . ')*' . ')';
my $LOCALPART = '(?:' . $WORD . '(?:' . '\\.' . $WORD . ')*' . ')';
my $ADDR      = '(?:' . $LOCALPART . '@' . $DOMAIN . ')';
my $PHRASE    = '(?:' . $WORD . ')+';
my $SEP       = "(?:^\\s*|\\s*,\\s*)";     ### before elems in a list

sub my_extract_addrs {
    my $str = shift;
    my @addrs;
    $str =~ s/\s/ /g;     ### collapse whitespace

    pos($str) = 0;
    while ($str !~ m{\G\s*\Z}gco) {
	### print STDERR "TACKLING: ".substr($str, pos($str))."\n";
	if    ($str =~ m{\G$SEP$PHRASE\s*<\s*($ADDR)\s*>}gco) {push @addrs,$1}
	elsif ($str =~ m{\G$SEP($ADDR)}gco)                   {push @addrs,$1}
	elsif ($str =~ m{\G$SEP($ATOM)}gco)                   {push @addrs,$1}
	else { 
	    my $problem = substr($str, pos($str));
	    die "can't extract address at <$problem> in <$str>\n";
	}
    }
    return @addrs;
}


    eval q{
        sub extract_addrs {
	    return my_extract_addrs(@_);
	}
    }; ### q


if (!$PARANOID and eval "require MIME::Base64") {
    import MIME::Base64 qw(encode_base64);
    push @Uses, "B$MIME::Base64::VERSION";
}
else {
    eval q{
sub encode_base64 {
    my $res = "";
    my $eol = "\n";

    pos($_[0]) = 0;        ### thanks, Andreas!
    while ($_[0] =~ /(.{1,45})/gs) {
	$res .= substr(pack('u', $1), 1);
	chop($res);
    }
    $res =~ tr|` -_|AA-Za-z0-9+/|;

    ### Fix padding at the end:
    my $padding = (3 - length($_[0]) % 3) % 3;
    $res =~ s/.{$padding}$/'=' x $padding/e if $padding;

    ### Break encoded string into lines of no more than 76 characters each:
    $res =~ s/(.{1,76})/$1$eol/g if (length $eol);
    return $res;
} ### sub
  } ### q
} ### if


if (!$PARANOID and eval "require MIME::QuotedPrint") {
    import MIME::QuotedPrint qw(encode_qp);
    push @Uses, "Q$MIME::QuotedPrint::VERSION";
}
else {
    eval q{
sub encode_qp {
    my $res = shift;
    local($_);
    $res =~ s/([^ \t\n!-<>-~])/sprintf("=%02X", ord($1))/eg;  ### rule #2,#3
    $res =~ s/([ \t]+)$/
      join('', map { sprintf("=%02X", ord($_)) }
	           split('', $1)
      )/egm;                        ### rule #3 (encode whitespace at eol)

    ### rule #5 (lines shorter than 76 chars, but can't break =XX escapes:
    my $brokenlines = "";
    $brokenlines .= "$1=\n" while $res =~ s/^(.{70}([^=]{2})?)//; ### 70 was 74
    $brokenlines =~ s/=\n$// unless length $res; 
    "$brokenlines$res";
} ### sub
  } ### q
} ### if


#------------------------------
#
# encode_8bit STRING
#
# Encode the given string using 8BIT.
# This breaks long lines into shorter ones.

sub encode_8bit {
    my $str = shift;
    $str =~ s/^(.{990})/$1\n/mg;
    $str;
}

#------------------------------
#
# encode_7bit STRING
#
# Encode the given string using 7BIT.
# This NO LONGER protects people through encoding.

sub encode_7bit {
    my $str = shift;
    $str =~ s/[\x80-\xFF]//g; 
    $str =~ s/^(.{990})/$1\n/mg;
    $str;
}




sub new {
    my $class = shift;

    ### Create basic object:
    my $self = {
	Attrs   => {},     ### MIME attributes
	Header  => [],     ### explicit message headers
	Parts   => [],     ### array of parts
    };    
    bless $self, $class;

    ### Build, if needed:
    return (@_ ? $self->build(@_) : $self);
}



sub attach {
    my $self = shift;

    ### Create new part, if necessary:
    my $part1 = ((@_ == 1) ? shift : ref($self)->new(Top=>0, @_));

    ### Do the "attach-to-singlepart" hack:
    if ($self->attr('content-type') !~ m{^(multipart|message)/}i) {

	### Create part zero:
	my $part0 = ref($self)->new;

	### Cut MIME stuff from self, and paste into part zero: 
	foreach (qw(Attrs Data Path FH)) {
	    $part0->{$_} = $self->{$_}; delete($self->{$_});
	}
	$part0->top_level(0);    ### clear top-level attributes

	### Make self a top-level multipart:
	$self->{Attrs} ||= {};   ### reset       
	$self->attr('content-type'              => 'multipart/mixed');
	$self->attr('content-type.boundary'     => gen_boundary());
	$self->attr('content-transfer-encoding' => '7bit');
	$self->top_level(1);     ### activate top-level attributes

	### Add part 0:
	push @{$self->{Parts}}, $part0;
    }

    ### Add the new part:
    push @{$self->{Parts}}, $part1;
    $part1;
}


sub build {
    my $self = shift;
    my %params = @_;
    my @params = @_;
    my $key;

    ### Miko's note: reorganized to check for exactly one of Data, Path, or FH
    (defined($params{Data})+defined($params{Path})+defined($params{FH}) <= 1)
	or croak "supply exactly zero or one of (Data|Path|FH).\n";

    ### Create new instance, if necessary:
    ref($self) or $self = $self->new;


    ### CONTENT-TYPE....
    ###

    ### Get content-type:
    my $type = ($params{Type} || 'TEXT');
    ($type eq 'TEXT')   and $type = 'text/plain';
    ($type eq 'BINARY') and $type = 'application/octet-stream';
    $type = lc($type);
    $self->attr('content-type' => $type);
   
    ### Get some basic attributes from the content type:
    my $is_multipart = ($type =~ m{^(multipart)/}i);

    ### Add in the multipart boundary:
    if ($is_multipart) {
	my $boundary = gen_boundary();
	$self->attr('content-type.boundary' => $boundary);
    }


    ### CONTENT-ID...
    ###
    $self->attr('content-id' => $params{Id}) if defined($params{Id});


    ### DATA OR PATH...
    ###    Note that we must do this *after* we get the content type, 
    ###    in case read_now() is invoked, since it needs the binmode().

    ### Get data, as...
    ### ...either literal data:
    if (defined($params{Data})) {
	$self->data($params{Data});
    }
    ### ...or a path to data:
    elsif (defined($params{Path})) {
	$self->path($params{Path});       ### also sets filename
	$self->read_now if $params{ReadNow};
    }
    ### ...or a filehandle to data:
    ### Miko's note: this part works much like the path routine just above,
    elsif (defined($params{FH})) {
	$self->fh($params{FH});
	$self->read_now if $params{ReadNow};  ### implement later
    }
    

    ### FILENAME... (added by Ian Smith <ian@safeway.dircon.co.uk> on 8/4/97)
    ###    Need this to make sure the filename is added.  The Filename
    ###    attribute is ignored, otherwise.
    if (defined($params{Filename})) {
	$self->filename($params{Filename});
    }
  

    ### CONTENT-TRANSFER-ENCODING...
    ###

    ### Get it:
    my $enc = ($params{Encoding} ||  
	       ($AUTO_ENCODE and $self->suggest_encoding($type)) ||
	       'binary');      
    $self->attr('content-transfer-encoding' => lc($enc));
	
    ### Sanity check:
    if ($type =~ m{^(multipart|message)/}) {
	($enc =~ m{^(7bit|8bit|binary)\Z}) or 
	    croak "illegal MIME: can't have encoding $enc with type $type\n";
    }

    ### CONTENT-DISPOSITION...
    ###    Default is inline for single, none for multis:
    ###
    my $disp = ($params{Disposition} or ($is_multipart ? undef : 'inline'));
    $self->attr('content-disposition' => $disp);

    ### CONTENT-LENGTH...
    ###
    my $length;
    if (exists($params{Length})) {   ### given by caller:
	$self->attr('content-length' => $params{Length});
    }
    else {                           ### compute it ourselves
	$self->get_length;
    }

    ### Init the top-level fields:
    my $is_top = defined($params{Top}) ? $params{Top} : 1;
    $self->top_level($is_top);

    ### Datestamp if desired:
    my $ds_wanted    = $params{Datestamp};
    my $ds_defaulted = ($is_top and !exists($params{Datestamp}));
    if (($ds_wanted or $ds_defaulted) and !exists($params{Date})) {
	my ($u_wdy, $u_mon, $u_mdy, $u_time, $u_y4) = 
	    split /\s+/, gmtime()."";   ### should be non-locale-dependent
	my $date = "$u_wdy, $u_mdy $u_mon $u_y4 $u_time UT";
	$self->add("date", $date);
    }
    
    ### Set message headers:
    my @paramz = @params;
    my $field;
    while (@paramz) {
	my ($tag, $value) = (shift(@paramz), shift(@paramz));

	### Get tag, if a tag:
	if ($tag =~ /^-(.*)/) {      ### old style, backwards-compatibility
	    $field = lc($1);
	}
	elsif ($tag =~ /^(.*):$/) {  ### new style
	    $field = lc($1);
	}
	elsif (known_field($field = lc($tag))) {   ### known field
	    ### no-op
	}
	else {                       ### not a field:
	    next;
	}
	
	### Add it:
	$self->add($field, $value);
    }

    ### Done!
    $self;
}



sub top_level {
    my ($self, $onoff) = @_;	
    if ($onoff) {
	$self->attr('MIME-Version' => '1.0');
	my $uses = (@Uses ? ("(" . join("; ", @Uses) . ")") : '');
	$self->replace('X-Mailer' => "MIME::Lite $VERSION $uses")
	    unless $VANILLA;
    }
    else {
	$self->attr('MIME-Version' => undef);
	$self->delete('X-Mailer');
    }
}


sub add {
    my $self = shift;
    my $tag = lc(shift);
    my $value = shift;

    ### If a dangerous option, warn them:
    carp "Explicitly setting a MIME header field ($tag) is dangerous:\n".
	 "use the attr() method instead.\n"
	if (is_mime_field($tag) && !$QUIET);

    ### Get array of clean values:
    my @vals = ref($value) ? @{$value} : ($value);
    map { s/\n/\n /g } @vals;

    ### Add them:
    foreach (@vals) {
	push @{$self->{Header}}, [$tag, $_];
    }
}


sub attr {
    my ($self, $attr, $value) = @_;
    $attr = lc($attr);

    ### Break attribute name up:
    my ($tag, $subtag) = split /\./, $attr;
    defined($subtag) or $subtag = '';

    ### Set or get?
    if (@_ > 2) {   ### set:
	$self->{Attrs}{$tag} ||= {};            ### force hash
	delete $self->{Attrs}{$tag}{$subtag};   ### delete first
	if (defined($value)) {                  ### set...
	    $value =~ s/[\r\n]//g;                   ### make clean
	    $self->{Attrs}{$tag}{$subtag} = $value;
	}
    }
	
    ### Return current value:
    $self->{Attrs}{$tag}{$subtag};
}

sub _safe_attr {
    my ($self, $attr) = @_;
    my $v = $self->attr($attr);
    defined($v) ? $v : '';
}


sub delete {
    my $self = shift;
    my $tag = lc(shift);

    ### Delete from the header:
    my $hdr = [];
    my $field;
    foreach $field (@{$self->{Header}}) {
	push @$hdr, $field if ($field->[0] ne $tag);
    }
    $self->{Header} = $hdr;
    $self;
}


sub fields {
    my $self = shift;
    my @fields;
    
    ### Get a lookup-hash of all *explicitly-given* fields:
    my %explicit = map { $_->[0] => 1 } @{$self->{Header}};
    
    ### Start with any MIME attributes not given explicitly:
    my $tag;
    foreach $tag (sort keys %{$self->{Attrs}}) {	

	### Skip if explicit:
	next if ($explicit{$tag});         

	### Skip if no subtags:
	my @subtags = keys %{$self->{Attrs}{$tag}}; 
	@subtags or next;

	### Create string:
	my $value;
	defined($value = $self->{Attrs}{$tag}{''}) or next;  ### need default 
	foreach (sort @subtags) {
	    next if ($_ eq '');
	    $value .= qq{; $_="$self->{Attrs}{$tag}{$_}"};
	}
	
	### Add to running fields;
	push @fields, [$tag, $value];
    }
    
    ### Add remaining fields (note that we duplicate the array for safety):
    foreach (@{$self->{Header}}) {
	push @fields, [@{$_}];
    }

    ### Done!
    return \@fields;
}

sub filename {
    my ($self, $filename) = @_;
    if (@_ > 1) {
	$self->attr('content-type.name' => $filename);
	$self->attr('content-disposition.filename' => $filename);
    }
    $self->attr('content-disposition.filename');
}


sub get {
    my ($self, $tag, $index) = @_;
    $tag = lc($tag); 
    croak "get: can't be used with MIME fields\n" if is_mime_field($tag);
    
    my @all = map { ($_->[0] eq $tag) ? $_->[1] : ()} @{$self->{Header}};
    (defined($index) ? $all[$index] : (wantarray ? @all : $all[0]));
}

#------------------------------


sub get_length {
    my $self = shift;

    my $is_multipart = ($self->attr('content-type') =~ m{^multipart/}i);
    my $enc = lc($self->attr('content-transfer-encoding') || 'binary');
    my $length;
    if (!$is_multipart && ($enc eq "binary")){  ### might figure it out cheap:
	if    (defined($self->{Data})) {               ### it's in core
	    $length = length($self->{Data});
	}
	elsif (defined($self->{FH})) {                 ### it's in a filehandle
	    ### no-op: it's expensive, so don't bother
	}
	elsif (defined($self->{Path})) {               ### it's a simple file!
	    $length = (-s $self->{Path})   if (-e $self->{Path});
	}
    }
    $self->attr('content-length' => $length);
    return $length;
}


sub replace {
    my ($self, $tag, $value) = @_;
    $self->delete($tag);
    $self->add($tag, $value) if defined($value);
}



sub scrub {
    my ($self, @a) = @_;
    my ($expl) = @a;
    local $QUIET = 1;

    ### Scrub me:
    if (!@a) {         ### guess

	### Scrub length always:
	$self->replace('content-length', '');

	### Scrub disposition if no filename, or if content-type has same info:
	if (!$self->_safe_attr('content-disposition.filename') ||
	    $self->_safe_attr('content-type.name')) {
	    $self->replace('content-disposition', '');
	}

	### Scrub encoding if effectively unencoded:
	if ($self->_safe_attr('content-transfer-encoding') =~
	    /^(7bit|8bit|binary)$/i) {
	    $self->replace('content-transfer-encoding', '');
	}

	### Scrub charset if US-ASCII:
	if ($self->_safe_attr('content-type.charset') =~ /^(us-ascii)/i) {
	    $self->attr('content-type.charset' => undef);
	}

	### TBD: this is not really right for message/digest:
	if ((keys %{$self->{Attrs}{'content-type'}} == 1) and
	    ($self->_safe_attr('content-type') eq 'text/plain')) {
	    $self->replace('content-type', '');
	}
    }
    elsif ($expl and (ref($expl) eq 'ARRAY')) {
	foreach (@{$expl}) { $self->replace($_, ''); }
    }

    ### Scrub my kids:
    foreach (@{$self->{Parts}}) { $_->scrub(@a); }
}


sub binmode {
    my $self = shift;
    $self->{Binmode} = shift if (@_);       ### argument? set override
    return (defined($self->{Binmode}) 
	    ? $self->{Binmode}
	    : ($self->attr("content-type") !~ m{^(text|message)/}i));
}


sub data {
    my $self = shift;
    if (@_) {
	$self->{Data} = ((ref($_[0]) eq 'ARRAY') ? join('', @{$_[0]}) : $_[0]);
	$self->get_length;
    }
    $self->{Data};
}



sub path {
    my $self = shift;
    if (@_) {

	### Set the path, and invalidate the content length:
	$self->{Path} = shift;

	### Re-set filename, extracting it from path if possible:
	my $filename;
	if ($self->{Path} and ($self->{Path} !~ /\|$/)) {  ### non-shell path:
	    ($filename = $self->{Path}) =~ s/^<//;    
	    ($filename) = ($filename =~ m{([^\/]+)\Z});
	}
	$self->filename($filename);

	### Reset the length:
	$self->get_length;
    }
    $self->{Path};
}


sub fh {
    my $self = shift;
    $self->{FH} = shift if @_;
    $self->{FH};
}


sub resetfh {
    my $self = shift;
    seek($self->{FH},0,0);
}


sub read_now {
    my $self = shift;
    local $/ = undef;
    
    if    ($self->{FH}) {       ### data from a filehandle:
	my $chunk;
	my @chunks;
	CORE::binmode($self->{FH}) if $self->binmode;
	while (read($self->{FH}, $chunk, 1024)) { 
	    push @chunks, $chunk; 
	}
	$self->{Data} = join '', @chunks;
    }
    elsif ($self->{Path}) {     ### data from a path:
	open SLURP, $self->{Path} or croak "open $self->{Path}: $!\n";
	CORE::binmode(SLURP) if $self->binmode;
	$self->{Data} = <SLURP>;        ### sssssssssssssslurp...
	close SLURP;                    ### ...aaaaaaaaahhh!
    }
}


sub sign {
    my $self = shift;
    my %params = @_;

    ### Default:
    @_ or $params{Path} = "$ENV{HOME}/.signature";

    ### Force message in-core:
    defined($self->{Data}) or $self->read_now;

    ### Load signature:
    my $sig;
    if (!defined($sig = $params{Data})) {      ### not given explicitly:
	local $/ = undef;
	open SIG, $params{Path} or croak "open sig $params{Path}: $!\n";
	$sig = <SIG>;                  ### sssssssssssssslurp...
	close SIG;                     ### ...aaaaaaaaahhh!
    }    
    $sig = join('',@$sig) if (ref($sig) and (ref($sig) eq 'ARRAY'));

    ### Append, following Internet conventions:
    $self->{Data} .= "\n-- \n$sig";

    ### Re-compute length:
    $self->get_length;
    1;
}


sub suggest_encoding {
    my ($self, $ctype) = @_;

    my ($type) = split '/', lc($ctype);
    if (($type eq 'text') || ($type eq 'message')) {    ### scan message body
	return 'binary';
    }
    else {
	return ($type eq 'multipart') ? 'binary' : 'base64';
    }
}


sub verify_data {
    my $self = shift;

    ### Verify self:
    my $path = $self->{Path};
    if ($path and ($path !~ /\|$/)) {  ### non-shell path:
	$path =~ s/^<//;    
	(-r $path) or die "$path: not readable\n";
    }

    ### Verify parts:
    foreach my $part (@{$self->{Parts}}) { $part->verify_data }
    1;
}


sub print {
    my ($self, $out) = @_;

    ### Coerce into a printable output handle:
    $out = wrap MIME::Lite::IO_Handle $out;

    ### Output head, separator, and body:
    $out->print($self->header_as_string, "\n");
    $self->print_body($out);
}

sub print_for_smtp {
    my ($self, $out) = @_;

    ### Coerce into a printable output handle:
    $out = wrap MIME::Lite::IO_Handle $out;
    
    ### Create a safe head:
    my @fields = grep { $_->[0] ne 'bcc' } @{$self->fields};
    my $header = $self->fields_as_string(\@fields);

    ### Output head, separator, and body:
    $out->print($header, "\n");
    $self->print_body($out);
}


sub print_body {
    my ($self, $out) = @_;

    ### Coerce into a printable output handle:
    $out = wrap MIME::Lite::IO_Handle $out;

    ### Output either the body or the parts.
    ###   Notice that we key off of the content-type!  We expect fewer 
    ###   accidents that way, since the syntax will always match the MIME type.
    my $type = $self->attr('content-type');
    if ($type =~ m{^multipart/}i) {	
	my $boundary = $self->attr('content-type.boundary');

	### Preamble:
	$out->print("This is a multi-part message in MIME format.\n");
	
	### Parts:
	my $part;
	foreach $part (@{$self->{Parts}}) {
	    $out->print("\n--$boundary\n");
	    $part->print($out);
	}

	### Epilogue:
	$out->print("\n--$boundary--\n\n");
    }
    elsif ($type =~ m{^message/}) {
	my @parts = @{$self->{Parts}};

	### It's a toss-up; try both data and parts:
	if    (@parts == 0) { $self->print_simple_body($out) }
	elsif (@parts == 1) { $parts[0]->print($out) }
	else                { croak "can't handle message with >1 part\n"; }
    }
    else {                    
	$self->print_simple_body($out); 
    }
    1;
}

sub print_simple_body {
    my ($self, $out) = @_;

    ### Coerce into a printable output handle:
    $out = wrap MIME::Lite::IO_Handle $out;

    ### Get content-transfer-encoding:
    my $encoding = uc($self->attr('content-transfer-encoding'));

    ### Notice that we don't just attempt to slurp the data in from a file:
    ### by processing files piecemeal, we still enable ourselves to prepare
    ### very large MIME messages...

    ### Is the data in-core?  If so, blit it out...
    if (defined($self->{Data})) {
      DATA: 
	{ $_ = $encoding;

	  /^BINARY$/ and do {
	      $out->print($self->{Data}); 
	      last DATA;
	  };
	  /^8BIT$/ and do {
	      $out->print(encode_8bit($self->{Data})); 
	      last DATA;
	  };
	  /^7BIT$/ and do {
	      $out->print(encode_7bit($self->{Data})); 
	      last DATA;
	  };
	  /^QUOTED-PRINTABLE$/ and do {
	      while ($self->{Data}=~ m{^(.*[\r\n]*)}mg) {
		  $out->print(encode_qp($1)); ### have to do it line by line...
	      }
	      last DATA;	 
	  };
	  /^BASE64/ and do {
	      $out->print(encode_base64($self->{Data})); 
	      last DATA;
	  };
	  croak "unsupported encoding: `$_'\n";
        }
    }

    ### Else, is the data in a file?  If so, output piecemeal...
    ###    Miko's note: this routine pretty much works the same with a path 
    ###    or a filehandle. the only difference in behaviour is that it does 
    ###    not attempt to open anything if it already has a filehandle
    elsif (defined($self->{Path}) || defined($self->{FH})) {
	no strict 'refs';          ### in case FH is not an object
	my $DATA;

	### Open file if necessary:
	if (defined($self->{Path})) {
	    $DATA = new FileHandle || croak "can't get new filehandle\n";
	    $DATA->open("$self->{Path}") or croak "open $self->{Path}: $!\n";
	}
	else {
	    $DATA=$self->{FH};
	}
	CORE::binmode($DATA) if $self->binmode;
		
	### Encode piece by piece:
      PATH: 
	{   $_ = $encoding;
	    
	    /^BINARY$/ and do {
		$out->print($_)                while read($DATA, $_, 2048); 
		last PATH;
	    };      
	    /^8BIT$/ and do {
		$out->print(encode_8bit($_))   while (<$DATA>); 
		last PATH;
	    };
	    /^7BIT$/ and do {
		$out->print(encode_7bit($_))   while (<$DATA>); 
		last PATH;
	    };
	    /^QUOTED-PRINTABLE$/ and do {
		$out->print(encode_qp($_))     while (<$DATA>); 
		last PATH;
	    };
	    /^BASE64$/ and do {
		$out->print(encode_base64($_)) while (read($DATA, $_, 45));
		last PATH;
	    };
	    croak "unsupported encoding: `$_'\n";
	}
	
	### Close file:
	close $DATA if defined($self->{Path});
    }
    
    else {
	croak "no data in this part\n";
    }
    1;
}


sub print_header {
    my ($self, $out) = @_;

    ### Coerce into a printable output handle:
    $out = wrap MIME::Lite::IO_Handle $out;

    ### Output the header:
    $out->print($self->header_as_string);
    1;
}


sub body_as_string {
    my $self = shift;
    my @buf;
    my $io = (wrap MIME::Lite::IO_ScalarArray \@buf);
    $self->print_body($io);
    join '', @buf;
}
*stringify_body = \&body_as_string;    ### backwards compatibility

sub fields_as_string {
    my ($self, $fields) = @_;
    my @lines;
    foreach (@$fields) {
	my ($tag, $value) = @$_; 
	next if ($value eq '');          ### skip empties
	$tag =~ s/\b([a-z])/uc($1)/ge;   ### make pretty
	$tag =~ s/^mime-/MIME-/ig;       ### even prettier
	push @lines, "$tag: $value\n";
    }
    join '', @lines;
}


sub header_as_string {
    my $self = shift;
    $self->fields_as_string($self->fields);
}
*stringify_header = \&header_as_string;    ### backwards compatibility


sub send {
    my $self = shift;

    if (ref($self)) {              ### instance method:
	my $method = "send_by_$Sender";
	my @args   = @{$SenderArgs{$Sender} || []};
	$self->verify_data if $AUTO_VERIFY;       ### prevents missing parts!
	return $self->$method(@args);
    }
    else {                         ### class method:
	my @old = ($Sender, @{$SenderArgs{$Sender}});
	$Sender = shift;
	$SenderArgs{$Sender} = [@_];    ### remaining args
	return @old;
    }
}


sub send_by_sendmail {
    my $self = shift;

    if (@_ == 1) {                    ### Use the given command...
	my $sendmailcmd = shift @_;

	### Do it:
	open SENDMAIL, "|$sendmailcmd" or croak "open |$sendmailcmd: $!\n";
	$self->print(\*SENDMAIL);
	close SENDMAIL;
	return (($? >> 8) ? undef : 1);
    }
    else {                            ### Build the command...
	my %p = @_;
	$p{Sendmail} ||= "/usr/lib/sendmail";   
	
	### Start with the command and basic args:
	my @cmd = ($p{Sendmail}, @{$p{BaseArgs} || ['-t', '-oi', '-oem']});

	### See if we are forcibly setting the sender:
	$p{SetSender} = 1 if defined($p{FromSender});

	### Add the -f argument, unless we're explicitly told NOT to:
	unless (exists($p{SetSender}) and !$p{SetSender}) {
	    my $from = $p{FromSender} || ($self->get('From'))[0];
	    if ($from) {
		my ($from_addr) = extract_addrs($from);
		push @cmd, "-f$from_addr"       if $from_addr;
	    }
	}

	### Open the command in a taint-safe fashion:
	my $pid = open SENDMAIL, "|-"; 
	defined($pid) or die "open of pipe failed: $!\n";
	if (!$pid) {    ### child
	    exec(@cmd) or die "can't exec $p{Sendmail}: $!\n";
	    ### NOTREACHED
	}
	else {          ### parent
	    $self->print(\*SENDMAIL);
	    close SENDMAIL || die "error closing $p{Sendmail}: $! (exit $?)\n";
	    return 1;
	}
    }
}


### Provided by Andrew McRae. Version 0.2  anm  09Sep97
### Copyright 1997 Optimation New Zealand Ltd.
### May be modified/redistributed under the same terms as Perl.
#
sub send_by_smtp {
    my ($self, @args) = @_;

    ### We need the "From:" and "To:" headers to pass to the SMTP mailer:
    my $hdr  = $self->fields();   
    my $from = $self->get('From');
    my $to   = $self->get('To');

    ### Sanity check:
    defined($to) or croak "send_by_smtp: missing 'To:' address\n";
 	       
    ### Get the destinations as a simple array of addresses:
    my @to_all = extract_addrs($to);
    if ($AUTO_CC) {
	foreach my $field (qw(Cc Bcc)) {
	    my $value = $self->get($field);
	    push @to_all, extract_addrs($value) if defined($value);
	}
    }

    ### Create SMTP client:
    require Net::SMTP;
    my $smtp = MIME::Lite::SMTP->new(@args)
        or croak "Failed to connect to mail server: $!\n\n Please check your SMTP mail server name. Make sure the server exists and will allow relay from this IP address or domain.\n\n The server you have entered into your configuration does not appear to exist or is not allowing a connection from this UBB.\n\n";
    $smtp->mail($from)
        or croak "SMTP MAIL command failed: $!\n\n Please check your SMTP mail server name.\n\n This server seems to exist but does not seem to allow us to relay mail.\n\n";
    $smtp->to(@to_all)
        or croak "SMTP RCPT command failed: $!\n\n Please check your SMTP mail server name.\n\n This server seems to exist but does not seem to allow us to relay mail.\n\n There may also be a problem with one of the email addresses you are trying to mail to.\n\n";
    $smtp->data()
        or croak "SMTP DATA command failed: $!\n Please check your SMTP mail server name.\n\n This server seems to exist but does not seem to allow us to relay mail.\n\n";

    ### MIME::Lite can print() to anything with a print() method:
    $self->print_for_smtp($smtp);
    $smtp->dataend();
    $smtp->quit;
    1;
}

#------------------------------
#
# send_by_sub [\&SUBREF, [ARGS...]]
#
# I<Instance method, private.>
# Send the message via an anonymous subroutine.
#
sub send_by_sub {
    my ($self, $subref, @args) = @_;
    &$subref($self, @args);
}


sub sendmail {
    my $self = shift;
    $self->send('sendmail', join(' ', @_));
}


sub quiet {
    my $class = shift;
    $QUIET = shift if @_;
    $QUIET;
}



#============================================================

package MIME::Lite::SMTP;

#============================================================
# This class just adds a print() method to Net::SMTP.
# Notice that we don't use/require it until it's needed!

use strict;
use vars qw( @ISA );
@ISA = qw(Net::SMTP);

sub print { shift->datasend(@_) }



#============================================================

package MIME::Lite::IO_Handle;

#============================================================

### Wrap a non-object filehandle inside a blessed, printable interface:
### Does nothing if the given $fh is already a blessed object.
sub wrap {
    my ($class, $fh) = @_;
    no strict 'refs';

    ### Get default, if necessary:
    $fh or $fh = select;        ### no filehandle means selected one
    ref($fh) or $fh = \*$fh;    ### scalar becomes a globref
    
    ### Stop right away if already a printable object:
    return $fh if (ref($fh) and (ref($fh) ne 'GLOB'));

    ### Get and return a printable interface:
    bless \$fh, $class;         ### wrap it in a printable interface
}

### Print:
sub print {
    my $self = shift;
    print {$$self} @_;
}


#============================================================

package MIME::Lite::IO_Scalar;

#============================================================

### Wrap a scalar inside a blessed, printable interface:
sub wrap {
    my ($class, $scalarref) = @_;
    defined($scalarref) or $scalarref = \"";
    bless $scalarref, $class;
}

### Print:
sub print {
    my $self = shift;
    $$self .= join('', @_);
    1;
}


#============================================================

package MIME::Lite::IO_ScalarArray;

#============================================================

### Wrap an array inside a blessed, printable interface:
sub wrap {
    my ($class, $arrayref) = @_;
    defined($arrayref) or $arrayref = [];
    bless $arrayref, $class;
}

### Print:
sub print {
    my $self = shift;
    push @$self, @_;
    1;
}

1;
__END__


