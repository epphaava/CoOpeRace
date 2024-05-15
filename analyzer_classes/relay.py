from .analyzer import Analyzer
import os
import subprocess
import re

class Relay(Analyzer):
  
  name = 'Relay'
  
  def __init__(self):
    super().__init__('relay', 
                     r'(Possible race between access to:[^*]*?)(?=[$*]{4})',
                     #r'Possible race between access to:[\s\S]*?\[.*\(.*\)\]\n',
                     r'(\[)(.*\(.*\))(\])',
                     r'(Possible race between access to:\s*)(.*?)(\s*@)')

  def run_analyzer(self, input_file_name):

    # where the files are saved, to reuse if needed?
    input_file_path = os.path.join(self.uploaded_files_folder, input_file_name)
    
    # generate the dir path within the 'results' directory for the input file name
    input_file_name_dir = os.path.join(self.results_folder, input_file_name)

    # if the input file name dir doesn't exist, create it
    if not os.path.exists(input_file_name_dir):
        print('no input file found')
        os.makedirs(input_file_name_dir)

    # output path reltaive to the location of relay
    output_path = os.path.join('../../', input_file_name_dir, self.name + '.txt')

    # where the file that will be analyzed is saved
    file_location = f'../../{input_file_path}.c'

    # change dir to run relay
    os.chdir('analyzers/relay-sv')

    try:
        # assuming we are in the APPLICATION directory when using this function
        command = f'./run_relay.sh {file_location}'
        with open(output_path, 'w+') as output_file:
            subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)

        # change dir back to original
        os.chdir('../../')

        print(f"Text has been written to {output_path}\n")

    except Exception as e:
        print(f"An error occurred: {e}")
        with open(output_path, 'w+') as output_file:
            output_file.write(f"An error occurred: {e}\n")
