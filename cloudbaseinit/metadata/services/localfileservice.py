
import os
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
        self._password_path = os.path.normpath(os.path.join(self._metadata_path, 'openstack\\latest\\password_data.json'))
        LOG.info('Local metadata path %s', self._metadata_path)

    def load(self):
        # 加载本地文件
        LOG.debug('Init LocalFileService load %s', self._metadata_file)
        super(LocalFileService, self).load()
        return self._meta_data_file_exists(self._metadata_file)

    def _get_data(self, path):
        LOG.info('Init LocalFileService _get_data')
        # 读取文件数据
        norm_path = os.path.normpath(os.path.join(self._metadata_path, path))
        try:
            with open(norm_path, 'rb') as stream:
                return stream.read()
        except IOError:
            raise base.NotExistingMetadataException()

    def cleanup(self):
        # 清除文件
        #LOG.info('Deleting metadata file: %r', self._mgr.target_path)
        self._metadata_path = None

    def get_admin_password(self):
        """Get the admin password from the Password File.

        .. note:
            The password is deleted from the File after the first
            call of this method.
        """
        password = self._get_password()
        if password:
            self._delete_password()
        return password

    def get_admin_username(self):
        meta_data = self._get_password_data()
        if meta_data is None:
            return None

        meta = meta_data.get('meta')

        if meta and 'name' in meta:
            name = meta['name']
        elif 'name' in meta_data:
            name = meta_data['name']
        else:
            name = None

        return name

    def _get_password(self):
        meta_data = self._get_password_data()
        if meta_data is None:
            return None

        meta = meta_data.get('meta')

        if meta and 'admin_pass' in meta:
            password = meta['admin_pass']
        elif 'admin_pass' in meta_data:
            password = meta_data['admin_pass']
        else:
            password = None

        return password

    def _get_password_data(self, version='latest'):
        if os.path.exists(self._password_path):
            return self._get_openstack_json_data(version, 'password_data.json')
        else:
            return None

    def _delete_password(self):
        try:
            os.remove(self._password_path)
        except OSError:  # pragma: no cover
            pass

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
        """Check if a new password exists in the Password File."""
        return bool(self._get_password())
