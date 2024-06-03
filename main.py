#Levi Hung
#11/22/2023
#Final Project
#Group Dragon: Levi Hung

# CONCEPT: 
# When my daughter is studying English, I would like to know how many words 
# she learned. I also want to know new words she read in a new book.
# After she reads stories and sings songs, I can use this program to do 
# word statistics from these stories and lyrics. The data will be stored in a 
# spreadsheet, and I can search for specific words to get the information 
# from the spreadsheet.
# So, I can know her progress in learning Vocabulary and create her 
# study plan according to word frequency.
#
# DESCRIPTION
# This program executes word analysis of text files.
# 1. It prompts the user to choose functions until exiting.
# 2. It reads and parses TXT/PDF files to get the amount of different words. 
# 3. It displays a bar chart for the word frequency from the database. 
# 4. It saves or loads CSV files as a database. 
# 5. It reads and contrasts TXT/PDF files with the database.
# 6. It shows the specific word and the database on the screen.
# 7. It prints the progress bar to predict execution time.
#
# APPROACH:
# 1. Use matplotlib to display bar graphs.
# 2. Use pandas to represent a database.
# 3. Use sys to display output directly to the screen console.
# 4. Use pypdf to read PDF files. 
import pandas as pd
import matplotlib.pyplot as plt
import sys
import pypdf

DATABASE_COL_HEADER = ['vocab', 'amount', 'sentence', 'filename']

class Word_Database:
  def __init__(self):
    self.db_df = pd.DataFrame(
       data    = [], 
       columns = DATABASE_COL_HEADER,
       index   = []) 
    self.dif_df= pd.DataFrame(
       data    = [], 
       columns = DATABASE_COL_HEADER,
       index   = []) 
    self.order_df = self.db_df

  def is_word_exist(self, word):
    if len(self.db_df[self.db_df['vocab'] == word]) == 0:
      return False
    else:
      return True

  def add_word(self, word, text, filename):
    self.db_df.loc[len(self.db_df)] = {'vocab':    word, 
                                       'amount':   1, 
                                       'sentence': text, 
                                       'filename': filename}

  def increase_amount(self, word):
    idx = self.db_df[self.db_df['vocab'] == word].index[0]
    self.db_df.loc[idx, 'amount'] = self.db_df.loc[idx, 'amount'] + 1

  def is_word_exist_diff(self, word):
    if len(self.dif_df[self.dif_df['vocab'] == word]) == 0:
      return False
    else:
      return True

  def add_word_diff(self, word, text, filename):
    self.dif_df.loc[len(self.dif_df)] = {'vocab':    word, 
                                         'amount':   1, 
                                         'sentence': text, 
                                         'filename': filename}

  def increase_amount_diff(self, word):
    idx = self.dif_df[self.dif_df['vocab'] == word].index[0]
    self.dif_df.loc[idx, 'amount'] = self.dif_df.loc[idx, 'amount'] + 1

  def set_db_from_dif(self):
    self.db_df = self.dif_df
    self.dif_df= pd.DataFrame(
       data    = [], 
       columns = DATABASE_COL_HEADER,
       index   = []) 

  def get_total_words(self):
    return len(self.db_df)

  def sort_db(self):
    self.order_df = self.db_df.sort_values(axis=0, by='amount', ascending=False)
    
  def get_sort_word_list(self, first, last):
    return self.order_df['vocab'].values[first:last]

  def get_sort_amount_list(self, first, last):
    return self.order_df['amount'].values[first:last]

  def write_csv(self, filename):
    # Add escapechar to fix no escapechar set error.
    self.db_df.to_csv(filename, index=False, sep=':', escapechar='\\') 

  def read_csv(self, filename):
    old_db_df = self.db_df
    self.db_df = pd.read_csv(filename, sep=':')
    if list(self.db_df.columns) == DATABASE_COL_HEADER:
      return True
    else:
      self.db_df = old_db_df
      return False

  def display_word(self, word):
    lower_word = word.lower()
    db_find_df = self.db_df[self.db_df['vocab'] == lower_word]
    if len(db_find_df) != 0:
      print('vocab:   ', db_find_df['vocab'].values[0])
      print('amount:  ', db_find_df['amount'].values[0])
      print('filename:', db_find_df['filename'].values[0])
      print('sentence:', db_find_df['sentence'].values[0])
    else:
      print(f'The word "{word}" does not exit.')

  def print_db(self):
    print(self.db_df)

def print_progress_bar(value, total):
  """Print the progress bar when parsing files.

  Arguments:
  value -- the number of lines that have already been processed.
  total -- the total number of lines that need to be processed.

  Returns:
  integer percent of prograss rate
  """
  prog_rate = value / total
  # update the progress bar when the progress increases by one percent 
  # or achieves one hundred percent.
  if value % (int(total / 100) + 1) == 0 or value == total:
    total_bar = 40 #size of progress bar
    sys.stdout.write('\r')
    bar = '#' * int(total_bar * prog_rate)
    bar = bar + '-' * (total_bar - int(total_bar * prog_rate))
    sys.stdout.write(f"Progress | [{bar}] {int(100 * prog_rate)}% ")
    sys.stdout.flush()

  return int(100 * prog_rate)

def strip_punctuation_mark(text_line):
  """Strip the punctuation marks in a line. The punctuation marks include 
  ',', '"', '“', '”', '(', ')','-', '|', '?', ';', and '!'.

  Arguments:
  text_line -- the text string that needs to be stripped.

  Returns:
  text_line -- the stripped text string.
  """
  text_line = text_line.replace(',', '')      
  text_line = text_line.replace('“', '')
  text_line = text_line.replace('”', '')
  text_line = text_line.replace('"', '')
  text_line = text_line.replace('(', '')
  text_line = text_line.replace(')', '')
  text_line = text_line.replace('-', '')
  text_line = text_line.replace(':', '')
  text_line = text_line.replace('?', '')
  text_line = text_line.replace(';', '')
  text_line = text_line.replace('!', '')
  return text_line

def get_file_extension(filename):
  """Get the extension string of the file.

  Arguments:
  filename -- the string of file name.

  Returns:
  string -- the extension string.
  """
  return filename[-3:]

def read_and_parse_file(db):
  """Read and parse the file to write different words and 
  the number of duplicated words in the database.
  Prompt the user to enter a filename and process it.

  Arguments:
  db -- the object of the database.
  """
  filename = input('Enter a filename: ')
  num_line = 0

  try:
    # This program only supports TXT and PDF files.
    if get_file_extension(filename) == 'txt':
      infile = open(filename, 'r')
      text_para = infile.read()

    elif get_file_extension(filename) == 'pdf':
      infile = open(filename, 'rb')
      pdf_reader = pypdf.PdfReader(infile) 
      text_para = pdf_reader.pages[0].extract_text()    
      for i in range(1, len(pdf_reader.pages)):
        text_para = text_para + pdf_reader.pages[i].extract_text()

    else:
      raise ValueError('Error! The file MUST be a TXT or PDF file.')

    text_para = text_para.replace('\n', ' ')
    total_lines = text_para.count('.') + 1   
    split_lines = text_para.split('.')

    for text_line in split_lines:
      orig_line = text_line.strip() + '.'
      text_line = strip_punctuation_mark(text_line)
      split_words = text_line.split(' ')

      for word in split_words:
        lower_word = word.lower()
        if word.isalpha() == True:
          if (db.is_word_exist(lower_word)):
            db.increase_amount(lower_word)

          else:
            db.add_word(lower_word, orig_line, filename)
        
      num_line = num_line + 1
      percent = print_progress_bar(num_line, total_lines)

    infile.close()

    print()
    print(f'The amount of vocabulary is {db.get_total_words()}.')
    
  except FileNotFoundError:
    print(f'Error! The file [{filename}] does not exist.')

  except ValueError as excpt:
    print(excpt)

def display_graph(db):
  """Display the bar graph of the word frequency in the database.

  Arguments:
  db -- the object of the database.
  """
  if db.get_total_words() != 0:
    db.sort_db()
    
    try:
      pg_num = int(input('Enter a page number: (\'0\' to exit) '))
      while pg_num != 0:
        # Every bar chart only displays 10 words.
        max_pg_num = int(db.get_total_words() / 10) + 1
        if pg_num <= max_pg_num:
          plt.clf()
          word_list   = db.get_sort_word_list((pg_num-1)*10, pg_num*10)          
          amount_list = db.get_sort_amount_list((pg_num-1)*10, pg_num*10)
          bar_width   = 0.5
          plt.bar(word_list, amount_list, bar_width)      
          plt.title('Word Frequency')
          plt.xlabel('Word')
          plt.ylabel('Amount')
          # Only display the integer number
          if (amount_list[0] < 5):
            plt.yticks(range(1,6))

          plt.show(block=False)

        else:          
          print(f'Error! Page number MUST NOT be greater than {max_pg_num}.')

        pg_num = int(input('Enter a page number: (\'0\' to exit) '))

    except ValueError:
      print('Error! You MUST enter a digital number.')

  else:
    print('Error! You MUST first read a file or load a database file.')  
  
def write_database_to_csv(db):
  """Write the database to a CSV file.

  Arguments:
  db -- the object of the database.
  """
  if db.get_total_words() != 0:
    filename = input('Enter a CSV filename: ')
    db.write_csv(filename)
    print(f'Write file [{filename}] completed.')

  else:
    print('Error! You MUST read a file or load a database file.')  
 
def load_csv_to_database(db):
  """Load a CSV file to the database.

  Arguments:
  db -- the object of the database.
  """
  filename = input('Enter a CSV filename: ')
  try:
    if db.read_csv(filename) == True:
      print(f'Load file [{filename}] completed.')
      print(f'The amount of vocabulary is {db.get_total_words()}.')

    else:
      print(f'Error! The file [{filename}] is NOT a CSV file.')
   
  except FileNotFoundError:
    print(f'Error! The file [{filename}] does not exist.')
  
  
def read_and_contrast_file(db):
  """Read and contrast the file with the database. 
  Write different words and the number of duplicated words in the database.
  Prompt the user to enter a filename and process it.

  Arguments:
  db_df -- the object of the database.
  """
  if db.get_total_words() != 0:
    filename = input('Enter a filename: ')
    num_line = 0

    try:
      if get_file_extension(filename) == 'txt':
        infile = open(filename, 'r')
        text_para = infile.read()

      elif get_file_extension(filename) == 'pdf':
        infile = open(filename, 'rb')
        pdf_reader = pypdf.PdfReader(infile) 
        text_para = pdf_reader.pages[0].extract_text()    
        for i in range(1, len(pdf_reader.pages)):
          text_para = text_para + pdf_reader.pages[i].extract_text()
      else:
        raise ValueError('Error! The file MUST be a TXT or PDF file.')

      text_para = text_para.replace('\n', ' ')
      total_lines = text_para.count('.') + 1   
      split_lines = text_para.split('.')

      for text_line in split_lines:
        orig_line = text_line.strip() + '.'
        text_line = strip_punctuation_mark(text_line)
        split_words = text_line.split(' ')

        for word in split_words:
          lower_word = word.lower()
          if word.isalpha() == True:
            if db.is_word_exist(lower_word) == False:
              if db.is_word_exist_diff(lower_word) == True:
                db.increase_amount_diff(lower_word)
              else:
                db.add_word_diff(lower_word, orig_line, filename)
        num_line = num_line + 1
        percent = print_progress_bar(num_line, total_lines)

      infile.close()
      db.set_db_from_dif()
     
      print()
      print(f'The amount of vocabulary is {db.get_total_words()}.')

    except FileNotFoundError:
      print(f'Error! The file [{filename}] does not exist.')

    except ValueError as excpt:
      print(excpt)

  else:
    print('Error! You MUST first read a file or load a database file.')  

  
def show_word_info(db):
  """Show word information including vocab, amount, filename, and sentence. 
  Prompt the user to enter a word and process it.

  Arguments:
  db -- the object of the database.
  """
  if db.get_total_words() != 0:
    word = input('Enter a word: ')
    db.display_word(word)

  else:
    print('Error! You MUST first read a file or load a database file.')  
  
def version_designer_decorator(original_func):
  def wrap_func():
    print('WordFreqCounter Version 1.1')
    original_func()
    print('Designer: Levi Hung')
  return wrap_func

@version_designer_decorator
def display_menu():
  """Display the menu.
  """
  print()
  print('---------------------------------------------------------')
  print('1) Read and parse a file to the database.')
  print('2) Display the graph of word frequency from the database.')
  print('3) Write the database to a CSV file.')
  print('4) Load a CSV file to the database.')
  print('5) Read and contrast a file with the database.')
  print('6) Show a word information.')
  print('7) Show the database.')
  print('0) Exit program.')
  print('---------------------------------------------------------')
  print()

def main():
  db = Word_Database()  
  display_menu()
  select_function = input('Enter function: ')
  while select_function != '0':
    if select_function == '1':
      read_and_parse_file(db)
    elif select_function == '2':
      display_graph(db)
    elif select_function == '3':
      write_database_to_csv(db)
    elif select_function == '4':
      load_csv_to_database(db)
    elif select_function == '5':
      read_and_contrast_file(db)
    elif select_function == '6':
      show_word_info(db)
    elif select_function == '7':
      db.print_db()
    else:
      print('Error! Invalid function!')

    display_menu()
    select_function = input('Enter function: ')

  print('Program exit.')

if __name__ == '__main__':
  # help(print_progress_bar)
  # help(strip_punctuation_mark)
  # help(get_file_extension)
  # help(read_and_parse_file)
  # help(display_menu)
  # help(write_database_to_csv)
  # help(load_csv_to_database)
  # help(read_and_contrast_file)
  # help(show_word_info)
  # help(display_menu)
  main()

# EXTRA CREDIT:
# I used Python decorator to add information before and after
# the function display_menu(). When I unmark @version_designer_decorator, 
# display_menu() will display the program version and designer.
