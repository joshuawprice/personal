
Set server icon with a 64x64 image named 'server-icon.png'
```sh
magick image.png -resize 64x64 -filter Lanczos server-icon.png
```

Build for arm with --platform linux/arm64
```sh
docker build -t velocity --platform linux/arm64 .
```

Write out image to file
```sh
docker save velocity:latest | zstd -12 > velocity-arm.img.zst
```

Load the image file
```sh
zstd -cd velocity.img.zst | docker load
```
