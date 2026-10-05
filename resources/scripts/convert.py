from pathlib import Path
import sys
import datetime
from zoneinfo import ZoneInfo

#-----------------------------準備-----------------------------------

if len(sys.argv) < 2:
    print("【エラー】ファイルのパスを指定してください。")
    sys.exit(1)  # プログラムを終了する ０は正常終了

source_file_path = Path(sys.argv[1])
directory_path_list = sys.argv[1].split("/")[:-1]#一番最後の空stringを削除したリスト
path_length = len(directory_path_list)#ホームを含まない

index_file_path = Path("/".join(directory_path_list) + "/index.html")

if not source_file_path.exists():
    print(f"【エラー】指定されたファイルが見つかりません: {source_file_path}")
    #fはpath型をstring型に自動で変えるために必要
    sys.exit(1)

today = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()

nest_stack = [] # ネスト

h_before = [
    "      <h1>",
    "        <h2>",
    "          <h3>",
    "            <h4>"
]
h_after = [
    "</h1>",
    "</h2>",
    "</h3>",
    "</h4>"
]

indent_list = [ # インデント用の空白 indexの二倍の数の半角スペース
    "",
    "  ",
    "    ",
    "      ",
    "        ",
    "          ",
    "            ",
    "              ",
    "                ",
    "                  ",
    "                    ",
    "                      ",
    "                        "
]

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
    "      <div class=\"site-name\">強迫的敗北主義反芻派</div>",
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

#---------------------------------抽出---------------------------------------

with open(source_file_path, mode="r", encoding="utf-8") as source:
    for line in source:
        if line == "\n":
            continue

        #--------------------------------mdの一行目--------------------------------------
        if not line[0] in ["-"," "]:
            directory_path_from_source_list = line.split("/")[:-1]#ホームから始まる
            if not len(directory_path_from_source_list) == path_length+1:
                print("pathの長さが合いません")
                print(len(directory_path_from_source_list))
                sys.exit(1)
            for i in range(path_length):
                if not directory_path_from_source_list[i+1] == directory_path_list[i]:
                    print("pathが合いません")
                    sys.exit(1)
            continue

        #--------------------------------mdの三行目---------------------------------
        if line[0] == "-":
            #---------------------メタデータの取得-------------------------
            metadata = line.split(":")
            if not len(metadata) == 3:
                print("メタデータの数が合いません")
                sys.exit(1)
            title_list = metadata[1].split("/")[:-1] # 一番最後の空を削除
            title = title_list[path_length]
            if not len(title_list) == path_length+1:
                print("日本語タイトルの数が合いません")
                sys.exit(1)
            description = metadata[2].strip() # 最後の開業文字を削除

            head_metadata = [
                "    <meta name=\"description\" content=\"" + description + "\"/>",
                "    <title>" + title + "｜強迫的敗北主義反芻派</title>"
            ]

            header_breadcrumb.append("      <nav aria-label=\"Breadcrumb\">")
            header_breadcrumb.append("        <ul class=\"breadcrumb\">")
            for i in range(path_length):
                header_breadcrumb.append("          <li><a href=\"")
                for j in range(i+1):
                    header_breadcrumb[-1] += (directory_path_from_source_list[j] + "/")
                header_breadcrumb[-1] += ("\">" + title_list[i] + "</a></li>")
            header_breadcrumb.append("          <li><span aria-current=\"page\">" + title + "</span></li>")
            header_breadcrumb.append("        </ul>")
            header_breadcrumb.append("      </nav>")

            main.append(h_before[0] + title + h_after[0])
            continue

        if not line[0] == " ":
            print(line)
            print("mdファイルの異常")
            sys.exit(1)

        #-----------------------------メイン---------------------------------------------

        striped_line = line.strip()
        striped_line = striped_line[2:]

        #------------------------------見出しか箇条書き--------------------------------
        if striped_line[0] == ":":
            if len(striped_line.split(":")) > 3:
                print(striped_line)
                print("md内での構文ミス")
                sys.exit(1)
            #------------------------------箇条書き----------------------------------
            if len(striped_line.split(":")) == 2:
                nest_stack.append("u")
                main.append(indent_list[len(nest_stack)+2] + "<ul>")
                continue

            #--------------------------------見出し-----------------------------------
            if len(striped_line.split(":")) == 3:
                if (len(nest_stack) > 0 and nest_stack[-1] == "u"): # 箇条書きを閉じる
                    main.append(indent_list[len(nest_stack)+2] + "</ul>")
                    del nest_stack[-1:]
                
                section_title = striped_line.split(":")[1]
                section_id = striped_line.split(":")[2]
                if not len(section_id.split("/"))*2 == len(line.split(":")[0])-2:
                    print("セクションのidのミス")
                    print(section_title + "  " + section_id)
                    sys.exit(1)
                
                while len(section_id.split("/")) < len(nest_stack): # ネストを同じ深さ以下にする
                    main.append(indent_list[len(nest_stack)+2] + "</section>")
                    header_contents.append(indent_list[len(nest_stack)*2+3] + "</li>")
                    header_contents.append(indent_list[len(nest_stack)*2+2] + "</ul>")
                    del nest_stack[-1:]
                
                if len(section_id.split("/")) == len(nest_stack): # 同じ深さを閉じてから始めるとき
                    main.append(indent_list[len(nest_stack)+2] + "</section>")
                    main.append("")
                    main.append(indent_list[len(nest_stack)+2] + "<section id=\"" + section_id + "\">")
                    main.append(h_before[len(nest_stack)] + section_title + h_after[len(nest_stack)])
                    header_contents.append(indent_list[len(nest_stack)*2+3] + "</li>")
                    header_contents.append(indent_list[len(nest_stack)*2+3] + "<li>")
                    header_contents.append(indent_list[len(nest_stack)*2+4] + "<a href=\"#" + section_id + "\">" + section_title + "</a>")
                
                if len(section_id.split("/")) > len(nest_stack): # 新しい深さに入るとき
                    nest_stack += "s"
                    main.append("")
                    main.append(indent_list[len(nest_stack)+2] + "<section id=\"" + section_id + "\">")
                    main.append(h_before[len(nest_stack)] + section_title + h_after[len(nest_stack)])
                    header_contents.append(indent_list[len(nest_stack)*2+2] + "<ul>")
                    header_contents.append(indent_list[len(nest_stack)*2+3] + "<li>")
                    header_contents.append(indent_list[len(nest_stack)*2+4] + "<a href=\"#" + section_id + "\">" + section_title + "</a>")
            continue

        #-----------------------------------本文か箇条書きの項目------------------------------------
        # あとでここにリンクの置換による記法を追加
        if (len(nest_stack) > 0 and nest_stack[-1] == "u"):
            main.append(indent_list[len(nest_stack)+4] + "<li>" + striped_line + "</li>")
        else:
            main.append(indent_list[len(nest_stack)+3] + "<p>" + striped_line + "</p>")

#-------------------------------------------メインの最後にタグを閉じる------------------------
while 0 < len(nest_stack): # ネストを同じ深さ以下にする
    if (len(nest_stack) > 0 and nest_stack[-1] == "u"): # 箇条書きを閉じる
        main.append(indent_list[len(nest_stack)+2] + "</ul>")
        del nest_stack[-1:]
        continue
    main.append(indent_list[len(nest_stack)+2] + "</section>")
    header_contents.append(indent_list[len(nest_stack)*2+3] + "</li>")
    header_contents.append(indent_list[len(nest_stack)*2+2] + "</ul>")
    del nest_stack[-1:]

main.append("    </main>")
header_contents.append("      </nav>")

#--------------------------------------生成---------------------------------------------
print(str(index_file_path))
with open(index_file_path, "w", encoding="utf-8") as result:
    print(*head_1, sep="\n", file=result)
    print(*head_metadata, sep="\n", file=result)
    print(*head_2, sep="\n", file=result)
    print("", file=result)
    print(*header_1, sep="\n", file=result)
    print(*header_breadcrumb, sep="\n", file=result)
    print(*header_2, sep="\n", file=result)
    print(*header_contents, sep="\n", file=result)
    print(*header_3, sep="\n", file=result)
    print("\n    <hr>\n", file=result)
    print(*main, sep="\n", file=result)
    print(*footer, sep="\n", file=result)