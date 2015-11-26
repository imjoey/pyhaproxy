from collections import defaultdict
import re


class TreeNode(object):
    """BNF tree node object

    Attributes:
        elements (list): treenodes after parsing
        offset (int): the offset of the treenode
        text (str): treenode text content
    """
    def __init__(self, text, offset, elements=None):
        self.text = text
        self.offset = offset
        self.elements = elements or []

    def __iter__(self):
        for el in self.elements:
            yield el


class GlobalSection(TreeNode):
    def __init__(self, text, offset, elements):
        super(GlobalSection, self).__init__(text, offset, elements)
        self.global_header = elements[0]
        self.config_block = elements[1]


class DefaultsSection(TreeNode):
    def __init__(self, text, offset, elements):
        super(DefaultsSection, self).__init__(text, offset, elements)
        self.defaults_header = elements[0]
        self.config_block = elements[1]


class UserlistSection(TreeNode):
    def __init__(self, text, offset, elements):
        super(UserlistSection, self).__init__(text, offset, elements)
        self.userlist_header = elements[0]
        self.config_block = elements[1]


class ListenSection(TreeNode):
    def __init__(self, text, offset, elements):
        super(ListenSection, self).__init__(text, offset, elements)
        self.listen_header = elements[0]
        self.config_block = elements[1]


class FrontendSection(TreeNode):
    def __init__(self, text, offset, elements):
        super(FrontendSection, self).__init__(text, offset, elements)
        self.frontend_header = elements[0]
        self.config_block = elements[1]


class BackendSection(TreeNode):
    def __init__(self, text, offset, elements):
        super(BackendSection, self).__init__(text, offset, elements)
        self.backend_header = elements[0]
        self.config_block = elements[1]


class GlobalHeader(TreeNode):
    def __init__(self, text, offset, elements):
        super(GlobalHeader, self).__init__(text, offset, elements)
        self.whitespace = elements[2]
        self.line_break = elements[4]


class UserlistHeader(TreeNode):
    def __init__(self, text, offset, elements):
        super(UserlistHeader, self).__init__(text, offset, elements)
        self.whitespace = elements[2]
        self.proxy_name = elements[3]
        self.line_break = elements[5]


class DefaultsHeader(TreeNode):
    def __init__(self, text, offset, elements):
        super(DefaultsHeader, self).__init__(text, offset, elements)
        self.whitespace = elements[4]
        self.line_break = elements[6]


class ListenHeader(TreeNode):
    def __init__(self, text, offset, elements):
        super(ListenHeader, self).__init__(text, offset, elements)
        self.whitespace = elements[4]
        self.proxy_name = elements[3]
        self.line_break = elements[8]


class FrontendHeader(TreeNode):
    def __init__(self, text, offset, elements):
        super(FrontendHeader, self).__init__(text, offset, elements)
        self.whitespace = elements[4]
        self.proxy_name = elements[3]
        self.line_break = elements[8]
        self.service_address = elements[5]
        self.value = elements[6]


class BackendHeader(TreeNode):
    def __init__(self, text, offset, elements):
        super(BackendHeader, self).__init__(text, offset, elements)
        self.whitespace = elements[4]
        self.proxy_name = elements[3]
        self.line_break = elements[7]


class ServerLine(TreeNode):
    def __init__(self, text, offset, elements):
        super(ServerLine, self).__init__(text, offset, elements)
        self.whitespace = elements[4]
        self.server_name = elements[3]
        self.service_address = elements[5]
        self.line_break = elements[8]
        self.value = elements[6]


class OptionLine(TreeNode):
    def __init__(self, text, offset, elements):
        super(OptionLine, self).__init__(text, offset, elements)
        self.whitespace = elements[4]
        self.keyword = elements[3]
        self.line_break = elements[7]
        self.value = elements[5]


class ConfigLine(TreeNode):
    def __init__(self, text, offset, elements):
        super(ConfigLine, self).__init__(text, offset, elements)
        self.whitespace = elements[3]
        self.keyword = elements[2]
        self.line_break = elements[6]
        self.value = elements[4]


class CommentLine(TreeNode):
    def __init__(self, text, offset, elements):
        super(CommentLine, self).__init__(text, offset, elements)
        self.whitespace = elements[0]
        self.comment_text = elements[1]
        self.line_break = elements[2]


class BlankLine(TreeNode):
    def __init__(self, text, offset, elements):
        super(BlankLine, self).__init__(text, offset, elements)
        self.whitespace = elements[0]
        self.line_break = elements[1]


class Keyword(TreeNode):
    def __init__(self, text, offset, elements):
        super(Keyword, self).__init__(text, offset, elements)
        self.whitespace = elements[1]


class ServiceAddress(TreeNode):
    def __init__(self, text, offset, elements):
        super(ServiceAddress, self).__init__(text, offset, elements)
        self.host = elements[0]
        self.port = elements[2]


class ParseError(SyntaxError):
    pass


FAILURE = object()


class Grammar(object):
    REGEX_1 = re.compile('^[\\n]')
    REGEX_2 = re.compile('^[a-z0-9\\-\\_\\.]')
    REGEX_3 = re.compile('^[a-zA-z0-9\\-\\_\\.:]')
    REGEX_4 = re.compile('^[:]')
    REGEX_5 = re.compile('^[\\d]')
    REGEX_6 = re.compile('^[\\d]')
    REGEX_7 = re.compile('^[\\d]')
    REGEX_8 = re.compile('^[\\d]')
    REGEX_9 = re.compile('^[\\d]')
    REGEX_10 = re.compile('^[a-zA-Z\\-\\.\\d]')
    REGEX_11 = re.compile('^[a-zA-Z0-9\\-\\_\\.:]')
    REGEX_12 = re.compile('^[^#\\n]')
    REGEX_13 = re.compile('^[\\n]')
    REGEX_14 = re.compile('^[ \\t]')

    def _read_configuration(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['configuration'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 0, self._offset, [], True
        while address1 is not FAILURE:
            index2 = self._offset
            address1 = self._read_comment_line()
            if address1 is FAILURE:
                self._offset = index2
                address1 = self._read_blank_line()
                if address1 is FAILURE:
                    self._offset = index2
                    address1 = self._read_global_section()
                    if address1 is FAILURE:
                        self._offset = index2
                        address1 = self._read_defaults_section()
                        if address1 is FAILURE:
                            self._offset = index2
                            address1 = self._read_userlist_section()
                            if address1 is FAILURE:
                                self._offset = index2
                                address1 = self._read_listen_section()
                                if address1 is FAILURE:
                                    self._offset = index2
                                    address1 = self._read_frontend_section()
                                    if address1 is FAILURE:
                                        self._offset = index2
                                        address1 = self._read_backend_section()
                                        if address1 is FAILURE:
                                            self._offset = index2
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['configuration'][index0] = (address0, self._offset)
        return address0

    def _read_global_section(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['global_section'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_global_header()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_config_block()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = GlobalSection(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['global_section'][index0] = (address0, self._offset)
        return address0

    def _read_defaults_section(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['defaults_section'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_defaults_header()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_config_block()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = DefaultsSection(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['defaults_section'][index0] = (address0, self._offset)
        return address0

    def _read_userlist_section(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['userlist_section'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_userlist_header()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_config_block()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = UserlistSection(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['userlist_section'][index0] = (address0, self._offset)
        return address0

    def _read_listen_section(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['listen_section'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_listen_header()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_config_block()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = ListenSection(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['listen_section'][index0] = (address0, self._offset)
        return address0

    def _read_frontend_section(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['frontend_section'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_frontend_header()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_config_block()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = FrontendSection(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['frontend_section'][index0] = (address0, self._offset)
        return address0

    def _read_backend_section(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['backend_section'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_backend_header()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_config_block()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = BackendSection(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['backend_section'][index0] = (address0, self._offset)
        return address0

    def _read_global_header(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['global_header'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 6]
            if chunk0 == 'global':
                address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset)
                self._offset = self._offset + 6
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"global"')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_whitespace()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    index2 = self._offset
                    address4 = self._read_comment_text()
                    if address4 is FAILURE:
                        address4 = TreeNode(self._input[index2:index2], index2)
                        self._offset = index2
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_line_break()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = GlobalHeader(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['global_header'][index0] = (address0, self._offset)
        return address0

    def _read_userlist_header(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['userlist_header'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 8]
            if chunk0 == 'userlist':
                address2 = TreeNode(self._input[self._offset:self._offset + 8], self._offset)
                self._offset = self._offset + 8
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"userlist"')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_whitespace()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_proxy_name()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        index2 = self._offset
                        address5 = self._read_comment_text()
                        if address5 is FAILURE:
                            address5 = TreeNode(self._input[index2:index2], index2)
                            self._offset = index2
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            address6 = self._read_line_break()
                            if address6 is not FAILURE:
                                elements0.append(address6)
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = UserlistHeader(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['userlist_header'][index0] = (address0, self._offset)
        return address0

    def _read_defaults_header(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['defaults_header'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 8]
            if chunk0 == 'defaults':
                address2 = TreeNode(self._input[self._offset:self._offset + 8], self._offset)
                self._offset = self._offset + 8
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"defaults"')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_whitespace()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    index2 = self._offset
                    address4 = self._read_proxy_name()
                    if address4 is FAILURE:
                        address4 = TreeNode(self._input[index2:index2], index2)
                        self._offset = index2
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_whitespace()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            index3 = self._offset
                            address6 = self._read_comment_text()
                            if address6 is FAILURE:
                                address6 = TreeNode(self._input[index3:index3], index3)
                                self._offset = index3
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                address7 = self._read_line_break()
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = DefaultsHeader(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['defaults_header'][index0] = (address0, self._offset)
        return address0

    def _read_listen_header(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['listen_header'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 6]
            if chunk0 == 'listen':
                address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset)
                self._offset = self._offset + 6
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"listen"')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_whitespace()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_proxy_name()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_whitespace()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            index2 = self._offset
                            address6 = self._read_service_address()
                            if address6 is FAILURE:
                                address6 = TreeNode(self._input[index2:index2], index2)
                                self._offset = index2
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                index3 = self._offset
                                address7 = self._read_value()
                                if address7 is FAILURE:
                                    address7 = TreeNode(self._input[index3:index3], index3)
                                    self._offset = index3
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                    address8 = FAILURE
                                    index4 = self._offset
                                    address8 = self._read_comment_text()
                                    if address8 is FAILURE:
                                        address8 = TreeNode(self._input[index4:index4], index4)
                                        self._offset = index4
                                    if address8 is not FAILURE:
                                        elements0.append(address8)
                                        address9 = FAILURE
                                        address9 = self._read_line_break()
                                        if address9 is not FAILURE:
                                            elements0.append(address9)
                                        else:
                                            elements0 = None
                                            self._offset = index1
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = ListenHeader(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['listen_header'][index0] = (address0, self._offset)
        return address0

    def _read_frontend_header(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['frontend_header'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 8]
            if chunk0 == 'frontend':
                address2 = TreeNode(self._input[self._offset:self._offset + 8], self._offset)
                self._offset = self._offset + 8
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"frontend"')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_whitespace()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_proxy_name()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_whitespace()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            index2 = self._offset
                            address6 = self._read_service_address()
                            if address6 is FAILURE:
                                address6 = TreeNode(self._input[index2:index2], index2)
                                self._offset = index2
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                index3 = self._offset
                                address7 = self._read_value()
                                if address7 is FAILURE:
                                    address7 = TreeNode(self._input[index3:index3], index3)
                                    self._offset = index3
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                    address8 = FAILURE
                                    index4 = self._offset
                                    address8 = self._read_comment_text()
                                    if address8 is FAILURE:
                                        address8 = TreeNode(self._input[index4:index4], index4)
                                        self._offset = index4
                                    if address8 is not FAILURE:
                                        elements0.append(address8)
                                        address9 = FAILURE
                                        address9 = self._read_line_break()
                                        if address9 is not FAILURE:
                                            elements0.append(address9)
                                        else:
                                            elements0 = None
                                            self._offset = index1
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = FrontendHeader(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['frontend_header'][index0] = (address0, self._offset)
        return address0

    def _read_backend_header(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['backend_header'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 7]
            if chunk0 == 'backend':
                address2 = TreeNode(self._input[self._offset:self._offset + 7], self._offset)
                self._offset = self._offset + 7
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"backend"')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_whitespace()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_proxy_name()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_whitespace()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            index2 = self._offset
                            address6 = self._read_value()
                            if address6 is FAILURE:
                                address6 = TreeNode(self._input[index2:index2], index2)
                                self._offset = index2
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                index3 = self._offset
                                address7 = self._read_comment_text()
                                if address7 is FAILURE:
                                    address7 = TreeNode(self._input[index3:index3], index3)
                                    self._offset = index3
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                    address8 = FAILURE
                                    address8 = self._read_line_break()
                                    if address8 is not FAILURE:
                                        elements0.append(address8)
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = BackendHeader(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['backend_header'][index0] = (address0, self._offset)
        return address0

    def _read_config_block(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['config_block'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 0, self._offset, [], True
        while address1 is not FAILURE:
            index2 = self._offset
            address1 = self._read_server_line()
            if address1 is FAILURE:
                self._offset = index2
                address1 = self._read_option_line()
                if address1 is FAILURE:
                    self._offset = index2
                    address1 = self._read_config_line()
                    if address1 is FAILURE:
                        self._offset = index2
                        address1 = self._read_comment_line()
                        if address1 is FAILURE:
                            self._offset = index2
                            address1 = self._read_blank_line()
                            if address1 is FAILURE:
                                self._offset = index2
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['config_block'][index0] = (address0, self._offset)
        return address0

    def _read_server_line(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['server_line'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 6]
            if chunk0 == 'server':
                address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset)
                self._offset = self._offset + 6
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"server"')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_whitespace()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_server_name()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_whitespace()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            address6 = self._read_service_address()
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                index2 = self._offset
                                address7 = self._read_value()
                                if address7 is FAILURE:
                                    address7 = TreeNode(self._input[index2:index2], index2)
                                    self._offset = index2
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                    address8 = FAILURE
                                    index3 = self._offset
                                    address8 = self._read_comment_text()
                                    if address8 is FAILURE:
                                        address8 = TreeNode(self._input[index3:index3], index3)
                                        self._offset = index3
                                    if address8 is not FAILURE:
                                        elements0.append(address8)
                                        address9 = FAILURE
                                        address9 = self._read_line_break()
                                        if address9 is not FAILURE:
                                            elements0.append(address9)
                                        else:
                                            elements0 = None
                                            self._offset = index1
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = ServerLine(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['server_line'][index0] = (address0, self._offset)
        return address0

    def _read_option_line(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['option_line'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 6]
            if chunk0 == 'option':
                address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset)
                self._offset = self._offset + 6
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"option"')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_whitespace()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_keyword()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_whitespace()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            index2 = self._offset
                            address6 = self._read_value()
                            if address6 is FAILURE:
                                address6 = TreeNode(self._input[index2:index2], index2)
                                self._offset = index2
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                index3 = self._offset
                                address7 = self._read_comment_text()
                                if address7 is FAILURE:
                                    address7 = TreeNode(self._input[index3:index3], index3)
                                    self._offset = index3
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                    address8 = FAILURE
                                    address8 = self._read_line_break()
                                    if address8 is not FAILURE:
                                        elements0.append(address8)
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = OptionLine(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['option_line'][index0] = (address0, self._offset)
        return address0

    def _read_config_line(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['config_line'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            index3 = self._offset
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 8]
            if chunk0 == 'defaults':
                address2 = TreeNode(self._input[self._offset:self._offset + 8], self._offset)
                self._offset = self._offset + 8
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"defaults"')
            if address2 is FAILURE:
                self._offset = index3
                chunk1 = None
                if self._offset < self._input_size:
                    chunk1 = self._input[self._offset:self._offset + 6]
                if chunk1 == 'global':
                    address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset)
                    self._offset = self._offset + 6
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"global"')
                if address2 is FAILURE:
                    self._offset = index3
                    chunk2 = None
                    if self._offset < self._input_size:
                        chunk2 = self._input[self._offset:self._offset + 6]
                    if chunk2 == 'listen':
                        address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset)
                        self._offset = self._offset + 6
                    else:
                        address2 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"listen"')
                    if address2 is FAILURE:
                        self._offset = index3
                        chunk3 = None
                        if self._offset < self._input_size:
                            chunk3 = self._input[self._offset:self._offset + 8]
                        if chunk3 == 'frontend':
                            address2 = TreeNode(self._input[self._offset:self._offset + 8], self._offset)
                            self._offset = self._offset + 8
                        else:
                            address2 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"frontend"')
                        if address2 is FAILURE:
                            self._offset = index3
                            chunk4 = None
                            if self._offset < self._input_size:
                                chunk4 = self._input[self._offset:self._offset + 7]
                            if chunk4 == 'backend':
                                address2 = TreeNode(self._input[self._offset:self._offset + 7], self._offset)
                                self._offset = self._offset + 7
                            else:
                                address2 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"backend"')
                            if address2 is FAILURE:
                                self._offset = index3
            self._offset = index2
            if address2 is FAILURE:
                address2 = TreeNode(self._input[self._offset:self._offset], self._offset)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_keyword()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_whitespace()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        index4 = self._offset
                        address5 = self._read_value()
                        if address5 is FAILURE:
                            address5 = TreeNode(self._input[index4:index4], index4)
                            self._offset = index4
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            index5 = self._offset
                            address6 = self._read_comment_text()
                            if address6 is FAILURE:
                                address6 = TreeNode(self._input[index5:index5], index5)
                                self._offset = index5
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                address7 = self._read_line_break()
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = ConfigLine(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['config_line'][index0] = (address0, self._offset)
        return address0

    def _read_comment_line(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['comment_line'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_comment_text()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_line_break()
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = CommentLine(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['comment_line'][index0] = (address0, self._offset)
        return address0

    def _read_blank_line(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['blank_line'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_whitespace()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_line_break()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = BlankLine(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['blank_line'][index0] = (address0, self._offset)
        return address0

    def _read_comment_text(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['comment_text'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '#':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"#"')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read_char()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address4 = FAILURE
                index3 = self._offset
                address4 = self._read_line_break()
                self._offset = index3
                if address4 is not FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset)
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements0.append(address4)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['comment_text'][index0] = (address0, self._offset)
        return address0

    def _read_line_break(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['line_break'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_1.search(chunk0):
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[\\n]')
        self._cache['line_break'][index0] = (address0, self._offset)
        return address0

    def _read_keyword(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['keyword'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        index3, elements1 = self._offset, []
        address2 = FAILURE
        index4 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 9]
        if chunk0 == 'errorfile':
            address2 = TreeNode(self._input[self._offset:self._offset + 9], self._offset)
            self._offset = self._offset + 9
        else:
            address2 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"errorfile"')
        if address2 is FAILURE:
            self._offset = index4
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 7]
            if chunk1 == 'timeout':
                address2 = TreeNode(self._input[self._offset:self._offset + 7], self._offset)
                self._offset = self._offset + 7
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"timeout"')
            if address2 is FAILURE:
                self._offset = index4
        if address2 is not FAILURE:
            elements1.append(address2)
            address3 = FAILURE
            address3 = self._read_whitespace()
            if address3 is not FAILURE:
                elements1.append(address3)
            else:
                elements1 = None
                self._offset = index3
        else:
            elements1 = None
            self._offset = index3
        if elements1 is None:
            address1 = FAILURE
        else:
            address1 = Keyword(self._input[index3:self._offset], index3, elements1)
            self._offset = self._offset
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2)
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address4 = FAILURE
            remaining0, index5, elements2, address5 = 1, self._offset, [], True
            while address5 is not FAILURE:
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 1]
                if chunk2 is not None and Grammar.REGEX_2.search(chunk2):
                    address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address5 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('[a-z0-9\\-\\_\\.]')
                if address5 is not FAILURE:
                    elements2.append(address5)
                    remaining0 -= 1
            if remaining0 <= 0:
                address4 = TreeNode(self._input[index5:self._offset], index5, elements2)
                self._offset = self._offset
            else:
                address4 = FAILURE
            if address4 is not FAILURE:
                elements0.append(address4)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['keyword'][index0] = (address0, self._offset)
        return address0

    def _read_server_name(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['server_name'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_3.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[a-zA-z0-9\\-\\_\\.:]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['server_name'][index0] = (address0, self._offset)
        return address0

    def _read_service_address(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['service_address'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_host()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_4.search(chunk0):
                address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[:]')
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2)
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_port()
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = ServiceAddress(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['service_address'][index0] = (address0, self._offset)
        return address0

    def _read_host(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['host'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_ipv4_host()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_dns_host()
            if address0 is FAILURE:
                self._offset = index1
                address0 = self._read_wildcard_host()
                if address0 is FAILURE:
                    self._offset = index1
        self._cache['host'][index0] = (address0, self._offset)
        return address0

    def _read_port(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['port'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 0, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_5.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[\\d]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['port'][index0] = (address0, self._offset)
        return address0

    def _read_ipv4_host(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['ipv4_host'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        remaining0, index2, elements1, address2 = 1, self._offset, [], True
        while address2 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_6.search(chunk0):
                address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[\\d]')
            if address2 is not FAILURE:
                elements1.append(address2)
                remaining0 -= 1
        if remaining0 <= 0:
            address1 = TreeNode(self._input[index2:self._offset], index2, elements1)
            self._offset = self._offset
        else:
            address1 = FAILURE
        if address1 is not FAILURE:
            elements0.append(address1)
            address3 = FAILURE
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 1]
            if chunk1 == '.':
                address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address3 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"."')
            if address3 is not FAILURE:
                elements0.append(address3)
                address4 = FAILURE
                remaining1, index3, elements2, address5 = 1, self._offset, [], True
                while address5 is not FAILURE:
                    chunk2 = None
                    if self._offset < self._input_size:
                        chunk2 = self._input[self._offset:self._offset + 1]
                    if chunk2 is not None and Grammar.REGEX_7.search(chunk2):
                        address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address5 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('[\\d]')
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        remaining1 -= 1
                if remaining1 <= 0:
                    address4 = TreeNode(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements0.append(address4)
                    address6 = FAILURE
                    chunk3 = None
                    if self._offset < self._input_size:
                        chunk3 = self._input[self._offset:self._offset + 1]
                    if chunk3 == '.':
                        address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address6 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"."')
                    if address6 is not FAILURE:
                        elements0.append(address6)
                        address7 = FAILURE
                        remaining2, index4, elements3, address8 = 1, self._offset, [], True
                        while address8 is not FAILURE:
                            chunk4 = None
                            if self._offset < self._input_size:
                                chunk4 = self._input[self._offset:self._offset + 1]
                            if chunk4 is not None and Grammar.REGEX_8.search(chunk4):
                                address8 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                self._offset = self._offset + 1
                            else:
                                address8 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('[\\d]')
                            if address8 is not FAILURE:
                                elements3.append(address8)
                                remaining2 -= 1
                        if remaining2 <= 0:
                            address7 = TreeNode(self._input[index4:self._offset], index4, elements3)
                            self._offset = self._offset
                        else:
                            address7 = FAILURE
                        if address7 is not FAILURE:
                            elements0.append(address7)
                            address9 = FAILURE
                            chunk5 = None
                            if self._offset < self._input_size:
                                chunk5 = self._input[self._offset:self._offset + 1]
                            if chunk5 == '.':
                                address9 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                self._offset = self._offset + 1
                            else:
                                address9 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"."')
                            if address9 is not FAILURE:
                                elements0.append(address9)
                                address10 = FAILURE
                                remaining3, index5, elements4, address11 = 1, self._offset, [], True
                                while address11 is not FAILURE:
                                    chunk6 = None
                                    if self._offset < self._input_size:
                                        chunk6 = self._input[self._offset:self._offset + 1]
                                    if chunk6 is not None and Grammar.REGEX_9.search(chunk6):
                                        address11 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                        self._offset = self._offset + 1
                                    else:
                                        address11 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('[\\d]')
                                    if address11 is not FAILURE:
                                        elements4.append(address11)
                                        remaining3 -= 1
                                if remaining3 <= 0:
                                    address10 = TreeNode(self._input[index5:self._offset], index5, elements4)
                                    self._offset = self._offset
                                else:
                                    address10 = FAILURE
                                if address10 is not FAILURE:
                                    elements0.append(address10)
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['ipv4_host'][index0] = (address0, self._offset)
        return address0

    def _read_dns_host(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['dns_host'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_10.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[a-zA-Z\\-\\.\\d]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['dns_host'][index0] = (address0, self._offset)
        return address0

    def _read_wildcard_host(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['wildcard_host'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '*':
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"*"')
        self._cache['wildcard_host'][index0] = (address0, self._offset)
        return address0

    def _read_proxy_name(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['proxy_name'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_11.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[a-zA-Z0-9\\-\\_\\.:]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['proxy_name'][index0] = (address0, self._offset)
        return address0

    def _read_value(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['value'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_12.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[^#\\n]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['value'][index0] = (address0, self._offset)
        return address0

    def _read_char(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['char'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_13.search(chunk0):
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[\\n]')
        self._offset = index2
        if address1 is FAILURE:
            address1 = TreeNode(self._input[self._offset:self._offset], self._offset)
            self._offset = self._offset
        else:
            address1 = FAILURE
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            if self._offset < self._input_size:
                address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('<any char>')
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['char'][index0] = (address0, self._offset)
        return address0

    def _read_whitespace(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['whitespace'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 0, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_14.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[ \\t]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['whitespace'][index0] = (address0, self._offset)
        return address0


class Parser(Grammar):
    def __init__(self, input, actions, types):
        self._input = input
        self._input_size = len(input)
        self._actions = actions
        self._types = types
        self._offset = 0
        self._cache = defaultdict(dict)
        self._failure = 0
        self._expected = []

    def parse(self):
        tree = self._read_configuration()
        if tree is not FAILURE and self._offset == self._input_size:
            return tree
        if not self._expected:
            self._failure = self._offset
            self._expected.append('<EOF>')
        raise ParseError(format_error(self._input, self._failure, self._expected))


def format_error(input, offset, expected):
    lines, line_no, position = input.split('\n'), 0, 0
    while position <= offset:
        position += len(lines[line_no]) + 1
        line_no += 1
    message, line = 'Line ' + str(line_no) + ': expected ' + ', '.join(expected) + '\n', lines[line_no - 1]
    message += line + '\n'
    position -= len(line) + 1
    message += ' ' * (offset - position)
    return message + '^'

def parse(input, actions=None, types=None):
    parser = Parser(input, actions, types)
    return parser.parse()
