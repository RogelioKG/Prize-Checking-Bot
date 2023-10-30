# standard library
import json
from typing import Any

# local library
from global_vars import PATH


def invo(prizeinfo: tuple[str, list]) -> dict[str, Any]:
    """
    中獎號碼 bubble

    Parameters
    ----------
    - `prizeinfo`: 獎項資訊 (tuple[str, list])

    Returns
    -------
    - JSON 格式 bubble (dict[str, Any]) 
    """
    title, prizelist = prizeinfo
    special, grand, first = prizelist
    
    # 讀入 bubble 模板
    template_name = "invoice_template.json"
    with open(PATH + template_name, encoding="utf-8") as json_file:
        contents = json.loads(json_file.read())
        
    # 修改模板 text
    contents["body"]["contents"][1]["text"] = title
    contents["body"]["contents"][2]["contents"][1]["text"] = special
    contents["body"]["contents"][4]["contents"][0]["contents"][1]["text"] = grand
    contents["body"]["contents"][4]["contents"][1]["contents"][1]["text"] = first[0]
    contents["body"]["contents"][4]["contents"][2]["contents"][1]["text"] = first[1]
    contents["body"]["contents"][4]["contents"][3]["contents"][1]["text"] = first[2]

    return contents

def multi_invo(prizeinfos: list[tuple[str, list]]) -> dict[str, Any]:
    """
    中獎號碼 carousel

    Parameters
    ----------
    - `prizeinfos`: 多期獎項資訊 (list[tuple[str, list]])

    Returns
    -------
    - JSON 格式 carousel (dict[str, Any])
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
