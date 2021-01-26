rm -f $(dirname $(readlink -f $0))/../temp/*
echo "running directory:" $(dirname $(readlink -f $0))
python $(dirname $(readlink -f $0))/send.py
