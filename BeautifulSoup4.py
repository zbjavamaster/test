import json
from bs4 import BeautifulSoup

class Test:
    def __init__(self):
        pass

    def run(self):
        # 源文件
        with open("E:\\2022.xml", encoding='utf-8') as fp:
            soup = BeautifulSoup(fp.read(), 'xml')
        # 结果文件
        with open("E:\\result.txt", 'a', encoding='utf-8') as file:
            for entry in soup.cnnvd.children:
                if not str(entry).strip():
                    continue
                # list_iterator类型 向下寻找子节点
                child = entry.children
                entry_dict = self.run_children(child)
                # Json序列化写入文件
                file.write(json.dumps(entry_dict, ensure_ascii=False)+"\n")

    def run_children(self, child):
        # 每一个entry存一条
        entry_dict = dict()
        for zi in child:
            if not str(zi).strip():
                continue
            # 判断是否存在子节点，存在则递归
            if not zi.string and zi.contents:
                key = zi.name
                value = self.run_children(zi.children)
            else:
                key = zi.name
                value = zi.string
            last_value = entry_dict.get(key)
            # 如果有值，则key重复，value存成list
            if last_value:
                # 3-n次追加：list.append追加新值
                if isinstance(last_value, list):
                    entry_dict[key] = last_value.append(value)
                else:
                    # 2次追加:值为string类型，追加新string后，类型变成list
                    entry_dict[key] = [last_value, value]
            else:
                # 首次：key:value
                entry_dict[key] = value
        return entry_dict


if __name__ == '__main__':
    test = Test()
    test.run()
