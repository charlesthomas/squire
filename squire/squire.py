from os import devnull, path, stat, walk
from subprocess import Popen
from time import sleep


class Squire(object):
    def __init__(self, *command, **options):
        # TODO add options for monitoring command's success?
        self.command = command
        self.poll_time = options.get('poll_time', 0.5)
        self.quiet = options.get('quiet', False)
        if self.quiet:
            self.verbose = False
        else:
            self.verbose = options.get('verbose', False)
        self.watch_dir = path.abspath(options.get('watch_dir', '.'))
        self.command_dir = path.abspath(options.get('command_dir', '.'))
        self.exclude_dirs = options.get('exclude_dirs', None)
        if self.exclude_dirs is not None:
            self.exclude_dirs = [path.abspath(p) for p in \
                                 self.exclude_dirs.split(',')]
        self.inode_hash = self.fetch_inode_hash()
        if self.verbose:
            print self.__str__()


    def __str__(self):
        string = ("Watching %s for changes every %s seconds and running '%s' "
                  "from %s on changes" % (self.watch_dir, self.poll_time,
                                          ' '.join(self.command),
                                          self.command_dir))
        if self.exclude_dirs is not None:
            string = "%s (not including directories %s)" % (string,
                                                            self.exclude_dirs)
        return string


    def __repr__(self):
        if self.exclude_dirs is None:
            exclude_dirs = None
        else:
            exclude_dirs = ','.join(self.exclude_dirs)
        return ('Squire("%s", watch_dir="%s", command_dir="%s", '
                'exclude_dirs="%s", poll_time=%s, verbose=%s, quiet=%s)' % \
               (self.command, self.watch_dir, self.command_dir, exclude_dirs,
                self.poll_time, self.verbose, self.quiet))


    def run_command(self):
        kwargs = dict(cwd=self.command_dir)
        if self.quiet:
            kwargs.update(stdout=open(devnull, 'w'))
        else:
            print '=' * 80
        Popen(self.command, **kwargs)


    def loop(self):
        while True:
            new_inode_hash = self.fetch_inode_hash()
            if self.inode_hash != new_inode_hash:
                if self.verbose:
                    print "%s doesn't match %s" % (new_inode_hash,
                                                   self.inode_hash)
                self.inode_hash = new_inode_hash
                self.run_command()
            if self.verbose:
                print 'sleeping %s seconds...' % self.poll_time
            sleep(self.poll_time)


    def fetch_inode_hash(self):
        inodes = list()
        for (cwd, subdirs, files) in walk(self.watch_dir):
            skip = False
            for d in self.exclude_dirs:
                if d in cwd:
                    skip = True
                    break
            if skip:
                continue
            inodes += [stat(path.join(cwd, f)).st_ino for f in files]
        return hash(''.join(sorted(str(inodes))))
