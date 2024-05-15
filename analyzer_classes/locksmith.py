from .analyzer import Analyzer
import os
import subprocess

class Locksmith(Analyzer):
  
  name = 'Locksmith'
  
  def __init__(self):
    super().__init__('locksmith', 
                     r'(Warning: Possible data race:[^*]*?)(?=(Warning|\*\*\*))', 
                     r'.*dereference of .*\n',
                     r'(Warning: Possible data race:\s*&)(.*?)(:)')
    



  def run_analyzer(self, input_file_name):

    # where the files are saved, to reuse if needed?
    input_file_path = os.path.join(self.uploaded_files_folder, input_file_name)
    
    # generate the dir path within the 'results' directory for the input file name
    input_file_name_dir = os.path.join(self.results_folder, input_file_name)

    # if the input file name dir doesn't exist, create it
    if not os.path.exists(input_file_name_dir):
        os.makedirs(input_file_name_dir)

    # output path reltaive to the location of locksmith
    output_path = os.path.join('../../', input_file_name_dir, self.name + '.txt')

    # where the file that will be analyzed is saved
    file_location = f'../../{input_file_path}.c'

    # change dir to run locksmith
    os.chdir('analyzers/locksmith')

    try:
        # assuming we are in the APPLICATION directory when using this function
        command = f'./locksmith --list-guardedby {file_location}'
        with open(output_path, 'w+') as output_file:
            subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)

        # change dir back to original
        os.chdir('../..')

        print(f"Text has been written to {output_path}\n")


    except Exception as e:
        print(f"An error occurred: {e}")
        with open(output_path, 'w+') as output_file:
            output_file.write(f"An error occurred: {e}\n")