# standard library
import xml.etree.ElementTree as ET

# third party library
import requests

# local library
from global_vars import URL


def mono_num(n: int) -> tuple[str, list]:
    """
    解析 XML 並取得中獎號碼資訊

    Parameters
    ----------
    - `n`: 前 n 期 (int)

    Returns
    -------
    - `prizeinfo`: 獎項資訊 (tuple[str, list])
        - `title`: 期別 (str) 
        - `prizelist`: 中獎號碼 (list)
            - 特別獎 (str)
            - 特獎 (str)
            - 頭獎 (list[str])
    """
    response = requests.get(URL)
    tree = ET.fromstring(response.text)             # 解析 XML
    items = list(tree.iter("item"))                 # 取得 item 標籤內容
    title = items[n].find("./title").text           # 取得 期別
    ptext = items[n].find("./description").text     # 取得 中獎號碼
    templist = ptext.replace("</p>", "").split("：")
    prizelist = []
    prizelist.append(templist[1][:8])               # 特別獎
    prizelist.append(templist[2][:8])               # 特獎
    prizelist.append(templist[3].split("、"))        # 頭獎
    prizeinfo = (title, prizelist)

    return prizeinfo

def formatted(prizeinfo: tuple[str, list]) -> str:
    """
    獎項資訊格式化

    Parameters
    ----------
    - `prizeinfo`: 獎項資訊 (tuple[str, list])

    Returns
    -------
    - 獎項資訊格式化字串 (str)
    """
    title, prizelist = prizeinfo
    special, grand, first = prizelist
    
    return f"""{title}\n特別獎：{special}\n特獎：{grand}\n頭獎：{first[0]}、{first[1]}、{first[2]}"""

def last_three_digit(mtext: str, prizeinfo: tuple[str, list]) -> str:
    """
    對後三碼進行對獎動作

    Parameters
    ----------
    - `mtext`: 後三碼 (str)
    - `prizeinfo`: 獎項資訊 (tuple[str, list])

    Returns
    -------
    - (tuple[bool, str])
        - 是否中獎 (bool)
        - 回傳訊息 (str)
    """
    try:
        _, prizelist = prizeinfo
        special, grand, first = prizelist
        three_digits = [num[-3:] for num in (special, grand, *first)]
        if mtext in three_digits:
            reply_text = "符合某獎項後三碼，請自行核對發票前五碼！"
            win = True
            # reply_text += "\n\n"
            # reply_text += formatted(prizeinfo)
        else:
            reply_text = "很可惜，未中獎。請輸入下一張發票最後三碼。"
            win = False

    except Exception:
        reply_text = "讀取發票號碼發生錯誤！"
        win = None

    finally:
        return (win, reply_text)


if __name__ == "__main__":
    pass
