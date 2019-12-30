
if [ -z "$1" ]
then
    echo "must provide folder name"
    return 0
fi

folder=$1

rm $folder/__init__.py*
rm $folder/*/__init__.py*
rm $folder/*/*/__init__.py*
rm $folder/*/*/*/__init__.py*
rm $folder/*/*/*/*/__init__.py*
rm $folder/*/*/*/*/*/__init__.py*
