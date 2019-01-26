# -*- coding: utf-8 -*-
# upload.py
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
import uploader
import os
import sys

def check_and_upload(path: str):
	if not os.path.exists(path):
		raise FileNotFoundError(path)
	if os.path.isdir(s):
		uploader.upload_folder(s)
	else:
		uploader.upload_file(s)

if __name__ == "__main__":
	if len(sys.argv) == 1:
		s = input('Please input folder or file name which you want to upload: ')
		check_and_upload(s)
	elif len(sys.argv) == 2:
		check_and_upload(sys.argv[1])