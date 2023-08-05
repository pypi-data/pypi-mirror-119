import os
import re
import sys
import time
from pathlib import Path
from nb_log import LoggerMixin
import paramiko


class ParamikoFolderUploader(LoggerMixin):
    """
    paramoki 实现的文件夹上传
    """

    def __init__(self, host, port, user, password, local_dir: str, remote_dir: str,
                 path_pattern_exluded_tuple=('/.git/', '/.idea/',),
                 file_suffix_tuple_exluded=('.pyc', '.log', '.gz'),
                 only_upload_within_the_last_modify_time=3650 * 24 * 60 * 60,
                 file_volume_limit=1000 * 1000, ):
        """

        :param host:
        :param port:
        :param user:
        :param password:
        :param local_dir:
        :param remote_dir:
        :param path_pattern_exluded_tuple: 命中了这些正则的直接排除
        :param file_suffix_tuple_exluded: 这些结尾的文件排除
        :param only_upload_within_the_last_modify_time: 仅仅上传最近多少天修改的文件
        :param file_volume_limit: 大于这个体积的不上传，单位b。
        """

        self._local_dir = str(local_dir).replace('\\', '/')
        if not self._local_dir.endswith('/'):
            self._local_dir += '/'
        self._remote_dir = str(remote_dir).replace('\\', '/')
        if not self._remote_dir.endswith('/'):
            self._remote_dir += '/'
        self._path_pattern_exluded_tuple = path_pattern_exluded_tuple
        self._file_suffix_tuple_exluded = file_suffix_tuple_exluded
        self._only_upload_within_the_last_modify_time = only_upload_within_the_last_modify_time
        self._file_volume_limit = file_volume_limit

        t = paramiko.Transport((host, port))
        t.connect(username=user, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(t)

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=user, password=password, compress=True)
        self.ssh = ssh

    def _judge_need_filter_a_file(self, filename: str):
        ext = filename.split('.')[-1]
        if '.' + ext in self._file_suffix_tuple_exluded:
            return True
        for path_pattern_exluded in self._path_pattern_exluded_tuple:
            if re.search(path_pattern_exluded, filename):
                return True
        file_st_mtime = os.stat(filename).st_mtime
        volume = os.path.getsize(filename)
        if time.time() - file_st_mtime > self._only_upload_within_the_last_modify_time:
            return True
        if volume > self._file_volume_limit:
            return True
        return False

    def _make_dir(self, dir, final_dir):
        """
        sftp.mkdir 不能直接越级创建深层级文件夹。
        :param dir:
        :param final_dir:
        :return:
        """
        # print(dir,final_dir)
        try:
            self.sftp.mkdir(dir)
            if dir != final_dir:
                self._make_dir(final_dir, final_dir)
        except (FileNotFoundError,):
            parrent_dir = os.path.split(dir)[0]
            self._make_dir(parrent_dir, final_dir)

    def upload(self):
        for parent, dirnames, filenames in os.walk(self._local_dir):
            for filename in filenames:
                file_full_name = os.path.join(parent, filename).replace('\\', '/')
                if not self._judge_need_filter_a_file(file_full_name):
                    remote_full_file_name = re.sub(f'^{self._local_dir}', self._remote_dir, file_full_name)
                    try:
                        self.sftp.put(file_full_name, remote_full_file_name)
                    except (FileNotFoundError,) as e:
                        # self.logger.warning(remote_full_file_name)
                        self._make_dir(os.path.split(remote_full_file_name)[0], os.path.split(remote_full_file_name)[0])
                        self.sftp.put(file_full_name, remote_full_file_name)
                else:
                    # self.logger.warning(f'此文件 {file_full_name} 符合过滤要求，不执行上传')
                    pass


if __name__ == '__main__':
    uploader = ParamikoFolderUploader('192.168.6.133', 22, 'ydf', '372148', sys.path[1], '/home/ydf/codes/dssf6/')
    uploader.upload()
