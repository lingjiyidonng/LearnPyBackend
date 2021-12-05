import os
from app.setting import UPLOAD_PATH
import subprocess

class CodeHandler():
    def __init__(self, codePath):
        self.codeFile = os.path.join(UPLOAD_PATH, codePath)
        self.res = None

    def check(self):
        with open(self.codeFile) as f:
            codes = f.readlines()
        if len(codes) > 12:
            return "行数过长"
        for code in codes:
            if "import" in code:
                return "非法引入包"
        return None


    def run(self):
        checkMsg =  self.check()
        if checkMsg is not None:
            self.res = [checkMsg]
            return
        os.chdir(UPLOAD_PATH)
        res = None
        try:
            res = subprocess.run(["python", self.codeFile], timeout=1, stdout=subprocess.PIPE)
        except subprocess.TimeoutExpired:
            self.res = ["运行超时"]
            return
        finally:
            pass
        if res.returncode != 0:
            self.res = ["执行失败"]
            return
        self.res = res.stdout.decode("utf8").split("\n")[:-1]

if __name__ == '__main__':
    codeHandler = CodeHandler("da343ca901f84d7bab66f37dd5cd3b1c.py")
    print(codeHandler.run())

