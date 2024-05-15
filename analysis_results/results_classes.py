from dataclasses import dataclass

@dataclass
class LineInfo:
   loc: str
   info: str

@dataclass
class Group:
   info : str
   accesses : list[LineInfo]
   targetvar: str=None

@dataclass
class FlatLineInfo:
   line: LineInfo
   group: Group
   analyzer: str