
# Ёффект плавной смены страниц (провер€ем настройки)

open(BO, "admin/layouts/settings"); my @settings = <BO>; close(BO);
foreach my $line(@settings)
	{
	chomp($line);
	my ($name_site, $cache_mode, $dir_main, $dir_cgi, $dir_css, $dir_fonts, $email_feedback, $email_orders, $fade_page) = split(/\|/, $line);
	$fadepage=qq~$fade_page~;		
	}
	
	if ($fadepage == "1") {$fade_page = '<script type="text/javascript" src="/admin/site/js/fadePage.js"></script>';}
	else {$fade_page='';}
	
1;