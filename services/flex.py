# standard library
from typing import Any
from pathlib import Path

# local library
from globals.variables import CWD
from services.prizes import PrizeInfo
from services.serialize import Accessor, Pickle


def invo(prizeinfo: PrizeInfo) -> dict[str, Any]:
    """中獎號碼 bubble

    Parameters
    ----------
    + `prizeinfo` (PrizeInfo): 獎項資訊

    Returns
    -------
    + (dict[str, Any]): JSON 格式 bubble
    """

    # 讀入 bubble 模板
    template_path = Path("templates/flex_messages/invoice_template.pkl")
    contents = Accessor(Pickle()).read(CWD / template_path)

    # 修改模板 text
    contents["body"]["contents"][1]["text"] = prizeinfo.title
    contents["body"]["contents"][2]["contents"][1]["text"] = prizeinfo.special
    contents["body"]["contents"][4]["contents"][0]["contents"][1]["text"] = prizeinfo.grand
    contents["body"]["contents"][4]["contents"][1]["contents"][1]["text"] = prizeinfo.first[0]
    contents["body"]["contents"][4]["contents"][2]["contents"][1]["text"] = prizeinfo.first[1]
    contents["body"]["contents"][4]["contents"][3]["contents"][1]["text"] = prizeinfo.first[2]

    return contents

def multi_invo(prizeinfos: list[PrizeInfo]) -> dict[str, Any]:
    """中獎號碼 carousel

    Parameters
    ----------
    + `prizeinfos`:  (list[PrizeInfo])

    Returns
    -------
    + JSON 格式 carousel (dict[str, Any])
    """
    contents_carousel = {
        "type": "carousel",
        "contents": []
    }
    for prizeinfo in prizeinfos:
        contents_carousel["contents"].append(invo(prizeinfo))
    return contents_carousel


if __name__ == "__main__":
    pass
