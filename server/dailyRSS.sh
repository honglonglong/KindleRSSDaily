rm -f $(dirname $(readlink -f $0))/../temp/*
echo $(dirname $(readlink -f $0))
python $(dirname $(readlink -f $0))/send.py
