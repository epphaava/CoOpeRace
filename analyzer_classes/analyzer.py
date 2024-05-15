import re
import analysis_results


results_folder = 'static/files/results'
uploaded_files_folder = 'static/files/uploaded_files'

class Analyzer(object):

  def __init__(self, name, group_pattern, race_line_pattern, global_variable_pattern):
    self.name = name
    self.group_pattern = group_pattern
    self.race_line_pattern = race_line_pattern
    self.global_variable_pattern = global_variable_pattern
    self.uploaded_files_folder = uploaded_files_folder
    self.results_folder = results_folder


  # aasumes the global variable is in the first row
  def find_race_lines(self, test):

    group_list = []

    with open(f"{self.results_folder}/{test}/{self.name}.txt", 'r') as file:
      file_rows = file.read()

    # find all groups 
    group_matches = re.finditer(self.group_pattern, file_rows)

    for group_match in group_matches:
      uus_grupp = None

      accesses = []

      warning_rows = [match.group() for match in re.finditer(self.race_line_pattern, group_match.group())]

      for warning_row in warning_rows:
        important_matches = list(re.finditer(rf'{test}.c:\d+', warning_row))

        if important_matches:
          # assumes that only the last mention is important in the last match of the row
          problematic_line_nr = re.findall(r'\d+', important_matches[-1].group())[-1]

        line_info = analysis_results.LineInfo(problematic_line_nr, warning_row)

        accesses.append(line_info)

      problematic_variable = re.search(self.global_variable_pattern, group_match.group())
      if problematic_variable:
        uus_grupp = analysis_results.Group(group_match.group(), accesses, problematic_variable.group(2))

      else: 
        uus_grupp = analysis_results.Group(group_match.group(), accesses)

      if uus_grupp:
        group_list.append(uus_grupp)
    return group_list