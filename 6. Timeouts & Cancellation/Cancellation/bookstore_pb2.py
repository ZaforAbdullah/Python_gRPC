# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bookstore.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x62ookstore.proto\"3\n\x04\x42ook\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\t\x12\r\n\x05price\x18\x03 \x01(\x05\"\x1a\n\nBookSearch\x12\x0c\n\x04name\x18\x01 \x01(\t\"$\n\x04\x43\x61rt\x12\r\n\x05price\x18\x01 \x01(\x05\x12\r\n\x05\x62ooks\x18\x02 \x01(\x05\x32J\n\tBookStore\x12\x1b\n\x05\x66irst\x12\x0b.BookSearch\x1a\x05.Book\x12 \n\x0etotalCartValue\x12\x05.Book\x1a\x05.Cart(\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bookstore_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_BOOK']._serialized_start=19
  _globals['_BOOK']._serialized_end=70
  _globals['_BOOKSEARCH']._serialized_start=72
  _globals['_BOOKSEARCH']._serialized_end=98
  _globals['_CART']._serialized_start=100
  _globals['_CART']._serialized_end=136
  _globals['_BOOKSTORE']._serialized_start=138
  _globals['_BOOKSTORE']._serialized_end=212
# @@protoc_insertion_point(module_scope)
