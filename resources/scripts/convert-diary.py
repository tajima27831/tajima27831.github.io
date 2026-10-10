from pathlib import Path
import sys
import datetime
from zoneinfo import ZoneInfo
today = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()

# diary.mdをばらして各日のsource.mdにする

if len(sys.argv) < 2:
    print("【エラー】ファイルのパスを指定してください。")
    sys.exit(1)  # プログラムを終了する ０は正常終了

source_file_path = Path(sys.argv[1])
directory_path_list = sys.argv[1].split("/")[:-1] # 例えば ['diary', '2026', '9']

#--------------------------ヘッド--------------------------------

head_1 = [
    "<!doctype html>",
    "<html lang=\"ja\">",
    "  <head>",
    "    <link rel=\"icon\" href=\"/resources/images/diagram.jpg\" type=\"image/x-icon\"/>",
    "    <meta charset=\"UTF-8\"/>",
    "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>",
    "    <link href=\"/resources/styles/common.css\" rel=\"stylesheet\"/>"
]

head_metadata = [
]

head_2 = [
    "  </head>"
]

#--------------------------------ヘッダー-----------------------------------

header_1 = [
    "  <body>",
    "    <header>",
    "      <div class=\"site-name\">今それどころじゃない</div>",
    "",
    "      <hr>",
    ""
]

header_breadcrumb = [
]

header_2 = [
    "",
    "      <div class=\"last-update\">このページの最終更新：<time datetime=\"" + today.strftime("%Y-%m-%d") + "\">" + today.strftime("%Y年%m月%d日") + "</time></div>",
    ""
]

header_contents = [
    "      <nav class=\"contents\">",
    "        このページの目次："
]

header_3 = [
    "    </header>"
]

#----------------------------------メイン------------------------------------

main = [
    "    <main>"
]

#---------------------------------フッター------------------------------------------

footer = [
    "",
    "    <hr>",
    "",
    "    <footer>",
    "      <nav class=\"back-to-top\">",
    "        <a href=\"#\">このページの一番上へ</a>",
    "      </nav>",
    "    </footer>",
    "  </body>",
    "</html>"
]

with open(source_file_path, "r", encoding="utf-8") as diary:
    for line in diary:
        if line[0] == "- index\n":
            print("something")