my ($ctm) = @ARGV;

open F, "<:utf8", $ctm;

$lastutt = "";
@words = ();

while (<F>) {
	chonp;
	($utt, $chan, $st, $end, $word, $conf) = split;
	if ($utt ne $lastutt)  {
		if ($lastutt ne "") {
			print "$lastutt @words\n";
			@words=();
		}
	}

	$lastutt = $utt;
	push @words, $word;
}
if ($lastutt ne "") {
	print "$lastutt @words\n";
	@words=();
}

	
