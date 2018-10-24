# LEDDetect
OpenCVを用いてLEDの発光色と座標情報を検出する．手順は以下の通り．

1. 発光したLEDを撮影する．
2. OpenCVで取り込み，HSVに変換
3. HSVの一定値域で抽出
4. 抽出した画像から，輪郭抽出を行い座標を出力する．

## 開発環境
* Python3.6.5
* OpenCV 3.4.0
* anaconda 3
* MacbookAir 2015

### 導入
```
$ pip install opencv-python
```

### 実行(実装まだ)
```
$ python run.py
```

## License
MIT
