import argparse
import subprocess
import longestPeps
import combineBlastAndStrandInformation

class Collinearity:
    def __init__(self):
        self.reffasta = "reffasta"
        self.qurfasta = "qurfasta"
        self.refgff = "refgff"
        self.qurgff = "qurgff"
        self.output_protein_file = "output_protein_file"
        self.longestpepfile = "longestpepfile"
        self.databasename = "refdatabase"
        self.blastpfile = "blastpfile"
        self.combinetable = "combinetable"
        self.anchorwavefile = "anchorwavefile"
        self.R = '1'
        self.Q = '2'

    def parse_command_line(self):
        parser = argparse.ArgumentParser(description='Collinearity')
        parser.add_argument('-f1', type=str, help='ref fa')
        parser.add_argument('-f2', type=str, help='qur fa')
        parser.add_argument('-g1', type=str, help='ref gff')
        parser.add_argument('-g2', type=str, help='qur gff')

        args = parser.parse_args()

        self.reffasta = args.f1
        self.qurfasta = args.f2
        self.refgff = args.g1
        self.qurgff = args.g2





    def run_gffread(self, fastafile, gfffile, output_protein_file):
        command_line = [
            'gffread',
            '-g', fastafile,
            '-y', output_protein_file,
            gfffile,
            '-S'
        ]

        try:
            subprocess.run(command_line, check=True)
        except subprocess.CalledProcessError as e:
            print(f'failed: {e}')


    def diamondmakedb(self,proteinfile,fastafile,database):
        commmand_line =[
            'diamond',
            'makedb',
            '--in',proteinfile,
            '--db',database
        ]

        try:
            subprocess.run(commmand_line, check=True)
            print(f'Diamond database "{self.databasename}" created successfully.')
        except subprocess.CalledProcessError as e:
            print(f'Failed to create Diamond database: {e}')


    def run_diamond_blastp(self,database, query_file, blastpfile, num_alignments=5, evalue=1e-10):
        command_line = ['diamond', 'blastp',
                        '--db', database,
                        '-q', query_file,
                        '-o', blastpfile,
                        '-k', str(num_alignments),
                        '-e', str(evalue)]

        try:
            subprocess.run(command_line, check=True)
            print(f'Diamond blastp completed successfully. Results saved in "{blastpfile}".')
        except subprocess.CalledProcessError as e:
            print(f'Error running Diamond blastp: {e}')


    def run_anchorwave_pro(self, input_file, output_file, R_value, Q_value):
        command_line = ['/home/lzy/Documents/wgdi/anchorwave/AnchorWave/anchorwave', 'pro',
                        '-i', input_file,
                        '-o', output_file,
                        '-R', str(R_value),
                        '-Q', str(Q_value)]


        try:
            subprocess.run(command_line, check=True)
            print(f'AnchorWave Pro completed successfully. Results saved in "{output_file}".')
        except subprocess.CalledProcessError as e:
            print(f'Error running AnchorWave Pro: {e}')

    def run_all_processes(self):
        self.parse_command_line()
        self.output_protein_file = "refpep"
        self.longestpepfile = "reflongestpep"
        self.run_gffread(fastafile=self.reffasta, gfffile=self.refgff, output_protein_file=self.output_protein_file)
        longestPeps.longestPeps(gffFile=self.refgff, fastaFile=self.reffasta, proteinSeqs=self.output_protein_file,
                                outputFile=self.longestpepfile)
        self.diamondmakedb(proteinfile=self.longestpepfile, fastafile=self.reffasta, database=self.databasename)

        self.output_protein_file = "qurpep"
        self.longestpepfile = "qurlongestpep"
        self.run_gffread(fastafile=self.qurfasta, gfffile=self.qurgff, output_protein_file=self.output_protein_file)
        longestPeps.longestPeps(gffFile=self.qurgff,fastaFile=self.qurfasta,proteinSeqs=self.output_protein_file,outputFile=self.longestpepfile)
        self.run_diamond_blastp(database=self.databasename, query_file=self.longestpepfile, blastpfile=self.blastpfile)

        combineBlastAndStrandInformation.anchorwave_quota(queryGffFile=self.qurgff,refGffFile=self.refgff,blastpresult=self.blastpfile,outputFile=self.combinetable)
        self.run_anchorwave_pro(input_file=self.combinetable, output_file=self.anchorwavefile, R_value=self.R, Q_value=self.Q)
        return self.anchorwavefile





my_instance = Collinearity()
my_instance.run_all_processes()



