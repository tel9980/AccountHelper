import os
import shutil
import sys
from platform import system
import logging
import logging.config
import yaml


class Util:
    @staticmethod
    def split_list_average_n(origin_list, n):
        """
        list均分成 n 份
        """
        # +1是取float 上限 ceil， 不+1会产生 n+1个数组
        each_count = int(len(origin_list) / n) + 1
        for i in range(0, len(origin_list), each_count):
            yield origin_list[i: i + each_count]

    @staticmethod
    def set_up_log(path="log.yaml", default_level=logging.INFO, env_key="LOG_CFG"):
        """
        从 ./log/log.yaml加载 logging 配置
        :return:
        """
        log_config_location = os.path.join(Util.get_executable_path(), 'log', path)
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(log_config_location):
            with open(log_config_location, "rb") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)

    @staticmethod
    def get_executable_path():
        """
        获取exe执行文件所在目录
        为啥不用 os.path.abspath(__file__)
        因为经过 pyinstaller打包后, 路径出错
        """
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    @staticmethod
    def get_save_picture_dir():
        """
        截图保存在当前目录 ./picture下
        :return:
        """
        root_dir = Util.get_executable_path()
        base_dir = 'picture'
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        return os.path.join(root_dir, base_dir)

    @staticmethod
    def remove_cropped_pictures():
        """
        删除 ./picture目录，等效于删除所有的截图
        :return:
        """
        picture_dir = Util.get_save_picture_dir()
        shutil.rmtree(picture_dir)

    @staticmethod
    def get_config_dir():
        """
        配置保存目录 ./config/下
        :return:
        """
        root_dir = Util.get_executable_path()
        base_dir = 'config'
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        return os.path.join(root_dir, base_dir)

    @staticmethod
    def get_driver_location():
        """
        根据操作系统选择 chrome driver
        :return:
        """
        os_type = system()
        root_dir = Util.get_executable_path()
        drivers_dir = os.path.join(root_dir, 'drivers')
        if os_type == 'Darwin':
            return os.path.join(drivers_dir, 'chromedriver_mac64')
        elif os_type == 'Windows':
            return os.path.join(drivers_dir, 'chromedriver_win32.exe')
        elif os_type == 'Linux':
            return os.path.join(drivers_dir, 'chromedriver_linux64')
        else:
            print('不支持的系统类型！')
            exit(-1)
    #
    # @staticmethod
    # def get_haven_delead_company_code():
    #     """
    #     获取 ./picture 下当前已经获取的公司的图片，用于判断还有哪些公司没有获取，继续获取剩下的公司的图片截图
    #     比如已经截取了图片 S00025_重庆民康实业有限公司.png
    #     取出 S00025类似的数组， 返回， 方便继续获取还没有处理的公司
    #     :return:
    #     """
    #     root_dir = Util.get_executable_path()
    #     picture_dir = os.path.join(root_dir, 'picture')
    #     dealed_company_code = []
    #     for file in os.listdir(picture_dir):
    #         matched = re.search("(\S*)_", file)
    #         dealed_company_code.append(matched[1])
    #     return dealed_company_code
    #
    # @staticmethod
    # def get_log_config():
    #     """
    #     Deprecated: 不从command line选取要执行的excel文件
    #     log_config
    #     :return:
    #     """
    #     root_dir = PathUtil.get_executable_path()
    #     base_dir = 'log'
    #     if not os.path.exists(base_dir):
    #         os.makedirs(base_dir)
    #     return os.path.join(root_dir, base_dir)
    #
    # @staticmethod
    # def is_same_address(address1, address2):
    #     """
    #     地址转换后, 格式类似这样的, 省/市/区/地址/邮编, 不存在则为None
    #     ['福建省' '泉州市' None '洛江万安塘西工业区安邦路10号' '350500']
    #     ['福建省' '泉州市' '洛江区' '万安塘西工业区安邦路9号' '350504']
    #     """
    #     data = cpca.transform([address1.strip(), address2.strip()]).values
    #     # 地址1
    #     a1 = data[0]
    #     # 地址2
    #     a2 = data[1]
    #     # 省
    #     if a1[0] != a2[0]:
    #         return False
    #     # 市
    #     if a1[1] != a2[1]:
    #         return False
    #     # 区
    #     if a1[2] != a2[2]:
    #         return False
    #     # 比较详细地址
    #     if len(a1[3]) != len(a2[3]):
    #         return False
    #     for x, y in zip(a1[3], a2[3]):
    #         if x != y:
    #             return False
    #     return True
    #
    # @staticmethod
    # def select_excel():
    #     """
    #     Deprecated: 不从command line选取要执行的excel文件
    #     从当前目录 excels/ 下选取一个 xlsx
    #     :return:
    #     """
    #     root_dir = PathUtil.get_executable_path()
    #     excels_dir = os.path.join(root_dir, 'excels')
    #     excels = []
    #     for file in os.listdir(excels_dir):
    #         file_path = os.path.join(excels_dir, file)
    #         if os.path.isfile(file_path):
    #             excels.append(file_path)
    #     if len(excels) > 0:
    #         print("选择要处理的excel：\n")
    #         for i in range(0, len(excels)):
    #             print("{index}: {file}\n".format(index=i, file=os.path.basename(excels[i])))
    #     while True:
    #         choose_index = input("请输入数字选择:\n")
    #         choose_index = int(choose_index)
    #         if choose_index < 0 or choose_index >= len(excels):
    #             print("请输入正确的数字选择:\n")
    #         else:
    #             break
    #     return excels[choose_index]
