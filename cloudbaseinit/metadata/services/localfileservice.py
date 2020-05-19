
import os
from oslo_log import log as oslo_logging

from cloudbaseinit import conf as cloudbaseinit_conf
from cloudbaseinit.metadata.services import baseopenstackservice

CONF = cloudbaseinit_conf.CONF
LOG = oslo_logging.getLogger(__name__)


class LocalFileService(baseopenstackservice.BaseOpenStackService):

    def __init__(self):
        super(LocalFileService, self).__init__()
        self._metadata_path = os.path.normpath(CONF.local_metadata_file)
        LOG.debug('Local metadata path %s', self._metadata_path)

    def load(self):
        # 加载本地文件
        super(LocalFileService, self).load()
        return self._meta_data_file_exists(self._metadata_path)

    def _get_data(self, path):
        # 读取文件数据
        norm_path = os.path.normpath(os.path.join(self._metadata_path, path))
        try:
            with open(norm_path, 'rb') as stream:
                return stream.read()
        except IOError:
            raise base.NotExistingMetadataException()

    def cleanup(self):
        # 清除文件
        LOG.debug('Deleting metadata file: %r', self._mgr.target_path)
        self._metadata_path = None

    def _meta_data_file_exists(self, metadata_file):

        if os.path.exists(metadata_file):
            return True

        LOG.debug('%s not found', metadata_file)
        return False