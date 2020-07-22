
import os
import shutil
from oslo_log import log as oslo_logging

from cloudbaseinit import conf as cloudbaseinit_conf
from cloudbaseinit.metadata.services import base
from cloudbaseinit.metadata.services import baseopenstackservice

CONF = cloudbaseinit_conf.CONF
LOG = oslo_logging.getLogger(__name__)


class LocalFileService(baseopenstackservice.BaseOpenStackService):

    def __init__(self):
        LOG.info('Init LocalFileService')
        super(LocalFileService, self).__init__()
        self._metadata_path = os.path.normpath(CONF.local_metadata_file_path)
        self._metadata_file = os.path.normpath(CONF.local_metadata_file)
        LOG.info('Local metadata path %s', self._metadata_path)

    def load(self):
        # 加载本地文件
        LOG.debug('Init LocalFileService load %s', self._metadata_file)
        super(LocalFileService, self).load()
        return self._meta_data_file_exists(self._metadata_file)

    def _get_data(self, path):
        LOG.info('Init LocalFileService _get_data')
        # 读取文件数据
        self._metadata_norm_path = os.path.normpath(os.path.join(self._metadata_path, path))

        try:
            with open(self._metadata_norm_path, 'rb') as stream:
                return stream.read()
        except IOError:
            raise base.NotExistingMetadataException()

    def cleanup(self):
        # 清除文件
        LOG.debug('Deleting metadata folder: %r', self._metadata_norm_path)
        shutil.rmtree(self._mgr.target_path, ignore_errors=True)
        self._metadata_path = None

    def _meta_data_file_exists(self, metadata_file):

        if os.path.exists(metadata_file):
            return True

        LOG.info('%s not found', metadata_file)
        return False

    @property
    def can_update_password(self):
        """The ability to update password of the metadata provider.

        If :meth:`~can_update_password` is True, plugins can check
        periodically (e.g. at every boot) if the password changed.

        :rtype: bool

        .. notes:
            The password will be updated only if the
            :meth:`~is_password_changed` returns True.
        """
        return True

    def is_password_changed(self):
        """Check if the metadata provider has a new password for this instance

        :rtype: bool

        .. notes:
            This method will be used only when :meth:`~can_update_password`
            is True.
        """
        return True
