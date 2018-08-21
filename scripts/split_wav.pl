my ($audio, $segments) = @ARGV;

open SEG, "< $segments";
while (<SEG>) {
	chomp;
	($id, $file, $start, $end) = split;
   push @st, $start;
   push @en, $end;

   $id =~ /.*_(\d+)$/;
   $time = $1;
   push @l, $time;
}

for ($i=0; $i < @l; $i++) {
    $audioOut = $audio;
    $audioOut =~ s/.wav$//;
    $audioOut = "$audioOut-$l[$i].wav";
    $dur = $en[$i]-$st[$i];
    system("sox $audio $audioOut trim $st[$i] $dur");
}

