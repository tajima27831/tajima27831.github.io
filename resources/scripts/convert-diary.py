from pathlib import Path
import sys

# diary.mdをばらして各日のsource.mdにする

if len(sys.argv) < 2:
    print("【エラー】ファイルのパスを指定してください。")
    sys.exit(1)  # プログラムを終了する ０は正常終了

source_file_path = Path(sys.argv[1])