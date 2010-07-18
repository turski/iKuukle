from threading import BoundedSemaphore, Thread
import re, modules

class BlockGrid(object):
    """Object that holds information about whole customizable area of website"""
    def __init__(self, conf=None):
        self._column_count_ = 0
        self.columns = []
        if conf:
            self.parse_conf(conf)

    def __str__(self):
        ret = str()
        for col in self.columns:
            ret += str(col)
        return ret

    def __unicode__(self):
        ret = unicode()
        for col in self.columns:
            ret += unicode(col)
        return ret

    @property
    def column_count(self):
        return self._column_count_

    def add_column(self, column):
        if isinstance(column, BlockColumn):
            self.columns.append(column)
            self._column_count_ += 1
        else:
            raise TypeError, 'Must be an instance of BlockColumn'

    def parse_conf(self, conf):
        """Parse layout configuration file and prepare BlockGrid for generate"""
        column_exp = re.compile('^\s*(?P<name>\w+)\s*:\s*$')
        block_exp = re.compile('^\s+(?P<method>\w+)\((?P<args>.*)\)\s*$')
        with open(conf) as conf:
            column = None
            for line in conf:
                column_match = column_exp.match(line)
                if column_match:
                    column = BlockColumn()
                    self.add_column(column)
                else:
                    block_match = block_exp.match(line)
                    if block_match:
                        if isinstance(column, BlockColumn):
                            method = block_match.group('method')
                            args = block_match.group('args')
                            block_string = 'modules.%s(%s)' % (method, args)
                            block = eval(block_string)
                            if isinstance(block, Block):
                                column.add_block(block)
                            else:
                                raise TypeError, 'Given line did not produce ' \
                                                 'a Block object'
                        else:
                            raise TypeError, 'Given block is not included ' \
                                             'in any column'

    def generate(self):
        """Threaded generation of html code"""
        sema = BoundedSemaphore(10)
        pool = []
        for column in self.columns:
            for block in column.blocks:
                thread = Thread(target=block.generate, kwargs={'lock':sema})
                pool.append(thread)
                thread.start()
        for thread in pool:
            thread.join()


class BlockColumn(object):
    """One column of BlockGrid, holding Block objects"""
    def __init__(self):
        self._block_count_ = 0
        self.blocks = []

    def __str__(self):
        ret = str()
        for block in self.blocks:
            ret += str(block)
        return ret

    def __unicode__(self):
        ret = unicode()
        for block in self.blocks:
            ret += unicode(block)
        return ret

    @property
    def block_count(self):
        return self._block_count_

    def add_block(self, block):
        if isinstance(block, Block):
            self.blocks.append(block)
            self._block_count_ += 1
        else:
            raise TypeError, 'Must be an instance of Block'


class Block(object):
    """Single block in BlockGrid, contains html-code of block"""
    def __init__(self):
        self._html_ = ''

    def __str__(self):
        return str(self._html_)

    def __unicode__(self):
        return unicode(self._html_)

    def generate(self, lock=None):
        pass