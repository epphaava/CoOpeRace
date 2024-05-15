from .analyzer import Analyzer
import os
import subprocess

class Goblint(Analyzer):
  
  name = 'Goblint'
  
  def __init__(self):
    super().__init__('goblint', 
                     r'(\[Warning\]\[Race\] Memory location .*?\(.*?conf.*?\):[^*]*?)(?=\[(Warning|Info)\])',
                     r'(write|read|spawn) with [\s\S]*? \(.*\)',
                     r'(Memory location )(.*)(@)')
    
  def find_race_lines_json(self, test):
     pass


  def run_analyzer(self, input_file_name):

    # path to the 
    input_file_path = os.path.join('./', self.uploaded_files_folder, input_file_name)

    # generate the dir path within the 'results' directory for the input file name
    input_file_name_dir = os.path.join(self.results_folder, input_file_name)

    # if the input file name dir doesn't exist, create it
    if not os.path.exists(input_file_name_dir):
        os.makedirs(input_file_name_dir)

    # Generate the output file path within the 'base_name' directory
    output_path = os.path.join(input_file_name_dir, self.name + '.txt')

    try:

        # Run the goblint command and redirect the output to the new file
        command = f'analyzers/goblint/goblint {input_file_path}.c'
        with open(output_path, 'w+') as output_file:
            subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)

        print(f"Text has been written to {output_path}\n")


    except Exception as e:
        print(f"An error occurred: {e}")
        with open(output_path, 'w+') as output_file:
            output_file.write(f"An error occurred: {e}\n")