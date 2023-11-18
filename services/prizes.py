# standard library
import xml.etree.ElementTree as ET

# third party library
import requests

# local library
from globals.variables import URL


class PrizeInfo():
    """獎項資訊
    """
    def __init__(self, title: str, special: str, grand: str, first: list[str]):
        """
        Attributes
        ----------
        + `title` (str): 期別
        + `special` (str): 特別獎
        + `grand` (str): 特獎
        + `first` (list[str]): 頭獎
        """
        self.title = title
        self.special = special
        self.grand = grand
        self.first = first

    @classmethod
    def from_fetch(cls, n: int) -> "PrizeInfo":
        """PrizeInfo 工廠函式，解析 XML 並取得中獎號碼資訊

        Parameters
        ----------
        + `n` (int): 前 n 期

        Returns
        -------
        + (PrizeInfo): 獎項資訊
        """
        
        response = requests.get(URL)
        tree = ET.fromstring(response.text)             # 解析 XML
        items = list(tree.iter("item"))                 # 取得 item 標籤內容
        title = items[n].find("./title").text           # 取得 期別
        ptext = items[n].find("./description").text     # 取得 中獎號碼
        templist = ptext.replace("</p>", "").split("：")

        return cls(title,                         # 期別
                   templist[1][:8],               # 特別獎
                   templist[2][:8],               # 特獎
                   templist[3].split("、"))       # 頭獎

    def format(self) -> str:
        """獎項資訊格式化

        Returns
        -------
        - (str): 獎項資訊格式化字串
        """
        return f"""{self.title}\n特別獎：{self.special}\n特獎：{self.grand}\n頭獎：{self.first[0]}、{self.first[1]}、{self.first[2]}"""

    def check_invoice(self, last_three_digits: str) -> tuple[bool, str]:
        """對後三碼進行對獎動作

        Parameters
        ----------
        - `last_three_digits` (str): 後三碼 

        Returns
        -------
        + (tuple[bool, str]): 
            - 是否中獎 (bool)
            - 回傳訊息 (str)
        """
        try:
            three_digits = [num[-3:] for num in (self.special, self.grand, *self.first)]
            if last_three_digits in three_digits:
                reply_text = "符合某獎項後三碼，請自行核對發票前五碼！"
                win = True
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
