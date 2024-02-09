out=$(echo "$1" | cut -f 1 -d '.')

mkdir out/$out
mkdir out/$out/segs
echo "splitting $1 into segments of $2 seconds with an fps of $3 and a width of $4"
ffmpeg -i $1 -reset_timestamps 1 -force_key_frames "expr:gte(t,n_forced*$2)" -r $3 -filter:v fps=$3 -filter:v scale=$4:-1 -map 0 -segment_time 00:00:$2 -f segment "out/$out/segs/%d.mp4"

mkdir "out/$out/gifs"
mkdir "out/$out/frames"
mkdir "out/$out/sheets"

cd out/$out/segs;

for i in *.mp4; do
    gifski --fps $3 --width $4 -o "../gifs/${i%.*}.gif" "$i"
    # ffmpeg -i "$i" -pix_fmt rgb8 "../gifs/${i%.*}.gif";
done

cd ../../../;
python3 spriter.py $out
