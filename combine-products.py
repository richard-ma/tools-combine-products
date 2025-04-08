#!/usr/bin/env python
# -*- coding: utf-8 -*-
# APP Framework 1.0
import copy
import csv
import os
import sys
import shutil
from pprint import pprint


class App:
    def __init__(self):
        self.title_line = sys.argv[0]
        self.counter = 1
        self.workingDir = None

    def printCounter(self, data=None):
        print("[%04d] Porcessing: %s" % (self.counter, str(data)))
        self.counter += 1

    def initCounter(self, value=1):
        self.counter = value

    def run(self):
        self.usage()
        self.process()
        self.pressAnyKeyToContinue()

    def usage(self):
        print("*" * 80)
        print("*", " " * 76, "*")
        print(" " * ((80 - 12 - len(self.title_line)) // 2),
              self.title_line,
              " " * ((80 - 12 - len(self.title_line)) // 2))
        print("*", " " * 76, "*")
        print("*" * 80)

    def input(self, notification, default=None):
        var = input(notification)

        if len(var) == 0:
            return default
        else:
            return var

    def readTxtToList(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            for row in f.readlines():
                # remove \n and \r
                data.append(row.replace('\n', '').replace('\r', ''))
        return data

    def readCsvToDict(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def writeCsvFromDict(self, filename, data, fieldnames=None, encoding="GBK", newline=''):
        if fieldnames is None:
            fieldnames = data[0].keys()

        with open(filename, 'w+', encoding=encoding, newline=newline) as f:
            writer = csv.DictWriter(f,
                                    fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def addSuffixToFilename(self, filename, suffix):
        filename, ext = os.path.splitext(filename)
        return filename + suffix + ext

    def getWorkingDir(self):
        return self.workingDir

    def setWorkingDir(self, wd):
        self.workingDir = wd
        return self.workingDir

    def getFilesFromDir(self, path, only_file=True, filter_with_ext=''):
        for file in os.listdir(path):
            if only_file:
                if os.path.isfile(os.path.join(path, file)):
                    if len(filter_with_ext) == 0:
                        yield file
                    elif len(filter_with_ext) > 0 and file.endswith(filter_with_ext):
                        yield file
                    else:
                        continue
                else:
                    continue
            else:
                yield file

    def setWorkingDirFromFilename(self, filename):
        return self.setWorkingDir(os.path.dirname(filename))

    def pressAnyKeyToContinue(self):
        os.system('pause')

    def process(self):
        pass


class MyApp(App):
    def __init__(self):
        super().__init__()

    def getProductCode(self, d):
        productCodeList = list()
        for row in d:
            productCodeList.append(row['ProductCode'])
        return productCodeList

    def process(self):
        # set working directory
        self.setWorkingDir('.')
        # pprint(self.workingDir)

        aFileName = "1.csv"
        bFileName = "2.csv"

        bothFileName = "new.csv"
        onlyAFileName = "first.csv"
        onlyBFileName = "second.csv"

        print("Loading files...")
        aData = self.readCsvToDict(aFileName)
        bData = self.readCsvToDict(bFileName)

        aProductCodeList = self.getProductCode(aData)
        print("Loaded %d records from %s" % (len(aData), aFileName))
        bProductCodeList = self.getProductCode(bData)
        print("Loaded %d records from %s" % (len(bData), bFileName))

        bothProductCodeList = list(set(aProductCodeList).intersection(set(bProductCodeList)))
        print("Found %d records in both files" % len(bothProductCodeList))
        onlyAProductCodeList = list(set(aProductCodeList).difference(set(bProductCodeList)))
        print("Found %d records only in %s" % (len(onlyAProductCodeList), aFileName))
        onlyBProductCodeList = list(set(bProductCodeList).difference(set(aProductCodeList)))
        print("Found %d records only in %s" % (len(onlyBProductCodeList), bFileName))

        bothData = list()
        onlyAData = list()
        onlyBData = list()
        for record in aData:
            if record['ProductCode'] in bothProductCodeList:
                t = record
                for b in bData:
                    if b['ProductCode'] == record['ProductCode']:
                        t.update(b)
                        break
                bothData.append(t)
            else:
                onlyAData.append(record)

        for record in bData:
            if record['ProductCode'] in onlyBProductCodeList:
                onlyBData.append(record)
        
        aTitleline = list(aData[0].keys())
        bTitleline = list(bData[0].keys())
        titleline = copy.deepcopy(aTitleline)
        for title in bTitleline:
            if title not in aTitleline:
                titleline.append(title)

        self.writeCsvFromDict(bothFileName, bothData, fieldnames=titleline)
        print("Wrote %d records to %s" % (len(bothData), bothFileName))
        self.writeCsvFromDict(onlyAFileName, onlyAData)
        print("Wrote %d records to %s" % (len(onlyAData), onlyAFileName))
        self.writeCsvFromDict(onlyBFileName, onlyBData)
        print("Wrote %d records to %s" % (len(onlyBData), onlyBFileName))

if __name__ == "__main__":
    app = MyApp()
    app.run()