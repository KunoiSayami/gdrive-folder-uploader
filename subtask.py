# -*- coding: utf-8 -*-
# subtask.py
# Copyright (C) 2019 KunoiSayami
#
# This module is part of gdrive-folder-uploader and is released under
# the AGPL v3 License: https://www.gnu.org/licenses/agpl-3.0.txt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
import subprocess
import time
class uploader(object):
	def __init__(self, file_name: str, callback: callable = None, exec_name: str = 'gdrive'):
		self.file_name = file_name
		self.exec_name = exec_name
		# Using call back function to print messages
		self.callback = callback
		self.upload_comand = [self.exec_name, 'upload' , '--no-progress', self.file_name]
		self.retries = 0
		self.msg = ''
	def upload(self):
		# disable show progress prevert some unexcept memory error
		while True:
			s = subprocess.Popen(self.upload_comand, stdout=subprocess.PIPE)
			if self.checker(s.communicate()[0].decode()):
				break
		return self.msg
	def checker(self, output_info: str):
		self.get_str(output_info)
		if 'Error' in output_info:
			self.retries += 1
			if self.retries > 3: self.retries = 5
			time.sleep(6000 * self.retries)
			return False
			#self.upload()
		self.custom_rewrite(output_info)
		return True
	def get_str(self, output_info: str):
		for line in output_info.splitlines():
			if any(substr in line for substr in ('Uploaded', 'Error')):
				if callable(self.callback):
					self.callback(line)
				else:
					return line
	def custom_rewrite(self, output_info: str):
		pass

class uploader_within_folder(uploader):
	def __init__(self, file_name: str, folder_id: str, callback: callable = None, exec_name: str = 'gdrive'):
		uploader.__init__(self, file_name, callback, exec_name)
		#self.folder_id = folder_id
		self.upload_comand.insert(2, folder_id)
		self.upload_comand.insert(2, '-p')

class create_folder(uploader):
	def __init__(self, folder_name: str, super_folder_id: str = '', callback: callable = None, exec_name: str = 'gdrive'):
		if super_folder_id != '':
			uploader.__init__(self, folder_name, callback, exec_name)
		else:
			uploader_folder.__init__(self, folder_name, super_folder_id, callback, exec_name)
		self.upload_comand[1] = 'mkdir'
	def custom_rewrite(self, output_info: str):
		self.msg = output_info.split()[1]