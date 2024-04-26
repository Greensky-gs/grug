from utils.config import configs

def parsePos(x, y):
    return (max(0, min(x, configs["WIDTH"])), max(0, min(y, configs["HEIGHT"])))