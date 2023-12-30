import re
import xml.sax
import argparse
from time import *


class BiosampleHandler(xml.sax.ContentHandler):
    # 创建一个BiosampleHandler类，继承xml.sax.ContentHandler类
    # 实现了它的 startElement()，endElement() 以及 characters()方法
    def __init__(self,output):
        self.CurrentData = ""
        self.n = ""
        self.output = output
    # 文档启动的时候调用
    def startDocument(self):
        self.__title = "Biosample_accession\tTitle\tPackage\tHost\ttaxonomy_id\ttaxonomy_name\tisolation_source\tgeo_loc_name\tcollection_date\tBacterial Vaginosis\tsample_type\thost_disease\n"
        with open(self.output, "w", encoding="utf-8", errors="ignore") as biosample_extract:
            biosample_extract.writelines(self.__title)

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        # 遇到XML开始标签时调用
        # tag表示标签名
        # attributes表示标签的属性值字典
        self.CurrentData = tag
        if self.CurrentData == "BioSample":
            self.dic = {"Biosample_accession": "", "Title": "", "Package": "", "Host": "",
                        "taxonomy_id": "", "taxonomy_name": "", "geo_loc_name": "",
                        "collection_date": "", "isolation_source": "", "Bacterial Vaginosis": "",
                        "sample_type": "","host_disease": ""}
            if "accession" in attributes:
                self.dic["Biosample_accession"] = attributes["accession"]
            else:
                self.dic["Biosample_accession"] = "not_exist"
        elif self.CurrentData == "Attribute":
            if "display_name" in attributes and attributes["display_name"] == "host":
                self.n = "host"
            if "display_name" in attributes and attributes["display_name"] == "isolation source":
                self.n = "isolation source"
            if "display_name" in attributes and attributes["display_name"] == "geographic location":
                self.n = "geographic location"
            if "display_name" in attributes and attributes["display_name"] == "collection date":
                self.n = "collection date"
            if "display_name" in attributes and attributes["attribute_name"] == "Bacterial Vaginosis":
                self.n = "Bacterial Vaginosis"
            if "display_name" in attributes and attributes["attribute_name"] == "sample_type":
                self.n = "sample_type"
            if "display_name" in attributes and attributes["display_name"] == "host disease":
                self.n = "host disease"
        elif self.CurrentData == "Organism":
            if "taxonomy_id" in attributes:
                self.dic["taxonomy_id"] = attributes["taxonomy_id"]
            else:
                self.dic["taxonomy_id"] = "not_exist"
            if "taxonomy_name" in attributes:
                self.dic["taxonomy_name"] = attributes["taxonomy_name"]

    # 元素结束事件处理
    def endElement(self, tag):
        # 遇到XML结束标签时调用
        # tag表示标签的名字
        self.n = ""
        if tag == "BioSample":
            with open(self.output, "a", encoding="utf-8", errors="ignore") as biosample_extract:
                biosample_extract.writelines(
                re.sub("[\t\n]","",self.dic["Biosample_accession"])+"\t"+
                re.sub("[\t\n]","",self.dic["Title"])+"\t"+
                re.sub("[\t\n]","",self.dic["Package"])+"\t"+
                re.sub("[\t\n]","",self.dic["Host"])+"\t"+
                re.sub("[\t\n]","",self.dic["taxonomy_id"])+"\t"+
                re.sub("[\t\n]","",self.dic["taxonomy_name"])+"\t"+
                re.sub("[\t\n]","",self.dic["isolation_source"])+"\t"+
                re.sub("[\t\n]","",self.dic["geo_loc_name"])+"\t"+
                re.sub("[\t\n]","",self.dic["collection_date"])+"\t"+
                re.sub("[\t\n]","",self.dic["Bacterial Vaginosis"])+"\t"+
                re.sub("[\t\n]","",self.dic["sample_type"])+"\t"+
                re.sub("[\t\n]","",self.dic["host_disease"])+"\n")
            # print(self.dic)
            # print("========我是一条美丽的Biosample分割线========")
        self.CurrentData = ""

    # 内容事件处理
    def characters(self, content):
        # 遇到XML元素内容时调用
        # content为元素的内容
        if self.CurrentData == "Title":
            self.dic["Title"] = content
        elif self.CurrentData == "Package":
            self.dic["Package"] = content
        elif self.n == "host":
            self.dic["Host"] = content
        elif self.n == "isolation source":
            self.dic["isolation_source"] = content
        elif self.n == "geographic location":
            self.dic["geo_loc_name"] = content
        elif self.n == "collection date":
            self.dic["collection_date"] = content
        elif self.n == "Bacterial Vaginosis":
            self.dic["Bacterial Vaginosis"] = content
        elif self.n == "sample_type":
            self.dic["sample_type"] = content
        elif self.n == "host disease":
            self.dic["host_disease"] = content


def main():
    parser = argparse.ArgumentParser(description="A script that can extract infomation of interest from NCBI BioSample database")
    parser.add_argument('--input', help="eg, biosample_set.xml", required=True)
    parser.add_argument('--output', help="eg, biosample_extract.tsv", required=True)
    argv = parser.parse_args()

    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # 重写 ContextHandler
    Handler = BiosampleHandler(argv.output)
    # 设置当前的ContentHandler为我们自己写的handler实例。如果不进行设置，content 事件会被忽略。
    parser.setContentHandler(Handler)
    # 开始解析 xml文件。
    parser.parse(argv.input)


if (__name__ == "__main__"):
    begin_time = time()
    main()
    end_time = time()
    print("RUN TIME:", end_time - begin_time)
