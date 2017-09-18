BEGIN{
if (max=="") max=3
cmd="for i in {0..255} | shuf "
while ( ( cmd | getline result ) > 0 ) {
print result
}
}
{
print
for (i=4; i >max ; i-=1)
	print $i
}
