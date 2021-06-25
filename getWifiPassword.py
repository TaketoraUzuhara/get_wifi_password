import subprocess
import re

"""PC内に保存されている接続履歴のあるWifiのパスワードを取得するプログラム。

※このプログラムは、Pythonの自己学習のために作成したものです。
　機密情報を取り扱うため、プログラムを実行する際は細心の注意を払ってください。
　また、このプログラムに伴うトラブルについては一切責任を負いません。
"""



# コマンドプロンプトの設定言語を英語に変更
subprocess.run(["chcp", "437"], shell=True)

# 接続済みWifiの情報取得
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

# 出力されたWifiのSSIDを取得
profile_names = re.findall("All User Profile     : (.*)\r", command_output)
# 最終的な結果リスト定義
wifi_list = list()

# 出力されたWifiのSSIDが存在した場合処理を行う
if len(profile_names) != 0:
    for name in profile_names:
        # 抽出した情報を辞書型で保存する
        wifi_profile = dict()
        # 各SSIDの詳細情報を出力
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        if re.search("Key Content            : Absent", profile_info):
            continue
        else:
            # 辞書型結果データに抽出したSSIDの名前を入れる
            wifi_profile["ssid"] = name
            # 隠されたWifiパスワードを見える状態で出力
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            # パスワードを抽出
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            # パスワードが存在するか判定
            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
        wifi_list.append(wifi_profile)

for index in range(len(wifi_list)):
    print(wifi_list[index])