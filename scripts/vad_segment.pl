$fname=shift @ARGV;
$frames = 0;
$start = 0;
$vcount = 0;
$uvcount = 0;
@segs = ();
open F, "> segments";
while (<STDIN>) {
  chomp;
  if (/^([01])/) {
     $frames++;
     $vad = $1;
     if ($vad == 0) {
        if ($uvcount > 0) {  
           $uvcount++;
           if ($uvcount >= 100 && $frames-$start > $uvcount) {
               $stop = $frames-1;
               printf F "${fname}_%07d $fname %0.2f %0.2f\n", $start, $start/100, $stop/100;
               $segid=sprintf "${fname}_%07d", $start;
               push @segs, $segid;
               $start = $frames;
			  }
           if ($uvcount == $frames - $start) {
 					$start++;
			  }
           
        }
        else {
           # was voiced
           $stop = $frames;
           if ($frames-$start > 1000) {
               printf F "${fname}_%07d $fname %0.2f %0.2f\n", $start, $start/100, $stop/100;
                $segid=sprintf "${fname}_%07d", $start;
                push @segs, $segid;
               $start = $frames;
           }
           $uvcount = 1;
           $vcount = 0;
       }
     } else {
 
        $vcount++;


	  }
     
    
  }

}

if ($frames- $start > $uvcount) {
  $stop = $frames - $uvcount;
  printf F "${fname}_%07d $fname %0.2f %0.2f\n", $start, $start/100, $stop/100;
  $segid=sprintf "${fname}_%07d", $start;
  push @segs, $segid;
}

close F;
open F, "> spk2utt";
print F "$fname @segs\n";
close F;
