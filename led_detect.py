import cv2
import numpy as np

"""
LEDのカラーと

author Riku Yamamoto
"""
class ColorLEDDetecter(object):

    """
    inputは，実行するファイルだけでなく，"rtsp://[ip_address]/[access_point].sdp"
    などの指定でIPカメラにも対応可能
    """
    def __init__(self, input="test.mov"):
        self.cap = cv2.VideoCapture(input)
        self.mask = cv2.imread("mask.png", cv2.IMREAD_GRAYSCALE)

    """
    HSV領域をカラーによって指定する．opencvでは色相は360°ではなく180°で考える．
    """
    def _get_range(self, color):
        if color == "blue":
            return self._hf(120)
        if color == "green":
            return self._hf(60)
        if color == "red":
            return self._hf(0)
        if color == "skyblue":
            return self._hf(90)
        if color == "yellow":
            return self._hf(30)
        if color == "purple":
            return self._hf(135)
        else:
            return (0, 0, 0), (0, 0, 0)

    """
    HSVの値域，lowerとupperのフォーマットを設定する．
    """
    def _hf(self, value, margin=10):
        return (value - margin, 100, 50), (value + margin, 255, 255)

    """
    輪郭検出．座標を抽出する．
    """
    def contours(self, org_image, mask, color, options="time"):
        # 輪郭の選択　もっとも外側のみ
        retr = cv2.RETR_EXTERNAL
        # 外郭点の保持の方法．近似
        approx = cv2.CHAIN_APPROX_SIMPLE
        _, contours, history = cv2.findContours(mask, cv2.RETR_EXTERNAL, approx)
        for i , cnt in enumerate(contours):
            # 次元削減
            cnt = np.squeeze(cnt, axis=1)
            # log
            print("[{}]{}: {}".format(options, color, cnt[0]))
            # 描画関数．
            if org_image is not None:
                fontType = cv2.FONT_HERSHEY_SIMPLEX
                try:
                    cv2.putText(org_image, "[{}]{}".format(i, color),(cnt[0][0], cnt[0][1]), fontType, 1, (0, 0, 255), 1)
                except:
                    pass


    """
    画像の前処理 (ぼかしてノイズを減らす)
    """
    def smooth(self, img, box=(11, 11)):
        # 平均フィルタ を使った平滑化
        # im_smooth = cv2.blur(img, box)

        # 中央値フィルタ 　を使った平滑化
        # im_smooth = cv2.medianBlur(img, box[0])

        # ガウスフィルタによる平滑化
        im_smooth = cv2.GaussianBlur(img, box, 0)
        return im_smooth

    """
    video output
    """
    def write_video(self, path="output.mp4"):
        fourcc = cv2.VideoWriter_fourcc(*"H264")
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width  = int(self.cap.get(3))
        height = int(self.cap.get(4))
        writer = cv2.VideoWriter(path, fourcc, fps, (width, height))

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = self.smooth(frame, box=(15, 15))
                # HSV空間に変換
                frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # 各色を検出する．
                mask = np.zeros(frame_hsv.shape[:2], dtype=np.uint8)
                # 各色に適応
                for color in list(["green", "blue", "red", "skyblue", "yellow", "purple"]):
                    # color情報を取得し，画像の色調範囲を指定する．
                    lower, upper = self._get_range(color)
                    m = cv2.inRange(frame_hsv, lower, upper)
                    # 必要ならマスク演算を行う (意図しない部分を消す )
                    m = cv2.bitwise_and(m, m, mask=self.mask)

                    # 領域抽出によって対象座標を見つける．
                    self.contours(frame, m, color, options=str(self.cap.get(1)))
                    # 各カラーのmaskを合算する．
                    #mask = cv2.bitwise_or(mask, m)
                # 全てのmaskを適用
                #frame = cv2.bitwise_and(frame, frame, mask=mask)
                # 動画に出力する．
                writer.write(frame)
            else:
                break



if __name__ == "__main__":
    detecter = ColorLEDDetecter()
    detecter.write_video()
