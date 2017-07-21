while read i;
do
  echo "$i" | python -m json.tool ;
done < $1
