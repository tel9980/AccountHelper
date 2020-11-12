import cpca
import os
import sys
from platform import system

# 是否对selenium截的全屏图裁剪, 默认截全屏图
IS_CROP_IMAGE = False


class Util:
	@staticmethod
	def is_same_address(address1, address2):
		"""
		地址转换后, 格式类似这样的, 省/市/区/地址/邮编, 不存在则为None
		['福建省' '泉州市' None '洛江万安塘西工业区安邦路10号' '350500']
		['福建省' '泉州市' '洛江区' '万安塘西工业区安邦路9号' '350504']
		"""
		data = cpca.transform([address1.strip(), address2.strip()]).values
		# 地址1
		a1 = data[0]
		# 地址2
		a2 = data[1]
		# 省
		if a1[0] != a2[0]:
			return False
		# 市
		if a1[1] != a2[1]:
			return False
		# 区
		if a1[2] != a2[2]:
			return False
		# 比较详细地址
		if len(a1[3]) != len(a2[3]):
			return False
		for x, y in zip(a1[3], a2[3]):
			if x != y:
				return False
		return True

	@staticmethod
	def split_list_average_n(origin_list, n):
		"""
		list均分成 n 份
		"""
		# +1是取float 上限 ceil， 不+1会产生 n+1个数组
		each_count = int(len(origin_list) / n) + 1
		for i in range(0, len(origin_list), each_count):
			yield origin_list[i: i + each_count]


class PathUtil:
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
		root_dir = PathUtil.get_executable_path()
		base_dir = 'picture'
		if not os.path.exists(base_dir):
			os.makedirs(base_dir)
		return os.path.join(root_dir, base_dir)

	@staticmethod
	def get_cookie_dir():
		"""
		浏览器cookie放置在 ./cookie 下
		:return:
		"""
		root_dir = PathUtil.get_executable_path()
		base_dir = 'cookie'
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
		root_dir = os.path.dirname(os.path.abspath(__file__))
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
	
	@staticmethod
	def select_excel():
		"""
		Deprecated: 不从command line选取要执行的excel文件
		从当前目录 excels/ 下选取一个 xlsx
		:return:
		"""
		root_dir = os.path.dirname(os.path.abspath(__file__))
		excels_dir = os.path.join(root_dir, 'excels')
		excels = []
		for file in os.listdir(excels_dir):
			file_path = os.path.join(excels_dir, file)
			if os.path.isfile(file_path):
				excels.append(file_path)
		if len(excels) > 0:
			print("选择要处理的excel：\n")
			for i in range(0, len(excels)):
				print("{index}: {file}\n".format(index=i, file=os.path.basename(excels[i])))
		while True:
			choose_index = input("请输入数字选择:\n")
			choose_index = int(choose_index)
			if choose_index < 0 or choose_index >= len(excels):
				print("请输入正确的数字选择:\n")
			else:
				break
		return excels[choose_index]
