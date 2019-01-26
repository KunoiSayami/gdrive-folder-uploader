# -*- coding: utf-8 -*-
# main.py
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
import subtask
import os

class upload_folder(upload_file):
	def __init__(self, folder_name: str, super_folder_id: str = '', callback: callable = None, exec_name: str = 'gdrive'):
		upload_file.__init__(folder_name, super_folder_id, callback, exec_name)
		self.folder_name = folder_name
	def uploader(self, folder_name: str, super_folder_id: str = '', callback: callable = None, exec_name: str = 'gdrive'):
		os.chdir(folder_name)
		super_id = subtask.create_folder(folder_name, super_folder_id, callback, exec_name).upload()
		for root, dir_names, file_names in os.walk('.'):
			if root != '.':
				continue
			for subdir_name in dir_names:
				self.uploader(subdir_name, super_id, callback, exec_name)
			for file_name in file_names:
				subtask.uploader_within_folder(file_name, super_id, callback, exec_name).upload()
		os.chdir('..')
	def activity(self):
		self.uploader(self.folder_name, self.super_folder_id, self.callback, self.exec_name)

class upload_file(object):
	def __init__(self, folder_name: str, super_folder_id: str = '', callback: callable = None, exec_name: str = 'gdrive'):
		self.folder_name = folder_name
		self.super_folder_id = super_folder_id
		self.callback = callback
		self.exec_name = exec_name
	def activity(self):
		if self.super_folder_id != '':
			subtask.uploader(self.file_name, callback, exec_name)
		else:
			subtask.uploader_within_folder(self.file_name, self.super_folder_id, self.callback, self.exec_name)