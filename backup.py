import datetime
import os
import shutil

from YaDiskClient.YaDiskClient import YaDisk

from settings import *


today = str(datetime.date.today())
filename = 'website-backup-%s.tar.bz2' % today

try:
    shutil.rmtree(TMPDIR)
except:
    pass

os.mkdir(TMPDIR)
os.chown(TMPDIR, 0, 0)
os.chmod(TMPDIR, 0o700)


cmd = 'docker exec -it db-site pg_dump -U postgres > %s/db.backup' % TMPDIR
os.system(cmd)

fullname = 'backups/%(filename)s' % {'filename': filename}
cmd = 'tar -cjpf %(fullname)s /opt/website/uploads %(path)s/db.backup' % {'path': TMPDIR, 'fullname': fullname}
os.system(cmd)

disk = YaDisk(YANDEX_LOGIN, YANDEX_PASSWORD)
disk.upload(fullname, 'website/%(filename)s' % {'filename': filename})
os.remove(fullname)
