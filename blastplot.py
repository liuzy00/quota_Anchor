import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import collinearity

class plot:
    def __init__(self):
        self.anchorwavefile = 'anchorwavefile'
        self.combineblastfile = 'combineblastpfile'
    def blast(self):
        anchorwavefile,combineblastfile = collinearity.Collinearity.run_all_processes()

        data = pd.read_table(self.combineblastfile, header=None)
        data.columns = ["gene_query", "chr_query","qurid", "start_query", "end_query", "strand_query",
                        "gene_ref", "chr_ref","refid", "start_ref", "end_ref", "strand_ref", "score"]
        data['strand'] = '+'
        data.loc[data['strand_query'] != data['strand_ref'], 'strand'] = '-'

        data = data[data['chr_query'].astype(str).isin(
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])]
        data = data[data['chr_ref'].astype(str).isin(
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])]
        data['chr_query'] = pd.Categorical(data['chr_query'],categories=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        data['chr_ref'] = pd.Categorical(data['chr_ref'],categories=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])

        sns.set(style="white")
        g = sns.FacetGrid(data, col='chr_query', row='chr_ref', hue='strand', height=1.5, aspect=1.5, margin_titles=True)
        g.map(sns.scatterplot, "start_query", "start_ref", s=0.5)
        g.set_axis_labels(x_var='sb',y_var='mz')
        g.set_titles(row_template="{row_name}", col_template="{col_name}")

        plt.show()


plot = plot()
plot.blast()


