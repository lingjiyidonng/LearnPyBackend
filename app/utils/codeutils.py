import os
from app.setting import UPLOAD_PATH

class CodeHandler():
    def __init__(self, codePath):
        self.codeFile = os.path.join(UPLOAD_PATH, codePath)
        self.res = None

    def run(self):
        os.chdir(UPLOAD_PATH)
        self.res = os.popen("python " + self.codeFile).readlines()

if __name__ == '__main__':
    codeHandler = CodeHandler("1.py")
    codeHandler.run()
    print(codeHandler.res)