# proto-formatter
Protocol Buffers file formatter.

## Install
```shell
pip install proto-formatter
```
## Usage
- Format protobuf file using default config:
  - indents=2 
  - all_top_comments=False
  - equal_sign=False
  - flatten=False
  - comment_max_length=None
  - new_fp=None

Original protobuf file `test.proto` will be rewritten with formatted content.
```python
from proto_formatter import format_file

format_file('test.proto')
```
- Format protobuf file with specified config:
  - indents=4 
  - all_top_comments=True
  - equal_sign=True
  - flatten=False
  - comment_max_length=None
  - new_fp='formatted.proto'

Original protobuf file `test.proto` not be rewritten, create new protobuf file `formatted.proto` instead.
```python
from proto_formatter import format_file

format_file('test.proto', indents=4, all_top_comments=True, equal_sign=True, flatten=False, comment_max_length=None, new_fp='formatted.proto')
```
- Format protobuf string align with equal sign: 
  - equal_sign=True
  - other configs are default values.
```python
from proto_formatter import format_str

proto_str = """
    /*
    Person balabala
*/
    message Person {
    // comment of name a
required string name = 1; // comment of name b
/* 
comment of id a
// comment of id b
         */
        required int32 id = 2;// comment of id c
       optional string email = 3;// comment of email
}
"""
formatted_proto_str = format_str(proto_str, equal_sign=True)
```
The formatted_proto_str is:
```protobuf
/*
**    Person balabala
*/
message Person {
    /*
    **    comment of name a
    */
    required string name  = 1;  // comment of name b
    /*
    **    comment of id a
    **    comment of id b
    */
    required int32 id     = 2;  // comment of id c
    optional string email = 3;  // comment of email
}


```