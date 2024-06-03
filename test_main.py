from main import strip_punctuation_mark
from main import print_progress_bar
from main import get_file_extension

def test_strip_punctuation_mark():
  assert strip_punctuation_mark('word,') == 'word'
  assert strip_punctuation_mark('word?') == 'word'
  assert strip_punctuation_mark('“word') == 'word'
  assert strip_punctuation_mark('”word') == 'word'
  assert strip_punctuation_mark('"word') == 'word'
  assert strip_punctuation_mark('(word') == 'word'
  assert strip_punctuation_mark('word)') == 'word'
  assert strip_punctuation_mark('-word') == 'word'
  assert strip_punctuation_mark('word?') == 'word'
  assert strip_punctuation_mark('word!') == 'word'
  assert strip_punctuation_mark('word;') == 'word'

def test_print_progress_bar():
  assert print_progress_bar(1, 100) == 1
  assert print_progress_bar(5, 100) == 5
  assert print_progress_bar(50, 100) == 50
  assert print_progress_bar(100, 100) == 100

def test_get_file_extension():
  assert get_file_extension('songs.txt') == 'txt'
  assert get_file_extension('Verina Songs.pdf') == 'pdf'
  assert get_file_extension('diff.csv') == 'csv'
